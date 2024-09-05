import csv
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, InvalidSessionIdException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC

def scrape_creator_details(driver, url):
    # driver.get(url)
    # print("\n\nstarted scraping creator details\n\n")
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

        driver.execute_script("window.scrollTo(0, 300);")
        
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
            details['creators in Last 30 Days'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div[3]/div/div[2]/div[3]/div').text
        except:
            details['creators in Last 30 Days'] = 'N/A'

        try:
            bio = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div[3]/div/div[2]').text
            if bio is None:
                details['Bio'] = "N/A"
            else:
                details['Bio'] = bio                
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
            email_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/div/a/div[2]/div/div')
            email_href = email_element.get_attribute('href')
            
            # Check if the email address is an empty string
            if email_href.strip() == '':
                details['Email address'] = 'N/A'
            else:
                details['Email address'] = email_href
        except:
            details['Email address'] = 'N/A'


        # Scrape data for each time range
        for range_name, range_xpath in time_ranges.items():
            try:
                driver.find_element(By.XPATH, range_xpath).click()
                # Wait for page content to update
                # Wait for the content to update after clicking
                try:
                    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div/div/div/div')))
                except:
                    driver.refresh()
                
                details[f'Revenue in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div/div/div/div').text
                details[f'Revenue per day in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[1]/div[2]/div[2]').text
                details[f'Live Revenue in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[2]/div[2]/div[1]/div/div/div/div').text
                details[f'Live Revenue per day in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[2]/div[2]/div[2]').text
                details[f'Video Revenue in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[3]/div[2]/div[1]/div/div/div/div').text
                details[f'Video Revenue per day in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[3]/div[2]/div[2]').text
                try:
                    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[4]/div[2]/div[1]/div/div/div/div')))
                except:
                    driver.refresh()
                    time.sleep(.5)
                details[f'Average unit price in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[4]/div[2]/div[1]/div/div/div/div').text
                details[f'Traffic live views in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[4]/div[1]/div[2]/div[1]/div/div/div/div').text
                details[f'Traffic live views per day in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[4]/div[1]/div[2]/div[2]').text
                details[f'Traffic video views in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[4]/div[2]/div[2]/div[1]/div/div/div/div').text
                details[f'Traffic video views per day in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[4]/div[2]/div[2]/div[2]').text
                details[f'New followers in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[4]/div[3]/div[2]/div[1]/div/div/div/div').text
                details[f'New followers per day in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[4]/div[3]/div[2]/div[2]').text
            except Exception as e:
                print(f"Error during scraping for range '{range_name}': {e}")
                continue
                

        # Write to CSV
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
        print(f"Error in scrape_creator_details: {e}")  

    return details         

# def scrape_creators(driver, url, output_csv):
#     # Visit the URL
#     driver.get(url)
#     count = 0

#     # Scroll to the bottom of the page to reveal more content
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#     # Click on the specified elements
#     try:
#         element_to_click1 = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/ul/li[10]/div'))
#         )
#         element_to_click1.click()

#         element_to_click2 = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/ul/li[10]/div/div[2]/div/div/div/div/div/div[3]/div'))
#         )
#         element_to_click2.click()

#     except TimeoutException:
#         print("The elements to show 50 creators on page were not found.")
#         return

#     header = ['Username', 'Number of Followers', 'Debut Time',
#        'creators in Last 30 Days', 'Bio', 'Earliest Date Recorded',
#        'Tiktok Link', 'Instagram Link', 'YouTube Link', 'Email address',
#        'Revenue in Yesterday', 'Revenue per day in Yesterday',
#        'Live Revenue in Yesterday', 'Live Revenue per day in Yesterday',
#        'Video Revenue in Yesterday', 'Video Revenue per day in Yesterday',
#        'Average unit price in Yesterday', 'Traffic live views in Yesterday',
#        'Traffic live views per day in Yesterday',
#        'Traffic video views in Yesterday',
#        'Traffic video views per day in Yesterday',
#        'New followers in Yesterday', 'New followers per day in Yesterday',
#        'Revenue in Last 7 Days', 'Revenue per day in Last 7 Days',
#        'Live Revenue in Last 7 Days', 'Live Revenue per day in Last 7 Days',
#        'Video Revenue in Last 7 Days', 'Video Revenue per day in Last 7 Days',
#        'Average unit price in Last 7 Days',
#        'Traffic live views in Last 7 Days',
#        'Traffic live views per day in Last 7 Days',
#        'Traffic video views in Last 7 Days',
#        'Traffic video views per day in Last 7 Days',
#        'New followers in Last 7 Days', 'New followers per day in Last 7 Days',
#        'Revenue in Last 30 Days', 'Revenue per day in Last 30 Days',
#        'Live Revenue in Last 30 Days', 'Live Revenue per day in Last 30 Days',
#        'Video Revenue in Last 30 Days',
#        'Video Revenue per day in Last 30 Days',
#        'Average unit price in Last 30 Days',
#        'Traffic live views in Last 30 Days',
#        'Traffic live views per day in Last 30 Days',
#        'Traffic video views in Last 30 Days',
#        'Traffic video views per day in Last 30 Days',
#        'New followers in Last 30 Days',
#        'New followers per day in Last 30 Days', 'Revenue in Last 90 Days',
#        'Revenue per day in Last 90 Days', 'Live Revenue in Last 90 Days',
#        'Live Revenue per day in Last 90 Days', 'Video Revenue in Last 90 Days',
#        'Video Revenue per day in Last 90 Days',
#        'Average unit price in Last 90 Days',
#        'Traffic live views in Last 90 Days',
#        'Traffic live views per day in Last 90 Days',
#        'Traffic video views in Last 90 Days',
#        'Traffic video views per day in Last 90 Days',
#        'New followers in Last 90 Days',
#        'New followers per day in Last 90 Days', 'Revenue in Last 180 Days',
#        'Revenue per day in Last 180 Days', 'Live Revenue in Last 180 Days',
#        'Live Revenue per day in Last 180 Days',
#        'Video Revenue in Last 180 Days',
#        'Video Revenue per day in Last 180 Days',
#        'Average unit price in Last 180 Days',
#        'Traffic live views in Last 180 Days',
#        'Traffic live views per day in Last 180 Days',
#        'Traffic video views in Last 180 Days',
#        'Traffic video views per day in Last 180 Days',
#        'New followers in Last 180 Days',
#        'New followers per day in Last 180 Days']

#     with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
#         writer = csv.DictWriter(file, fieldnames=header)
#         writer.writeheader()

#         # Continue scraping until no more pages
#         while True:   
#             # Find all creators
#             time.sleep(.5)
#             creator_rows = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr')
#             creator_rows = creator_rows[1:]  # Exclude the header row

#             print(f"Total number of creators found (excluding header): {len(creator_rows)}")

#             original_window = driver.current_window_handle  # Store the current window handle

#             # Loop through each creator
#             for index, creator in enumerate(creator_rows[:50], start=1):
#                 count = count + 1
#                 if(count > 500):
#                     break
#                 # print(f"\nProcessing creator {index}/{len(creator_rows)}")
#                 print(f'processing Creator #{count}')

#                 try:
#                     # Find the element again just before clicking
#                     creator = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr')[index]
#                     creator.click()

#                     WebDriverWait(driver, 10).until(EC.new_window_is_opened)
#                     new_tab = [window for window in driver.window_handles if window != original_window][0]
#                     driver.switch_to.window(new_tab)

#                     data = {field: 'Not scraped' for field in header}
#                     creator_url = driver.current_url
#                     scraped_data = scrape_creator_details(driver, creator_url)
#                     if scraped_data is not None:
#                         data.update(scraped_data)

#                     writer.writerow(data)

#                     driver.close()
#                     driver.switch_to.window(original_window)

#                 except StaleElementReferenceException:
#                     print(f"StaleElementReferenceException: Retrying for Creator #{count}")
#                     continue
#                 except Exception as e:
#                     print(f"Error processing Creator #{count}: {e}")

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

#     print("\nFinished scraping all creators.")

def scrape_creators(driver, url, output_csv):
    # Visit the URL
    driver.get(url)
    count = 0

    # Scroll to the bottom of the page to reveal more content
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Click on the specified elements
    try:
        element_to_click1 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/ul/li[10]/div'))
        )
        element_to_click1.click()
        time.sleep(.5)

        element_to_click2 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/ul/li[10]/div/div[2]/div/div/div/div/div/div[3]/div'))
        )
        element_to_click2.click()

    except TimeoutException:
        print("The elements to show 50 creators on page were not found.")
        return

    header = ['Username', 'Number of Followers', 'Debut Time',
       'creators in Last 30 Days', 'Bio', 'Earliest Date Recorded',
       'Tiktok Link', 'Instagram Link', 'YouTube Link', 'Email address',
       'Revenue in Yesterday', 'Revenue per day in Yesterday',
       'Live Revenue in Yesterday', 'Live Revenue per day in Yesterday',
       'Video Revenue in Yesterday', 'Video Revenue per day in Yesterday',
       'Average unit price in Yesterday', 'Traffic live views in Yesterday',
       'Traffic live views per day in Yesterday',
       'Traffic video views in Yesterday',
       'Traffic video views per day in Yesterday',
       'New followers in Yesterday', 'New followers per day in Yesterday',
       'Revenue in Last 7 Days', 'Revenue per day in Last 7 Days',
       'Live Revenue in Last 7 Days', 'Live Revenue per day in Last 7 Days',
       'Video Revenue in Last 7 Days', 'Video Revenue per day in Last 7 Days',
       'Average unit price in Last 7 Days',
       'Traffic live views in Last 7 Days',
       'Traffic live views per day in Last 7 Days',
       'Traffic video views in Last 7 Days',
       'Traffic video views per day in Last 7 Days',
       'New followers in Last 7 Days', 'New followers per day in Last 7 Days',
       'Revenue in Last 30 Days', 'Revenue per day in Last 30 Days',
       'Live Revenue in Last 30 Days', 'Live Revenue per day in Last 30 Days',
       'Video Revenue in Last 30 Days',
       'Video Revenue per day in Last 30 Days',
       'Average unit price in Last 30 Days',
       'Traffic live views in Last 30 Days',
       'Traffic live views per day in Last 30 Days',
       'Traffic video views in Last 30 Days',
       'Traffic video views per day in Last 30 Days',
       'New followers in Last 30 Days',
       'New followers per day in Last 30 Days', 'Revenue in Last 90 Days',
       'Revenue per day in Last 90 Days', 'Live Revenue in Last 90 Days',
       'Live Revenue per day in Last 90 Days', 'Video Revenue in Last 90 Days',
       'Video Revenue per day in Last 90 Days',
       'Average unit price in Last 90 Days',
       'Traffic live views in Last 90 Days',
       'Traffic live views per day in Last 90 Days',
       'Traffic video views in Last 90 Days',
       'Traffic video views per day in Last 90 Days',
       'New followers in Last 90 Days',
       'New followers per day in Last 90 Days', 'Revenue in Last 180 Days',
       'Revenue per day in Last 180 Days', 'Live Revenue in Last 180 Days',
       'Live Revenue per day in Last 180 Days',
       'Video Revenue in Last 180 Days',
       'Video Revenue per day in Last 180 Days',
       'Average unit price in Last 180 Days',
       'Traffic live views in Last 180 Days',
       'Traffic live views per day in Last 180 Days',
       'Traffic video views in Last 180 Days',
       'Traffic video views per day in Last 180 Days',
       'New followers in Last 180 Days',
       'New followers per day in Last 180 Days']

    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()

        # Continue scraping until no more pages
        while True:   
            # Find all creators
            time.sleep(.5)
            creator_rows = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr')
            creator_rows = creator_rows[1:]  # Exclude the header row

            print(f"Total number of creators found (excluding header): {len(creator_rows)}")

            original_window = driver.current_window_handle  # Store the current window handle

            # Loop through each creator
            for index, creator in enumerate(creator_rows[:50], start=1):
                count = count + 1
                if count > 500:
                    break
                print(f'Processing Creator #{count}')

                max_retries = 2
                retries = 0
                success = False

                while retries < max_retries and not success:
                    try:
                        # Re-locate the creator element before clicking
                        creator = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr')[index]
                        creator.click()

                        WebDriverWait(driver, 10).until(EC.new_window_is_opened)
                        new_tab = [window for window in driver.window_handles if window != original_window][0]
                        driver.switch_to.window(new_tab)

                        data = {field: 'Not scraped' for field in header}
                        creator_url = driver.current_url
                        scraped_data = scrape_creator_details(driver, creator_url)
                        if scraped_data is not None:
                            data.update(scraped_data)

                        writer.writerow(data)

                        driver.close()
                        driver.switch_to.window(original_window)
                        success = True  # Mark success if everything goes well

                    except StaleElementReferenceException:
                        retries += 1
                        print(f"StaleElementReferenceException: Retrying for Creator #{count}, attempt {retries}/{max_retries}")
                        driver.refresh()  # Refresh the page to avoid stale elements

                    except Exception as e:
                        print(f"Error processing Creator #{count}: {e}")
                        break  # Break the retry loop for any other exception

                if not success:
                    print(f"Failed to process Creator #{count} after {max_retries} attempts")

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
                    
    print("\nFinished scraping all creators.")