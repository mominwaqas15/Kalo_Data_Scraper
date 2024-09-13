import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from initial import attempt_login
import time
from products import scrape_product_details, scrape_products
from creators import scrape_creator_details, scrape_creators
from live_streams import scrape_live_stream_details, scrape_live_streams, product_names


load_dotenv()

def main():

    service = Service(os.getenv("PATH_TO_CHROMEDRIVER"))
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Enable headless mode
    chrome_options.add_argument("--window-size=1920,1080")  # Set a large window size
    chrome_options.add_argument("--start-maximized")  # Maximized in case it's not headless

    prefs = {
    "profile.managed_default_content_settings.images": 2  # 2 disables images
    }
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(service=service, options=chrome_options)
    # driver = webdriver.Chrome(service=service)

    try:
        
        start_time = time.time()

        attempt_login(driver)
        login_time = time.time() - start_time

        start_time = time.time()

        scrape_products(driver, 'https://www.kalodata.com/product', "Products.csv")
        products_time = (time.time() - start_time) / 1000

        start_time = time.time()

        scrape_live_streams(driver, 'https://www.kalodata.com/livestream', "Live_Streams.csv")  
        live_stream_time = (time.time() - start_time) / 1000

        start_time = time.time()

        scrape_creators(driver, 'https://www.kalodata.com/creator', "Creators.csv")
        creator_time = (time.time() - start_time) / 1000

    finally:
        driver.quit()

        print(f"Time for login = {login_time} seconds")
        print(f"Avg Time for Products = {products_time} seconds")
        print(f"Avg Time for live Streams = {live_stream_time} seconds")
        print(f"Time for login = {creator_time} seconds")

if __name__ == "__main__":
    main()