from selenium.webdriver.common.by import By                         # type: ignore
from selenium.webdriver.support.ui import WebDriverWait             # type: ignore
from selenium.webdriver import ActionChains                         # type: ignore
from selenium.webdriver.support import expected_conditions as EC    # type: ignore
import traceback
import time
from browser import get_driver_settings
from youtube import accept_cookies

start_time = int(time.time())

def play():
    
    ## BIG TRY CATCH
    try:
        ## DRIVER SETTINGS
        driver = get_driver_settings()
        
        ## COOKIES FUNCTION
        accept_cookies(driver ,start_time)
        
        ## CONNECTORS BEFORE CONTINUE FLOW
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'h1.ytd-watch-metadata')))
        time.sleep(1)
        print(f"RUN: {start_time} | ts {int(time.time())} Video should start shortly")
     
        # PREPARE VIDEO PLAYER
        try:
            
            movie_player = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "movie_player")))   
            print(f" run {start_time}-> YouTube player loaded")
        
        except Exception:           
            print(f" run  {start_time}-> YouTube player not found after waiting")
            raise
        # PLAY VIDEO
        hover = ActionChains(driver).move_to_element(movie_player)
        hover.perform()
        
        #ActionChains(driver).context_click(movie_player).perform() # to activate nerd mode
        
        time.sleep(1990)
        # WAIT UNTIL VIDEO ENDS
        print("Waiting for video to finish...")

        while True:
            state = driver.execute_script("return document.getElementById('movie_player').getPlayerState()")
            time.sleep(1)

        # 0 means ENDED
            if state == 0:
                print("Video finished.")
            break
            
        # 1 means PLAYING, 2 means PAUSED, 3 means BUFFERING, etc.
        
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
    
    try:
        play()
    except Exception as e:
            print(f"RUN: {start_time} | ts {int(time.time())} Exception outside video playing {traceback.format_exc()}")