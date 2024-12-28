from flask import Flask, render_template, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time
import random
import requests
import pymongo
import chromedriver_autoinstaller
from datetime import datetime
import os


print("Starting the flask app...")

app = Flask(__name__)

# MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["trending_db"]
collection = db["trends"]

# ProxyMesh configuration (single proxy with username and password)
PROXY = "http://open.proxymesh.com:31280"
PROXY_USERNAME = "rxtxk_"  # Replace with your ProxyMesh username
PROXY_PASSWORD = "Welcome-123456"  # Replace with your ProxyMesh password

def run_selenium_script():
    # Install the correct version of ChromeDriver based on the installed Chrome version
    chromedriver_autoinstaller.install()

    # Set up Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--disable-gpu')

    # Add your Chrome profile to Selenium
    profile_path = r"C:\Users\ritik\AppData\Local\Google\Chrome\User Data\Default"  # Update with the correct profile path
    options.add_argument(f"user-data-dir={profile_path}")

    # Add the proxy extension to Selenium
    extension_path = r"C:\Users\ritik\OneDrive\Desktop\MyProxyExtension.crx"  # Path to your Chrome extension (.crx or .zip)
    options.add_extension(extension_path)  # Add the extension for proxy handling

    # Specify the path to your ChromeDriver
    chromedriver_path = r"C:\Users\ritik\Downloads\chrome-win64\chrome-win64\chrome.exe"  # Replace with the correct path to your downloaded ChromeDriver

    # Create a Service object with the path to the ChromeDriver
    service = Service(chromedriver_path)

    # Initialize the WebDriver with the Service object
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Log into Twitter
        driver.get("https://twitter.com/login")
        wait = WebDriverWait(driver, 10)

        # Enter username
        username = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='text']"))
        )
        username.send_keys("Your_X_userName")
        username.send_keys(Keys.RETURN)  # Proceed to next field

        # Wait for password field to appear and enter password
        password = wait.until(
            EC.presence_of_element_located((By.NAME, "session[password]"))
        )
        password.send_keys("Your_X_Password")  # Use your actual password
        password.send_keys(Keys.RETURN)

        # Wait for login to complete
        time.sleep(5)

        # Navigate to trending topics section
        driver.get("https://twitter.com/explore/tabs/trending")
        time.sleep(3)

        # Get the top 5 trending topics
        trending_topics = []
        topics = driver.find_elements(By.XPATH, "//div[@aria-label='Trending now']/div/div/div/div/div[2]/div[1]")
        for topic in topics[:5]:  # Grab the first 5 topics
            trending_topics.append(topic.text)

        # Get current IP address (using the proxy)
        ip_address = requests.get('https://api.ipify.org', proxies={"http": PROXY, "https": PROXY}).text

        # Create a unique ID for the record
        unique_id = str(random.randint(100000, 999999))

        # Record data to MongoDB
        record = {
            "unique_id": unique_id,
            "trend1": trending_topics[0] if len(trending_topics) > 0 else None,
            "trend2": trending_topics[1] if len(trending_topics) > 1 else None,
            "trend3": trending_topics[2] if len(trending_topics) > 2 else None,
            "trend4": trending_topics[3] if len(trending_topics) > 3 else None,
            "trend5": trending_topics[4] if len(trending_topics) > 4 else None,
            "dateTime": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "ipAddress": ip_address
        }
        collection.insert_one(record)

        return trending_topics, ip_address, record

    except Exception as e:
        print(f"An error occurred: {e}")
        return [], "Error", {}

    finally:
        driver.quit()  # Close the browser

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-scraper', methods=["GET"])
def run_scraper():
    trending_topics, ip_address, mongo_record = run_selenium_script()
    response_data = {
        "datetime": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "trendingTopics": trending_topics,
        "ip_address": ip_address,
        "mongoRecord": mongo_record
    }
    return jsonify(response_data)

if __name__ == "__main__":
    app.run(debug=True)