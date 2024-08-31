import csv
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, InvalidSessionIdException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC

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
                time.sleep(.5)                
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


def scrape_products(driver, url, output_csv):
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
                if(count > 500):
                    break
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
                    if(count < 500):
                    # Try to find and click the 'Next Page' button with the first XPath
                        next_button = WebDriverWait(driver, 1).until(
                            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/ul/li[9]/button'))
                        )
                        next_button.click()
            except TimeoutException:
                print("First 'Next Page' button not found or not clickable.")
                try:
                    # Try to find and click the 'Next Page' button with the second XPath
                    next_button = WebDriverWait(driver, 1).until(
                        EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/ul/li[10]/button'))
                    )
                    next_button.click()
                except TimeoutException:
                    print("No more pages to scrape or 'Next Page' button not found.")
                    try:
                        # Try to find and click the 'Next Page' button with the second XPath
                        next_button = WebDriverWait(driver, 1).until(
                            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/ul/li[11]/button'))
                        )
                        next_button.click()
                    except TimeoutException:
                        print("No more pages to scrape or 'Next Page' button not found.")
                        break  # Exit the loop if neither button is found or clickable

    print("\nFinished scraping all products.")