
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





def scrape_shop_details(driver, url, output_csv):
    driver.get(url)
    print("\n\nStarted scraping\n\n")
    details = {}

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[2]/div[1]/div[1]')))
        details['shop_name'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[2]/div[1]/div[1]').text
        details['shop_type'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[2]/div[2]/div/span').text
        details['shop_earliest_date_recorded'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[2]/div[1]/span').text

        # # Revenue and metrics XPaths
        # details['revenue_entity_id'] = driver.find_element(By.XPATH, '//*[@id="revenue-entity-id"]').text
        # details['avg_unit_price'] = driver.find_element(By.XPATH, '//*[@id="avg-unit-price-entity-id"]').text
        # details['item_sold_entity_id'] = driver.find_element(By.XPATH, '//*[@id="item-sold-entity-id"]').text
        # details['mall_revenue_entity_id'] = driver.find_element(By.XPATH, '//*[@id="mall-revenue-entity-id"]').text

        # Revenue for different periods
        time_ranges = {
            'Yesterday': '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/label[1]/span[2]',
            'Last 7 Days': '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/label[2]/span[2]',
            'Last 30 Days': '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/label[3]/span[2]',
            'Last 90 Days': '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/label[4]/span[2]',
            'Last 180 Days': '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/label[5]/span[2]'
        }
        for range_name, range_xpath in time_ranges.items():
            driver.find_element(By.XPATH, range_xpath).click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[1]/div[1]/div[2]/div/div/div/div')))

            # Scrape SOA revenue metrics
            details[f'shop_soa_revenue_{range_name}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[1]/div[1]/div[2]/div/div/div/div').text
            details[f'shop_soa_revenue_per_day_{range_name}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[1]/div[1]/div[3]').text

            # Scrape affiliate revenue metrics
            details[f'shop_affiliate_revenue_{range_name}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[1]/div[2]/div/div/div/div').text
            details[f'shop_affiliate_revenue_per_day_{range_name}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[1]/div[3]').text

            # # Scrape SOA revenue share metrics
            details[f'shop_soa_revenue_share_{range_name}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[4]/div[2]/div[1]/div/div/div/div[3]/div[2]/div/div/div[3]/div[1]/div/div[1]/div/div[2]/span[2]').text
            details[f'shop_aff_revenue_share_{range_name}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[4]/div[2]/div[1]/div/div/div/div[3]/div[2]/div/div/div[3]/div[1]/div/div[2]/div/div[2]/span[2]').text
            details[f'shop_mall_revenue_share_{range_name}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[4]/div[2]/div[1]/div/div/div/div[3]/div[2]/div/div/div[3]/div[3]/div/div/div[2]/span[2]').text
    except NoSuchElementException as e:
        print(f"Error while scraping: {e}")

    # Write the details to CSV
    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(details.keys())
        writer.writerow(details.values())

    return details
