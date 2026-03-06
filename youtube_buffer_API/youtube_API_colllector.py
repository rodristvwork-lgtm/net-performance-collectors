import traceback
import time
from browser_settings import get_driver_settings

start_time = int(time.time())

def play(url,minutes):
    
    try:
        
        ## DRIVER SETTINGS
        driver = get_driver_settings(url)
          
        time.sleep(minutes*60) 
        
    finally:
        try:
            driver.close()
        except:
            pass
        try:
            driver.quit()
        except:
            pass
    return True

if __name__ == "__main__":
    
    try:
        url = "http://192.168.1.58:8000/"
        play(url, 1)
    except Exception as e:
            print(f"RUN: {start_time} | ts {int(time.time())} Exception outside video playing {traceback.format_exc()}")