import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

def scrape_product_details(driver):
    print("\n\nstarted scraping\n\n")
    details = {}
    
    try:
        # Wait until the product name element is present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div[1]/div[1]/div[2]/div/div[1]/div')))
        
        # Product name
        details['Product Name'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div[1]/div[1]/div[2]/div/div[1]/div').text
        
        # Shipped from
        details['Shipped From'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div[1]/div[1]/div[2]/div/div[2]/div').text
        
        # Product category
        details['Product Category'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div[1]/div[1]/div[2]/div/div[3]/div[2]').text
        
        # Product price
        details['Product Price'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div[1]/div[1]/div[2]/div/div[6]/div').text
        
        # 30 days lowest price
        details['30 Days Lowest Price'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div[1]/div[1]/div[2]/div/div[7]/div/span').text
        
        # Shop name
        details['Shop Name'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div[1]/div[1]/div[4]/div[2]/div[2]').text
        
        # Revenue in last 7 days
        details['Revenue in Last 7 Days'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[1]/div[1]/div[2]/div/div/div/div').text
        
        # Number of times product sold
        details['Number of Times Product Sold'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[1]/div[2]/div[2]/div/div/div/div').text
        
        # Avg unit price
        details['Avg Unit Price'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[1]/div[3]/div[2]/div/div/div/div').text
        
        # Live Revenue
        details['Live Revenue'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[1]/div[2]/div/div/div/div').text
        
        # Video Revenue
        details['Video Revenue'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div').text
        
        # Shopping mall revenue
        details['Shopping Mall Revenue'] = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[3]/div/div[2]/div[1]/div/div[2]/div[3]/div[2]/div/div/div/div').text

    except NoSuchElementException as e:
        print(f"Error finding element: {e}")
    
    # Save the scraped data to a CSV file
    with open('Cakes_cover.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(details.keys())
        # Write data
        writer.writerow(details.values())

    return details

# Path to your chromedriver executable
chromedriver_path = r'C:\Users\momin\Desktop\chromedriver-win64\chromedriver.exe'

# Set up the service and options for Chrome
service = Service(chromedriver_path)
options = Options()
options.add_argument("--start-maximized")

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=options)

# Open the URL
driver.get('https://kalodata.com/login')

# Allow the page to load completely
time.sleep(2)

# Find the email input element and enter the email
email_input = driver.find_element(By.ID, 'register_email')
email_input.send_keys('info@ejex.co.uk')

# Find the password input element and enter the password
password_input = driver.find_element(By.ID, 'register_password')
password_input.send_keys('111222333Pp!@#')

# Find the login button and click it
login_button = driver.find_element(By.XPATH, '//button[@type="submit" and contains(@class, "login_submit-btn")]')
login_button.click()
time.sleep(4)

# Wait for the login process to complete and the next page to load
#WebDriverWait(driver, 10).until(EC.url_contains('product/detail'))

# Navigate to the product page
driver.get('https://kalodata.com/product/detail?id=1729418496836080191&language=en-US&currency=USD&region=US')


# Wait until the product details are present
#WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[3]/div[1]/div[1]/div[1]/div[2]/div/div[1]/div')))

# Get the product details and save to CSV
product_details = scrape_product_details(driver)
print(product_details)

# Close the driver
driver.quit()
