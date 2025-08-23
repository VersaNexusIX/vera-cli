import os
import time
import base64
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

def handle(args):
    """
    WhatsApp Profile Downloader
    Usage: wa <number>
    Example: wa 6281234567890
    """

    if not args:
        return "⚠️ Usage: wa <number>"

    number = args[0]
    file_path = f"/sdcard/Download/{number}.jpg"
    status = "ɢᴀɢᴀʟ"
    name = "Unknown"

    try:
        # Jalankan Selenium (Chrome/Chromium harus tersedia)
        options = webdriver.ChromeOptions()
        options.add_argument("--user-data-dir=/sdcard/Download/chrome_whatsapp")
        options.add_argument("--profile-directory=Default")
        driver = webdriver.Chrome(options=options)

        driver.get("https://web.whatsapp.com")
        print("👉 Scan QR Code WhatsApp di browser...")

        # Tunggu login WA Web
        time.sleep(15)

        # Cari nomor
        search_box = driver.find_element(By.XPATH, '//div[@title="Search input textbox"]')
        search_box.click()
        time.sleep(1)
        search_box.send_keys(number)
        time.sleep(3)

        # Klik hasil chat
        driver.find_element(By.XPATH, f'//span[@title="{number}"]').click()
        time.sleep(3)

        # Klik header untuk buka profil
        driver.find_element(By.XPATH, '//header').click()
        time.sleep(3)

        # Ambil username (nama profil WA)
        try:
            name_el = driver.find_element(By.XPATH, '//span[@dir="auto" and @title]')
            name = name_el.get_attribute("title")
        except:
            name = "Unknown"

        # Ambil foto profil
        img = driver.find_element(By.XPATH, '//img[contains(@src,"https://pps.whatsapp.net")]')
        src = img.get_attribute("src")

        if src.startswith("data:image"):
            data = src.split(",")[1]
            img_data = base64.b64decode(data)
        else:
            img_data = requests.get(src).content

        with open(file_path, "wb") as f:
            f.write(img_data)

        status = "ʙᴇʀʜᴀsɪʟ"

    except Exception as e:
        return f"❌ Error WA handler: {e}"
    finally:
        try:
            driver.quit()
        except:
            pass

    return f"""
╭────────────────
│ ɴᴀᴍᴇ   : {name}
│ ɴᴜᴍʙᴇʀ : {number}
│ sᴛᴀᴛᴜs : {status}
╰────────────────
"""