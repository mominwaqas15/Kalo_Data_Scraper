import os
from dotenv import load_dotenv
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
#from webdriver_manager.chrome import ChromeDriverManager
from initial import attempt_login
from products import scrape_product_details, scrape_products
from creators import scrape_creator_details, scrape_creators
from live_streams import scrape_live_stream_details, scrape_live_streams, product_names
from category import scrape_category, scrape_category_details
from videos import scrape_video, scrape_video_details
from shops import scrape_shop_details, scrape_shop

load_dotenv()

def log_time(func_name, start_time):
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"{func_name} took {elapsed_time:.2f} seconds.")

def main():
    service = Service(os.getenv("PATH_TO_CHROMEDRIVER"))
    # service = Service("/home/ubuntu/chromedriver-linux64/chromedriver")
    # service = Service(ChromeDriverManager().install())

    # service = Service(ChromeDriverManager().install())
    # driver = webdriver.Chrome(service=service, options=chrome_options)
    
    chrome_options = Options()

    chrome_options.add_argument("--headless")  # Enable headless mode
    chrome_options.add_argument("--window-size=1920,1080")  # Set a large window size
    chrome_options.add_argument("--start-maximized")  # Maximized in case it's not headless
    chrome_options.add_argument("--mute-audio")  # Mute audio
    chrome_options.add_argument('--no-sandbox')  # Bypass OS security model
    chrome_options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
    chrome_options.add_argument('--disable-gpu')  # Applicable for non-GPU instances

    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        print("attempted login")
        attempt_login(driver)

        # Start timing each scrape function
        # print("started scraping live streams")
        # start_time = time.time()  # Start timing
        # scrape_live_streams(driver, 'https://www.kalodata.com/livestream', "Live_Streams.csv")
        # log_time("scrape_live_streams", start_time)

        print("started scraping videos")
        start_time = time.time()  # Start timing
        scrape_video(driver, 'https://www.kalodata.com/video', "Videos.csv")
        log_time("scrape_video", start_time)

        # print("started scraping creators")
        # start_time = time.time()  # Start timing
        # scrape_creators(driver, 'https://www.kalodata.com/creator', "Creators.csv")
        # log_time("scrape_creators", start_time)

        # print("started scraping products")
        # start_time = time.time()  # Start timing
        # scrape_products(driver, 'https://www.kalodata.com/product', "Products.csv")
        # log_time("scrape_products", start_time)

        # print("started scraping shops")
        # start_time = time.time()  # Start timing
        # scrape_shop(driver, 'https://www.kalodata.com/shop', "Shops.csv")
        # log_time("scrape_shop", start_time)

        # print("started scraping categories")
        # start_time = time.time()  # Start timing
        # scrape_category(driver, 'https://www.kalodata.com/category', "Categories.csv")
        # log_time("scrape_category", start_time)
    finally:
        driver.quit()
        print("closed")

if __name__ == "__main__":
    main()