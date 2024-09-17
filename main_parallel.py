import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
#from selenium_stealth import stealth
#from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor
from initial import attempt_login
from products import scrape_product_details, scrape_products
from creators import scrape_creator_details, scrape_creators
from live_streams import scrape_live_stream_details, scrape_live_streams, product_names
from category import scrape_category
from videos import scrape_video
from shops import scrape_shop

load_dotenv()

def create_driver():
    service = Service(os.getenv("PATH_TO_CHROMEDRIVER"))
    # chromedriver_path = r'C:\Users\arham\Desktop\chromedriver-win64\chromedriver.exe'
    # service = Service(chromedriver_path)
    chrome_options = Options()
    # ua = UserAgent()
    # user_agent = ua.random  # Get a random User-Agent
    # chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_argument("--headless")  # Enable headless mode
    chrome_options.add_argument("--window-size=1920,1080")  # Set a large window size
    chrome_options.add_argument("--start-maximized")  # Maximized in case it's not headless
    chrome_options.add_argument("--mute-audio")  # Mute audio

    driver = webdriver.Chrome(service=service, options=chrome_options)

    # stealth(
    #     driver,
    #     languages=["en-US", "en"],
    #     vendor="Google Inc.",
    #     platform="Win32",
    #     webgl_vendor="Intel Inc.",
    #     renderer="Intel Iris OpenGL Engine",
    #     fix_hairline=True,
    # )
    
    return driver

def scrape_products_task():
    driver = create_driver()
    try:
        attempt_login(driver)  # Attempt login within this task
        scrape_products(driver, 'https://www.kalodata.com/product', "Products.csv")
    finally:
        driver.quit()

def scrape_live_streams_task():
    driver = create_driver()
    try:
        attempt_login(driver)  # Attempt login within this task
        scrape_live_streams(driver, 'https://www.kalodata.com/livestream', "Live_Streams.csv")
    finally:
        driver.quit()

def scrape_creators_task():
    driver = create_driver()
    try:
        attempt_login(driver)  # Attempt login within this task
        scrape_creators(driver, 'https://www.kalodata.com/creator', "Creators.csv")
    finally:
        driver.quit()

# def scrape_shop_task():
#     driver = create_driver()
#     try:
#         attempt_login(driver)  # Attempt login within this task
#         scrape_shop(driver, 'https://kalodata.com/shop', 'Shop.csv')
#     finally:
#         driver.quit()

# def scrape_category_task():
#     driver = create_driver()
#     try:
#         attempt_login(driver)  # Attempt login within this task
#         scrape_category(driver,'https://www.kalodata.com/category','Category.csv')
#     finally:
#         driver.quit()

# def scrape_video_task():
#     driver = create_driver()
#     try:
#         attempt_login(driver)  # Attempt login within this task
#         scrape_video(driver, 'https://www.kalodata.com/video', 'Video.csv')
#     finally:
#         driver.quit()

def main():
    start_time = time.time()
    
    # Use ThreadPoolExecutor to run scraping tasks in parallel
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            # executor.submit(scrape_shop_task),
            # executor.submit(scrape_category_task),
            # executor.submit(scrape_video_task),
            executor.submit(scrape_live_streams_task),
            executor.submit(scrape_products_task),
            executor.submit(scrape_creators_task)
        ]
    
        # Wait for all tasks to complete
        for future in futures:
            future.result()  # This will raise any exceptions that occurred
    
    total_time = time.time() - start_time
    print(f"Total scraping time: {total_time} seconds")

if __name__ == "__main__":
    main()