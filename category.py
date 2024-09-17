from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,TimeoutException,StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

def scrape_category_details(driver, url, output_csv):
    # Load the webpage
    driver.get(url)
    #print("\n\nStarted scraping category details\n\n")
    details = {}

    try:
        # Wait for key elements to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[2]/div[1]/div[1]'))
        )
        
        # Extract category details with error handling
        try:
            details['category_name'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div/div/div[1]').text
        except NoSuchElementException:
            details['category_name'] = "N/A"

        try:
            details['category_level'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[2]/div[1]/div/span/span').text
        except NoSuchElementException:
            details['category_level'] = "N/A"
        try:
            details['category_hierarchy']=driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[2]/div[1]/div/div/span').text 
        except NoSuchElementException:
            details['category_hierarchy'] = "N/A"    

        # Category change in revenue over different time periods
        time_periods = {
            'Yesterday': '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div/div/div[2]/div[2]/div/label[1]/span[2]',
            'Last_7_Days': '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div/div/div[2]/div[2]/div/label[2]/span[2]',
            'Last_30_Days': '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div/div/div[2]/div[2]/div/label[3]/span[2]',
            'Last_90_Days': '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div/div/div[2]/div[2]/div/label[4]/span[2]',
            'Last_180_Days': '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div/div/div[2]/div[2]/div/label[5]/span[2]'
        }
        
        for period, range_xpath in time_periods.items():
            driver.find_element(By.XPATH, range_xpath).click()
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[2]/div/div[1]/div[1]/div[2]/div[3]/div[2]'))
            )
            
            # Scraping with try-except for each data point to handle missing data
            try:
                details[f'category_change_in_revenue_{period}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[2]/div/div[1]/div[1]/div[2]/div[3]/div[2]').text
            except NoSuchElementException:
                details[f'category_change_in_revenue_{period}'] = "N/A"

            try:
                details[f'category_no_of_shops_{period}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[2]/div/div[2]/div[1]/div/div[1]/div[2]/div[2]/div/div/div/div/div/span').text
            except NoSuchElementException:
                details[f'category_no_of_shops_{period}'] = "N/A"

            try:
                details[f'category_revenue_growth_rate_{period}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[2]/div/div[2]/div[1]/div/div[2]/div[1]/div[2]/div/div/div/div').text
            except NoSuchElementException:
                details[f'category_revenue_growth_rate_{period}'] = "N/A"

            try:
                details[f'category_avg_revenue_per_shop_{period}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[2]/div/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div').text
            except NoSuchElementException:
                details[f'category_avg_revenue_per_shop_{period}'] = "N/A"

            try:
                details[f'category_top_3_shops_revenue_ratio_{period}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[2]/div/div[2]/div[1]/div/div[2]/div[3]/div[2]/div/div/div/div').text
            except NoSuchElementException:
                details[f'category_top_3_shops_revenue_ratio_{period}'] = "N/A"

            try:
                details[f'category_top_10_shops_revenue_ratio_{period}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[2]/div/div[2]/div[1]/div/div[2]/div[4]/div[2]/div/div/div/div').text
            except NoSuchElementException:
                details[f'category_top_10_shops_revenue_ratio_{period}'] = "N/A"

            try:
                details[f'category_soa_revenue_share_{period}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[3]/div[2]/div[1]/div/div/div/div[3]/div/div[2]/div[3]/div[1]/div/div[1]/div/div[2]/span[2]').text
            except NoSuchElementException:
                details[f'category_soa_revenue_share_{period}'] = "N/A"

            try:
                details[f'category_aff_revenue_share_{period}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[3]/div[2]/div[1]/div/div/div/div[3]/div/div[2]/div[3]/div[1]/div/div[2]/div/div[2]/span[2]').text
            except NoSuchElementException:
                details[f'category_aff_revenue_share_{period}'] = "N/A"

            try:
                details[f'category_mall_revenue_share_{period}'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[3]/div[2]/div[1]/div/div/div/div[3]/div/div[2]/div[3]/div[3]/div/div/div[2]/span[2]').text
            except NoSuchElementException:
                details[f'category_mall_revenue_share_{period}'] = "N/A"

    except NoSuchElementException as e:
        print(f"Error while scraping category: {e}")

    return details

def scrape_category(driver, url, output_csv):
    # Visit the URL
    driver.get(url)
    count = 0

    # Scroll to the bottom of the page to reveal more content
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # time.sleep(1)  # Give time for content to load

    # Click on the specified elements
    try:
        element_to_click1 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/ul/li[10]/div/div/span[2]'))
        )
        element_to_click1.click()

        element_to_click2 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/ul/li[10]/div/div[2]/div/div/div/div/div/div[3]/div'))
        )
        element_to_click2.click()

    except TimeoutException:
        print("The elements to show 50 category on page were not found.")
        return

    header = ['category_name','category_level','category_hierarchy','category_change_in_revenue_Yesterday','category_no_of_shops_Yesterday','category_revenue_growth_rate_Yesterday','category_avg_revenue_per_shop_Yesterday','category_top_3_shops_revenue_ratio_Yesterday','category_top_10_shops_revenue_ratio_Yesterday','category_soa_revenue_share_Yesterday','category_aff_revenue_share_Yesterday','category_mall_revenue_share_Yesterday','category_change_in_revenue_Last_7_Days','category_no_of_shops_Last_7_Days','category_revenue_growth_rate_Last_7_Days','category_avg_revenue_per_shop_Last_7_Days','category_top_3_shops_revenue_ratio_Last_7_Days','category_top_10_shops_revenue_ratio_Last_7_Days','category_soa_revenue_share_Last_7_Days','category_aff_revenue_share_Last_7_Days','category_mall_revenue_share_Last_7_Days','category_change_in_revenue_Last_30_Days','category_no_of_shops_Last_30_Days','category_revenue_growth_rate_Last_30_Days','category_avg_revenue_per_shop_Last_30_Days','category_top_3_shops_revenue_ratio_Last_30_Days','category_top_10_shops_revenue_ratio_Last_30_Days','category_soa_revenue_share_Last_30_Days','category_aff_revenue_share_Last_30_Days','category_mall_revenue_share_Last_30_Days','category_change_in_revenue_Last_90_Days','category_no_of_shops_Last_90_Days','category_revenue_growth_rate_Last_90_Days','category_avg_revenue_per_shop_Last_90_Days','category_top_3_shops_revenue_ratio_Last_90_Days','category_top_10_shops_revenue_ratio_Last_90_Days','category_soa_revenue_share_Last_90_Days','category_aff_revenue_share_Last_90_Days','category_mall_revenue_share_Last_90_Days','category_change_in_revenue_Last_180_Days','category_no_of_shops_Last_180_Days','category_revenue_growth_rate_Last_180_Days','category_avg_revenue_per_shop_Last_180_Days','category_top_3_shops_revenue_ratio_Last_180_Days','category_top_10_shops_revenue_ratio_Last_180_Days','category_soa_revenue_share_Last_180_Days','category_aff_revenue_share_Last_180_Days','category_mall_revenue_share_Last_180_Days']

    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()

        # Continue scraping until no more pages
        while True:
            # Find all category
            time.sleep(.5)
            category_rows = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr')
            
            category_rows = category_rows[1:]  # Exclude the header row

            #print(f"Total number of category found (excluding header): {len(category_rows)}")

            original_window = driver.current_window_handle  # Store the current window handle

            # Loop through each category
            for index, product in enumerate(category_rows[:50], start=1):
                count = count + 1
                if count >  10:
                    break
                
                # print(f"\nProcessing product {index}/{len(product_rows)}")
                #print(f'processing category: {count}')
                try:
                    product.click()

                except StaleElementReferenceException:
                    print(f"Stale element at video {count}, trying to re-locate and click.")
                    # Re-locate the product and click again
                    video_rows = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div[2]/div/table/tbody/tr')
                    video_rows = video_rows[1:]
                    product = video_rows[index - 1]  # Re-fetch the element
                    product.click()

                # Wait for the new tab to open and switch to it
                WebDriverWait(driver, 10).until(EC.new_window_is_opened)
                new_tab = [window for window in driver.window_handles if window != original_window][0]
                driver.switch_to.window(new_tab)

                # Scrape the category details
                category_url = driver.current_url
                try:
                    data = scrape_category_details(driver, category_url,output_csv)
                except Exception as e:
                    print(f"Error scraping category {count}: {e}")
                    # Fill the row with "Not scraped" if there's an error
                    data = {field: 'Not scraped' for field in header}

                # Write the details to CSV
                writer.writerow(data)

                # Close the current tab and switch back to the original tab
                driver.close()
                driver.switch_to.window(original_window)

            try:
                    if(count > 10):
                        break
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

    print("\nFinished scraping all category.")    