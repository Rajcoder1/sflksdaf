from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

data = pd.read_csv('AdmetLab2.0/rawsmiles.csv')
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_experimental_option(
    "prefs", {
        # Block image loading
        "profile.managed_default_content_settings.images": 2,
    })

# Initialize the WebDriver with options
driver = webdriver.Chrome(options=chrome_options)
errorList = []

for index, row in data.iterrows():
    smileString = row['SMILES']
    driver.get('https://admetmesh.scbdd.com/service/evaluation/index')
    
    input_box = driver.find_element(By.ID, "smiles")
    input_box.send_keys(smileString)
    input_box.submit()

    page_source = driver.page_source

    page_source_lower = page_source.lower()
    if 'server error' in page_source_lower:
        print("Server Error detected on the page.", smileString)
        errorList.append('ERROR')
    else:
        print("sucess", smileString)
        errorList.append('SUCCESS')

    print(smileString)
    

print(errorList)
data['ERRORS'] = errorList
time.sleep(10)
driver.quit()

data.to_csv('rawAdmetLab2.0.csv')