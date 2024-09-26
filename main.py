import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from initial import attempt_login
from products import scrape_product_details, scrape_products
from creators import scrape_creator_details, scrape_creators
from live_streams import scrape_live_stream_details, scrape_live_streams, product_names
from category import scrape_category, scrape_category_details

load_dotenv()

def main():
    print("started scraping")
    # service = Service(os.getenv("PATH_TO_CHROMEDRIVER"))
    # service = Service("/home/ubuntu/chromedriver-linux64/chromedriver")
    service = Service(ChromeDriverManager().install())

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

        # scrape_products(driver, 'https://www.kalodata.com/product', "Products.csv")

        # print("started scraping creators")
        # scrape_creators(driver, 'https://www.kalodata.com/creator', "Creators.csv")

    finally:
        driver.quit()
        print("closed")

if __name__ == "__main__":
    main()