import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for new content to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def scrape_product_details(driver, output_csv):
    # Wait for the page to load and the table to render
    time.sleep(5)
    
    # # Scroll to the bottom to load all products
    # scroll_to_bottom(driver)

    # time.sleep(2)

    # dropdown_menu = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/ul/li[10]/div')
    # dropdown_menu.click()

    # # Click the option "20 / page" directly using XPath
    # option_20_per_page = driver.find_element(By.XPATH, '//*[@id="rc_select_0_list_1"]/div')
    # option_20_per_page.click()

    # Get the total number of product rows (excluding header row)
    product_rows = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr')
    
    # Skip the first row (header or empty row)
    product_rows = product_rows[1:]

    print(f"Total number of products found (excluding header): {len(product_rows)}")

    # Open a CSV file for writing
    with open(output_csv, mode='w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        # Write the header row
        csv_writer.writerow(['Product Name', 'Price', 'Revenue', 'Items Sold', 'Avg Unit Price', 'Number of Creators', 'Launch Date', 'Conversion Ratio'])
        
        # Iterate over each row and extract product details
        for index, row in enumerate(product_rows, start=2):  # Start from 2 as we skipped the first row
            try:
                # XPaths to get the product details
                product_name_xpath = f'//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr[{index}]/td[2]/div/div[2]/div[1]/div[1]/div'
                product_price_xpath = f'//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr[{index}]/td[2]/div/div[2]/div[2]'
                revenue_xpath = f'//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr[{index}]/td[3]'
                items_sold_xpath = f'//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr[{index}]/td[5]'
                avg_unit_price_xpath = f'//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr[{index}]/td[6]'
                number_of_creators_xpath = f'//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr[{index}]/td[8]'
                launch_date_xpath = f'//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr[{index}]/td[9]'
                conversion_ratio_xpath = f'//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr[{index}]/td[10]/div'
                
                # Extract the text for each detail
                product_name = driver.find_element(By.XPATH, product_name_xpath).text
                product_price = driver.find_element(By.XPATH, product_price_xpath).text
                revenue = driver.find_element(By.XPATH, revenue_xpath).text
                items_sold = driver.find_element(By.XPATH, items_sold_xpath).text
                avg_unit_price = driver.find_element(By.XPATH, avg_unit_price_xpath).text
                number_of_creators = driver.find_element(By.XPATH, number_of_creators_xpath).text
                launch_date = driver.find_element(By.XPATH, launch_date_xpath).text
                conversion_ratio = driver.find_element(By.XPATH, conversion_ratio_xpath).text
                
                # Write the details to the CSV file
                csv_writer.writerow([product_name, product_price, revenue, items_sold, avg_unit_price, number_of_creators, launch_date, conversion_ratio])
                
            except Exception as e:
                print(f"Error occurred for row {index}: {e}")

# Path to your chromedriver executable
chromedriver_path = r'C:\Users\momin\Desktop\chromedriver-win64\chromedriver.exe'

# Set up the service and options for Chrome
service = Service(chromedriver_path)
options = Options()
options.add_argument("--start-maximized")

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=options)

try:
    # Open the URL
    driver.get('https://kalodata.com/login')

    # Allow the page to load completely
    time.sleep(2)

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

    # Open the product page and scrape data
    url = 'https://kalodata.com/product'
    driver.get(url)
    scrape_product_details(driver, 'products.csv')    

    time.sleep(100)

finally:
    # Close the driver
    driver.quit()