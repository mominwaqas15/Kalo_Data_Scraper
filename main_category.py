import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from helpers_shop import attempt_login
from helpers_category import scrape_category_details,get_category_links,scrape_500_category

load_dotenv()

def main():
    chromedriver_path = r'C:\Users\arham\Desktop\chromedriver-win64\chromedriver.exe'
    service = Service(chromedriver_path)
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        attempt_login(driver)
        
        # # Example usage
        # shop_info = scrape_shop_info(driver, 'https://kalodata.com/shop')
        # save_to_csv(shop_info, 'shops_info.csv')

        # scrape_products_info(driver, 'https://kalodata.com/product', 'products_info.csv')
        scrape_500_category(driver,'https://www.kalodata.com/category','Category.csv')
        #scrape_category_details(driver, 'https://www.kalodata.com/category/detail?id=601450&language=en-US&currency=USD&region=US&dateRange=%5B%222024-08-12%22%2C%222024-08-18%22%5D&cateValue=%5B%22601450%22%5D', 'Cateory_Details.csv')

    finally:
        driver.quit()

if __name__ == "__main__":
    main()