
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import traceback
import time
from browser_settings import get_driver_settings


start_time = int(time.time())

def play(url, minutes):
    driver = None
    try:
        driver = get_driver_settings(url)

        # Wait for iframe
        iframe = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "iframe"))
        )

        # Switch into YouTube iframe
        driver.switch_to.frame(iframe)

        # Wait for play button
        play_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ytp-large-play-button"))
        )
        # still wait before play
        time.sleep(5)
        # Click play
        play_button.click()

        # Work loop
        end_time = time.time() + minutes * 60
        while time.time() < end_time:
            print("To Fetch Data")
            time.sleep(1)

        return True

    except Exception as e:
        print(f"[play] Exception: {e}\n{traceback.format_exc()}")
        return False

    finally:
        if driver:
            try: driver.quit()
            except: pass
            

if __name__ == "__main__":
    
    try:
        url = "http://192.168.1.58:8000/"
        play(url, 10)
    except Exception as e:
            print(f"RUN: {start_time} | ts {int(time.time())} Exception outside video playing {traceback.format_exc()}")