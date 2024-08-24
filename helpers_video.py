import csv
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
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
    print("\n\nStarted scraping video details\n\n")
    video_details = {}

    try:
        # Wait for key elements to be present (adjust the XPath as needed)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div/div[1]/div[1]/div'))
        )

        # Scrape each video detail field (replace <XPATH> with the actual XPaths)
        #video_details['video_id'] = driver.find_element(By.XPATH, '<XPATH_for_video_id>').text
        video_link_element = driver.find_element(By.CLASS_NAME, 'LayoutPageDetail-TikTokLink')
        svg_use_element = video_link_element.find_element(By.TAG_NAME, 'use')
        video_link = svg_use_element.get_attribute('xmlns:xlink')

# Store the link in the dictionary
        video_details['video_link'] = video_link
        #video_details['video_description'] = driver.find_element(By.XPATH, '<XPATH_for_video_description>').text
        video_details['video_tags'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div/div[2]/div[2]/div/div').text
        video_details['video_music_info'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div/div[3]/div[2]').text
        #video_details['revenue_entity_id'] = driver.find_element(By.XPATH, '<XPATH_for_revenue_entity_id>').text
        #video_details['video_revenue_entity_id'] = driver.find_element(By.XPATH, '<XPATH_for_video_revenue_entity_id>').text
        #video_details['item_sold_entity_id'] = driver.find_element(By.XPATH, '<XPATH_for_item_sold_entity_id>').text
        video_details['video_publish_date'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div/div[4]/div[2]').text
        video_details['video_duration'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div/div[4]/div[4]').text
        video_details['video_advertising_information'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div[2]/div/div[6]/div/div[2]/div/div').text
        video_details['video_earliest_date_recorded'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[2]/div[1]/span').text

        # Scrape view counts and followers over different periods
        time_periods = {
            'yesterday': '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[2]/div/div/div/div[2]/div/div[2]/div/label[1]/span[2]',
            'last_7_days': '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[2]/div/div/div/div[2]/div/div[2]/div/label[2]/span[2]',
            'last_30_days': '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[2]/div/div/div/div[2]/div/div[2]/div/label[3]/span[2]',
            'last_90_days': '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[2]/div/div/div/div[2]/div/div[2]/div/label[4]/span[2]',
            'last_180_days': '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[2]/div/div/div/div[2]/div/div[2]/div/label[5]/span[2]'
        }

        for period, xpath in time_periods.items():
            driver.find_element(By.XPATH, xpath).click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[4]/div/div[2]/div[1]/div/div[2]/div[1]/div[2]/div/div/div/div')))
            
            video_details[f'video_views_{period}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[4]/div/div[2]/div[1]/div/div[2]/div[1]/div[2]/div/div/div/div').text
            video_details[f'video_views_per_day_{period}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[4]/div/div[2]/div[1]/div/div[2]/div[1]/div[3]').text
            video_details[f'item_sold_{period}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[4]/div/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div').text
            video_details[f'item_sold_per_day_{period}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[4]/div/div[2]/div[1]/div/div[2]/div[2]/div[3]').text
            video_details[f'video_revenue_{period}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[4]/div/div[2]/div[1]/div/div[2]/div[3]/div[2]/div/div/div/div').text
            video_details[f'video_revenue_per_day_{period}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[4]/div/div[2]/div[1]/div/div[2]/div[3]/div[3]').text
            video_details[f'video_new_followers_{period}'] = driver.find_element(By.XPATH,  '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[4]/div/div[2]/div[1]/div/div[2]/div[4]/div[2]/div/div/div/div/span').text
            video_details[f'video_new_followers_per_day_{period}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[4]/div/div[2]/div[1]/div/div[2]/div[4]/div[3]').text
        
        # Scrape additional video metrics
            video_details[f'video_ad_view_ratio_{period}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[4]/div/div[2]/div[1]/div/div[4]/div[1]/div[2]/div/div/div/div').text
            video_details[f'video_ad_revenue_ratio_{period}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[4]/div/div[2]/div[1]/div/div[4]/div[2]/div[2]/div/div/div/div').text
            video_details[f'video_ad_spend_{period}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[4]/div/div[2]/div[1]/div/div[4]/div[3]/div[2]/div/div/div/div').text
            video_details[f'video_ad_roas_{period}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[4]/div/div[2]/div[1]/div/div[4]/div[4]/div[2]/div/div/div/div/span').text

    except NoSuchElementException as e:
        print(f"Error while scraping: {e}")

    # Write the details to CSV
    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(video_details.keys())
        writer.writerow(video_details.values())

    return video_details

# Example usage:
# driver = webdriver.Chrome()
# url = 'http://example.com/video-details'
# output_csv = 'video_details.csv'
# scrape_video_details(driver, url, output_csv)
# driver.quit()
