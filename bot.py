from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import winsound
import time
import os
import sys

def run_bot(location_config, preferences, stop_flag=None, status_callback=None):
    driver = None
    try:
        # Determine the base path for assets
        if getattr(sys, 'frozen', False):
            # Running as a PyInstaller bundle
            base_path = sys._MEIPASS
            success_sound_path = os.path.join(base_path, "gui", "assets", "success.wav")
            error_sound_path = os.path.join(base_path, "gui", "assets", "error.wav")
        else:
            # Running from source
            current_script_dir = os.path.dirname(os.path.abspath(__file__))
            success_sound_path = os.path.join(current_script_dir, "gui", "assets", "success.wav")
            error_sound_path = os.path.join(current_script_dir, "gui", "assets", "error.wav")

        chrome_options = Options()
        chrome_options.add_argument("--headless=new") # For silent operation
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

        driver = webdriver.Chrome(options=chrome_options)

        wait = WebDriverWait(driver, 10)

        driver.get(location_config["job_url"])
        time.sleep(5)

        if stop_flag and stop_flag.is_set(): return False

        # STEP 1: Enter location
        if status_callback: status_callback(f"Checking {location_config['city']}: Filling location filters...")
        wait.until(EC.presence_of_element_located((By.NAME, "postalCode"))).send_keys(location_config["postal_code"])
        wait.until(EC.presence_of_element_located((By.NAME, "city"))).send_keys(location_config["city"])
        time.sleep(1)

        if stop_flag and stop_flag.is_set(): return False

        # STEP 2: Work hours
        if status_callback: status_callback(f"Checking {location_config['city']}: Selecting hours...")
        work_hours = preferences.get("weekly_hours", "Full-time (30+ hours)")
        dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//select")))
        dropdown.click()
        time.sleep(1)
        try:
            driver.find_element(By.XPATH, f"//option[contains(text(), '{work_hours}')]").click()
        except:
            pass
        time.sleep(1)

        if stop_flag and stop_flag.is_set(): return False

        # STEP 3: Time preferences
        if status_callback: status_callback(f"Checking {location_config['city']}: Selecting time preferences...")
        time_options = preferences.get("time_preferences", [])
        for option in time_options:
            try:
                driver.find_element(By.XPATH, f"//button[contains(text(), '{option}')]").click()
                time.sleep(0.5)
            except:
                pass

        # STEP 4: Duration
        if status_callback: status_callback(f"Checking {location_config['city']}: Selecting duration...")
        try:
            driver.find_element(By.XPATH, f"//label[contains(text(), '{preferences['duration']}')]").click()
        except:
            pass
        time.sleep(1)

        if stop_flag and stop_flag.is_set(): return False

        # STEP 5: Start time
        if status_callback: status_callback(f"Checking {location_config['city']}: Selecting start time...")
        try:
            dropdowns = driver.find_elements(By.TAG_NAME, "select")
            for dropdown in dropdowns:
                dropdown.click()
                time.sleep(0.5)
                option = dropdown.find_element(By.XPATH, f".//option[contains(text(), '{preferences['start_time']}')]").click()
                break
        except:
            pass
        time.sleep(1)

        if stop_flag and stop_flag.is_set(): return False

        # Final step: Click apply/book
        if status_callback: status_callback(f"Checking {location_config['city']}: Submitting your shift booking...")
        apply_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Apply') or contains(text(),'Book')]")))
        apply_button.click()

        time.sleep(3)

        if status_callback:
            status_callback(f"Shift booked successfully in {location_config['city']}! ✅")
            try:
                winsound.PlaySound(success_sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
            except Exception as e:
                status_callback(f"Error playing sound: {e}")
        return True

    except Exception as e:
        if status_callback:
            status_callback(f"Error checking {location_config['city']}: {str(e)}")
            # winsound.PlaySound(error_sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC) # This line is commented out
        return False

    finally:
        try:
            if driver:
                driver.quit()
        except:
            pass
        # The sleep logic moved to main_gui.py to control overall retry for all locations
        # if stop_flag and not stop_flag.is_set():
        #     time.sleep(5)