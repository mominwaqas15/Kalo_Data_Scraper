from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time
import logging
import csv

def scroll_to_bottom(driver):
    # Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Wait for new content to load

def scrape_shop_info(driver):
    shops_info = []

    # Locate all the rows in the table
    rows = driver.find_elements(By.CSS_SELECTOR, 'tr.ant-table-row')

    for row in rows:
        shop_info = {}

        # Extract shop rank
        shop_rank = row.find_element(By.CSS_SELECTOR, 'td.ant-table-cell.ant-table-cell-fix-left').text.strip()
        shop_info['rank'] = shop_rank

        # Extract shop name
        shop_name = row.find_element(By.CSS_SELECTOR, 'div.line-clamp-1').text.strip()
        shop_info['name'] = shop_name

        # Extract shop type
        shop_type = row.find_element(By.CSS_SELECTOR, 'div.text-base-999.line-clamp-1').text.strip()
        shop_info['type'] = shop_type

        # Extract best selling products
        best_selling_products = row.find_elements(By.CSS_SELECTOR, 'div.PageProduct-BestSaleProducts div.Component-Image.cover')
        products = [product.get_attribute('style').split('url("')[1].split('")')[0] for product in best_selling_products]
        shop_info['best_selling_products'] = products

        # Extract revenue
        revenue = row.find_element(By.XPATH, './td[4]').text.strip()
        shop_info['revenue'] = revenue

        # Extract average unit price
        avg_unit_price = row.find_element(By.XPATH, './td[6]').text.strip()
        shop_info['avg_unit_price'] = avg_unit_price

        shops_info.append(shop_info)

    return shops_info

def save_product_data_to_csv(data, filename):
    # Define the headers based on the product data fields
    headers = ['name', 'price', 'revenue', 'items_sold', 'avg_price', 'num_creators', 'launch_date', 'conversion_rate']

    # Write data to CSV file
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def save_to_csv(data, filename):
    # Define the headers
    headers = ['rank', 'name', 'type', 'best_selling_products', 'revenue', 'avg_unit_price']

    # Write data to CSV file
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def scrape_product_info(driver):
    products_info = []
    wait = WebDriverWait(driver, 10)
    scroll_to_bottom(driver)

    while True:
        # Locate all product containers
        product_containers = driver.find_elements(By.CSS_SELECTOR, 'tr.ant-table-row.ant-table-row-level-0')
        logging.info(f'Found {len(product_containers)} product containers')

        if not product_containers:
            logging.info('No more product containers found, stopping the scrape.')
            break

        for container in product_containers:
            product_info = {}

            try:
                # Extract product name
                product_name = container.find_element(By.CSS_SELECTOR, 'div.max-w-full.font-medium > div.line-clamp-2').text.strip()
                product_info['name'] = product_name
            except Exception as e:
                logging.error(f'Error extracting product name: {e}')
                product_info['name'] = 'N/A'

            try:
                # Extract product price
                product_price = container.find_element(By.CSS_SELECTOR, 'div.text-[13px].font-medium.line-clamp-2').text.strip()
                product_info['price'] = product_price
            except Exception as e:
                logging.error(f'Error extracting product price: {e}')
                product_info['price'] = 'N/A'

            try:
                # Extract revenue
                revenue = container.find_element(By.XPATH, './/td[contains(@class, "ant-table-column-sort") and contains(text(), "$")]').text.strip()
                product_info['revenue'] = revenue
            except Exception as e:
                logging.error(f'Error extracting revenue: {e}')
                product_info['revenue'] = 'N/A'

            try:
                # Extract items sold
                items_sold = container.find_element(By.XPATH, './/td[contains(@class, "ant-table-cell") and contains(text(), "k")]').text.strip()
                product_info['items_sold'] = items_sold
            except Exception as e:
                logging.error(f'Error extracting items sold: {e}')
                product_info['items_sold'] = 'N/A'

            try:
                # Extract average price
                avg_price = container.find_element(By.XPATH, './/td[contains(@class, "ant-table-cell") and contains(text(), "$")][2]').text.strip()
                product_info['avg_price'] = avg_price
            except Exception as e:
                logging.error(f'Error extracting average price: {e}')
                product_info['avg_price'] = 'N/A'

            try:
                # Extract number of creators promoting the product
                num_creators = container.find_element(By.XPATH, './/td[contains(@class, "ant-table-cell")][last()-2]').text.strip()
                product_info['num_creators'] = num_creators
            except Exception as e:
                logging.error(f'Error extracting number of creators: {e}')
                product_info['num_creators'] = 'N/A'

            try:
                # Extract launch date
                launch_date = container.find_element(By.XPATH, './/td[contains(@class, "ant-table-cell")][last()-1]').text.strip()
                product_info['launch_date'] = launch_date
            except Exception as e:
                logging.error(f'Error extracting launch date: {e}')
                product_info['launch_date'] = 'N/A'

            try:
                # Extract conversion rate of creators
                conversion_rate = container.find_element(By.CSS_SELECTOR, 'div.PageProduct-MostViewVideos').text.strip()
                product_info['conversion_rate'] = conversion_rate
            except Exception as e:
                logging.error(f'Error extracting conversion rate: {e}')
                product_info['conversion_rate'] = 'N/A'

            products_info.append(product_info)

        # Scroll down to load more products
        scroll_to_bottom(driver)

    return products_info    

# Path to your chromedriver executable
chromedriver_path = r'C:\Users\momin\Desktop\chromedriver-win64\chromedriver.exe'

# Set up the service and options for Chrome
service = Service(chromedriver_path)
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=options)
driver.set_window_size(1920, 1080)

# Open the URL
driver.get('https://kalodata.com/login')

# Allow the page to load completely
time.sleep(3)

# Find the email input element and enter the email
email_input = driver.find_element(By.ID, 'register_email')
email_input.send_keys('info@ejex.co.uk')

# Find the password input element and enter the password
password_input = driver.find_element(By.ID, 'register_password')
password_input.send_keys('111222333Pp!@#')

# Allow some time for inputs to be registered
time.sleep(1)

# Find the login button and click it
login_button = driver.find_element(By.XPATH, '//button[@type="submit" and contains(@class, "login_submit-btn")]')
login_button.click()

# Allow some time for the login process
#time.sleep(60)

url = 'https://kalodata.com/shop?cateValue=%7B%22601450%22%3A%5B%5B%22601450%22%5D%5D%7D&dateRange=%5B%222024-07-30%22%2C%222024-08-05%22%5D'

driver.get(url)

shop_data = scrape_shop_info(driver)
save_to_csv(shop_data, 'shop_data.csv')

url = 'https://kalodata.com/product'
driver.get(url)

product_data = scrape_product_info(driver)
save_product_data_to_csv(product_data, 'product_data.csv')

time.sleep(60)    

# Close the driver
driver.quit()