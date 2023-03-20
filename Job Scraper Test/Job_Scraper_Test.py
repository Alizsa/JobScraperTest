import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure Selenium
options = Options()
options.headless = True # Run browser in background
service = Service('./chromedriver') # path to chromedriver executable
driver = webdriver.Chrome(service=service, options=options)

# Define the base URL and number of pages to scrape
base_url = 'https://www.roberthalf.com/jobs/all-jobs/all-locations/all-types/technology?page='
num_pages = 5

# Navigate to each page and extract job titles
job_titles = []
for i in range(1, num_pages+1):
    url = base_url + str(i)
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, "//h3[@class='sc-jKJlTe htHwMS rh_job_search__card_title']")))
    for job in driver.find_elements(By.XPATH, "//h3[@class='sc-jKJlTe htHwMS rh_job_search__card_title']"):
        job_titles.append(job.text.strip())

job_titles = job_titles[:100] # keep only first 100 job titles

if job_titles:
    df = pd.DataFrame({'Job Titles': job_titles})

    df.to_csv('job_titles.csv', index=False)
    print('Data saved to CSV file.')
else:
    print('No data found.')

# Clean up
driver.quit()
