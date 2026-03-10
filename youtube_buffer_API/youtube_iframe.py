import time
from selenium.webdriver.common.by import By   # type: ignore

def change_resolution(driver, start_time):

    resolutions_priority = [
        "2160p",   # 4K
        "1440p",   # 2K
        "1080p",
        "720p"
    ]

    print(f"RUN: {start_time} | Selecting best available resolution")

    time.sleep(0.2)

    # open settings
    sb = driver.find_element(By.CSS_SELECTOR, ".ytp-button.ytp-settings-button")
    sb.click()

    time.sleep(0.3)

    # open quality menu
    try:
        elem = driver.find_element(By.CSS_SELECTOR, 'div.ytp-menuitem[role="menuitem"] > div.ytp-menuitem-content span')
        elem.click()
    except:
        try:
            elem = driver.find_element(By.CSS_SELECTOR, 'div.ytp-menuitem:nth-child(5)')
            elem.click()
        except:
            elem = driver.find_element(By.CSS_SELECTOR, 'div.ytp-menuitem:nth-child(4)')
            elem.click()

    time.sleep(2)

    # get available resolutions
    res = driver.find_elements(By.CLASS_NAME, "ytp-menuitem-label")

    for target in resolutions_priority:
        for item in res:
            if target in item.text:
                item.click()
                print(f"RUN: {start_time} | Resolution selected {target}")
                return

    print(f"RUN: {start_time} | No preferred resolution available")