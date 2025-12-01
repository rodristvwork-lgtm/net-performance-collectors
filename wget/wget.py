import subprocess
import os
import re
from datetime import datetime

def wget_function(url, output_file, final_file, bitrate_file):
    
	try:
		dir_name = "results"
		os.makedirs(dir_name, exist_ok=True)
		file_path = os.path.join(dir_name, final_file)
		command = ["wget", url, "-o", output_file]
		subprocess.run(command)
  
		with open(file_path,"a") as file_sav:
			file_sav.write("-----------------------------------------------\n")
			file_sav.write(str(datetime.now())+"\n")
			file_sav.write("\n")
   
			with open(output_file, "r") as file:
				aa=file.readlines()
				for i in range (4,1,-1):
					file_sav.write(aa[-i])
	
	except Exception as e:
		print("Error:", e)
  
if __name__ == "__main__":
	
	url = "http://ipv4.download.thinkbroadband.com:8080/1GB.zip"
	file_path = 'bitrates.csv'  
	output_file = "terminal_output.txt"
	current_date = datetime.now().strftime("%Y-%m-%d")
	final_file= f"terminal_wget_output_{current_date}.txt"
	dir = os.getcwd()
	
	wget_function(url, output_file, final_file, file_path)

	for f in os.listdir(dir):
		if re.search(r"1GB.zip\d?", f):
			os.remove(f)

	os.remove(output_file)