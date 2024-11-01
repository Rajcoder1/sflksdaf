from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor

# Load SMILES data
data = pd.read_csv('AdmetLab2.0/rawsmiles.csv')
errorList = [''] * len(data)

# Configure Chrome to run in headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})

def process_smiles(smile_string, index):
    try:
        # Initialize WebDriver for each thread
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('https://admetmesh.scbdd.com/service/evaluation/index')

        # Input SMILES string and submit
        input_box = driver.find_element(By.ID, "smiles")
        input_box.send_keys(smile_string)
        input_box.submit()

      

        page_source = driver.page_source.lower()

        # Check for errors
        if 'server error' in page_source:
            errorList[index] = 'ERROR'
            print(f"Server Error detected: {smile_string}")
        else:
            errorList[index] = 'SUCCESS'
            print(f"Success: {smile_string}")
    except Exception as e:
        errorList[index] = 'ERROR'
        print(f"Error processing {smile_string}: {e}")
    finally:
        driver.quit()

# Process SMILES strings concurrently with a thread pool
with ThreadPoolExecutor(max_workers=1) as executor:
    for idx, row in data.iterrows():
        executor.submit(process_smiles, row['SMILES'], idx)

# Save results to CSV
data['ERRORS'] = errorList
data.to_csv('rawAdmetLab2.0.csv', index=False)
