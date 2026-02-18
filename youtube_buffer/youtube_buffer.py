from selenium.webdriver.common.by import By                         # type: ignore
from selenium.webdriver.support.ui import WebDriverWait             # type: ignore
from selenium.webdriver import ActionChains                         # type: ignore
from selenium.webdriver.support import expected_conditions as EC    # type: ignore
import traceback
import time
import os
from browser import get_driver_settings
from youtube import accept_cookies
from runner import perform_buffer_video

video_links_class_name = "yt-simple-endpoint.ytd-thumbnail"
consent_button_xpath = "//button[@aria-label='Accept the use of cookies and other data for the purposes described']"
ads_button_selectors = [".ytp-skip-ad button"]
start_time = int(time.time())

## BIG FUNCTION
def play():
    
    ## BIG TRY CATCH
    try:
        ## BLOCK 1 - DRIVER SETTINGS
        driver = get_driver_settings()
        
        ## BLOCK 2 - ACCEPT COOKIES FUNCTION
        accept_cookies(driver ,start_time)
        
        ## CONNECTORS BEFORE CONTINUE FLOW
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'h1.ytd-watch-metadata')))
        time.sleep(1)
        print(f"RUN: {start_time} | ts {int(time.time())} Video should start shortly")
     
        # prepare video player
        try:
        
            movie_player = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "movie_player")))   
            print(f" run {start_time}-> YouTube player loaded")
        
        except Exception:
            
            print(f" run  {start_time}-> YouTube player not found after waiting")
            driver.save_screenshot("debug_no_movie_player.png")
            raise
        
        # play video
        hover = ActionChains(driver).move_to_element(movie_player)
        hover.perform()
        ActionChains(driver).context_click(movie_player).perform()
        time.sleep(2)

        DIV_TO_KEY = {
            
            '1': "Video ID / sCPN",
            '2': "Viewport / Frames",
            '3': "Current / Optimal Res",
            '4': "Volume / Normalized",
            '5': "Codecs",
            '6': "Color",
            '9': "Connection Speed", 
            '10': "Network Activity", 
            '11': "Buffer Health",
            '12': "Live Latency",
            '15': "Mystery Text"
        }
        
        keys = [
            
            "Video ID / sCPN",
            "Viewport / Frames",
            "Current / Optimal Res",
            "Volume / Normalized",
            "Codecs",
            "Color",
            "Connection Speed", 
            "Network Activity", 
            "Buffer Health",
            "Live Latency",
            "Mystery Text"
        ]

        headers = ['script_time', 'start_time', 'Video ID', 'Frames', 'Current Res', 'Connection Speed', 'Network Activity', 'Buffer Health', 'time', 'i']
        video_id = "PdzOkN9_F9A"
        last_not_found_div_id = ''
        file_path = "youtube_stats.txt"
        first_line = None
        
        ## IF STATEMENT 1 - FIRST GRADE of BIG TRY CATCH

        if not os.path.isfile(file_path):
            first_line = f"{';'.join(headers)}\n"
            
        with open(file_path, 'a+') as f:
            
            if first_line is not None:
                f.write(first_line)
            j = 0
            i = 0
            factor = float(0)
            enable_skipping = True
            last_video_id = video_id
            last_ad_ts = 0.0
            last_ts = 0.0
            last_buffer = 0.0
            last_res = ''
            
            # retrive buffer of the video       
            perform_buffer_video(   j ,i ,f,
                                    hover,
                                    driver,
                                    video_id,
                                    last_not_found_div_id,
                                    start_time,
                                    keys ,
                                    headers,
                                    factor,
                                    enable_skipping,
                                    last_video_id ,
                                    last_ad_ts,
                                    last_ts,
                                    last_buffer,
                                    last_res)
                    
        print(f"RUN: {start_time} | Ending")
        
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
    
    retry = 0
    while retry < 5:
        try:
            play()
            break
        except Exception as e:
            print(f"RUN: {start_time} | ts {int(time.time())} Exception outside video playing, retry {retry} {traceback.format_exc()}")
        retry+=1
        time.sleep(5)