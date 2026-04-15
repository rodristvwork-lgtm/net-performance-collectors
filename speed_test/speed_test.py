import os
import subprocess
import time
from typing import  Optional
import pandas as pd
import asyncio
import logging
from datetime import datetime, timezone
import json
from playwright.async_api import async_playwright
import platform
import re
from openpyxl import load_workbook
import requests
from requests.exceptions import RequestException
import socket
from kafka import KafkaProducer
from kafka.errors import KafkaError

# Configurazione della cache
CACHE_FILE = os.path.expanduser('~/network_info_cache.json')
CACHE_DURATION = 86400  # 12 ore in secondi


def get_network_info():
    # Controllo se esiste una cache valida
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            cache = json.load(f)
        if time.time() - cache['timestamp'] < CACHE_DURATION:
            logging.debug("Utilizzando informazioni di rete dalla cache locale")
            return cache['data']

    network_info = {
        'ip': 'Unknown',
        'isp': 'Unknown',
        'country': 'Unknown'
    }

    # Lista di servizi da provare
    services = [
        ('http://ip-api.com/json', lambda r: {'ip': r.get('query'), 'isp': r.get('isp'), 'country': r.get('country')}),
        ('https://ipapi.co/json/', lambda r: {'ip': r.get('ip'), 'isp': r.get('org'), 'country': r.get('country_name')})
    ]

    for url, parser in services:
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            network_info = parser(data)
            logging.info(f"Informazioni di rete recuperate con successo da {url}")
            break
        except RequestException as e:
            logging.warning(f"Errore nel recupero delle informazioni da {url}: {e}")
        except json.JSONDecodeError as e:
            logging.warning(f"Errore nel parsing JSON da {url}: {e}")

    # Se non sono riuscito a ottenere l'IP, provio un servizio di fallback
    if network_info['ip'] == 'Unknown':
        try:
            network_info['ip'] = requests.get('https://api.ipify.org', timeout=5).text
            logging.info("IP recuperato da api.ipify.org")
        except RequestException as e:
            logging.error(f"Errore nel recupero dell'IP da api.ipify.org: {e}")

    # Salvo le informazioni nella cache
    with open(CACHE_FILE, 'w') as f:
        json.dump({'timestamp': time.time(), 'data': network_info}, f)

    return network_info

def get_local_ip():
    """
    Ottengo l'indirizzo IP locale della mia macchina. Creo una connessione
    temporanea a un server DNS pubblico e estraggo l'IP locale. In caso di
    errore, restituisco "Unknown" per gestire l'eccezione.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "Unknown"
    
def get_hostname():
    """
    Recupero il nome host della mia macchina. Utilizzo la funzione
    socket.gethostname() per ottenere questa informazione in modo
    semplice e diretto.
    """
    return socket.gethostname()

def get_gateway_mac(max_retries=3):
    """
    Recupero il mac-addr del modem a cui sono collegato Utilizzo la libreria
    di sistema ifconfig e ipconfig  per ottenere questa informazione in modo
    semplice e diretto.
    """
    for attempt in range(max_retries):
        try:
            if platform.system() == "Windows":
                gateway_ip = subprocess.check_output("ipconfig | findstr /i \"Default Gateway\"", shell=True).decode().split(":")[1].strip()
                arp_output = subprocess.check_output(f"arp -a {gateway_ip}", shell=True).decode()
                mac_match = re.search(r"([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})", arp_output)
            else:  # Linux
                gateway_ip = subprocess.check_output("ip route show default | awk '/default/ {print $3}'", shell=True).decode().strip()
                arp_output = subprocess.check_output(f"arp -e {gateway_ip}", shell=True).decode()
                mac_match = re.search(r"([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})", arp_output)
            
            if mac_match:
                return mac_match.group()
        except subprocess.CalledProcessError as e:
            logging.warning(f"Tentativo {attempt + 1} fallito nel recupero del MAC address del gateway: {e}")
        except Exception as e:
            logging.warning(f"Errore imprevisto durante il tentativo {attempt + 1} di recupero del MAC address del gateway: {e}")
        
        if attempt == max_retries - 1:
            logging.error("Tutti i tentativi di recupero del MAC address del gateway sono falliti.")
    
    return "Unknown"

def get_isp_info(max_retries=3, timeout=10):
    """
    Recupero l'indirizzo IP pubblico della mia macchina. Faccio una richiesta
    a ipify.org e restituisco l'IP ottenuto. Se la richiesta fallisce,
    restituisco "Unknown" per gestire l'errore in modo elegante.
    """
    network_info = get_network_info()
    return {
        'isp': network_info['isp'],
        'ip': network_info['ip']
    }
      
def flatten_dict(d, parent_key='', sep='_'):
    """
    Appiattisco un dizionario annidato. Trasformo un dizionario con strutture
    gerarchiche in uno piatto, concatenando le chiavi dei livelli superiori
    con quelle dei livelli inferiori. Gestisco anche liste all'interno del dizionario.
    
    Args:
        d (dict): Dizionario da appiattire
        parent_key (str): Chiave padre per i valori annidati
        sep (str): Separatore per concatenare le chiavi
        
    Returns:
        dict: Dizionario appiattito
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            # Per le liste semplici di valori primitivi, utilizza una rappresentazione JSON
            if all(isinstance(x, (int, float, str, bool)) for x in v):
                items.append((new_key, json.dumps(v)))
            else:
                # Per liste di oggetti complessi, appiattisci ogni elemento
                for i, item in enumerate(v):
                    if isinstance(item, dict):
                        items.extend(flatten_dict({str(i): item}, new_key, sep=sep).items())
                    else:
                        items.append((f"{new_key}{sep}{i}", item))
        else:
            items.append((new_key, v))
    return dict(items)

def prepare_flat_message(metric_type: str, data: dict, test_id: str = None) -> dict:
    """
    Prepara un messaggio flat per Kafka, includendo metadati e dati del test.
    
    Args:
        metric_type (str): Tipo di metrica, es. 'ping', 'download', ecc.
        data (dict): Dati del test
        test_id (str, optional): ID univoco del test
        
    Returns:
        dict: Messaggio flat per Kafka
    """
    if 'timestamp' not in data:
        data['timestamp'] = datetime.now(timezone.utc).isoformat()
        
    isp_info = get_isp_info()
    gateway_mac = get_gateway_mac()
    hostname = get_hostname()
    local_ip = get_local_ip()
    
    # Crea un dizionario flat con tutti i metadati
    flat_message = {
        "metric_type": metric_type,
        "timestamp": data['timestamp'],
        "hostname": hostname,
        "source_ip": local_ip,
        "public_ip": isp_info['ip'],
        "service_provider": isp_info['isp'],
        "gateway_mac": gateway_mac
    }
    
    # Aggiungi test_id se presente
    if test_id:
        flat_message["test_id"] = test_id
    elif 'test_id' in data:
        flat_message["test_id"] = data['test_id']
    
    # Aggiungi tutti i dati del test con prefisso metric_type
    for k, v in data.items():
        if k not in ['timestamp', 'test_id']:
            # Gestisci liste di valori primitivi
            if isinstance(v, list) and all(isinstance(x, (int, float, str, bool)) for x in v):
                # Converti in JSON stringa
                flat_message[f"{metric_type}_{k}"] = json.dumps(v)
            # Gestisci dizionari annidati
            elif isinstance(v, dict):
                nested_dict = flatten_dict(v, f"{metric_type}_{k}")
                flat_message.update(nested_dict)
            # Gestisci valori semplici
            elif isinstance(v, (int, float, str, bool)) or v is None:
                flat_message[f"{metric_type}_{k}"] = v
    
    # Rimuovi campi con valore "Unknown" o None
    flat_message = {k: v for k, v in flat_message.items() if v != "Unknown" and v is not None}
    
    return flat_message

def prepare_speedtest_message(result):
    """
    Prepara un messaggio specifico per i risultati dello speedtest in formato flat.
    
    Args:
        result (dict): Risultato dello speedtest
        
    Returns:
        dict: Messaggio flat per Kafka
    """
    # Appiattisci il risultato
    flat_data = flatten_dict(result)
    
    # Rimuovi il prefisso 'result_' dalle chiavi
    flat_data = {k[7:] if k.startswith("result_") else k: v for k, v in flat_data.items()}
    
    # Aggiungi timestamp se non presente
    if 'timestamp' not in flat_data:
        flat_data['timestamp'] = datetime.now(timezone.utc).isoformat()

    isp_info = get_isp_info()
    gateway_mac = get_gateway_mac()
    
    # Crea un messaggio flat
    flat_message = {
        "metric_type": "speedtest",
        "timestamp": flat_data['timestamp'],
        "hostname": get_hostname(),
        "public_ip": isp_info['ip'],
        "service_provider": isp_info['isp'],
        "gateway_mac": gateway_mac,
        "isp": flat_data.get('isp', 'unknown'),
        "server_name": flat_data.get('server_name', 'unknown'),
        "server_location": flat_data.get('server_location', 'unknown')
    }
    
    # Aggiungi tutti i dati dello speedtest con prefisso 'speedtest_'
    for k, v in flat_data.items():
        if k not in ['timestamp', 'isp', 'server_name', 'server_location']:
            #flat_message[f"speedtest_{k}"] = v
            flat_message[f"{k}"] = v
    
    # Rimuovi campi con valore "Unknown" o None
    flat_message = {k: v for k, v in flat_message.items() if v != "Unknown" and v is not None}
    
    return flat_message

def send_to_kafka(metric_type: str, data: dict, kafka_config: dict, max_retries: int = 3, retry_delay: int = 10, mirror_config: dict = None) -> bool:
    """
    Invia i dati a Kafka in formato flat JSON, supportando l'autenticazione SASL_SSL.
    
    Args:
        metric_type (str): Tipo di metrica, es. 'ping', 'download', ecc.
        data (dict): Dati del test
        kafka_config (dict): Configurazione per la connessione a Kafka
        max_retries (int, optional): Numero massimo di tentativi di invio. Default 3.
        retry_delay (int, optional): Ritardo tra i tentativi in secondi. Default 10.
        
    Returns:
        bool: True se l'invio è riuscito, False altrimenti
    """

    # Prepara un messaggio flat
    flat_message = prepare_flat_message(metric_type, data)
    
    for attempt in range(max_retries):
        try:
            # Configurazione di base
            producer_config = {
                'bootstrap_servers': kafka_config['bootstrap_servers'].split(','),
                'value_serializer': lambda v: json.dumps(v).encode('utf-8'),
                'acks': 1,  # Come intero, non come stringa
                'request_timeout_ms': int(kafka_config.get('request_timeout_ms', 30000)),
                'retry_backoff_ms': int(kafka_config.get('retry_backoff_ms', 1000)),
                'reconnect_backoff_ms': 5000,
                'reconnect_backoff_max_ms': 60000,
                'security_protocol': 'SASL_SSL',
                'sasl_mechanism': 'PLAIN',
                'sasl_plain_username': kafka_config['sasl_plain_username'],
                'sasl_plain_password': kafka_config['sasl_plain_password'],
                'ssl_check_hostname': False,
                'api_version_auto_timeout_ms': 60000
                }

            #producer_config['api_version'] = (1, 0, 0)
            
            # Log delle configurazioni (escludendo password)
            log_config = {k: v for k, v in producer_config.items() if k != 'sasl_plain_password'}
            logging.debug(f"Kafka producer configuration: {log_config}")
            
            # Crea il producer con la configurazione
            producer = KafkaProducer(**producer_config)

            # Aggiungi un timestamp attuale al messaggio
            if 'timestamp' not in flat_message:
                flat_message['timestamp'] = datetime.now(timezone.utc).isoformat()

            # Tenta di inviare il messaggio
            logging.info(f"Sending message to Kafka topic {kafka_config['topic']} for metric type: {metric_type}")
            future = producer.send(kafka_config['topic'], value=flat_message)
            record_metadata = future.get(timeout=int(kafka_config.get('request_timeout_ms', 30000)) / 1000)
            
            producer.flush()
            producer.close()  # Chiudi esplicitamente il producer per liberare risorse
            
            logging.info(f"Message successfully sent to topic {record_metadata.topic}, partition {record_metadata.partition}, offset {record_metadata.offset}")

            # Log di debug per verificare la struttura del messaggio
            logging.debug(f"Kafka message structure: {json.dumps(flat_message, indent=2)}")

            # Invio al cluster mirror (non blocca il flusso principale)
            if mirror_config:
                send_to_kafka_mirror(metric_type, flat_message, mirror_config)

            return True
        except KafkaError as e:
            logging.error(f"Failed to send data to Kafka (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logging.error("Max retries reached. Failed to send data to Kafka.")
                return False
        except Exception as e:
            logging.error(f"Unexpected error while sending to Kafka: {e}")
            import traceback
            logging.error(traceback.format_exc())
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logging.error("Max retries reached. Failed to send data to Kafka.")
                return False

def send_to_kafka_mirror(metric_type: str, flat_message: dict, mirror_config: dict, max_retries: int = 2, retry_delay: int = 5) -> None:
    """
    Invia un messaggio già preparato al cluster mirror in base al metric_type.
    Non blocca il flusso principale: errori vengono solo loggati come warning.

    Args:
        metric_type (str): Tipo di metrica (ping, download, web_browsing, iperf, speedtest)
        flat_message (dict): Messaggio flat già preparato
        mirror_config (dict): Configurazione del cluster mirror
        max_retries (int): Numero massimo di tentativi. Default 2.
        retry_delay (int): Ritardo tra tentativi in secondi. Default 5.
    """
    topic_key = f"topic_{metric_type}"
    if topic_key not in mirror_config:
        logging.debug(f"No mirror topic configured for metric_type '{metric_type}', skipping mirror send")
        return

    mirror_topic = mirror_config[topic_key]

    for attempt in range(max_retries):
        try:
            producer_config = {
                'bootstrap_servers': mirror_config['bootstrap_servers'].split(','),
                'value_serializer': lambda v: json.dumps(v).encode('utf-8'),
                'acks': 1,
                'request_timeout_ms': 30000,
                'retry_backoff_ms': 1000,
                'reconnect_backoff_ms': 5000,
                'reconnect_backoff_max_ms': 60000,
                'security_protocol': 'SASL_SSL',
                'sasl_mechanism': 'PLAIN',
                'sasl_plain_username': mirror_config['sasl_plain_username'],
                'sasl_plain_password': mirror_config['sasl_plain_password'],
                'ssl_check_hostname': False,
                'api_version_auto_timeout_ms': 60000
            }

            producer = KafkaProducer(**producer_config)
            future = producer.send(mirror_topic, value=flat_message)
            record_metadata = future.get(timeout=30)
            producer.flush()
            producer.close()

            logging.info(f"[MIRROR] Message sent to {mirror_topic}, partition {record_metadata.partition}, offset {record_metadata.offset}")
            return

        except Exception as e:
            logging.warning(f"[MIRROR] Failed to send to {mirror_topic} (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                logging.warning(f"[MIRROR] Max retries reached for topic {mirror_topic}. Mirror send skipped.")
                
async def test_speedtest(server_id: str, kafka_config: dict, mirror_config: dict = None) -> Optional[pd.DataFrame]:
    
    
    """
    Eseguo un test di velocità utilizzando speedtest-cli. Misuro la velocità di
    download, upload e la latenza verso un server specifico. Analizzo l'output
    JSON, preparo un messaggio formattato e lo invio a Kafka.
    
    
    command:
        
        speedtest -f json --output-header --accept-license --accept-gdpr
        
    """
    
    logging.info(f"{'=' * 80}")
    logging.info(f"SPEEDTEST - Starting")
    logging.info(f"Command: {' '.join(['/usr/bin/speedtest', '-f', 'json', '--output-header', '--accept-license', '--accept-gdpr'])}")
    logging.info(f"{'=' * 80}")
    try:
        cmd = ['/usr/bin/speedtest', '-f', 'json', '--output-header', '--accept-license', '--accept-gdpr']
        logging.info(f"Executing command: {' '.join(cmd)}")
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        # Speedtest scrive messaggi di licenza su stderr (non sono errori)
        if stderr:
            stderr_text = stderr.decode()
            # Solo log DEBUG (non ERROR) per messaggi di licenza
            if 'License acceptance recorded' in stderr_text or 'EULA' in stderr_text:
                logging.debug(f"Speedtest license info: {stderr_text[:200]}...")
            else:
                # Veri errori
                logging.warning(f"Speedtest stderr: {stderr_text}")

        logging.info("Speedtest completed successfully. Processing results...")
        result = json.loads(stdout.decode())
        
        logging.info("Preparing speedtest message...")
        speedtest_message = prepare_speedtest_message(result)
        
        #send_to_kafka("speedtest", speedtest_message['fields'], kafka_config)
        send_to_kafka("speedtest", speedtest_message, kafka_config, mirror_config=mirror_config)

        # Risultati stampati alla fine dello script nel riepilogo generale
        #return pd.DataFrame([speedtest_message['fields']])
        return pd.DataFrame([speedtest_message])
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from speedtest output: {e}")
        logging.error(f"Raw stdout: {stdout.decode()}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error during speedtest: {e}")
        logging.error(f"Raw stdout: {stdout.decode()}")
        return None