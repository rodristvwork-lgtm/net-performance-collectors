from selenium import webdriver # type: ignore
import time
import os

start_time = int(time.time())

def get_driver_settings():
    
    homepage = "https://www.youtube.com/watch?v=PdzOkN9_F9A"
    #homepage = "https://www.youtube.com/watch?v=WO2b03Zdu4Q" # 45 seconds of video
    
    print(f"RUN: {start_time} | {homepage}")
    
    srv = webdriver.FirefoxService(os.path.join("driver", "geckodriver"))
    opt = webdriver.FirefoxOptions()
    opt.add_argument("--no-sandbox")
    opt.add_argument("--disable-dev-shm-usage")
    opt.add_argument("--display=:0")     # to visualize the video
    
    opt.set_preference("media.ffmpeg.enabled", True)
    opt.set_preference("media.ffvpx.enabled", False)
    opt.set_preference("media.av1.enabled", False)
    opt.set_preference("media.webm.enabled", False)
    opt.set_preference("media.hardware-video-decoding.enabled", True)

    driver = webdriver.Firefox(service=srv, options=opt)
    driver.maximize_window()
    time.sleep(3)
    driver.get(homepage)
    
    return driver