import csv
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException,StaleElementReferenceException
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def attempt_login(driver):
    driver.get('https://kalodata.com/login')

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'register_email')))
    
    email_input = driver.find_element(By.ID, 'register_email')
    email_input.send_keys('info@ejex.co.uk')

    password_input = driver.find_element(By.ID, 'register_password')
    password_input.send_keys('111222333Pp!@#')

    login_button = driver.find_element(By.XPATH, '//button[@type="submit" and contains(@class, "login_submit-btn")]')
    login_button.click()

def scrape_video_details(driver, url, output_csv):
    # Load the webpage
    driver.get(url)
    #print("\n\nStarted scraping video details\n\n")
    video_details = {}

    try:
        # Wait for key elements to be present (adjust the XPath as needed)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div/div[1]/div[1]/div'))
        )
        try:
            video_details['video_title'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div/div[1]/div[1]/div').text
        
        except NoSuchElementException:
             video_details['video_title'] = "N/A"

        try:
            video_details['video_tags'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div/div[2]/div[2]/div/div').text
        except NoSuchElementException:
            video_details['video_tags'] = "N/A"


        if video_details['video_tags']=="N/A":
           video_details['video_music_info']=driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div/div[2]/div[2]').text
           video_details['video_duration']=driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div/div[3]/div[4]').text 
           video_details['video_publish_date']=driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div/div[3]/div[2]').text
           video_details['video_advertising_information']=driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div/div[5]/div/div[2]/div/div').text
           

        else:
            try:
                video_details['video_music_info'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div/div[3]/div[2]').text
            except NoSuchElementException:
                video_details['video_music_info'] = "N/A"

            try:
                video_details['video_publish_date'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div/div[4]/div[2]').text
            except NoSuchElementException:
                video_details['video_publish_date'] = "N/A"

            try:
                video_details['video_duration'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div/div[4]/div[4]').text
            except NoSuchElementException:
                video_details['video_duration'] = "N/A"

            try:
                video_details['video_advertising_information'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div/div[6]/div/div[2]/div/div').text
            except NoSuchElementException:
                video_details['video_advertising_information'] = "N/A"    

        try:
            video_details['video_creator'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]').text
        except NoSuchElementException:
            video_details['video_creator'] = "N/A"


        try:
            video_details['video_product_name'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[3]/div/div/div[2]/div/div[2]/div/div[2]/div[1]/div/div').text
        except NoSuchElementException:
            video_details['video_product_name'] = "N/A"        

        # try:
        #     video_details['video_advertising_information'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div/div[6]/div/div[2]/div/div').text
        # except NoSuchElementException:
        #     video_details['video_advertising_information'] = "N/A"

        try:
            video_details['video_earliest_date_recorded'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[2]/div[1]/span').text
        except NoSuchElementException:
            video_details['video_earliest_date_recorded'] = "N/A"

        # Scrape view counts and followers over different periods
        time_periods = {
            'yesterday': '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[2]/div/div/div/div[2]/div/div[2]/div/label[1]/span[2]',
            'last_7_days': '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[2]/div/div/div/div[2]/div/div[2]/div/label[2]/span[2]',
            'last_30_days': '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[2]/div/div/div/div[2]/div/div[2]/div/label[3]/span[2]',
            'last_90_days': '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[2]/div/div/div/div[2]/div/div[2]/div/label[4]/span[2]',
            'last_180_days': '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[2]/div/div/div/div[2]/div/div[2]/div/label[5]/span[2]'
        }

        for period, xpath in time_periods.items():
            try:
                driver.find_element(By.XPATH, xpath).click()
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[4]/div/div[2]/div[1]/div/div[2]/div[1]/div[2]/div/div/div/div'))
                )

                video_details[f'video_views_{period}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[4]/div/div[2]/div[1]/div/div[2]/div[1]/div[2]/div/div/div/div').text
            except NoSuchElementException:
                video_details[f'video_views_{period}'] = "N/A"

            try:
                video_details[f'video_views_per_day_{period}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[4]/div/div[2]/div[1]/div/div[2]/div[1]/div[2]/div[2]').text
            except NoSuchElementException:
                video_details[f'video_views_per_day_{period}'] = "N/A"

            try:
                video_details[f'item_sold_{period}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[4]/div/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div').text
            except NoSuchElementException:
                video_details[f'item_sold_{period}'] = "N/A"

            try:
                video_details[f'item_sold_per_day_{period}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[4]/div/div[2]/div[1]/div/div[2]/div[2]/div[2]/div[2]').text
            except NoSuchElementException:
                video_details[f'item_sold_per_day_{period}'] = "N/A"

            try:
                video_details[f'video_revenue_{period}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[4]/div/div[2]/div[1]/div/div[2]/div[3]/div[2]/div/div/div/div').text
            except NoSuchElementException:
                video_details[f'video_revenue_{period}'] = "N/A"

            try:
                video_details[f'video_revenue_per_day_{period}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[4]/div/div[2]/div[1]/div/div[2]/div[3]/div[2]/div[2]').text
            except NoSuchElementException:
                video_details[f'video_revenue_per_day_{period}'] = "N/A"

            try:
                video_details[f'video_new_followers_{period}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[4]/div/div[2]/div[1]/div/div[2]/div[4]/div[2]/div[1]/div/div/div/div').text
            except NoSuchElementException:
                video_details[f'video_new_followers_{period}'] = "N/A"

            try:
                video_details[f'video_new_followers_per_day_{period}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[4]/div/div[2]/div[1]/div/div[2]/div[4]/div[2]/div[2]').text
            except NoSuchElementException:
                video_details[f'video_new_followers_per_day_{period}'] = "N/A"

            # Scrape additional video metrics
            try:
                video_details[f'video_ad_view_ratio_{period}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[4]/div/div[2]/div[1]/div/div[4]/div[1]/div[2]/div/div/div/div').text
            except NoSuchElementException:
                video_details[f'video_ad_view_ratio_{period}'] = "N/A"

            try:
                video_details[f'video_ad_revenue_ratio_{period}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[4]/div/div[2]/div[1]/div/div[4]/div[2]/div[2]/div/div/div/div').text
            except NoSuchElementException:
                video_details[f'video_ad_revenue_ratio_{period}'] = "N/A"

            try:
                video_details[f'video_ad_spend_{period}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[4]/div/div[2]/div[1]/div/div[4]/div[3]/div[2]/div/div/div/div').text
            except NoSuchElementException:
                video_details[f'video_ad_spend_{period}'] = "N/A"

            try:
                video_details[f'video_ad_roas_{period}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[4]/div/div[2]/div[1]/div/div[4]/div[4]/div[2]/div/div/div/div/div/span').text
            except NoSuchElementException:
                video_details[f'video_ad_roas_{period}'] = "N/A"

    except Exception as e:
        print(f"Error while scraping: {e}")


    return video_details




def scrape_video(driver, url, output_csv):
    # Visit the URL
    driver.get(url)
    count = 0
    page_number=0

    # Scroll to the bottom of the page to reveal more content
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

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

        # WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div[2]/div[2]/div/div[1]/div/div/div/div[1]/div/table/tbody'))
        # )

    except TimeoutException:
        print("The elements to show 50 video on page were not found.")
        return

    header = ['video_title', 'video_tags', 'video_music_info', 'video_publish_date', 'video_duration','video_creator','video_product_name','video_advertising_information', 'video_earliest_date_recorded',
              'video_views_yesterday', 'video_views_per_day_yesterday', 'item_sold_yesterday', 'item_sold_per_day_yesterday', 'video_revenue_yesterday', 'video_revenue_per_day_yesterday',
              'video_new_followers_yesterday', 'video_new_followers_per_day_yesterday', 'video_ad_view_ratio_yesterday', 'video_ad_revenue_ratio_yesterday', 'video_ad_spend_yesterday',
              'video_ad_roas_yesterday', 'video_views_last_7_days', 'video_views_per_day_last_7_days', 'item_sold_last_7_days', 'item_sold_per_day_last_7_days',
              'video_revenue_last_7_days', 'video_revenue_per_day_last_7_days', 'video_new_followers_last_7_days', 'video_new_followers_per_day_last_7_days', 'video_ad_view_ratio_last_7_days',
              'video_ad_revenue_ratio_last_7_days', 'video_ad_spend_last_7_days', 'video_ad_roas_last_7_days', 'video_views_last_30_days', 'video_views_per_day_last_30_days',
              'item_sold_last_30_days', 'item_sold_per_day_last_30_days', 'video_revenue_last_30_days', 'video_revenue_per_day_last_30_days', 'video_new_followers_last_30_days',
              'video_new_followers_per_day_last_30_days', 'video_ad_view_ratio_last_30_days', 'video_ad_revenue_ratio_last_30_days', 'video_ad_spend_last_30_days', 'video_ad_roas_last_30_days',
              'video_views_last_90_days', 'video_views_per_day_last_90_days', 'item_sold_last_90_days', 'item_sold_per_day_last_90_days', 'video_revenue_last_90_days',
              'video_revenue_per_day_last_90_days', 'video_new_followers_last_90_days', 'video_new_followers_per_day_last_90_days', 'video_ad_view_ratio_last_90_days',
              'video_ad_revenue_ratio_last_90_days', 'video_ad_spend_last_90_days', 'video_ad_roas_last_90_days', 'video_views_last_180_days', 'video_views_per_day_last_180_days',
              'item_sold_last_180_days', 'item_sold_per_day_last_180_days', 'video_revenue_last_180_days', 'video_revenue_per_day_last_180_days', 'video_new_followers_last_180_days',
              'video_new_followers_per_day_last_180_days', 'video_ad_view_ratio_last_180_days', 'video_ad_revenue_ratio_last_180_days', 'video_ad_spend_last_180_days', 'video_ad_roas_last_180_days']

    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()

        # Continue scraping until no more pages
        while True:
            # Find all video
            time.sleep(0.5)
            video_rows = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[1]/div/table/tbody/tr')
            video_rows = video_rows[1:]  # Exclude the header row
            # print(f"Total number of videos found (excluding header): {len(video_rows)}")


            original_window = driver.current_window_handle  # Store the current window handle

            # Loop through each video
            for index, video in enumerate(video_rows, start=1):
                # count += 1
                # if count >  100:
                #     break
                #print(f'Processing video: {count}')
                # Wait for the spinner to disappear before clicking the video product row
                try:
                 # Wait for the spinner to disappear
                     WebDriverWait(driver, 10).until(
                     EC.invisibility_of_element_located((By.CLASS_NAME, 'ant-spin-spinning'))
                    )
                except TimeoutException:
                    print("Spinner took too long to disappear.")
        

                # Click on the product to open in a new tab
                try:
                    video.click()
                except StaleElementReferenceException:
                    print(f"Stale element at video {count}, trying to re-locate and click.")
                    # Re-locate the product and click again
                    video_rows = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[1]/div/table/tbody')
                    video_rows = video_rows[1:]
                    video = video_rows[index - 1]  # Re-fetch the element
                    video.click()

                # Wait for the new tab to open and switch to it
                WebDriverWait(driver, 10).until(EC.new_window_is_opened)
                new_tab = [window for window in driver.window_handles if window != original_window][0]
                driver.switch_to.window(new_tab)

                # Scrape the video details
                video_url = driver.current_url
                try:
                    data = scrape_video_details(driver, video_url, output_csv)
                except Exception as e:
                    print(f"Error scraping video {count}: {e}")
                    # Fill the row with "Not scraped" if there's an error
                    data = {field: 'Not scraped' for field in header}

                # Write the details to CSV
                writer.writerow(data)

                # Close the current tab and switch back to the original tab
                driver.close()
                driver.switch_to.window(original_window)

            try:
                # if count >  100:
                #     break
                page_number += 1
                next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//li[@title='Next Page' and @class='ant-pagination-next']/button"))
                )
                next_button.click()
            except TimeoutException:
                print(f"No more pages to scrape or 'Next Page' button not found on page {page_number}.")
                break  # Exit the loop if no more pages are found
            # Try to find and click the 'Next Page' button
            # try:
            #     page_number=page_number+1
            #     next_button = WebDriverWait(driver, 10).until(
            #         EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/ul/li[9]/button'))
            #     )
            #     next_button.click()
            # except TimeoutException:
            #     print(f"First 'Next Page' button not found or not clickable.",page_number)
            #     try:
            #         next_button = WebDriverWait(driver, 10).until(
            #             EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/ul/li[10]/button'))
            #         )
            #         next_button.click()
            #     except TimeoutException:
            #         print(f"No more pages to scrape or 'Next Page' button not found.",page_number)
            #         try:
            #             next_button = WebDriverWait(driver, 10).until(
            #             EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/ul/li[11]/button'))
            #         )
            #             next_button.click()
            #         except TimeoutException:
            #             print(f"No more pages to scrape or 'Next Page' button not found.  exc2",page_number)    
            #             break  # Exit the loop if neither button is found or clickable

    print("\nFinished scraping all videos.")

