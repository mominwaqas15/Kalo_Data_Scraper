import csv
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, InvalidSessionIdException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC

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

# def scrape_live_streams(driver, url, output_csv):
#     # Visit the URL
#     driver.get(url)
#     count = 0

#     # Scroll to the bottom of the page to reveal more content
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     # time.sleep(1)  # Give time for content to load

#     # Click on the specified elements
#     try:
#         element_to_click1 = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/ul/li[10]/div/div[1]'))
#         )
#         element_to_click1.click()

#         element_to_click2 = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/ul/li[10]/div/div[2]/div/div/div/div/div/div[3]/div'))
#         )
#         element_to_click2.click()

#         # WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[1]/div[1]/div[2]/div[1]')))

#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr'))
#         )
        

#     except TimeoutException:
#         print("The elements to show 50 live streams on page were not found.")
#         return

#     header = ['Live stream name', 'Number of products', 'Top 3 categories',
#        'Live stream time', 'Stream duration', 'Creator name', 'Revenue',
#        'Revenue per minute', 'Online viewers', 'Online viewers per minute',
#        'Views', 'Views per minute', 'Items sold', 'Items sold per minute',
#        'Average unit price']

#     with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
#         writer = csv.DictWriter(file, fieldnames=header)
#         writer.writeheader()

#         # Continue scraping until no more pages
#         while True:
#             # Find all live_streams
#             time.sleep(.5)
#             live_stream_rows = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr')

#             print(f"Total number of live streams found: {len(live_stream_rows)}")

#             original_window = driver.current_window_handle  # Store the current window handle

#             # Loop through each live_stream
#             for index, live_stream in enumerate(live_stream_rows[:50], start=1):
#                 count = count + 1
#                 if(count > 500):
#                     break
#                 print(f'processing live stream #{count}')

#                 try:
#                     # Re-locate the live stream element to avoid stale reference
#                     live_stream_rows = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr')
#                     live_stream = live_stream_rows[index]

#                     # Click on the live stream to open it in a new tab
#                     live_stream.click()

#                     # Wait for the new tab to open and switch to it
#                     WebDriverWait(driver, 10).until(EC.new_window_is_opened)
#                     new_tab = [window for window in driver.window_handles if window != original_window][0]
#                     driver.switch_to.window(new_tab)

#                     # Scrape the live_stream details
#                     live_stream_url = driver.current_url
#                     try:
#                         data = scrape_live_stream_details(driver, live_stream_url)
#                     except Exception as e:
#                         print(f"Error scraping live stream {count}: {e}")
#                         # Fill the row with "Not scraped" if there's an error
#                         data = {field: 'Not scraped' for field in header}

#                     # Write the details to CSV
#                     writer.writerow(data)

#                     driver.close()
#                     driver.switch_to.window(original_window)
          
#                 except StaleElementReferenceException:
#                     print(f"StaleElementReferenceException encountered for live stream #{count}. Retrying...")
#                     continue                    
                    
#             try:
#                 if(count < 500):
#                 # Try to find and click the 'Next Page' button with the first XPath
#                     next_button = WebDriverWait(driver, 1).until(
#                         EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/ul/li[9]/button'))
#                     )
#                     next_button.click()
#             except TimeoutException:
#                 print("First 'Next Page' button not found or not clickable.")
#                 try:
#                     # Try to find and click the 'Next Page' button with the second XPath
#                     next_button = WebDriverWait(driver, 1).until(
#                         EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/ul/li[10]/button'))
#                     )
#                     next_button.click()
#                 except TimeoutException:
#                     print("No more pages to scrape or 'Next Page' button not found.")
#                     try:
#                         # Try to find and click the 'Next Page' button with the second XPath
#                         next_button = WebDriverWait(driver, 1).until(
#                             EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/ul/li[11]/button'))
#                         )
#                         next_button.click()
#                     except TimeoutException:
#                         print("No more pages to scrape or 'Next Page' button not found.")
#                         break  # Exit the loop if neither button is found or clickable

#     print("\nFinished scraping all Live Streams.")

def scrape_live_streams(driver, url, output_csv):
    driver.get(url)
    count = 0
    max_streams = 500

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
        print("The elements to show 50 live streams on page were not found.")
        return

    header = [
        'Live stream name', 'Number of products', 'Top 3 categories',
        'Live stream time', 'Stream duration', 'Creator name', 'Revenue',
        'Revenue per minute', 'Online viewers', 'Online viewers per minute',
        'Views', 'Views per minute', 'Items sold', 'Items sold per minute',
        'Average unit price'
    ]

    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()

        while count < max_streams:
            # Find all live streams on the current page
            time.sleep(.5)
            live_stream_rows = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr')
            print(f"Total number of live streams found: {len(live_stream_rows)}")

            original_window = driver.current_window_handle

            for index in range(min(50, len(live_stream_rows))):
                count += 1
                if count > max_streams:
                    break
                print(f'Processing live stream #{count}')

                # Retry mechanism in case of StaleElementReferenceException
                max_retries = 2
                retries = 0
                success = False
                
                while retries < max_retries and not success:
                    try:
                        # Re-locate the live stream elements before clicking
                        live_stream_rows = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr')
                        live_stream = live_stream_rows[index]
                        live_stream.click()

                        WebDriverWait(driver, 10).until(EC.new_window_is_opened)
                        new_tab = [window for window in driver.window_handles if window != original_window][0]
                        driver.switch_to.window(new_tab)

                        live_stream_url = driver.current_url
                        try:
                            data = scrape_live_stream_details(driver, live_stream_url)
                        except Exception as e:
                            print(f"Error scraping live stream {count}: {e}")
                            data = {field: 'Not scraped' for field in header}

                        writer.writerow(data)

                        driver.close()
                        driver.switch_to.window(original_window)

                        success = True  # Mark success if scraping completes successfully

                    except StaleElementReferenceException:
                        retries += 1
                        print(f"StaleElementReferenceException encountered for live stream #{count}, retrying {retries}/{max_retries}...")
                        driver.refresh()  # Refresh the page in case of stale elements

                    except Exception as e:
                        retries += 1
                        print(f"Error processing live stream #{count}: {e}")
                        driver.refresh()  # Refresh the page in case of stale elements

                if not success:
                    print(f"Failed to process live stream #{count} after {max_retries} attempts.")

            if count >= max_streams:
                break

            try:
                if(count < 500):
                    # Try to find and click the 'Next Page' button with the first XPath
                    next_button = WebDriverWait(driver, 1).until(
                        EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/ul/li[9]/button'))
                    )
                    next_button.click()
                else:
                    break
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

    print("\nFinished scraping all Live Streams.")
