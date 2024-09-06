import os
from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from helpers_shop import attempt_login
from helpers_video import scrape_video_details,scrape_500_video

load_dotenv()

def main():
    # chromedriver_path = r'C:\Users\arham\Desktop\chromedriver-win64\chromedriver.exe'

    service = Service(os.getenv("PATH_TO_CHROMEDRIVER"))

    # service = Service(chromedriver_path)

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Enable headless mode
    chrome_options.add_argument("--window-size=1920,1080")  # Set a large window size
    chrome_options.add_argument("--start-maximized")  # Maximized in case it's not headless

    # options = webdriver.ChromeOptions()
    # options.add_argument("--start-maximized")
    # driver = webdriver.Chrome(service=service, options=options)

    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        attempt_login(driver)
        
        # # Example usage
        # shop_info = scrape_shop_info(driver, 'https://kalodata.com/shop')
        # save_to_csv(shop_info, 'shops_info.csv')

        # scrape_products_info(driver, 'https://kalodata.com/product', 'products_info.csv')
        
        scrape_500_video(driver, 'https://www.kalodata.com/video', 'Video.csv')

    finally:
        driver.quit()

if __name__ == "__main__":
    main()