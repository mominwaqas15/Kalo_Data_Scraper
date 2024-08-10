import csv
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

def attempt_login(driver):
    driver.get('https://kalodata.com/login')

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'register_email')))
    
    email_input = driver.find_element(By.ID, 'register_email')
    email_input.send_keys('info@ejex.co.uk')

    password_input = driver.find_element(By.ID, 'register_password')
    password_input.send_keys('111222333Pp!@#')

    login_button = driver.find_element(By.XPATH, '//button[@type="submit" and contains(@class, "login_submit-btn")]')
    login_button.click()

    # # Wait for login to complete by checking the presence of some element on the landing page after login
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'some_element_on_homepage_after_login')))

def save_to_csv(data, filename):
    headers = ['rank', 'name', 'type', 'best_selling_products', 'revenue', 'avg_unit_price']
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for row in data:
            writer.writerow(row)    

def scrape_shop_info(driver, url):
    driver.get(url)
    shops_info = []

    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'tr.ant-table-row')))

    rows = driver.find_elements(By.CSS_SELECTOR, 'tr.ant-table-row')

    for row in rows:
        shop_info = {}

        shop_rank = row.find_element(By.CSS_SELECTOR, 'td.ant-table-cell.ant-table-cell-fix-left').text.strip()
        shop_info['rank'] = shop_rank

        shop_name = row.find_element(By.CSS_SELECTOR, 'div.line-clamp-1').text.strip()
        shop_info['name'] = shop_name

        shop_type = row.find_element(By.CSS_SELECTOR, 'div.text-base-999.line-clamp-1').text.strip()
        shop_info['type'] = shop_type

        best_selling_products = row.find_elements(By.CSS_SELECTOR, 'div.PageProduct-BestSaleProducts div.Component-Image.cover')
        products = [product.get_attribute('style').split('url("')[1].split('")')[0] for product in best_selling_products]
        shop_info['best_selling_products'] = products

        revenue = row.find_element(By.XPATH, './td[4]').text.strip()
        shop_info['revenue'] = revenue

        avg_unit_price = row.find_element(By.XPATH, './td[6]').text.strip()
        shop_info['avg_unit_price'] = avg_unit_price

        shops_info.append(shop_info)

    return shops_info

def scrape_products_info(driver, url, output_csv):
    driver.get(url)
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr')))
    time.sleep(2)

    product_rows = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr')
    
    product_rows = product_rows[1:]

    print(f"Total number of products found (excluding header): {len(product_rows)}")

    with open(output_csv, mode='w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Product Name', 'Price', 'Revenue', 'Items Sold', 'Avg Unit Price', 'Number of Creators', 'Launch Date', 'Conversion Ratio'])

        for index, row in enumerate(product_rows, start=2):
            try:
                product_name_xpath = f'//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr[{index}]/td[2]/div/div[2]/div[1]/div[1]/div'
                product_price_xpath = f'//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr[{index}]/td[2]/div/div[2]/div[2]'
                revenue_xpath = f'//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr[{index}]/td[3]'
                items_sold_xpath = f'//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr[{index}]/td[5]'
                avg_unit_price_xpath = f'//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr[{index}]/td[6]'
                number_of_creators_xpath = f'//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr[{index}]/td[8]'
                launch_date_xpath = f'//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr[{index}]/td[9]'
                conversion_ratio_xpath = f'//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr[{index}]/td[10]/div'

                product_name = driver.find_element(By.XPATH, product_name_xpath).text
                product_price = driver.find_element(By.XPATH, product_price_xpath).text
                revenue = driver.find_element(By.XPATH, revenue_xpath).text
                items_sold = driver.find_element(By.XPATH, items_sold_xpath).text
                avg_unit_price = driver.find_element(By.XPATH, avg_unit_price_xpath).text
                number_of_creators = driver.find_element(By.XPATH, number_of_creators_xpath).text
                launch_date = driver.find_element(By.XPATH, launch_date_xpath).text
                conversion_ratio = driver.find_element(By.XPATH, conversion_ratio_xpath).text
                
                csv_writer.writerow([product_name, product_price, revenue, items_sold, avg_unit_price, number_of_creators, launch_date, conversion_ratio])
                
            except Exception as e:
                print(f"Error occurred for row {index}: {e}")

def scrape_product_details(driver, url, output_csv):

    driver.get(url)
    print("\n\nstarted scraping\n\n")
    details = {}
    
    try:
        # Wait until the product name element is present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div[1]/div[1]/div[2]/div/div[1]/div')))
        
        # Product name
        details['Product Name'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div[1]/div[1]/div[2]/div/div[1]/div').text
        
        # Shipped from
        details['Shipped From'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div[1]/div[1]/div[2]/div/div[2]/div').text
        
        # Product category
        details['Product Category'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div[1]/div[1]/div[2]/div/div[3]/div[2]').text
        
        # Product price
        details['Product Price'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div[1]/div[1]/div[2]/div/div[6]/div').text
        
        # 30 days lowest price
        details['30 Days Lowest Price'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div[1]/div[1]/div[2]/div/div[7]/div/span').text
        
        # Shop name
        details['Shop Name'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[2]').text
        
        # Revenue in last 7 days
        details['Revenue in Last 7 Days'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[1]/div[1]/div[2]/div/div/div/div').text
        
        # Number of times product sold
        details['Number of Times Product Sold'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[1]/div[2]/div[2]/div/div/div/div').text
        
        # Avg unit price
        details['Avg Unit Price'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[1]/div[3]/div[2]/div/div/div/div').text
        
        # Live Revenue
        details['Live Revenue'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[1]/div[2]/div/div/div/div').text
        
        # Video Revenue
        details['Video Revenue'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div').text
        
        # Shopping mall revenue
        details['Shopping Mall Revenue'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[3]/div[2]/div/div/div/div').text

    except NoSuchElementException as e:
        print(f"Error finding element: {e}")
    
    # Save the scraped data to a CSV file
    with open('Cakes_cover.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(details.keys())
        # Write data
        writer.writerow(details.values())

    return details                