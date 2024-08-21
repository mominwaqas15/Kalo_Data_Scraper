from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

# def get_revenue_with_symbol(driver, element_xpath, arrow_xpath):
#     try:
#         # Extract the revenue text
#         revenue_text = driver.find_element(By.XPATH, element_xpath).text

#         # Extract the src or alt attribute of the arrow image
#         arrow_element = driver.find_element(By.XPATH, arrow_xpath)
#         arrow_image_src = arrow_element.get_attribute("src")  # You could also use 'alt' if it provides meaningful info

#         # Determine the direction based on the src or alt attribute
#         if "down" in arrow_image_src.lower():  # Assuming 'down' is part of the image name or alt text for a decrease
#             symbol = "-"  # Negative symbol
#         elif "up" in arrow_image_src.lower():  # Assuming 'up' is part of the image name or alt text for an increase
#             symbol = "+"  # Positive symbol
#         else:
#             symbol = ""  # Default case if no direction is found

#         # Append the symbol to the revenue text
#         revenue_with_symbol = f"{symbol}{revenue_text}"
#         return revenue_with_symbol

#     except NoSuchElementException as e:
#         print(f"Error while scraping: {e}")
#         return None

def scrape_category_details(driver, url, output_csv):
    # Load the webpage
    driver.get(url)
    print("\n\nStarted scraping category details\n\n")
    details = {}

    try:
        # Wait for key elements to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[2]/div[1]/div[1]'))
        )
        
        # Extract category details
        details['category_name'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div/div/div[1]').text
        details['category_level'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[2]/div[1]/div/span/span').text
        #details['category_hierarchy'] = driver.find_element(By.XPATH, '<XPATH_for_category_hierarchy>').text

        # Revenue entity IDs
        #details['revenue_entity_id'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[2]/div/div[2]/div[1]/div/div[1]/div[1]/div[2]/div/div/div/div').text
        #details['live_revenue_entity_id'] = driver.find_element(By.XPATH, '<XPATH_for_live_revenue_entity_id>').text
        #details['video_revenue_entity_id'] = driver.find_element(By.XPATH, '<XPATH_for_video_revenue_entity_id>').text

        # Category change in revenue over different time periods
        time_periods = {'Yesterday': '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div/div/div[2]/div[2]/div/label[1]/span[2]',
            'Last 7 Days': '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div/div/div[2]/div[2]/div/label[2]/span[2]',
            'Last 30 Days': '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div/div/div[2]/div[2]/div/label[3]/span[2]',
            'Last 90 Days': '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div/div/div[2]/div[2]/div/label[4]/span[2]',
            'Last 180 Days': '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[1]/div[1]/div/div/div[2]/div[2]/div/label[5]/span[2]'}
        
        for period, range_xpath in time_periods.items():
            driver.find_element(By.XPATH, range_xpath).click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[2]/div/div[1]/div[1]/div[2]/div[3]/div[2]')))
            #arrow_xpath='//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div[2]'
            details[f'category_change_in_revenue_{period}'] = driver.find_element(By.XPATH, f'//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[2]/div/div[1]/div[1]/div[2]/div[3]/div[2]').text
            #get_revenue_with_symbol(driver,'//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div/div[2]/div/div[1]/div[1]/div[2]/div[3]/div[2]',arrow_xpath)
            details[f'category_no_of_shops_{period}'] = driver.find_element(By.XPATH, f'//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[2]/div/div[2]/div[1]/div/div[1]/div[2]/div[2]/div/div/div/div').text
            details[f'category_revenue_growth_rate_{period}'] = driver.find_element(By.XPATH, f'//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[2]/div/div[2]/div[1]/div/div[2]/div[1]/div[2]/div/div/div/div').text
            details[f'category_avg_revenue_per_shop_{period}'] = driver.find_element(By.XPATH, f'//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[2]/div/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div').text
            details[f'category_top_3_shops_revenue_ratio_{period}'] = driver.find_element(By.XPATH, f'//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[2]/div/div[2]/div[1]/div/div[2]/div[3]/div[2]/div/div/div/div').text
            details[f'category_top_10_shops_revenue_ratio_{period}'] = driver.find_element(By.XPATH, f'//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[2]/div/div[2]/div[1]/div/div[2]/div[4]/div[2]/div/div/div/div').text
            details[f'category_soa_revenue_share_{period}'] = driver.find_element(By.XPATH, f'//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[3]/div[2]/div[1]/div/div/div/div[3]/div/div[2]/div[3]/div[1]/div/div[1]/div/div[2]/span[2]').text
            details[f'category_aff_revenue_share_{period}'] = driver.find_element(By.XPATH, f'//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[3]/div[2]/div[1]/div/div/div/div[3]/div/div[2]/div[3]/div[1]/div/div[2]/div/div[2]/span[2]').text
            details[f'category_mall_revenue_share_{period}'] = driver.find_element(By.XPATH, f'//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[3]/div[2]/div[1]/div/div/div/div[3]/div/div[2]/div[3]/div[3]/div/div/div[2]/span[2]').text

    except NoSuchElementException as e:
        print(f"Error while scraping: {e}")

    # Write the details to CSV
    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(details.keys())
        writer.writerow(details.values())

    return details

# Example usage:
# driver = webdriver.Chrome()
# url = 'http://example.com/category-details'
# output_csv = 'category_details.csv'
# scrape_category_details(driver, url, output_csv)
# driver.quit()
