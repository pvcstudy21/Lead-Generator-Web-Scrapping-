# first pip install -r requirements.txt to import packages

# import libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd

# Set up the path to the chromedriver executable (change path accordingly)
chromedriver_path = r"C:\Users\Dell\Desktop\Lead Genarator (Web Scraping)\chromedriver-win64\chromedriver.exe"

# Create a Service object
service = Service(chromedriver_path)

# Set up the Selenium WebDriver
driver = webdriver.Chrome(service=service)

# LinkedIn URL
driver.get('https://www.linkedin.com/login')

# Allow time for the page to load
time.sleep(30)

# Allow time for the login process
time.sleep(10)

# Navigate to the LinkedIn search page or the desired URL (This url find list of product managers)
driver.get('https://www.linkedin.com/search/results/people/?keywords=product%20manager&origin=SWITCH_SEARCH_VERTICAL&sid=aB%2C')

# Allow time for the page to load
time.sleep(10)

# Scraping the data
data = []

while len(data) < 50:
    soup = BeautifulSoup(driver.page_source, 'lxml')         # creating object to extract specific kind of data
    boxes = soup.find_all('li', class_='reusable-search__result-container')

    for i in boxes:
        try:
            link = i.find('a').get('href')
            name = i.find('span', {'dir': 'ltr'}).find('span', {'aria-hidden': 'true'}).text
            title = i.find('div', class_='entity-result__primary-subtitle t-14 t-black t-normal').text.strip()
            location = i.find('div', class_='entity-result__secondary-subtitle t-14 t-normal').text.strip()
            data.append({'Link': link, 'Name': name, 'Title': title, 'Location': location})
            if len(data) >= 50:
                break
        except Exception as e:
            print(e)
            pass

    if len(data) >= 50:                 # insert number of leads required
        break

    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')  # Scroll to the bottom of the page
    time.sleep(3)
    try:
        next_button = driver.find_element(By.XPATH, '//button[contains(@aria-label, "Next")]')
        next_button.click()
    except:
        break
    time.sleep(3)

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(data)
df.drop_duplicates(inplace=True)

# Save the scraped data to a CSV file
df.to_csv('output_final2.csv', index=False)

# Close the driver
driver.quit()

