import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
# from helpers import attempt_login, scrape_product_details, scrape_creator_details, scrape_live_stream_details, scrape_600_products
from initial import attempt_login
from products import scrape_product_details, scrape_products
from creators import scrape_creator_details, scrape_creators


load_dotenv()

def main():

    service = Service(os.getenv("PATH_TO_CHROMEDRIVER"))
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Enable headless mode
    chrome_options.add_argument("--window-size=1920,1080")  # Set a large window size
    chrome_options.add_argument("--start-maximized")  # Maximized in case it's not headless

    driver = webdriver.Chrome(service=service, options=chrome_options)
    # driver = webdriver.Chrome(service=service)

    try:
        attempt_login(driver)
        
        # # Example usage
        # shop_info = scrape_shop_info(driver, 'https://kalodata.com/shop')
        # save_to_csv(shop_info, 'shops_info.csv')

        # scrape_products_info(driver, 'https://kalodata.com/product', 'products_info.csv')
        
        # scrape_product_details(driver, 'https://www.kalodata.com/product/detail?id=1729527313880355335&language=en-US&currency=USD&region=US&dateRange=%5B%222024-08-20%22%2C%222024-08-26%22%5D&cateValue=%5B%5D', 'Product_Details.csv')

        #scrape_creator_details(driver, 'https://kalodata.com/creator/detail?id=7319965202961728555&language=en-US&currency=USD&region=US&dateRange=%5B%222024-08-12%22%2C%222024-08-18%22%5D&cateValue=%5B%5D', 'Creator_Details.csv')

        #scrape_live_stream_details(driver, 'https://kalodata.com/livestream/detail?id=7404153601582517038&language=en-US&currency=USD&region=US&dateRange=%5B%222024-08-16%22%2C%222024-08-22%22%5D&cateValue=%5B%5D', 'Live_Stream_Details.csv')


        # scrape_all_products(driver, 'https://www.kalodata.com/product', "Data.csv")

        scrape_products(driver, 'https://www.kalodata.com/product', "Products.csv")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()