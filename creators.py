import csv
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, InvalidSessionIdException, TimeoutException, StaleElementReferenceException

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
            # Try to locate the 'Independent' account type
            details['Account Type'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div[2]/div[1]/span').text
            details['Account Type'] = "Independent"
            details['Creator Shop Name'] = "N/A"
        except:
            # Fallback if not 'Independent', assume 'Seller operated'
            details['Account Type'] = 'Seller operated'
            try:
                # Try to find the creator shop name
                details['Creator Shop Name'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div[2]/div/div/div/span').text
                details['Account Type'] = "Seller Operated"  # Update account type if creator shop is found
            except:
                # If creator shop name not found, set defaults
                details['Account Type'] = 'Independent'
                details['Creator Shop Name'] = "N/A"

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
            # print(f'Bio is "{bio}"')
            if bio.strip() == '':
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
            # email_href = email_element.get_attribute('href')
            email = email_element.text
            
            # Check if the email address is an empty string
            if email.strip() == '':
                details['Email address'] = 'N/A'
            else:
                details['Email address'] = email
        except:
            details['Email address'] = 'N/A'


        # # Scrape data for each time range
        # for range_name, range_xpath in time_ranges.items():
        #     try:
        #         driver.find_element(By.XPATH, range_xpath).click()
        #         # Wait for page content to update
        #         # Wait for the content to update after clicking
        #         try:
        #             WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div/div/div/div')))
        #         except:
        #             driver.refresh()
        #             time.sleep(1)
                
        #         details[f'Revenue in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div/div/div/div').text
        #         details[f'Revenue per day in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[1]/div[2]/div[2]').text
        #         details[f'Live Revenue in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[2]/div[2]/div[1]/div/div/div/div').text
        #         details[f'Live Revenue per day in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[2]/div[2]/div[2]').text
        #         details[f'Video Revenue in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[3]/div[2]/div[1]/div/div/div/div').text
        #         details[f'Video Revenue per day in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[3]/div[2]/div[2]').text
        #         try:
        #             WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[4]/div[2]/div[1]/div/div/div/div')))
        #         except:
        #             driver.refresh()
        #             time.sleep(1)
        #         details[f'Average unit price in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[4]/div[2]/div[1]/div/div/div/div').text
        #         details[f'Traffic live views in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[4]/div[1]/div[2]/div[1]/div/div/div/div').text
        #         details[f'Traffic live views per day in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[4]/div[1]/div[2]/div[2]').text
        #         details[f'Traffic video views in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[4]/div[2]/div[2]/div[1]/div/div/div/div').text
        #         details[f'Traffic video views per day in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[4]/div[2]/div[2]/div[2]').text
        #         details[f'New followers in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[4]/div[3]/div[2]/div[1]/div/div/div/div').text
        #         details[f'New followers per day in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[4]/div[3]/div[2]/div[2]').text
        #     except Exception as e:
        #         print(f"Error during scraping for range '{range_name}': {e}")
        #         continue
                
        for range_name, range_xpath in time_ranges.items():
            retry_count = 0
            max_retries = 2  # Set the maximum number of retries

            while retry_count < max_retries:
                try:
                    driver.find_element(By.XPATH, range_xpath).click()
                    
                    # Wait for the content to update after clicking
                    try:
                        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div/div/div/div')))
                    except TimeoutException as e:
                        time.sleep(10)
                        driver.refresh()
                        time.sleep(3)

                    # Scrape the required details
                    details[f'Revenue in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div/div/div/div').text
                    details[f'Revenue per day in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[1]/div[2]/div[2]').text
                    details[f'Live Revenue in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[2]/div[2]/div[1]/div/div/div/div').text
                    details[f'Live Revenue per day in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[2]/div[2]/div[2]').text
                    details[f'Video Revenue in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[3]/div[2]/div[1]/div/div/div/div').text
                    details[f'Video Revenue per day in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[3]/div[2]/div[2]').text

                    try:
                        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[4]/div[2]/div[1]/div/div/div/div')))
                    except:
                        time.sleep(10)
                        driver.refresh()
                        time.sleep(3)
                    
                    # More scraping as required (e.g. Average unit price, Traffic live views, etc.)
                    details[f'Average unit price in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[4]/div[2]/div[1]/div/div/div/div').text
                    details[f'Traffic live views in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[4]/div[1]/div[2]/div[1]/div/div/div/div').text
                    details[f'Traffic live views per day in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[4]/div[1]/div[2]/div[2]').text
                    details[f'Traffic video views in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[4]/div[2]/div[2]/div[1]/div/div/div/div').text
                    details[f'Traffic video views per day in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[4]/div[2]/div[2]/div[2]').text
                    details[f'New followers in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[4]/div[3]/div[2]/div[1]/div/div/div/div').text
                    details[f'New followers per day in {range_name}'] = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[4]/div[3]/div[2]/div[2]').text
                    
                    # If successful, break out of the retry loop
                    break
                
                except Exception as e:
                    retry_count += 1
                    # print(f"Error during scraping for range '{range_name}', retry number{retry_count}.")
                    if retry_count < max_retries:
                        time.sleep(30)
                        driver.refresh()  # Refresh page and retry
                        time.sleep(5)

                        # time.sleep(120)  # Small delay to allow the page to reload
                        # try:
                        #     WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div/div/div/div')))
                        # except:
                        #     driver.refresh()
                        #     time.sleep(2)
                    else:
                        print(f"Failed to scrape data for range '{range_name}' after {max_retries} retries.")             
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

def scrape_creators(driver, url, output_csv):
    # Visit the URL
    driver.get(url)
    count = 0

    # Scroll to the bottom of the page to reveal more content
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    max_retries_elements = 2
    element_retries = 0

    # Click on the specified elements to show more creators (adjust these based on your page behavior)
    while element_retries < max_retries_elements:
        try:
            element_to_click1 = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/ul/li[10]/div'))
            )
            element_to_click1.click()
            time.sleep(1)
            break  # Break the loop if click succeeds
        except TimeoutException:
            element_retries += 1
            # print(f"Retrying click for the first element (Attempt {element_retries}/{max_retries_elements})")
            time.sleep(2)

    if element_retries == max_retries_elements:
        print("The elements to show 50 creators on page were not found.")
    else:
        element_retries = 0  # Reset retry counter for the next element

        # Retry for the second element
        while element_retries < max_retries_elements:
            try:
                element_to_click2 = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/ul/li[10]/div/div[2]/div/div/div/div/div/div[3]/div'))
                )
                element_to_click2.click()
                break  # Break the loop if click succeeds
            except TimeoutException:
                element_retries += 1
                print(f"Retrying click for the second element (Attempt {element_retries}/{max_retries_elements})")
                time.sleep(2)

        if element_retries == max_retries_elements:
            print("The elements to show 50 creators on page were not found.")
        # else:
        #     print("buttons clicked!")

    header = ['Username', 'Number of Followers', 'Debut Time',
       'creators in Last 30 Days', 'Bio', 'Earliest Date Recorded',
       'Tiktok Link', 'Instagram Link', 'YouTube Link', 'Email address',
       'Creator Shop Name', 'Account Type',
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
            time.sleep(1)
            creator_rows = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[1]/div/table/tbody/tr')
            creator_rows = creator_rows[1:]  # Exclude the header row

            # print(f"Total number of creators found (excluding header): {len(creator_rows)}")

            original_window = driver.current_window_handle  # Store the current window handle

            # Loop through each creator
            for index, creator in enumerate(creator_rows[:50], start=1):
                count += 1
                if count >  100:
                    break
                # print(f'Processing Creator #{count}')

                max_retries = 2
                retries = 0
                success = False

                while retries < max_retries and not success:
                    try:
                        creator = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[1]/div/table/tbody/tr')[index]
                        ActionChains(driver).move_to_element_with_offset(creator, 75, 40).click().perform()
                        # size = creator.size
                        # print(f"Width: {size['width']} px, Height: {size['height']} px")
                        # time.sleep(30)
                        # creator.click()

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
                        success = True

                    except StaleElementReferenceException:
                        retries += 1
                        # print(f"Stale Element Reference Exception: Retrying for Creator #{count}, attempt {retries}/{max_retries}")
                        driver.refresh()
                        time.sleep(2)

                    except TimeoutException:
                        retries += 1
                        # print(f"TimeoutException for Creator #{count}: Retrying {retries}/{max_retries}")
                        driver.refresh()      
                        time.sleep(2)                  

                    except Exception as e:
                        retries += 1
                        # print(f"Error processing Creator #{count}: {e}")
                        driver.refresh()
                        time.sleep(2)

                if not success:
                    print(f"Failed to process Creator #{count} after {max_retries} attempts")

            # Next page retry mechanism
            next_page_found = False
            retry_attempts = 1

            while retry_attempts > 0 and not next_page_found:
                for i in range(9, 12):  # Check for 'li[9]' to 'li[99]' dynamically
                    try:
                        if count < 100:
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

                # Retry logic: refresh the page and try again if no button found
                if not next_page_found:
                    # print(f"Retrying page refresh... Remaining attempts: {retry_attempts - 1}")
                    retry_attempts -= 1
                    driver.refresh()
                    time.sleep(2)  # Allow time for the page to reload

            if not next_page_found:
                # print("No more pages to scrape or buttons not found.")
                break  # Exit the outer loop if no next button is found even after retries

    print("\nFinished scraping all creators.")