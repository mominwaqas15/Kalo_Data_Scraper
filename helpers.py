import csv
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, InvalidSessionIdException, TimeoutException
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
    time.sleep(0.5)
    # # Wait for login to complete by checking the presence of some element on the landing page after login
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'some_element_on_homepage_after_login')))

def save_to_csv(data, filename):
    headers = ['rank', 'name', 'type', 'best_selling_products', 'revenue', 'avg_unit_price']
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for row in data:
            writer.writerow(row)                

# def scrape_shop_info(driver, url):
#     driver.get(url)
#     shops_info = []

#     WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'tr.ant-table-row')))

#     rows = driver.find_elements(By.CSS_SELECTOR, 'tr.ant-table-row')

#     for row in rows:
#         shop_info = {}

#         shop_rank = row.find_element(By.CSS_SELECTOR, 'td.ant-table-cell.ant-table-cell-fix-left').text.strip()
#         shop_info['rank'] = shop_rank

#         shop_name = row.find_element(By.CSS_SELECTOR, 'div.line-clamp-1').text.strip()
#         shop_info['name'] = shop_name

#         shop_type = row.find_element(By.CSS_SELECTOR, 'div.text-base-999.line-clamp-1').text.strip()
#         shop_info['type'] = shop_type

#         best_selling_products = row.find_elements(By.CSS_SELECTOR, 'div.PageProduct-BestSaleProducts div.Component-Image.cover')
#         products = [product.get_attribute('style').split('url("')[1].split('")')[0] for product in best_selling_products]
#         shop_info['best_selling_products'] = products

#         revenue = row.find_element(By.XPATH, './td[4]').text.strip()
#         shop_info['revenue'] = revenue

#         avg_unit_price = row.find_element(By.XPATH, './td[6]').text.strip()
#         shop_info['avg_unit_price'] = avg_unit_price

#         shops_info.append(shop_info)

#     return shops_info

# def scrape_products_info(driver, url, output_csv):
#     driver.get(url)
#     # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr')))
#     time.sleep(2)

#     product_rows = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr')
    
#     product_rows = product_rows[1:]

#     print(f"Total number of products found (excluding header): {len(product_rows)}")

#     with open(output_csv, mode='w', newline='', encoding='utf-8') as csv_file:
#         csv_writer = csv.writer(csv_file)
#         csv_writer.writerow(['Product Name', 'Price', 'Revenue', 'Items Sold', 'Avg Unit Price', 'Number of Creators', 'Launch Date', 'Conversion Ratio'])

#         for index, row in enumerate(product_rows, start=2):
#             try:
#                 product_name_xpath = f'//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr[{index}]/td[2]/div/div[2]/div[1]/div[1]/div'
#                 product_price_xpath = f'//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr[{index}]/td[2]/div/div[2]/div[2]'
#                 revenue_xpath = f'//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr[{index}]/td[3]'
#                 items_sold_xpath = f'//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr[{index}]/td[5]'
#                 avg_unit_price_xpath = f'//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr[{index}]/td[6]'
#                 number_of_creators_xpath = f'//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr[{index}]/td[8]'
#                 launch_date_xpath = f'//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr[{index}]/td[9]'
#                 conversion_ratio_xpath = f'//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr[{index}]/td[10]/div'

#                 product_name = driver.find_element(By.XPATH, product_name_xpath).text
#                 product_price = driver.find_element(By.XPATH, product_price_xpath).text
#                 revenue = driver.find_element(By.XPATH, revenue_xpath).text
#                 items_sold = driver.find_element(By.XPATH, items_sold_xpath).text
#                 avg_unit_price = driver.find_element(By.XPATH, avg_unit_price_xpath).text
#                 number_of_creators = driver.find_element(By.XPATH, number_of_creators_xpath).text
#                 launch_date = driver.find_element(By.XPATH, launch_date_xpath).text
#                 conversion_ratio = driver.find_element(By.XPATH, conversion_ratio_xpath).text
                
#                 csv_writer.writerow([product_name, product_price, revenue, items_sold, avg_unit_price, number_of_creators, launch_date, conversion_ratio])
                
#             except Exception as e:
#                 print(f"Error occurred for row {index}: {e}")    

def scrape_product_details(driver, url):
    # driver.get(url)
    # print("\n\nstarted scraping product details\n\n")
    details = {}
    # time.sleep()

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div[1]/div[1]/div[2]/div/div[1]/div')))
        details['Product Name'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div[1]/div[1]/div[2]/div/div[1]/div').text
        details['Shipped From'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/div[1]/div[1]/div[2]/div/div[2]/div').text
        details['Product Category'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/div[1]/div[1]/div[2]/div/div[3]/div[2]').text
        details['Product Price'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/div[1]/div[1]/div[2]/div/div[4]/div').text
        details['30 Days Lowest Price'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/div[1]/div[1]/div[2]/div/div[5]/div/span').text
        details['Shop Name'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[2]').text

        time_ranges = {
            'Yesterday': '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div/label[1]',
            'Last 7 Days': '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div/label[2]',
            'Last 30 Days': '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div/label[3]',
            'Last 90 Days': '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div/label[4]',
            'Last 180 Days': '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div/label[5]'
        }

        driver.execute_script("window.scrollTo(0, 300);")
        for range_name, range_xpath in time_ranges.items():
            driver.find_element(By.XPATH, range_xpath).click()

            # Wait for the content to update after clicking
            try:
                WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[1]/div[1]/div[2]/div[1]')))
            except:
                driver.refresh()                

            details[f'Revenue in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[1]/div[1]/div[2]/div[1]').text
            details[f'Revenue per day in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[1]/div[1]/div[2]/div[2]').text
            details[f'Number of products sold in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[1]/div[2]/div[2]/div[1]/div/div/div/div').text
            details[f'Number of products sold per day in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[1]/div[2]/div[2]/div[2]').text
            try:
                WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[1]/div[3]/div[2]/div[1]/div/div/div/div')))
            except:
                driver.refresh()                
            details[f'Avg Unit Price in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[1]/div[3]/div[2]/div[1]/div/div/div/div').text
            details[f'Live Revenue in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div/div/div/div').text
            details[f'Live Revenue per day in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[1]/div[2]/div[2]').text
            details[f'Video Revenue in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[2]/div[2]/div[1]/div/div/div/div').text
            details[f'Video Revenue per day in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[2]/div[2]/div[2]').text
            details[f'Shopping Mall Revenue in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[3]/div[2]/div[1]/div/div/div/div').text
            details[f'Shopping Mall Revenue per day in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[3]/div[2]/div[2]').text

        driver.execute_script("window.scrollTo(0, -300);")
        # # Scrape other details that don't change with time range
        details['Earliest Date Recorded'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/div[1]/div[2]/div[1]/span').text

        # TikTok links and images
        original_window = driver.current_window_handle
        try:
            # print('\n\nscraping tiktok link')
            tiktok_link_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/div[1]/div[1]/div[2]/div/div[7]/div')
            tiktok_link_element.click()
            WebDriverWait(driver, 10).until(EC.new_window_is_opened)
            windows = driver.window_handles
            driver.switch_to.window(windows[-1])
            tiktok_link = driver.current_url
            details['TikTok Link'] = tiktok_link
            driver.close()
            driver.switch_to.window(original_window)
        except NoSuchElementException as e:
            print(f"Error finding TikTok link element: {e}")

        try:
            # print('\n\nscraping product images')
            image_elements = driver.find_elements(By.XPATH, '//*[@class="images scrollbar flex flex-col pt-0 h-[168px] overflow-y-auto  gap-2"]/div')
            image_urls = []
            for image_element in image_elements:
                style_attribute = image_element.get_attribute('style')
                url = style_attribute.split('url("')[1].split('");')[0]
                image_urls.append(url)
            details['Image URLs'] = ','.join(image_urls)
        except NoSuchElementException as e:
            print(f"Error finding image elements: {e}")

    except NoSuchElementException as e:
        print(f"Error while scraping: {e}")   

    # # Write the details to CSV
    # with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(details.keys())
    #     writer.writerow(details.values())

    return details

def scrape_all_products(driver, url, output_csv):
    # Visit the URL
    driver.get(url)
    count = 0

    # Scroll to the bottom of the page to reveal more content
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # time.sleep(1)  # Give time for content to load

    # Click on the specified elements
    try:
        element_to_click1 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/ul/li[10]/div/div[1]'))
        )
        element_to_click1.click()

        element_to_click2 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/ul/li[10]/div/div[2]/div/div/div/div/div/div[3]/div'))
        )
        element_to_click2.click()

    except TimeoutException:
        print("The elements to show 50 products on page were not found.")
        return

    # Find all products
    time.sleep(.5)
    product_rows = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr')
    product_rows = product_rows[1:]  # Exclude the header row

    # print(f"Total number of products found (excluding header): {len(product_rows)}")

    original_window = driver.current_window_handle  # Store the current window handle
    header = ['Product Name', 'Shipped From', 'Product Category', 'Product Price','30 Days Lowest Price', 'Shop Name', 'Revenue in Yesterday','Revenue per day in Yesterday', 'Number of products sold in Yesterday','Number of products sold per day in Yesterday','Avg Unit Price in Yesterday', 'Live Revenue in Yesterday','Live Revenue per day in Yesterday', 'Video Revenue in Yesterday','Video Revenue per day in Yesterday','Shopping Mall Revenue in Yesterday','Shopping Mall Revenue per day in Yesterday', 'Revenue in Last 7 Days','Revenue per day in Last 7 Days','Number of products sold in Last 7 Days','Number of products sold per day in Last 7 Days','Avg Unit Price in Last 7 Days', 'Live Revenue in Last 7 Days','Live Revenue per day in Last 7 Days', 'Video Revenue in Last 7 Days','Video Revenue per day in Last 7 Days','Shopping Mall Revenue in Last 7 Days','Shopping Mall Revenue per day in Last 7 Days','Revenue in Last 30 Days', 'Revenue per day in Last 30 Days','Number of products sold in Last 30 Days','Number of products sold per day in Last 30 Days','Avg Unit Price in Last 30 Days', 'Live Revenue in Last 30 Days','Live Revenue per day in Last 30 Days', 'Video Revenue in Last 30 Days','Video Revenue per day in Last 30 Days','Shopping Mall Revenue in Last 30 Days','Shopping Mall Revenue per day in Last 30 Days','Revenue in Last 90 Days', 'Revenue per day in Last 90 Days','Number of products sold in Last 90 Days','Number of products sold per day in Last 90 Days','Avg Unit Price in Last 90 Days', 'Live Revenue in Last 90 Days','Live Revenue per day in Last 90 Days', 'Video Revenue in Last 90 Days','Video Revenue per day in Last 90 Days','Shopping Mall Revenue in Last 90 Days','Shopping Mall Revenue per day in Last 90 Days','Revenue in Last 180 Days', 'Revenue per day in Last 180 Days','Number of products sold in Last 180 Days','Number of products sold per day in Last 180 Days','Avg Unit Price in Last 180 Days', 'Live Revenue in Last 180 Days','Live Revenue per day in Last 180 Days','Video Revenue in Last 180 Days','Video Revenue per day in Last 180 Days','Shopping Mall Revenue in Last 180 Days','Shopping Mall Revenue per day in Last 180 Days','Earliest Date Recorded', 'TikTok Link', 'Image URLs']

    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()

    # Loop through each product
        for index, product in enumerate(product_rows[:50], start=1):
            count = count + 1
            # print(f"\nProcessing product {index}/{len(product_rows)}")

            # Click on the product to open in a new tab
            product.click()

            print(f'processing product: {count}')
            # Wait for the new tab to open and switch to it
            WebDriverWait(driver, 10).until(EC.new_window_is_opened)
            new_tab = [window for window in driver.window_handles if window != original_window][0]
            driver.switch_to.window(new_tab)

            # Scrape the product details
            product_url = driver.current_url
            try:
                data = scrape_product_details(driver, product_url)
            except Exception as e:
                print(f"Error scraping product {count}: {e}")
                # Fill the row with "Not scraped" if there's an error
                data = {field: 'Not scraped' for field in header}

            # Write the details to CSV
            writer.writerow(data)

            # Close the current tab and switch back to the original tab
            driver.close()
            driver.switch_to.window(original_window)

    print("\nFinished scraping all products.")          

def scrape_500_products(driver, url, output_csv):
    # Visit the URL
    driver.get(url)
    count = 0

    # Scroll to the bottom of the page to reveal more content
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # time.sleep(1)  # Give time for content to load

    # Click on the specified elements
    try:
        element_to_click1 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/ul/li[10]/div/div[1]'))
        )
        element_to_click1.click()

        element_to_click2 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/ul/li[10]/div/div[2]/div/div/div/div/div/div[3]/div'))
        )
        element_to_click2.click()

    except TimeoutException:
        print("The elements to show 50 products on page were not found.")
        return

    header = ['Product Name', 'Shipped From', 'Product Category', 'Product Price','30 Days Lowest Price', 'Shop Name', 'Revenue in Yesterday','Revenue per day in Yesterday', 'Number of products sold in Yesterday','Number of products sold per day in Yesterday','Avg Unit Price in Yesterday', 'Live Revenue in Yesterday','Live Revenue per day in Yesterday', 'Video Revenue in Yesterday','Video Revenue per day in Yesterday','Shopping Mall Revenue in Yesterday','Shopping Mall Revenue per day in Yesterday', 'Revenue in Last 7 Days','Revenue per day in Last 7 Days','Number of products sold in Last 7 Days','Number of products sold per day in Last 7 Days','Avg Unit Price in Last 7 Days', 'Live Revenue in Last 7 Days','Live Revenue per day in Last 7 Days', 'Video Revenue in Last 7 Days','Video Revenue per day in Last 7 Days','Shopping Mall Revenue in Last 7 Days','Shopping Mall Revenue per day in Last 7 Days','Revenue in Last 30 Days', 'Revenue per day in Last 30 Days','Number of products sold in Last 30 Days','Number of products sold per day in Last 30 Days','Avg Unit Price in Last 30 Days', 'Live Revenue in Last 30 Days','Live Revenue per day in Last 30 Days', 'Video Revenue in Last 30 Days','Video Revenue per day in Last 30 Days','Shopping Mall Revenue in Last 30 Days','Shopping Mall Revenue per day in Last 30 Days','Revenue in Last 90 Days', 'Revenue per day in Last 90 Days','Number of products sold in Last 90 Days','Number of products sold per day in Last 90 Days','Avg Unit Price in Last 90 Days', 'Live Revenue in Last 90 Days','Live Revenue per day in Last 90 Days', 'Video Revenue in Last 90 Days','Video Revenue per day in Last 90 Days','Shopping Mall Revenue in Last 90 Days','Shopping Mall Revenue per day in Last 90 Days','Revenue in Last 180 Days', 'Revenue per day in Last 180 Days','Number of products sold in Last 180 Days','Number of products sold per day in Last 180 Days','Avg Unit Price in Last 180 Days', 'Live Revenue in Last 180 Days','Live Revenue per day in Last 180 Days','Video Revenue in Last 180 Days','Video Revenue per day in Last 180 Days','Shopping Mall Revenue in Last 180 Days','Shopping Mall Revenue per day in Last 180 Days','Earliest Date Recorded', 'TikTok Link', 'Image URLs']

    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()

        # Continue scraping until no more pages
        while True:
            # Find all products
            time.sleep(.5)
            product_rows = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr')
            product_rows = product_rows[1:]  # Exclude the header row

            print(f"Total number of products found (excluding header): {len(product_rows)}")

            original_window = driver.current_window_handle  # Store the current window handle

            # Loop through each product
            for index, product in enumerate(product_rows[:50], start=1):
                count = count + 1
                # print(f"\nProcessing product {index}/{len(product_rows)}")
                print(f'processing product: {count}')

                # Click on the product to open in a new tab
                product.click()

                # Wait for the new tab to open and switch to it
                WebDriverWait(driver, 10).until(EC.new_window_is_opened)
                new_tab = [window for window in driver.window_handles if window != original_window][0]
                driver.switch_to.window(new_tab)

                # Scrape the product details
                product_url = driver.current_url
                try:
                    data = scrape_product_details(driver, product_url)
                except Exception as e:
                    print(f"Error scraping product {count}: {e}")
                    # Fill the row with "Not scraped" if there's an error
                    data = {field: 'Not scraped' for field in header}

                # Write the details to CSV
                writer.writerow(data)

                # Close the current tab and switch back to the original tab
                driver.close()
                driver.switch_to.window(original_window)

            try:
                # Try to find and click the 'Next Page' button with the first XPath
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/ul/li[9]/button'))
                )
                next_button.click()
            except TimeoutException:
                print("First 'Next Page' button not found or not clickable.")
                try:
                    # Try to find and click the 'Next Page' button with the second XPath
                    next_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/ul/li[11]/button'))
                    )
                    next_button.click()
                except TimeoutException:
                    print("No more pages to scrape or 'Next Page' button not found.")
                    break  # Exit the loop if neither button is found or clickable

            print("Moving to the next page...")

    print("\nFinished scraping all products.")


def scrape_creator_details(driver, url, output_csv):
    driver.get(url)
    print("\n\nstarted scraping creator details\n\n")
    details = {}

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div[1]/div[1]/div/div'))
        )

        time_ranges = {
            'Yesterday': '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div/label[1]',
            'Last 7 Days': '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div/label[2]',
            'Last 30 Days': '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div/label[3]',
            'Last 90 Days': '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div/label[4]',
            'Last 180 Days': '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[2]/div/div/div[2]/div/div[2]/div/label[5]'
        }
        
        # Scrape creator details
        try:
            details['Username'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div[1]/div[1]/div/div').text
        except:
            details['Username'] = 'N/A'

        try:
            details['Number of Followers'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div[3]/div/div[2]/div[1]/div').text
        except:
            details['Number of Followers'] = 'N/A'

        # try:
        #     details['Profile Pic URL'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div[1]').get_attribute('src')
        # except:
        #     details['Profile Pic URL'] = 'N/A'

        try:
            details['Debut Time'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div[3]/div/div[2]/div[2]/div').text
        except:
            details['Debut Time'] = 'N/A'

        try:
            details['Products in Last 30 Days'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div[3]/div/div[2]/div[3]/div').text
        except:
            details['Products in Last 30 Days'] = 'N/A'

        try:
            details['Bio'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div[3]/div/div[2]').text
        except:
            details['Bio'] = 'N/A'

        try:
            details['Earliest Date Recorded'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[2]/div[1]/span').text
        except:
            details['Earliest Date Recorded'] = 'N/A'

        try:
            tiktok_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[2]/div[2]/div/div[2]/div/div[1]/div[1]/div')
            details['Tiktok Link'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[2]/div[2]/div/div[2]/div/div[1]/div[1]/div/a').get_attribute('href')
        except:
            details['Tiktok Link'] = 'N/A'

        try:
            instagram_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[1]/div')
            details['Instagram Link'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[1]/div/a').get_attribute('href')
        except:
            details['Instagram Link'] = 'N/A'

        try:
            youtube_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[2]/div[2]/div/div[2]/div/div[4]/div[1]/div')
            details['YouTube Link'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[2]/div[2]/div/div[2]/div/div[4]/div[1]/div/a').get_attribute('href')
        except:
            details['YouTube Link'] = 'N/A'            

        # Scrape email
        try:
            email_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/div')
            details['Email address'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/div/a').get_attribute('href').replace('mailto:', '')
        except:
            details['Email address'] = 'N/A'

        # Scrape data for each time range
        for range_name, range_xpath in time_ranges.items():
            try:
                driver.find_element(By.XPATH, range_xpath).click()
                # Wait for page content to update
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[1]/div[2]/div/div/div/div'))
                )
                
                details[f'Revenue in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[1]/div[2]/div/div/div/div').text
                details[f'Revenue per day in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[1]/div[3]').text
                details[f'Live Revenue in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div').text
                details[f'Live Revenue per day in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[2]/div[3]').text
                details[f'Video Revenue in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[3]/div[2]/div/div/div/div').text
                details[f'Video Revenue per day in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[3]/div[3]').text
                details[f'Average unit price in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[4]/div[2]/div/div/div/div').text
                details[f'Traffic live views in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[4]/div[1]/div[2]/div/div/div/div').text
                details[f'Traffic live views per day in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[4]/div[1]/div[3]').text
                details[f'Traffic video views in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[4]/div[2]/div[2]/div/div/div/div').text
                details[f'Traffic video views per day in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[4]/div[2]/div[3]').text
                details[f'New followers in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[4]/div[3]/div[2]/div/div/div/div').text
                details[f'New followers per day in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[4]/div[3]/div[3]').text
            except Exception as e:
                print(f"Error during scraping for range '{range_name}': {e}")
                continue

        # Write to CSV
        try:
            with open(output_csv, 'a', newline='', encoding='utf-8') as csvfile:
                fieldnames = details.keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # Write header only if file is empty
                if csvfile.tell() == 0:
                    writer.writeheader()

                writer.writerow(details)
        except Exception as e:
            print(f"Error writing to CSV: {e}")

    except Exception as e:
        print(f"Error in scrape_creator_details: {e}")   

def scrape_live_stream_details(driver, url, output_csv):
    driver.get(url)
    print("\n\nstarted scraping live details")
    details = {}    

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/div/div/div[1]/div[2]/div/div[1]'))
        )

        try:
            details['Live stream name'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/div/div/div[1]/div[2]/div/div[1]').text
        except:
            details['Live stream name'] = 'N/A'

        try:
            details['Number of products'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/div/div/div[1]/div[2]/div/div[2]/div[2]').text
        except:
            details['Number of products'] = 'N/A'

        try:
            details['Top 3 categories'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/div/div/div[1]/div[2]/div/div[3]/div[2]/div').text
        except:
            details['Top 3 categories'] = 'N/A' 

        try:
            details['Live stream time'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/div/div/div[1]/div[2]/div/div[4]/div/div[2]/span').text
        except:
            details['Live stream time'] = 'N/A'

        try:
            details['Stream duration'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/div/div/div[1]/div[2]/div/div[4]/div/div[2]/div/div').text
        except:
            details['Stream duration'] = 'N/A'  

        try:
            details['Creator name'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/div/div/div[2]/div[2]/div[2]/div[2]/div[1]').text
        except:
            details['Creator name'] = 'N/A'                                   

        try:
            details['Revenue'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[2]/div[2]/div[1]/div[1]/div/div/div/div/div[1]/div[2]/div/div/div/div').text
        except:
            details['Revenue'] = 'N/A'            

        try:
            details['Revenue per minute'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[2]/div[2]/div[1]/div[1]/div/div/div/div/div[1]/div[3]').text
        except:
            details['Revenue per minute'] = 'N/A'

        try:
            details['Online viewers'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[2]/div[2]/div[1]/div[1]/div/div/div/div/div[2]/div[2]/div/div/div/div').text
        except:
            details['Online viewers'] = 'N/A' 

        try:
            details['Online viewers per minute'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[2]/div[2]/div[1]/div[1]/div/div/div/div/div[2]/div[3]').text
        except:
            details['Online viewers per minute'] = 'N/A'

        try:
            details['Views'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[2]/div[2]/div[1]/div[1]/div/div/div/div/div[3]/div[2]/div/div/div/div').text
        except:
            details['Views'] = 'N/A' 

        try:
            details['Views per minute'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[2]/div[2]/div[1]/div[1]/div/div/div/div/div[3]/div[3]').text
        except:
            details['Views per minute'] = 'N/A' 

        try:
            details['Items sold'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[2]/div[2]/div[1]/div[1]/div/div/div/div/div[4]/div[2]/div/div/div/div').text
        except:
            details['Items sold'] = 'N/A' 

        try:
            details['Items sold per minute'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[2]/div[2]/div[1]/div[1]/div/div/div/div/div[4]/div[3]').text
        except:
            details['Items sold per minute'] = 'N/A'                                                 

        try:
            details['Average unit price'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[2]/div[2]/div[1]/div[1]/div/div/div/div/div[5]/div[2]/div/div/div/div').text
        except:
            details['Average unit price'] = 'N/A'   

        try:
            with open(output_csv, 'a', newline='', encoding='utf-8') as csvfile:
                fieldnames = details.keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # Write header only if file is empty
                if csvfile.tell() == 0:
                    writer.writeheader()

                writer.writerow(details)
        except Exception as e:
            print(f"Error writing to CSV: {e}")

    except Exception as e:
        print(f"Error in scraping live stream details: {e}")                      