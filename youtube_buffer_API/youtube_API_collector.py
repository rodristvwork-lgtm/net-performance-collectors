from selenium.webdriver.support.ui import WebDriverWait             # type: ignore
from selenium.webdriver.support import expected_conditions as EC    # type: ignore
from selenium.webdriver.common.by import By                         # type: ignore
import pandas as pd
import traceback
import time
from browser_settings import get_driver_settings
from youtube_iframe import change_resolution
import os
import time
import sys
from datetime import datetime

start_time = int(time.time())

def fetch_video_buffer(url, minutes, resolution):

    driver = None
    data = []

    try:
        
        # Initialize driver settings
        driver = get_driver_settings(url)
        iframe = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#player"))
        )
        
        # Switch to the YouTube iframe and play the video
        driver.switch_to.frame(iframe)
        
        print("\n--- DEBUG INSIDE IFRAME ---")

        print("URL:", driver.current_url)

        print("\n[HTML snippet]")
        print(driver.page_source[:2000])

        buttons = driver.find_elements(By.TAG_NAME, "button")
        print(f"\nButtons found: {len(buttons)}")

        for b in buttons:
            print("->", b.get_attribute("aria-label"))

        videos = driver.find_elements(By.TAG_NAME, "video")
        print(f"\nVideos found: {len(videos)}")
        
        
        play_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label*='Play']")
        ))
        
        time.sleep(3)
        play_button.click()
        time.sleep(2)
        
        # Change to the selected resolution
        change_resolution(driver, start_time, resolution)
        
        # Fetch YouTube buffer information
        end_time = time.time() + minutes * 60
        buffer_second = 0
        
        while time.time() < end_time:

            buffer_second += 1    
            # Switch back to the main page
            driver.switch_to.default_content()
            current_time = int(time.time())           
            health_text = driver.find_element(By.ID, "health").text
            resolution_text = driver.find_element(By.ID, "resolution").text
            health = health_text.split(":", 1)[1].strip().replace("s", "")
            resolution = resolution_text.split(":", 1)[1].strip()

            data.append({
                "start_time": start_time,
                "current_time": current_time,
                "health": health,
                "resolution": resolution,
                "buffer_second": buffer_second,
            })
            time.sleep(1)
            
        # Save the data into a DataFrame
        df = pd.DataFrame(data)

        return df

    except Exception as e:
        print(f"[play] Exception: {e}\n{traceback.format_exc()}")
        return None

    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass
            
def save_yt_buffer_results(df, minutes, resolution):

    try:
        if df is None or df.empty:
            print("No data to save.")
            return

        # Create directory if it does not exist
        results_dir = "results"
        os.makedirs(results_dir, exist_ok=True)

        # Create timestamp
        today = datetime.now().strftime("%d_%B_%Y").upper() 

        # Find next available counter
        counter = 1
        while True:
            filename = f"yt_buffer_{minutes}_minutes_{resolution}_resolution_{today}_{counter}.txt"
            
            # also add -> resolution
            filepath = os.path.join(results_dir, filename)

            if not os.path.exists(filepath):
                break
            counter += 1

        # Save DataFrame
        df.to_csv(filepath, sep=";", index=False)
        print(f"Results saved to: {filepath}")

    except Exception as e:
        print(f"Error saving results: {e}")
        
if __name__ == "__main__":

    try:
        if len(sys.argv) < 2:
            print("Usage: python youtube_API_collector.py <ip_address>")
            sys.exit(1)
            
        address = sys.argv[1]
        url = f"http://{address}:8000/"
        resolution = "medium" 
        minutes = 3
        df = fetch_video_buffer(url, minutes ,resolution)
        print(df)
        # Save data in txt format
        save_yt_buffer_results(df,minutes, resolution)

    except Exception as e:
        print(f"Exception outside video playing: {e}")