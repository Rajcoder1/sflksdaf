from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import csv
import time

# Set up Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_experimental_option(
        "prefs", {
            # block image loading
            "profile.managed_default_content_settings.images": 2,
        })
# Initialize the WebDriver with options
driver = webdriver.Chrome(options=chrome_options)

# Keywords to check
keywords = ["Antineoplastic", "Beta Lactam", "Sulfonamide", "Taxane", "Tetracycline", "Camptothecin", "Nucleotide"]

# Input file
input_file = 'ZSCORE_EIGEN - Raw_AdmetLab2.0 (1).csv'  # Replace with your actual CSV file name

# Open the specified webpage once
base_url = "https://go.drugbank.com/drugs/DB01039"
driver.get(base_url)

# Read the CSV file, process each row, and write the updated data back to the same file
rows = []

with open(input_file, mode='r', newline='') as infile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames
    
    # Ensure 'Drug Class' is included in fieldnames
    if 'Drug Class' not in fieldnames:
        fieldnames.append('Drug Class')
    
    for row in reader:
        drug_name = row['Active Ingredient']
        print(f"Processing {drug_name}")

        # Find the search input field using its ID and enter the drug name
        search_input = driver.find_element(By.ID, "query")
        search_input.clear()
        search_input.send_keys(drug_name)
        search_input.send_keys(Keys.RETURN)

        # Wait for the page to load
        time.sleep(3)

        # Get page source and parse with BeautifulSoup
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        # Find all elements with the specified class for drug class information
        results = soup.find_all('div', class_='category-columns')

        # Extract the text from the elements
        extracted_text = " ".join([result.get_text(strip=True) for result in results])

        # Check if any of the keywords are present in the extracted text
        found_keyword = None
        for keyword in keywords:
            if keyword.lower() in extracted_text.lower():
                found_keyword = keyword
                break

        # Update the 'Drug Class' column with the extracted drug class
        row['Drug Class'] = found_keyword if found_keyword else ''

        rows.append(row)
        

# Close the browser
driver.quit()

# Write the updated data back to the same CSV file
with open(input_file, mode='w', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Process completed. The file {input_file} has been updated with drug class information.")
