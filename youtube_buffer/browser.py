from selenium import webdriver
import time
import os

start_time = int(time.time())

def get_driver_settings():
    
    homepage = "https://www.youtube.com/watch?v=PdzOkN9_F9A"
    print(f"RUN: {start_time} | {homepage}")

    srv = webdriver.FirefoxService(os.path.join("driver", "geckodriver"))
    opt = webdriver.FirefoxOptions()
    opt.set_preference(
        "general.useragent.override",
         "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                            "(KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36")
    profile_path = "/home/situser/.mozilla/firefox/qnjqjqw5.default-release"
    opt.set_preference("profile", profile_path)
    opt.set_preference("layers.acceleration.disabled", True)
    opt.set_preference("gfx.canvas.azure.accelerated", False)
    opt.set_preference("dom.webdriver.enabled", False)
    opt.set_preference('useAutomationExtension', False)
    opt.set_preference("security.mixed_content.block_active_content", False)
    opt.set_preference("security.mixed_content.block_display_content", False)
    opt.add_argument("--headless")
    opt.add_argument("--no-sandbox")
    opt.add_argument("--disable-dev-shm-usage")
    opt.set_preference("security.sandbox.content.level", 0)

    driver = webdriver.Firefox(service=srv, options=opt)
    driver.maximize_window()
    time.sleep(3)
    driver.get(homepage)
    
    return driver