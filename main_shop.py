import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from arham.helpers_shop import attempt_login,scrape_shop_details

load_dotenv()

def main():
    chromedriver_path = r'C:\Users\arham\Desktop\chromedriver-win32\chromedriver-win32\chromedriver.exe'
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
        
        scrape_shop_details(driver, 'https://www.kalodata.com/shop/detail?id=7494949083499694765&language=en-US&currency=USD&region=US&dateRange=%5B%222024-08-12%22%2C%222024-08-18%22%5D&cateValue=%5B%5D', 'Shop_Details.csv')

    finally:
        driver.quit()

if __name__ == "__main__":
    main()