import time
from selenium.webdriver.common.by import By # type: ignore
from selenium.common.exceptions import NoSuchElementException # type: ignore

start_time = int(time.time())
ads_button_selectors = [".ytp-skip-ad button"]


## FUNCTION 1
def change_resolution(driver):

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
        
        
## FUNCTION 2
def click_skip_adds(driver):
    
    for selector in ads_button_selectors:
        try:
            skip_adds_button = driver.find_element(By.CSS_SELECTOR, selector)
            if not skip_adds_button.is_displayed():
                time.sleep(3)
                driver.execute_script("arguments[0].style.display = 'block';", skip_adds_button)
            skip_adds_button.click()
            print(f'RUN: {start_time} | ts {int(time.time())} Skipped advertisement')
            break
        except NoSuchElementException as e:
            pass
        except Exception:
            pass