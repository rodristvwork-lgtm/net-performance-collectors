import socket
import subprocess
import os
from datetime import datetime
from IperfModel import IperfJob

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
    proto = "UDP" if udp else "TCP"
    direction = "DL" if download else "UP"
    iperf_type = f"{direction}{proto}"
    
    # prepare result directory if saving  
    os.makedirs(f"results/{proto}", exist_ok=True)
    today = datetime.now().strftime("%m%y")
    base_name = f"{iperf_type}_iperf_{today}_"
    
    # find next avaiable counter
    counter = 1
    while True:
        filename = f"results/{proto}/{base_name}{counter}.txt"
        if not os.path.exists(filename):
            break
        counter += 1
        
    return filename

def run_iperf(server_ip, duration, udp, download ,start_port ,end_port, bandwidth = None, save = False):
    
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

        print(f"using port: {port}")
        print(f"command: {cmd}")
        
        # catch error input
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            # save temporary the iperf lines
            process_lines = []
                        
            for line in process.stdout:
                process_lines.append(line)

                if "iperf Done." in line:
                    process.terminate()
                    print("iperf done successful")

                    if save:
                        filename = build_type_for_result(udp, download)
                        with open(filename, "w") as f:
                            f.writelines(process_lines)
                    return port

        except subprocess.CalledProcessError:
            pass
        
    return None


def run_iperf_job(job, server_ip, start_port, end_port):
    return run_iperf(
        server_ip=server_ip,
        duration=job.duration,
        udp=job.udp,
        download=job.download,
        start_port=start_port,
        end_port=end_port,
        bandwidth=job.bandwidth,
        save=job.save
    )
    
def iperf_orchestrator(server_ip, jobs, start_port, end_port):
    
    current_port = start_port

    for index, job in enumerate(jobs, start=1):

        proto = "UDP" if job.udp else "TCP"
        direction = "DL" if job.download else "UP"
        print(f"\n=== Running job #{index}: {direction}-{proto} on port {current_port} ===")

        result_port = run_iperf_job(
            job=job,
            server_ip=server_ip,
            start_port=current_port,
            end_port=end_port
        )

        if result_port is None:
            print(f"Job #{index} failed on all ports.")
            return False

        print(f"Job #{index} succeeded on port {result_port}.")
        current_port = result_port

    print("\nAll iperf jobs completed successfully.")
    return True

if __name__ == "__main__":

    jobs = [
        IperfJob(udp=False, download=False, duration=90),
        IperfJob(udp=False, download=True,  duration=90),
        IperfJob(udp=True,  download=False, duration=90, bandwidth="10M"),
        IperfJob(udp=True,  download=True,  duration=90, bandwidth="10M"),
        
    ]
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    print(f" start : {hour}:{minute}")
    iperf_orchestrator(
        server_ip="iperf3.moji.fr", # 5200-5240
        jobs=jobs,
        start_port=5220,
        end_port=5230
    )
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    print(f" end : {hour}:{minute}")