# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "004CEE27A938DFE88FE2F7EFA5D2921A96397A2749B4C74E477FDD8EC05CF1F3CFF7246DD64E61720D1B15A4A54521B07913161E5FE012AA2E37AA8F506DC6E1A5CB064C637CE2DAE4CA39FD246FD5F01323B2644E13EA07055CDA871CACC51864BE60367F372740C4CEF015A800FE106BE749B6711AAE7E25A5BD29CFA6AD9CAFA617289D0FC71AF47C37C4F2C9672C35040F248FC7F3B46E1FBB89304ECA68CE832365929DF9434F8019D86C3D3BC9152971FB743BB3F209774979136FB0345BB3DCB81F056E972C876FA6B1E12B32CC924DBC92A1BE3CDDD7970BDE1C2F1853CBBF117A192A06F22EB523ED8105B741CC00710CBFA473E9369D50B7640A23ED7E1E28E8C166F8D4A5B12E85B0743EB70EA4F632F103D8C58FE4BE5054FE5498D734532CC0DCC28C024E495D36090F45965343757E7C34BD14AAB5DA3DBBE44AB1F6A8922035882B6FC1BF70F37BACFD"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
