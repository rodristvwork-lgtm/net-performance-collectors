from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import traceback
import time
import os
from utils import change_resolution , click_skip_adds
from browser import get_driver_settings

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
        
        ## BLOCK 2 - BIG SUB TRY EXECEPT - 1
        try:
            consent_overlay = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, 'dialog'))
            )
            time.sleep(2)

            consent_buttons = consent_overlay.find_elements(By.CSS_SELECTOR, '.eom-buttons button.yt-spec-button-shape-next')
            if len(consent_buttons) > 1:
                accept_all_button = consent_buttons[1]
                accept_all_button.click()
                print(f'RUN: {start_time} | Accepted cookes')
        except Exception:
            print(f'RUN: {start_time} | Cookie modal missing')
        
        
        ## CONNECTORS BEFORE CONTINUE FLOW

        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'h1.ytd-watch-metadata'))
            )
        time.sleep(1)
            
        print(f"RUN: {start_time} | ts {int(time.time())} Video should start shortly")
     
        ## BLOCK 3 - BIG SUB TRY EXECEPT - 2

        try:
            movie_player = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "movie_player"))
        )   
            print(f" run {start_time}-> YouTube player loaded")
        except Exception:
            print(f" run  {start_time}-> YouTube player not found after waiting")
            driver.save_screenshot("debug_no_movie_player.png")
            raise
        
        ## connectors before launch
        
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
            '15': "Mystery Text",


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
        
        ## IF STATEMENT of BIG TRY CATCH

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
            
            while j < 10000:
                try:
                    hover.perform()
                    stat_dict = {}
                    not_found_div_id = []

                    try:
                        elements = driver.find_element(by=By.CSS_SELECTOR, value=f".html5-video-info-panel-content").text
                        elements = elements.split("\n")
                        cnt = 0
                        for elem in elements:
                            for key in keys[cnt:]:
                                if elem.startswith(key):
                                    res = elem.split(key)[-1].strip()
                                    break
                            else:
                                continue

                            res = elem.split(key)[-1].strip()
                            if ' / ' in res:
                                res = res.split(' / ')

                            if 'Video ID' in key:
                                stat_dict['Video ID'] = res[0]
                            elif 'Viewport' in key:
                                stat_dict['Viewport'] = res[0]
                                stat_dict['Frames'] = res[1]
                            elif 'Optimal Res' in key:
                                stat_dict['Current Res'] = res[0]
                                stat_dict['Optimal Res'] = res[1]
                            elif 'Buffer Health' in key:
                                stat_dict['Buffer Health'] = res.rstrip(' s')
                            else:
                                stat_dict[key] = res
    
                            cnt += 1
                    except NoSuchElementException: pass
                    except Exception:
                        print(traceback.format_exc())

                    if len(keys) - len(stat_dict) > 0:
                        not_found_div_id = set(keys)-set(stat_dict)

                    if ','.join(list(not_found_div_id)) != last_not_found_div_id:
                        last_not_found_div_id = ','.join(list(not_found_div_id)) 

                    if "Video ID" in not_found_div_id or len(stat_dict) == 0:
                        print('Video ID not found')

                        try:
                            options = driver.find_elements(by=By.CLASS_NAME, value='ytp-menuitem')
                            for option in options:
                                option_child = option.find_element(by=By.CLASS_NAME, value='ytp-menuitem-label')
                                if ' nerd' in option_child.text:
                                    option_child.click()
                                    print(f"RUN: {start_time} | Enabled stats collection.")
                                    break

                            time.sleep(2)
                        except:
                            pass

                        continue

                    stat_dict['Network Activity'] = stat_dict['Network Activity'].rstrip(' KB')
                    stat_dict['start_time'] = str(start_time)
                    stat_dict['script_time'] = str(int(time.time()))

                    ts = 0.0
                    try:
                        ts = float(stat_dict["Mystery Text"].split(' b:')[0].split(' t:')[-1])
                    except Exception as e:
                        print(stat_dict["Mystery Text"], e)
                        print(f"RUN: {start_time} | {stat_dict['Video ID']} Could not recover time from Mystery Text")
                        ts = last_ts + 0.5  # try sth

                    if video_id not in stat_dict['Video ID']:                      
                        if not enable_skipping:
                            print(f"RUN: {start_time} | {stat_dict['Video ID']} | ts {int(time.time())} | vid time: {ts} (last: {last_ts}) Video ID Changed, Ending.")
                            f.flush()
                            break
                        click_skip_adds(driver)

                    if stat_dict['Video ID'] != last_video_id:
                        last_video_id = stat_dict['Video ID']
                        last_ad_ts = 0.0

                    if video_id not in stat_dict['Video ID'] and ts < last_ts:
                        ts = last_ts + ts  
                    if '@' not in stat_dict['Current Res'] or '0x0@' in stat_dict['Current Res']:
                        stat_dict['Current Res'] = last_res  
                    if video_id in stat_dict['Video ID']:
                        last_res = stat_dict['Current Res']

                        try:
                            cur_buffer = float(stat_dict['Buffer Health'])
                            if cur_buffer < last_buffer-10.0 and last_buffer > 10.0 and ts - last_ts < 5.0:
                                stat_dict['Buffer Health'] = str(last_buffer)
                            last_buffer = cur_buffer
                        except Exception:
                            print(f"RUN: {start_time} | {stat_dict['Video ID']} | ts {stat_dict['script_time']} | Vid time: {ts} | Buffer invalid: {stat_dict['Buffer Health']} | cur res: {stat_dict['Current Res']}")
                            continue

                        if ts < last_ts and last_ts > 0.0:
                            print(f"RUN: {start_time} | {stat_dict['Video ID']} | ts {stat_dict['script_time']} | Vid time invalid: {ts} (last: {last_ts}) | cur res: {stat_dict['Current Res']}")
                            continue

                        if ts > 1960:
                            enable_skipping = False

                        if ts - last_ts > 1.2 and factor < 0.9:
                            factor = factor+0.1
                        elif ts - last_ts < 0.8 and factor > 0.3:
                            factor = factor-0.1

                        last_ts = ts
                    else:
                        if ts < last_ad_ts and last_ad_ts > 0.0:
                            print(f"RUN: {start_time} | {stat_dict['Video ID']} | ts {stat_dict['script_time']} | Vid time invalid: {ts} (last: {last_ad_ts}) | cur res: {stat_dict['Current Res']}")
                            continue
                        last_ad_ts = ts

                    stat_dict['time'] = str(ts).replace('.', ',')
                    stat_dict['Buffer Health'] = stat_dict['Buffer Health'].replace('.', ',')

                    s = [stat_dict[s] for s in headers[:-1]]
                    f.write(f"{';'.join(s)};{i}\n")

                    if video_id in stat_dict['Video ID']:
                        if i % 10 == 0:
                            f.flush()
                            try:
                                res = stat_dict['Current Res']
                                if '1920x' not in res:
                                    change_resolution(driver)
                            except Exception as e:
                                print(f"RUN: {start_time} | Exception while trying to change resolution {e}")

                        if i < 10 or i % 30 == 0:
                            print(f"RUN: {start_time} | {stat_dict['Video ID']} | ts {int(time.time())} | vid time: {ts} | cur res: {stat_dict['Current Res']}")

                        i = i+1
                    else:
                        print(f"RUN: {start_time} | {stat_dict['Video ID']} | ts {int(time.time())} | vid time: {ts} | cur res: {stat_dict['Current Res']}")

                    sleep_time = 1.0
                    if 1 - factor > 0.3:
                        sleep_time = sleep_time-factor

                    time.sleep(sleep_time)
                except Exception as e:
                    print(f"RUN: {start_time} | ts {int(time.time())} Error {traceback.format_exc()}")

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