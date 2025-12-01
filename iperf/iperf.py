import socket
import subprocess
import os
from datetime import datetime

def get_local_ip():
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]         
    finally:
        s.close()
    return ip

def build_type_for_result(udp, download):
    
    # build type string for filename
    proto = "udp" if udp else "tcp"
    direction = "dl" if download else "up"
    iperf_type = f"{proto}_{direction}"
    
    # prepare result directory if saving  
    os.makedirs("results", exist_ok=True)
    today = datetime.now().strftime("%H_%M_%d_%m_%y")
    filename = f"results/iperf_result_time_{today}_{iperf_type}.txt"
    
    return filename

def run_iperf(server_ip, duration, udp, download, bandwidth = None, save = False):
    
    start_port = 9204
    end_port = 9240
    ip_address = get_local_ip()
      
    for port in range(start_port, end_port+1):
        
        cmd = [
            "iperf3",
            "-c", server_ip,
            "-B", ip_address,
            "-t", str(duration),
            "-p", str(port)
        ]
        
        if save:
            filename = build_type_for_result(udp, download)  
        if udp:
            cmd.extend(["-u","-b",bandwidth])
        
        if download: 
            cmd.extend(["-R"])
        else:
            cmd.extend(["--get-server-output"])

        print(f"port: {port}")
        print(f"command: {cmd}")
        
        # catch error input
        try:
            
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

            # save temporary the iperf lines
            process_lines = []
                        
            for line in process.stdout:
                
                print(line, end="")
                process_lines.append(line)
                                    
                if "iperf Done." in line:
                    process.terminate()
                    
                    if save:
                        
                        filename = build_type_for_result(udp, download)
                        
                        with open(filename, "w") as f:
                            f.writelines(process_lines)
                            f.close()
                            
                    return True
                
        except subprocess.CalledProcessError as e:

            print(f"error found: {e}")
            print(f"lets try with port: {port}")
            
    return False

if __name__ == "__main__":
    
    # TCP DOWNLOAD
    #run_iperf("178.215.228.109", duration=50, udp=False, download=True, save=True)
    # TCP UPLOAD
    #run_iperf("178.215.228.109", duration=50, udp= False, download=False, save= True )
    # UDP DOWNLOAD
    #run_iperf("178.215.228.109", duration=50, udp= True, download=True, bandwidth="10M", save= True)
    # UDP DOWNLOAD
    run_iperf("178.215.228.109", duration=50, udp= True, download= False, bandwidth="10M", save= True)

    