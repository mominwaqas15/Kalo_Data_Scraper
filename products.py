import csv
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, InvalidSessionIdException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
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
        try: 
            category = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/div[1]/div[1]/div[2]/div/div[3]/div[2]').text
            category = category.strip()
            if category:
                details['Product Category'] = category
            else:
                details['Product Category'] = "N/A"            
        except: 
            details['Product Category'] = "N/A"   
        details['Product Price'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/div[1]/div[1]/div[2]/div/div[4]/div').text

        try:
            commission =  driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/div[1]/div[1]/div[2]/div/div[6]/span').text
            commission = commission.strip()
            if commission:
                details['Product Commission Rate'] = commission
            else:
                details['Product Commission Rate'] = "N/A"
        except Exception as E:
            details['Product Commission Rate'] = "N/A"

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
            retry_count = 0
            max_retries = 2  # Set the maximum number of retries

            while retry_count<max_retries:
                try:

                    driver.find_element(By.XPATH, range_xpath).click()

                    # Wait for the content to update after clicking
                    try:
                        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[1]/div[1]/div[2]/div[1]')))
                    except TimeoutException as e:
                        # time.sleep(5)
                        driver.refresh()
                        time.sleep(3)              

                    details[f'Revenue in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[1]/div[1]/div[2]/div[1]').text
                    details[f'Revenue per day in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[1]/div[1]/div[2]/div[2]').text
                    details[f'Number of products sold in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[1]/div[2]/div[2]/div[1]/div/div/div/div').text
                    details[f'Number of products sold per day in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[1]/div[2]/div[2]/div[2]').text
                    
                    try:
                        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[4]/div[2]/div[1]/div/div/div/div')))
                    except:
                        # time.sleep()
                        driver.refresh()
                        time.sleep(3)

                    details[f'Avg Unit Price in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[1]/div[3]/div[2]/div[1]/div/div/div/div').text
                    details[f'Live Revenue in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div/div/div/div').text
                    details[f'Live Revenue per day in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[1]/div[2]/div[2]').text
                    details[f'Video Revenue in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[2]/div[2]/div[1]/div/div/div/div').text
                    details[f'Video Revenue per day in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[2]/div[2]/div[2]').text
                    details[f'Shopping Mall Revenue in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[3]/div[2]/div[1]/div/div/div/div').text
                    details[f'Shopping Mall Revenue per day in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[3]/div[2]/div[2]').text

                    break

                except Exception as e:
                    retry_count += 1
                    print(f"Error during scraping for range '{range_name}', retry number{retry_count}.")
                    if retry_count < max_retries:
                        time.sleep(10)
                        driver.refresh()  # Refresh page and retry
                        time.sleep(5)
                    else:
                        print(f"Failed to scrape data for range '{range_name}' after {max_retries} retries.")   

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
            # Attempt to scrape multiple product images
            image_elements = driver.find_elements(By.XPATH, '//*[@class="images scrollbar flex flex-col pt-0 h-[168px] overflow-y-auto  gap-2"]/div')
            
            # If no image elements are found, attempt to scrape the single image
            if not image_elements:
                image_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]')
                style_attribute = image_element.get_attribute('style')
                
                # Ensure the style attribute contains the expected URL format
                if 'url("' in style_attribute:
                    image_url = style_attribute.split('url("')[1].split('");')[0]
                    details['Image URLs'] = image_url
                else:
                    print("Style attribute does not contain a valid URL")
                    details['Image URLs'] = "N/A"
            
            # If multiple images are found, scrape all of them
            else:
                image_urls = []
                for image_element in image_elements:
                    style_attribute = image_element.get_attribute('style')
                    
                    # Ensure the style attribute contains the expected URL format
                    if 'url("' in style_attribute:
                        url = style_attribute.split('url("')[1].split('");')[0]
                        image_urls.append(url)
                    else:
                        print("Style attribute does not contain a valid URL")
                
                details['Image URLs'] = ','.join(image_urls) if image_urls else "N/A"
                
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

    header = ['Product Name', 'Shipped From', 'Product Category', 'Product Price', 'Product Commission Rate', '30 Days Lowest Price', 'Shop Name', 'Revenue in Yesterday','Revenue per day in Yesterday', 'Number of products sold in Yesterday','Number of products sold per day in Yesterday','Avg Unit Price in Yesterday', 'Live Revenue in Yesterday','Live Revenue per day in Yesterday', 'Video Revenue in Yesterday','Video Revenue per day in Yesterday','Shopping Mall Revenue in Yesterday','Shopping Mall Revenue per day in Yesterday', 'Revenue in Last 7 Days','Revenue per day in Last 7 Days','Number of products sold in Last 7 Days','Number of products sold per day in Last 7 Days','Avg Unit Price in Last 7 Days', 'Live Revenue in Last 7 Days','Live Revenue per day in Last 7 Days', 'Video Revenue in Last 7 Days','Video Revenue per day in Last 7 Days','Shopping Mall Revenue in Last 7 Days','Shopping Mall Revenue per day in Last 7 Days','Revenue in Last 30 Days', 'Revenue per day in Last 30 Days','Number of products sold in Last 30 Days','Number of products sold per day in Last 30 Days','Avg Unit Price in Last 30 Days', 'Live Revenue in Last 30 Days','Live Revenue per day in Last 30 Days', 'Video Revenue in Last 30 Days','Video Revenue per day in Last 30 Days','Shopping Mall Revenue in Last 30 Days','Shopping Mall Revenue per day in Last 30 Days','Revenue in Last 90 Days', 'Revenue per day in Last 90 Days','Number of products sold in Last 90 Days','Number of products sold per day in Last 90 Days','Avg Unit Price in Last 90 Days', 'Live Revenue in Last 90 Days','Live Revenue per day in Last 90 Days', 'Video Revenue in Last 90 Days','Video Revenue per day in Last 90 Days','Shopping Mall Revenue in Last 90 Days','Shopping Mall Revenue per day in Last 90 Days','Revenue in Last 180 Days', 'Revenue per day in Last 180 Days','Number of products sold in Last 180 Days','Number of products sold per day in Last 180 Days','Avg Unit Price in Last 180 Days', 'Live Revenue in Last 180 Days','Live Revenue per day in Last 180 Days','Video Revenue in Last 180 Days','Video Revenue per day in Last 180 Days','Shopping Mall Revenue in Last 180 Days','Shopping Mall Revenue per day in Last 180 Days','Earliest Date Recorded', 'TikTok Link', 'Image URLs']

    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()

        # Continue scraping until no more pages
        while True:
            # Find all products
            time.sleep(.5)
            product_rows = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr')
            product_rows = product_rows[1:]  # Exclude the header row

            print(f"Total number of products found: {len(product_rows)}")

            original_window = driver.current_window_handle  # Store the current window handle

            # Loop through each product
            for index, product in enumerate(product_rows[:50], start=1):
                count = count + 1
                if(count > 10):
                    break
                # print(f"\nProcessing product {index}/{len(product_rows)}")
                print(f'processing product #{count}')

                max_retries = 2
                retries = 0
                success = False

                while retries < max_retries and not success:
                    try:
                        product.click()
                        # product = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr')
                        # WebDriverWait(driver, 10).until(
                        # EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr'))
                        # )
                        # ActionChains(driver).move_to_element_with_offset(product, 75, 40).click().perform()

                        WebDriverWait(driver, 10).until(EC.new_window_is_opened)
                        new_tab = [window for window in driver.window_handles if window != original_window][0]
                        driver.switch_to.window(new_tab)

                        data = {field: 'Not scraped' for field in header}

                        # Scrape the product details
                        product_url = driver.current_url
                        scraped_data = scrape_product_details(driver, product_url)
                        if scraped_data is not None:
                            data.update(scraped_data)

                        # Write the details to CSV
                        writer.writerow(data)

                        # Close the current tab and switch back to the original tab
                        driver.close()
                        driver.switch_to.window(original_window)
                        success = True
                        
                    except StaleElementReferenceException:
                        retries +=1
                        print(f"StaleElementReferenceException: Retrying for Product #{count}, attempt {retries}/{max_retries}")
                        driver.refresh()
                        time.sleep(3)

                    except TimeoutException:
                        retries += 1
                        print(f"TimeoutException for Product #{count}: Retrying {retries}/{max_retries}")
                        driver.refresh() 
                        time.sleep(3)

                    except Exception as e:
                        retries += 1
                        print(f"Error processing Product #{count}: {e}")
                        driver.refresh()
                        time.sleep(3)

                if not success:
                    print(f"Failed to process Product #{count} after {max_retries} attempts")
            
            next_page_found = False
            retry_attempts = 1

            while retry_attempts > 0 and not next_page_found:
                for i in range(9, 12):  # Check for 'li[9]' to 'li[99]' dynamically
                    try:
                        if count < 10:
                            next_button_xpath = f'/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/ul/li[{i}]/button'
                            next_button = WebDriverWait(driver, 2).until(
                                EC.element_to_be_clickable((By.XPATH, next_button_xpath))
                            )
                            next_button.click()
                            time.sleep(1)
                            next_page_found = True  # A next button was found and clicked
                            break  # Exit the loop once the next button is clicked
                        else:
                            break
                    except TimeoutException:
                        print(f"Next Page button li[{i}] not found or clickable.")
                        continue  # Try the next button if this one is not found

                if not next_page_found:
                    print(f"Retrying page refresh... Remaining attempts: {retry_attempts - 1}")
                    retry_attempts -= 1
                    driver.refresh()
                    time.sleep(3)  # Allow time for the page to reload

            if not next_page_found:
                print("No more pages to scrape or buttons not found.")
                break  # Exit the outer loop if no next button is found even after retries

    print("\nFinished scraping all creators.")
                        
            
    #         try:
    #             if(count < 500):
    #             # Try to find and click the 'Next Page' button with the first XPath
    #                 next_button = WebDriverWait(driver, 1).until(
    #                     EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/ul/li[9]/button'))
    #                 )
    #                 next_button.click()
    #         except TimeoutException:
    #             print("First 'Next Page' button not found or not clickable.")
    #             try:
    #                 # Try to find and click the 'Next Page' button with the second XPath
    #                 next_button = WebDriverWait(driver, 1).until(
    #                     EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/ul/li[10]/button'))
    #                 )
    #                 next_button.click()
    #             except TimeoutException:
    #                 print("No more pages to scrape or 'Next Page' button not found.")
    #                 try:
    #                     # Try to find and click the 'Next Page' button with the second XPath
    #                     next_button = WebDriverWait(driver, 1).until(
    #                         EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/ul/li[11]/button'))
    #                     )
    #                     next_button.click()
    #                 except TimeoutException:
    #                     print("No more pages to scrape or 'Next Page' button not found.")
    #                     break  # Exit the loop if neither button is found or clickable

    # print("\nFinished scraping all products.")