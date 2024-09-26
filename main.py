import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
# from selenium_stealth import stealth
from initial import attempt_login
from products import scrape_product_details, scrape_products
from creators import scrape_creator_details, scrape_creators
from live_streams import scrape_live_stream_details, scrape_live_streams, product_names
from category import scrape_category, scrape_category_details

load_dotenv()

def main():
    service = Service(os.getenv("PATH_TO_CHROMEDRIVER"))
    
    chrome_options = Options()

    # chrome_options = Options()
    # chrome_options.binary_location = "/usr/bin/google-chrome"  # Ensure Chrome is installed

    chrome_options.add_argument("--headless")  # Enable headless mode
    chrome_options.add_argument("--window-size=1920,1080")  # Set a large window size
    chrome_options.add_argument("--start-maximized")  # Maximized in case it's not headless
    chrome_options.add_argument("--mute-audio")  # Mute audio


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
        attempt_login(driver)

        # scrape_products(driver, 'https://www.kalodata.com/product', "Products.csv")

        scrape_creators(driver, 'https://www.kalodata.com/creator', "Creators.csv")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()