import logging
import os
import json

from datetime import datetime

settings: dict

def _init_logging() -> None:
    """initialize logging system"""

    logging.basicConfig(filename=settings["log_file_path"], filemode="w", format='%(asctime)s - %(levelname)s:%(message)s', level=logging.DEBUG)
    logging.info("logging system initialized")

def _read_settings() -> None:
    """read and stores settings to global variable"""

    global settings
    with open(f"{os.path.dirname(__file__)}/settings.json") as json_file:
        settings = json.load(json_file) 

def _init() -> None:
    """initialize config"""

    _read_settings()
    _init_logging()
    #sets result file name for current execution
    settings["results_file_name"] = settings["results_file_name"].format(
        hostname = get_nodename(),
        ts=datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    )

def get_nodename() -> str:
    """returns host name"""

    name: str
    try:
        name = settings["host"]["default_node_name"]
    except Exception:
        logging.error(f"failed to get host name, default: {name}")
    return name

def get_modem_info(to_ret):
    
    try:
        to_ret["ipgw"] = settings["host"]["ipgw"]
        to_ret["esn"] = settings["host"]["esn"]
        to_ret["siteid"] = settings["host"]["siteid"]
        to_ret["beam"] = settings["host"]["beam"]
        to_ret["outroute_freq"] = settings["host"]["outroute_freq"]

    except Exception:
        logging.error(f"failed to get modem info")
    return to_ret

def get_hw_type():
    """returns Hardware type"""
    hw_type: str
    try:
        hw_type = settings["host"]["Hardware_type"]
    except Exception:
        logging.error(f"failed to get Hardware type, default: {hw_type}")
    return hw_type   

def get_sw_type():
    """returns Software type"""
    sw_type: str
    try:
        sw_type = settings["host"]["Software_version"]
    except Exception:
        logging.error(f"failed to get Software type, default: {sw_type}")
    return sw_type


def _init():
    _read_settings()
    _init_logging()
    settings["results_file_name"] = settings["results_file_name"].format(
        hostname=get_nodename(),
        ts=datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    )

_init()

if __name__ == "__main__":
    print("Config initialized")
