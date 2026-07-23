import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

APP_URL = "https://medpulse-app.streamlit.app/"

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

try:
    print(f"Visiting {APP_URL}...")
    driver.get(APP_URL)
    time.sleep(5)

    # Look for the Streamlit wake-up button
    wake_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Yes, get this app back up!')]")
    
    if wake_buttons:
        print("App is sleeping! Clicking the wake-up button...")
        wake_buttons[0].click()
        time.sleep(10)
        print("Successfully sent wake-up signal! ✅")
    else:
        print("App is already awake! ✅")

except Exception as e:
    print(f"Error checking app state: {e}")
finally:
    driver.quit()
