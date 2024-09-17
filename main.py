import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from fake_useragent import UserAgent
import time
from initial import attempt_login
from products import scrape_product_details, scrape_products
from creators import scrape_creator_details, scrape_creators
from live_streams import scrape_live_stream_details, scrape_live_streams, product_names
from category import scrape_category, scrape_category_details

load_dotenv()

# ua = UserAgent()
# user_agent = ua.random  # Get a random User-Agent

def main():
    service = Service(os.getenv("PATH_TO_CHROMEDRIVER"))
    
    chrome_options = Options()

    # chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_argument("--headless")  # Enable headless mode
    chrome_options.add_argument("--window-size=1920,1080")  # Set a large window size
    chrome_options.add_argument("--start-maximized")  # Maximized in case it's not headless
    chrome_options.add_argument("--mute-audio")  # Mute audio

    # prefs = {
    # "profile.managed_default_content_settings.images": 2  # 2 disables images
    # }
    # chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(service=service, options=chrome_options)

    # stealth(
    # driver,
    # languages=["en-US", "en"],
    # vendor="Google Inc.",
    # platform="Win32",
    # webgl_vendor="Intel Inc.",
    # renderer="Intel Iris OpenGL Engine",
    # fix_hairline=True,
    # )
    
    # driver = webdriver.Chrome(service=service)

    try:
        
        start_time = time.time()

        attempt_login(driver)
        login_time = time.time() - start_time

        # start_time = time.time()

        # scrape_category(driver, 'https://www.kalodata.com/category', "Category.csv")
        # category_time = (time.time() - start_time) / 10

        start_time = time.time()

        scrape_products(driver, 'https://www.kalodata.com/product', "Products.csv")
        products_time = (time.time() - start_time) / 10
        start_time = time.time()

        scrape_live_streams(driver, 'https://www.kalodata.com/livestream', "Live_Streams.csv")  
        live_stream_time = (time.time() - start_time) / 10

        start_time = time.time()

        scrape_creators(driver, 'https://www.kalodata.com/creator', "Creators.csv")
        creator_time = (time.time() - start_time) / 100

    finally:
        driver.quit()

        print(f"Time for login = {login_time} seconds")
        print(f"Avg Time for products = {products_time} seconds")
        # print(f"Time for category = {category_time} seconds")
        print(f"Avg Time for live Streams = {live_stream_time} seconds")
        print(f"Time for creators = {creator_time} seconds")

if __name__ == "__main__":
    main()