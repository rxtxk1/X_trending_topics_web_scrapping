# scraper.py

import time
import uuid
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
from config import PROXY_URL, TWITTER_URL, MONGO_URI, DATABASE_NAME, COLLECTION_NAME

def scrape_twitter():
    # Set up proxy and headless options
    chrome_options = Options()
    chrome_options.add_argument(f'--proxy-server={PROXY_URL}')
    chrome_options.add_argument('--headless')  # Run in headless mode
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')

    # Start Selenium WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(TWITTER_URL)

    # Login to Twitter
    time.sleep(5)  # Adjust as needed
    driver.find_element(By.NAME, "text").send_keys("your_twitter_email")
    driver.find_element(By.XPATH, '//span[text()="Next"]').click()
    time.sleep(2)
    driver.find_element(By.NAME, "password").send_keys("your_twitter_password")
    driver.find_element(By.XPATH, '//span[text()="Log in"]').click()
    time.sleep(5)

    # Scrape trending topics
    trends = driver.find_elements(By.XPATH, '//div[@data-testid="trend"]')[:5]
    trend_names = [trend.text for trend in trends]

    # Capture the IP address
    driver.get("https://api.ipify.org/?format=text")
    ip_address = driver.find_element(By.TAG_NAME, "body").text

    # Close the driver
    driver.quit()

    # Save to MongoDB
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    record = {
        "_id": str(uuid.uuid4()),
        "trend1": trend_names[0] if len(trend_names) > 0 else None,
        "trend2": trend_names[1] if len(trend_names) > 1 else None,
        "trend3": trend_names[2] if len(trend_names) > 2 else None,
        "trend4": trend_names[3] if len(trend_names) > 3 else None,
        "trend5": trend_names[4] if len(trend_names) > 4 else None,
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ip_address": ip_address,
    }
    collection.insert_one(record)

    return record
