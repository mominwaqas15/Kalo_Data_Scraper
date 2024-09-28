import csv
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, InvalidSessionIdException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

def product_names(driver):
    names = []
    product_count = 0
    
    while True:

        retry_limit = 2

        product_rows = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[3]/div[1]/div/div/div/div[1]/div/table/tbody/tr')
        for index, product in enumerate(product_rows):
            retries = 0  # Track the number of retries for each product
            while retries < retry_limit:
                try:
                    # Extract product name relative to the current row
                    product_name = product.find_element(By.XPATH, './td[2]/div/div[2]/div/div[1]/div').text
                    names.append(product_name)
                    # print(f"Product #{index + 1}: {product_name}")  # Optional: Debugging output
                    break  # Break the loop if successful
                except StaleElementReferenceException as e:
                    retries += 1
                    # print(f"StaleElementReferenceException at product row {index + 1}. Retrying {retries}/{retry_limit}...")

                    if retries < retry_limit:
                        # Refresh the page and find product rows again
                        driver.refresh()
                        time.sleep(3)  # Allow some time for the page to load
                        product_rows = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[3]/div[1]/div/div/div/div[1]/div/table/tbody/tr')
                        product = product_rows[index]  # Reassign the specific product row for retry
                    else:
                        print(f"Failed to process product at row {index + 1} after {retry_limit} retries.")
                except Exception as e:
                    retries += 1
                    # print(f"Exception occurred at product row {index + 1}: {str(e)}. Retrying {retries}/{retry_limit}...")

                    if retries < retry_limit:
                        # Refresh the page and find product rows again
                        driver.refresh()
                        time.sleep(3)  # Allow some time for the page to load
                        product_rows = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[3]/div[1]/div/div/div/div[1]/div/table/tbody/tr')
                        product = product_rows[index]  # Reassign the specific product row for retry
                    else:
                        print(f"Failed to process product at row {index + 1} after {retry_limit} retries.")

        next_product_page_found = False

        # Find and click the next button
        for i in range(9, 12):  # Check dynamically for buttons from li[9] to li[12]
            try:
                next_button_xpath = f'/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[3]/div[1]/div/div/ul/li[{i}]/button'
                next_button = WebDriverWait(driver, 2).until(
                    EC.element_to_be_clickable((By.XPATH, next_button_xpath))
                )
                next_button.click()
                time.sleep(1)  # Allow time for the next page to load
                next_product_page_found = True
                break  # Exit the loop once the next button is clicked
            except TimeoutException:
                # print(f"Next Products Page button li[{i}] not found or clickable.")
                continue  # Try the next button if this one is not found

        if not next_product_page_found:
            # print("No more pages to scrape or buttons not found.")
            return ",".join(names)

def scrape_live_stream_details(driver, url):
    # driver.get(url)
    # print("\n\nstarted scraping live details")
    details = {}    
    driver.execute_script("window.scrollTo(0, 250);")

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/div/div/div[1]/div[2]/div/div[1]'))
        )

        try:
            details['Live stream name'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/div/div/div[1]/div[2]/div/div[1]').text
            if details['Live stream name'] == "":
                details['Live stream name'] = 'N/A'
        except:
            details['Live stream name'] = 'N/A'

        try:
            details['Creator name'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/div/div/div[2]/div[2]/div[2]/div[2]/div[1]').text
        except:
            details['Creator name'] = 'N/A'   

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
            details['Revenue'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[2]/div[2]/div[1]/div[1]/div/div/div/div/div[1]/div[2]/div/div/div/div').text
        except:
            details['Revenue'] = 'N/A'            

        try:
            details['Revenue per minute'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[2]/div[2]/div[1]/div[1]/div/div/div/div/div[1]/div[2]/div[2]').text
        except:
            details['Revenue per minute'] = 'N/A'

        try:
            details['Online viewers'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[2]/div[2]/div[1]/div[1]/div/div/div/div/div[2]/div[2]/div/div/div/div').text
        except:
            details['Online viewers'] = 'N/A' 

        try:
            details['Online viewers per minute'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[2]/div[2]/div[1]/div[1]/div/div/div/div/div[2]/div[2]/div[2]').text
        except:
            details['Online viewers per minute'] = 'N/A'

        try:
            details['Views'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[2]/div[2]/div[1]/div[1]/div/div/div/div/div[3]/div[2]/div/div/div/div').text
        except:
            details['Views'] = 'N/A' 

        try:
            details['Views per minute'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[2]/div[2]/div[1]/div[1]/div/div/div/div/div[3]/div[2]/div[2]').text
        except:
            details['Views per minute'] = 'N/A' 

        try:
            details['Items sold'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[2]/div[2]/div[1]/div[1]/div/div/div/div/div[4]/div[2]/div/div/div/div').text
        except:
            details['Items sold'] = 'N/A' 

        try:
            details['Items sold per minute'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[2]/div[2]/div[1]/div[1]/div/div/div/div/div[4]/div[2]/div[2]').text
        except:
            details['Items sold per minute'] = 'N/A'                                                 

        try:
            details['Average unit price'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[2]/div[2]/div[1]/div[1]/div/div/div/div/div[5]/div[2]/div/div/div/div').text
        except:
            details['Average unit price'] = 'N/A'   

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        try:
            details['Product Names'] = product_names(driver)
        except:
            details['Product Names'] = 'N/A'

        # try:
        #     with open(output_csv, 'a', newline='', encoding='utf-8') as csvfile:
        #         fieldnames = details.keys()
        #         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        #         # Write header only if file is empty
        #         if csvfile.tell() == 0:
        #             writer.writeheader()

        #         writer.writerow(details)
        # except Exception as e:
        #     print(f"Error writing to CSV: {e}")

    except Exception as e:
        print(f"Error in scraping live stream details: {e}")  

    return details              

def scrape_live_streams(driver, url, output_csv):
    driver.get(url)
    count = 0
    # max_streams = 500
    print('enter live stream function')

    # Scroll to the bottom of the page to load content
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    try:
        # Click necessary elements to reveal live streams
        element_to_click1 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div[2]/div[2]/div/div[1]/div/div/ul/li[10]/div/div[1]'))
        )
        element_to_click1.click()

        time.sleep(.5)

        element_to_click2 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div[2]/div[2]/div/div[1]/div/div/ul/li[10]/div/div[2]/div/div/div/div/div/div[3]'))
        )
        element_to_click2.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr'))
        )

    except TimeoutException:
        # print("The elements to show 50 live streams on page were not found.")
        return

    header = [
        'Live stream name', 'Number of products', 'Top 3 categories',
        'Live stream time', 'Stream duration', 'Creator name', 'Revenue',
        'Revenue per minute', 'Online viewers', 'Online viewers per minute',
        'Views', 'Views per minute', 'Items sold', 'Items sold per minute',
        'Average unit price', 'Product Names'
    ]

    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()

        while True:
            # Find all live streams on the current page
            time.sleep(.5)
            live_stream_rows = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div[2]/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr')
            # live_stream_rows = live_stream_rows[1:]  # Exclude the header row

            # print(f"Total number of live streams found: {len(live_stream_rows)}")

            original_window = driver.current_window_handle

            for index, live_stream in enumerate(live_stream_rows[:50], start=0):
                count += 1
                if count > 10:
                    break
                # print(f'Processing live stream #{count}')

                # Retry mechanism in case of StaleElementReferenceException
                max_retries = 2
                retries = 0
                success = False
                
                while retries < max_retries and not success:
                    try:
                        # Re-locate the live stream elements before clicking
                        live_stream = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div[2]/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr')[index]
                        ActionChains(driver).move_to_element_with_offset(live_stream, 75, 40).click().perform()
                        # live_stream.click()
                        # live_stream = live_stream_rows[index]


                        WebDriverWait(driver, 10).until(EC.new_window_is_opened)
                        new_tab = [window for window in driver.window_handles if window != original_window][0]
                        driver.switch_to.window(new_tab)

                        data = {field: 'Not scraped' for field in header}

                        live_stream_url = driver.current_url

                        scraped_data = scrape_live_stream_details(driver, live_stream_url)
                        if scraped_data is not None:
                            data.update(scraped_data)

                        writer.writerow(data)

                        driver.close()
                        driver.switch_to.window(original_window)

                        success = True  # Mark success if scraping completes successfully

                    except StaleElementReferenceException:
                        retries += 1
                        # print(f"StaleElementReferenceException encountered for live stream #{count}, retrying {retries}/{max_retries}...")
                        driver.refresh()  # Refresh the page in case of stale elements
                        time.sleep(5)

                    except TimeoutException:
                        retries += 1
                        # print(f"TimeoutException for live stream #{count}: Retrying {retries}/{max_retries}")
                        driver.refresh() 
                        time.sleep(5)

                    except Exception as e:
                        retries += 1
                        # print(f"Error processing live stream #{count}: {e}")
                        driver.refresh()  # Refresh the page in case of stale elements
                        time.sleep(5)

                if not success:
                    print(f"Failed to process live stream #{count} after {max_retries} attempts.")

            next_page_found = False
            retry_attempts = 1

            while retry_attempts > 0 and not next_page_found:
                for i in range(9, 12):  # Check for 'li[9]' to 'li[99]' dynamically
                    try:
                        if(count < 10):
                            next_button_xpath = f'/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/ul/li[{i}]/button'
                            # Try to find and click the 'Next Page' button with the first XPath
                            next_button = WebDriverWait(driver, 1).until(
                                EC.element_to_be_clickable((By.XPATH, next_button_xpath))
                            )
                            next_button.click()
                            time.sleep(1)
                            next_page_found = True  # A next button was found and clicked
                            break  # Exit the loop once the next button is clicked
                        else:
                            break

                    except TimeoutException:
                        # print(f"Next Page button li[{i}] not found or clickable.")
                        continue  # Try the next button if this one is not found

                if not next_page_found:
                    # print(f"Retrying page refresh... Remaining attempts: {retry_attempts - 1}")
                    retry_attempts -= 1
                    driver.refresh()
                    time.sleep(5)  # Allow time for the page to reload

            if not next_page_found:
                # print("No more pages to scrape or buttons not found.")
                break  # Exit the outer loop if no next button is found even after retries

    print("\nFinished scraping all Live Streams.")