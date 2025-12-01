import subprocess
from datetime import datetime
import time
import os

def ping_func():
    
	try:
		dir_name = "results"	
		os.makedirs(dir_name, exist_ok=True)
		file_path = os.path.join(dir_name, "ping_Ebay_1500B_SL_10s.txt")
  
		with open(file_path, 'a') as file:
			command = ['ping', '-c', '10', '-s', '1500', '-O', 'ebay.com']
			file.write('\n')
			file.write(str(datetime.now())+'\n')
			file.write('\n')
			result = subprocess.run(command, stdout = file)
			time.sleep(10)

		dir_name = "results"	
		os.makedirs(dir_name, exist_ok=True)
		file_path = os.path.join(dir_name, "ping_Ebay_6400B_SL_10s.txt")
  
		with open(file_path, 'a') as file:
			
			command = ['ping', '-c', '10', '-s', '6400', '-O', 'ebay.com']
			file.write('\n')
			file.write(str(datetime.now())+'\n')
			file.write('\n')
			result = subprocess.run(command, stdout = file)
			time.sleep(10)

		dir_name = "results"	
		os.makedirs(dir_name, exist_ok=True)
		file_path = os.path.join(dir_name, "ping_Ebay_64B_SL_10s.txt")
		with open(file_path, 'a') as file:
			
			command = ['ping', '-c', '10', '-O', 'ebay.com']
			file.write('\n')
			file.write(str(datetime.now())+'\n')
			file.write('\n')
			result = subprocess.run(command, stdout = file)
			time.sleep(10)
   
		dir_name = "results"	
		os.makedirs(dir_name, exist_ok=True)
		file_path = os.path.join(dir_name, "ping_Ebay_1500B_SL_300s.txt")
		with open(file_path, 'a') as file:
			
			command = ['ping', '-c', '240', '-s', '1500', '-O', 'ebay.com']
			file.write('\n')
			file.write(str(datetime.now())+'\n')
			file.write('\n')
			result = subprocess.run(command, stdout = file)
			time.sleep(10)

		dir_name = "results"	
		os.makedirs(dir_name, exist_ok=True)
		file_path = os.path.join(dir_name, "ping_Ebay_64B_SL_300s.txt")
		with open(file_path, 'a') as file:
			
			command =  ['ping', '-c', '240', '-O', 'ebay.com']
			file.write('\n')
			file.write(str(datetime.now())+'\n')
			file.write('\n')
			result = subprocess.run(command, stdout = file)
			time.sleep(10)

		dir_name = "results"	
		os.makedirs(dir_name, exist_ok=True)
		file_path = os.path.join(dir_name, "ping_Ebay_6400B_SL_300s.txt")
		with open(file_path, 'a') as file:
			
			command =  ['ping', '-c', '240', '-s', '6400', '-O', 'ebay.com']
			file.write('\n')
			file.write(str(datetime.now())+'\n')
			file.write('\n')
			result = subprocess.run(command, stdout = file)
			time.sleep(10)

	except Exception as e:
		print(f"Error: {e}")
  
if __name__ == "__main__":
    ping_func()