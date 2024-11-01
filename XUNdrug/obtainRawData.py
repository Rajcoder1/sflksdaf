import time
import csv
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

# Set up Chrome options
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
driver.get("https://xundrug.cn/molgpka")

input_element = driver.find_element(By.ID, "myinput")
results_list = []

with open("XUNdrug/raw_smiles.csv", "r") as csv_file:
    csv_reader = csv.reader(csv_file)

    # Loop through each row (SMILES string) in the CSV
    for row in csv_reader:
        try:
            
            smiles_string = row[0]

            input_element.clear()
            input_element.send_keys(smiles_string)
            input_element.send_keys(Keys.RETURN)
            time.sleep(10)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            table = soup.find('table', class_='table table-hover table-condensed')

            properties = {}
            table_rows = table.find_all('tr')
            for row in table_rows:
                cells = row.find_all('td')
                if len(cells) == 2:
                    property_name = cells[0].text.strip()
                    property_value = cells[1].text.strip()
                    properties[property_name] = property_value

            properties["SMILES"] = smiles_string
            results_list.append(properties)

            time.sleep(10)

            driver.get("https://xundrug.cn/molgpka")
            input_element = driver.find_element(By.ID, "myinput")

            time.sleep(10)
            print(smiles_string)
        except Exception as e:
            print(f"ERROR: {e}")
            results_df = pd.DataFrame(results_list)
            results_df.to_csv("out2.csv", index=False)

results_df = pd.DataFrame(results_list)
results_df.to_csv("out2.csv", index=False)

driver.quit()
