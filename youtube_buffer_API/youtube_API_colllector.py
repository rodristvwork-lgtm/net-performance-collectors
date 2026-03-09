from selenium.webdriver.support.ui import WebDriverWait             # type: ignore
from selenium.webdriver.support import expected_conditions as EC    # type: ignore
from selenium.webdriver.common.by import By                         # type: ignore
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

        resolution = "1080p"
        resolution2 = "720p"
        
        print(f"RUN: {start_time} | Selecting resolution {resolution}")
        time.sleep(0.2)
        sb = driver.find_element(by=By.CSS_SELECTOR, value='.ytp-button.ytp-settings-button')
        sb.click()
        time.sleep(0.3)
        try:
            elem = driver.find_element(by=By.CSS_SELECTOR, value='div.ytp-menuitem[role="menuitem"] > div.ytp-menuitem-content span')
            elem.click()
        except:
            try:
                elem = driver.find_element(by=By.CSS_SELECTOR, value='div.ytp-menuitem:nth-child(5) > div:nth-child(1)')
                elem.click()
            except:
                elem = driver.find_element(by=By.CSS_SELECTOR, value='div.ytp-menuitem:nth-child(4) > div:nth-child(1)')
                elem.click()

        time.sleep(2)
        res = driver.find_elements(by=By.CLASS_NAME, value="ytp-menuitem-label")
        for item in res:
            # print(item.text)
            if resolution in item.text:
                item.click()
                print(f"RUN: {start_time} | Resolution selected", resolution)
                break
        else:
            for item in res:
                if resolution2 in item.text:
                    item.click()
                    print(f"RUN: {start_time} | Resolution selected", resolution2)
                    break

        print(f'RUN: {start_time} | Resolution {resolution} not available yet')
        
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