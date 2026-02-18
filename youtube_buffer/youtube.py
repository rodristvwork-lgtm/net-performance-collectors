from selenium.webdriver.common.by import By                         # type: ignore
from selenium.webdriver.support.ui import WebDriverWait             # type: ignore
from selenium.webdriver.support import expected_conditions as EC    # type: ignore
import time

# Accept cookies statements:
def accept_cookies(driver ,start_time):
    
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