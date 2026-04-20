import time
from selenium.webdriver.common.by import By                         # type: ignore 
from selenium.webdriver.common.action_chains import ActionChains    # type: ignore
from selenium.webdriver.support.ui import WebDriverWait             # type: ignore
from selenium.webdriver.support import expected_conditions as EC    # type: ignore


def change_resolution(driver, start_time, resolution):

    resolution_map = {
        "high": ["2160p", "1440p", "1080p"],
        "medium": ["720p", "480p"],
        "low": ["360p", "240p", "144p"]
    }

    resolutions_priority = resolution_map.get(
        resolution,
        ["2160p", "1440p", "1080p", "720p", "480p", "360p", "240p", "144p"]
    )

    print(f"RUN: {start_time} | Selecting best available resolution")

    
    try:
        actions = ActionChains(driver)
        actions.move_by_offset(10, 10).perform()
        time.sleep(0.3)
    except:
        pass

    # selector
    settings_selectors = [
        ".player-settings-icon > c3-icon:nth-child(1) > span:nth-child(1) > div:nth-child(1)"
        ".player-settings-icon"
        "button.player-settings-icon",
        "button[aria-label='Playback Settings']",
        ".player-settings-icon",
        ".icon-button.player-settings-icon",
        # fallbacks for older UI
        "button[aria-label='Settings']",
        ".ytp-settings-button",
        "button.ytp-button.ytp-settings-button",
    ]

    sb = None
    for sel in settings_selectors:
        try:
            sb = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, sel))
            )
            print(f"RUN: {start_time} | Settings button found via: {sel}")
            break
        except:
            continue

    if not sb:
        print(f"RUN: {start_time} | ERROR: Settings button not found")
        return

    sb.click()
    time.sleep(0.4)

    # select desired resolution
    try:
        quality_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//yt-list-item-view-model[.//span[contains(text(), 'Quality')]]"
            ))
        )
        quality_button.click()
        print(f"RUN: {start_time} | Quality menu opened via C3 selector")
    except Exception as e:
        print(f"RUN: {start_time} | ERROR: Could not open quality menu (C3 UI): {e}")
        return

    time.sleep(1.2)


    for target in resolutions_priority:
        try:
            res_option = driver.find_element(
                By.XPATH,
                f"//yt-list-item-view-model//span[contains(text(), '{target}')]"
            )
            res_option.click()
            print(f"RUN: {start_time} | Resolution selected {target}")
            return
        except:
            continue
    print(f"RUN: {start_time} | No preferred resolution available")