import os
import time
import base64
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
def handle(args):
    if not args:
        return "⚠️ Usage: wa <number>"
    number = args[0]
    file_path = f"/sdcard/Download/{number}.jpg"
    status = "FAILED"
    name = "Unknown"
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--user-data-dir=/sdcard/Download/chrome_whatsapp")
        options.add_argument("--profile-directory=Default")
        driver = webdriver.Chrome(options=options)
        driver.get("https://web.whatsapp.com")
        print("👉 Scan the WhatsApp QR Code in the browser...")
        time.sleep(15)
        search_box = driver.find_element(By.XPATH, '//div[@title="Search input textbox"]')
        search_box.click()
        time.sleep(1)
        search_box.send_keys(number)
        time.sleep(3)
        driver.find_element(By.XPATH, f'//span[@title="{number}"]').click()
        time.sleep(3)
        driver.find_element(By.XPATH, '//header').click()
        time.sleep(3)
        try:
            name_el = driver.find_element(By.XPATH, '//span[@dir="auto" and @title]')
            name = name_el.get_attribute("title")
        except:
            name = "Unknown"
        img = driver.find_element(By.XPATH, '//img[contains(@src,"https://pps.whatsapp.net")]')
        src = img.get_attribute("src")
        if src.startswith("data:image"):
            data = src.split(",")[1]
            img_data = base64.b64decode(data)
        else:
            img_data = requests.get(src).content
        with open(file_path, "wb") as f:
            f.write(img_data)
        status = "SUCCESS"
    except Exception as e:
        return f"❌ Error WA handler: {e}"
    finally:
        try:
            driver.quit()
        except:
            pass
    return f"""
╭────────────────
│ NAME   : {name}
│ NUMBER : {number}
│ STATUS : {status}
╰────────────────
"""
