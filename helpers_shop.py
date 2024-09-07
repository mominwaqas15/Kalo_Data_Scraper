
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
from selenium.webdriver.common.action_chains import ActionChains


def attempt_login(driver):
    driver.get('https://kalodata.com/login')

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'register_email')))
    
    email_input = driver.find_element(By.ID, 'register_email')
    email_input.send_keys('info@ejex.co.uk')

    password_input = driver.find_element(By.ID, 'register_password')
    password_input.send_keys('111222333Pp!@#')

    login_button = driver.find_element(By.XPATH, '//button[@type="submit" and contains(@class, "login_submit-btn")]')
    login_button.click()





def scrape_shop_details(driver, url):
    driver.get(url)
    print("\n\nStarted scraping\n\n")
    details = {}

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[2]/div[1]/div[1]'))
        )

        # Shop name
        try:
            details['shop_name'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[2]/div[1]/div[1]').text
        except NoSuchElementException:
            details['shop_name'] = "N/A"

        # Shop type
        try:
            details['shop_type'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[2]/div[2]/div/span').text
        except NoSuchElementException:
            details['shop_type'] = "N/A"

        # Shop earliest date recorded
        try:
            details['shop_earliest_date_recorded'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[2]/div[1]/span').text
        except NoSuchElementException:
            details['shop_earliest_date_recorded'] = "N/A"

        # Revenue for different periods
        time_ranges = {
            'Yesterday': '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/label[1]/span[2]',
            'Last 7 Days': '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/label[2]/span[2]',
            'Last 30 Days': '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/label[3]/span[2]',
            'Last 90 Days': '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/label[4]/span[2]',
            'Last 180 Days': '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/div/label[5]/span[2]'
        }

        for range_name, range_xpath in time_ranges.items():
            try:
                driver.find_element(By.XPATH, range_xpath).click()
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[1]/div[1]/div[2]/div/div/div/div'))
                )
            except NoSuchElementException:
                continue  # If clicking the time range fails, skip to the next range

            # SOA revenue
            try:
                details[f'shop_soa_revenue_{range_name}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[1]/div[1]/div[2]/div/div/div/div').text
            except NoSuchElementException:
                details[f'shop_soa_revenue_{range_name}'] = "N/A"

            # SOA revenue per day
            try:
                details[f'shop_soa_revenue_per_day_{range_name}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[1]/div[3]/div[2]/div[2]').text
            except NoSuchElementException:
                details[f'shop_soa_revenue_per_day_{range_name}'] = "N/A"

            # Affiliate revenue
            try:
                details[f'shop_affiliate_revenue_{range_name}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[1]/div[2]/div/div/div/div').text
            except NoSuchElementException:
                details[f'shop_affiliate_revenue_{range_name}'] = "N/A"

            # Affiliate revenue per day
            try:
                details[f'shop_affiliate_revenue_per_day_{range_name}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[1]/div[2]/div[2]').text
            except NoSuchElementException:
                details[f'shop_affiliate_revenue_per_day_{range_name}'] = "N/A"

            # SOA revenue share
            try:
                details[f'shop_soa_revenue_share_{range_name}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[4]/div[2]/div[1]/div/div/div/div[3]/div[2]/div/div/div[3]/div[1]/div/div[1]/div/div[2]/span[2]').text
            except NoSuchElementException:
                details[f'shop_soa_revenue_share_{range_name}'] = "N/A"

            # Affiliate revenue share
            try:
                details[f'shop_aff_revenue_share_{range_name}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[4]/div[2]/div[1]/div/div/div/div[3]/div[2]/div/div/div[3]/div[1]/div/div[2]/div/div[2]/span[2]').text
            except NoSuchElementException:
                details[f'shop_aff_revenue_share_{range_name}'] = "N/A"

            # Mall revenue share
            try:
                details[f'shop_mall_revenue_share_{range_name}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[4]/div[2]/div[1]/div/div/div/div[3]/div[2]/div/div/div[3]/div[3]/div/div/div[2]/span[2]').text
            except NoSuchElementException:
                details[f'shop_mall_revenue_share_{range_name}'] = "N/A"

    except NoSuchElementException as e:
        print(f"Error while scraping: {e}")

    return details



def scrape_500_shop(driver, url, output_csv):
    # Visit the URL
    driver.get(url)
    count = 0

    # Scroll to the bottom of the page to reveal more content
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # time.sleep(1)  # Give time for content to load

    # Click on the specified elements
    try:
        print('scrol')
        element_to_click1 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/ul/li[10]/div'))
        )
        element_to_click1.click()
        print('10 pege')

        element_to_click2 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/ul/li[10]/div/div[2]/div/div/div/div/div/div[3]/div'))
        )
        element_to_click2.click()
        print('50 page')

    except TimeoutException:
        print("The elements to show 50 shop on page were not found.")
        return

    header = ['shop_name','shop_type','shop_earliest_date_recorded','shop_soa_revenue_Yesterday','shop_soa_revenue_per_day_Yesterday','shop_affiliate_revenue_Yesterday','shop_affiliate_revenue_per_day_Yesterday','shop_soa_revenue_share_Yesterday','shop_aff_revenue_share_Yesterday','shop_mall_revenue_share_Yesterday','shop_soa_revenue_Last 7 Days','shop_soa_revenue_per_day_Last 7 Days','shop_affiliate_revenue_Last 7 Days','shop_affiliate_revenue_per_day_Last 7 Days','shop_soa_revenue_share_Last 7 Days','shop_aff_revenue_share_Last 7 Days','shop_mall_revenue_share_Last 7 Days','shop_soa_revenue_Last 30 Days','shop_soa_revenue_per_day_Last 30 Days','shop_affiliate_revenue_Last 30 Days','shop_affiliate_revenue_per_day_Last 30 Days','shop_soa_revenue_share_Last 30 Days','shop_aff_revenue_share_Last 30 Days','shop_mall_revenue_share_Last 30 Days','shop_soa_revenue_Last 90 Days','shop_soa_revenue_per_day_Last 90 Days','shop_affiliate_revenue_Last 90 Days','shop_affiliate_revenue_per_day_Last 90 Days','shop_soa_revenue_share_Last 90 Days','shop_aff_revenue_share_Last 90 Days','shop_mall_revenue_share_Last 90 Days','shop_soa_revenue_Last 180 Days','shop_soa_revenue_per_day_Last 180 Days','shop_affiliate_revenue_Last 180 Days','shop_affiliate_revenue_per_day_Last 180 Days','shop_soa_revenue_share_Last 180 Days','shop_aff_revenue_share_Last 180 Days','shop_mall_revenue_share_Last 180 Days']

    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()

        # Continue scraping until no more pages
        while True:
            # Find all shop
            time.sleep(.5)
            
            shop_rows = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr/td[2]')
            
            shop_rows = shop_rows[1:]  # Exclude the header row

            print(f"Total number of shop found (excluding header): {len(shop_rows)}")

            original_window = driver.current_window_handle  # Store the current window handle

            # Loop through each shop
            for index, product in enumerate(shop_rows[:50], start=1):
                count = count + 1
                if(count > 500):
                    break
                # print(f"\nProcessing product {index}/{len(product_rows)}")
                print(f'processing shop: {count}')
                try:
                    product.click()

                except StaleElementReferenceException:
                    print(f"Stale element at video {count}, trying to re-locate and click.")
                    # Re-locate the product and click again
                    video_rows = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr')
                    video_rows = video_rows[1:]
                    product = video_rows[index - 1]  # Re-fetch the element
                    product.click()

                # Move to the element and then click it
                


                # Wait for the new tab to open and switch to it
                WebDriverWait(driver, 10).until(EC.new_window_is_opened)
                new_tab = [window for window in driver.window_handles if window != original_window][0]
                driver.switch_to.window(new_tab)

                # Scrape the shop details
                shop_url = driver.current_url
                try:
                    data = scrape_shop_details(driver, shop_url)
                except Exception as e:
                    print(f"Error scraping shop {count}: {e}")
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

    print("\nFinished scraping all shop.")


