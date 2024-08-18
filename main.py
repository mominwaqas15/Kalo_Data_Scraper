import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from helpers import attempt_login, save_to_csv, scrape_shop_info, scrape_products_info, scrape_product_details

load_dotenv()

def main():
    service = Service(os.getenv("PATH_TO_CHROMEDRIVER"))
    driver = webdriver.Chrome(service=service)

    try:
        attempt_login(driver)
        
        # # Example usage
        # shop_info = scrape_shop_info(driver, 'https://kalodata.com/shop')
        # save_to_csv(shop_info, 'shops_info.csv')

        # scrape_products_info(driver, 'https://kalodata.com/product', 'products_info.csv')
        
        scrape_product_details(driver, 'https://kalodata.com/product/detail?id=1729418496836080191&language=en-US&currency=USD&region=US&dateRange=%5B%222024-08-11%22%2C%222024-08-17%22%5D&cateValue=%5B%5D', 'Product_Details.csv')

    finally:
        driver.quit()

if __name__ == "__main__":
    main()