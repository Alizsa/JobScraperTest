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

# Navigate to page and wait for JavaScript to load
driver.get('https://www.roberthalf.com/jobs/all-jobs/all-locations/all-types/technology')
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.XPATH, "//h3[contains(@class, 'rh_job_search__card_title')]")))

# Extract job titles
job_titles = []
while True:
    for job in driver.find_elements(By.XPATH, "//h3[contains(@class, 'rh_job_search__card_title')]"):
        job_titles.append(job.text.strip())

    try:
        # Click on the "Next" button and wait for the next page to load
        next_button = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@class='sc-jbKcbu kEpEsa']")))
        driver.execute_script("arguments[0].click();", next_button)
        wait.until(EC.staleness_of(next_button))
    except:
        # If there is no "Next" button, break out of the loop
        break

job_titles = job_titles[:100] # keep only first 2000 job titles

if job_titles:
    df = pd.DataFrame({'Job Titles': job_titles})

    df.to_csv('job_titles.csv', index=False)
    print('Data saved to CSV file.')
else:
    print('No data found.')

# Clean up
driver.quit()
