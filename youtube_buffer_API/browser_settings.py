from selenium import webdriver                          # type: ignore
from selenium.webdriver.firefox.service import Service  # type: ignore
import time
import os

start_time = int(time.time())

def get_driver_settings(url):

    print(f"RUN: {start_time} | {url}")

    # Absolute path to geckodriver in project root
    gecko_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "geckodriver")
    )

    srv = Service(executable_path=gecko_path)

    opt = webdriver.FirefoxOptions()
    opt.add_argument("--headless")
    opt.add_argument("--no-sandbox")
    opt.add_argument("--disable-dev-shm-usage")
    opt.add_argument("--width=1920")
    opt.add_argument("--height=1080")

    opt.set_preference("media.ffmpeg.enabled", True)
    opt.set_preference("media.ffvpx.enabled", False)
    opt.set_preference("media.av1.enabled", False)
    opt.set_preference("media.webm.enabled", False)
    opt.set_preference("media.hardware-video-decoding.enabled", True)

    driver = webdriver.Firefox(service=srv, options=opt)
    driver.maximize_window()
    time.sleep(3)
    driver.get(url)
    
    return driver