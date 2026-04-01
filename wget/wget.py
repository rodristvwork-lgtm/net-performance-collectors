import subprocess
import os
import re
from datetime import datetime

def wget_function(url, output_file, final_file, bitrate_file):
    
    try:
        dir_name = "results"
        os.makedirs(dir_name, exist_ok=True)
        file_path = os.path.join(dir_name, final_file)

        # Run wget (blocking)
        command = ["wget", url, "-o", output_file]
        subprocess.run(command)

        # Append last lines of wget log
        with open(file_path, "a") as file_sav:
            file_sav.write("-----------------------------------------------\n")
            file_sav.write(str(datetime.now()) + "\n\n")

            with open(output_file, "r") as file:
                lines = file.readlines()
                last_lines = lines[-4:] if len(lines) >= 4 else lines
                file_sav.writelines(last_lines)

    except Exception as e:
        print("Error:", e)

    finally:
        # Delete the downloaded file (minimal required fix)
        downloaded_file = os.path.basename(url)
        if os.path.exists(downloaded_file):
            os.remove(downloaded_file)
            print(f"Deleted downloaded file: {downloaded_file}")
        
        
if __name__ == "__main__":
    
    url = "http://ipv4.download.thinkbroadband.com:8080/1GB.zip"
    file_path = 'bitrates.csv'
    output_file = "terminal_output.txt"
    current_date = datetime.now().strftime("%Y-%m-%d")
    final_file = f"terminal_wget_output_{current_date}.txt"
    dir = os.getcwd()
    
    wget_function(url, output_file, final_file, file_path)

    for f in os.listdir(dir):
        if re.search(r"1GB.zip\d?", f):
            os.remove(f)

    if os.path.exists(output_file):
        os.remove(output_file)