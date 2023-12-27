from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
import re

# Function to extract information from each HTML block


def extract_info(html_block):
    company_name_tag = html_block.find('h4')
    company_name = company_name_tag.text.strip() if company_name_tag else None

    # Find all p tags
    all_p_tags = html_block.find_all('p')

    # Filter p tags containing relevant information
    relevant_p_tags = [p for p in all_p_tags if any(
        keyword in p.text for keyword in ['Email :', 'State :', 'Contact No. :'])]

    if relevant_p_tags:
        info_text = ' '.join(tag.text.strip() for tag in relevant_p_tags)

        # Use regular expressions to extract email, state, and phone number
        email_match = re.search(r'Email\s*:\s*(.*?)(?=\w+\s*:|$)', info_text)
        email = email_match.group(1).strip() if email_match else None

        state_match = re.search(r'State\s*:\s*(.*?)(?=\w+\s*:|$)', info_text)
        state = state_match.group(1).strip() if state_match else None

        phone_match = re.search(
            r'Contact No.\s*:\s*(.*?)(?=\w+\s*:|$)', info_text)
        phone = phone_match.group(1).strip() if phone_match else None

        return company_name, email, state, phone

    return company_name, None, None, None


# Path to your ChromeDriver executable, download from: https://sites.google.com/chromium.org/driver/
chrome_driver_path = 'chromedriver.exe'

# Set up Chrome options to run headless (without opening a browser window)
chrome_options = ChromeOptions()
chrome_service = ChromeService(chrome_driver_path)

# chrome_options.add_argument('--headless')


# URLs to scrape


# Create a new instance of the Chrome driver
driver = webdriver.Chrome(
    service=chrome_service, options=chrome_options)

html_contents = []  # To store HTML content for each URL

for p in range(1,  47):
    x = (p-1)*50
    url = f"https://ihgfdelhifair.in/mis/Exhibitors/index/{x}"
    if p == 1:
        url = f"https://ihgfdelhifair.in/mis/Exhibitors/index"
    driver.get(url)

    # Wait for some time to allow dynamic content to load (you may need to adjust this)
    t = 20
    print(f"Waiting for {t} seconds...")
    driver.implicitly_wait(t)
    # Get the updated page source after dynamic content has loaded
    html_content = driver.page_source
    # if p == 1:
    #     print(html_content)
    html_contents.append(html_content)
    print(f"Page {p} done...")


# Close the browser window
driver.quit()

# Parse the HTML content for each URL
dataframes = []
p = 1
for html_content in html_contents:
    soup = BeautifulSoup(html_content, 'html.parser')
    html_blocks = soup.find_all('div', class_='col-md-3')

    # Function to extract information from each HTML block
    # Create a list of tuples containing information from each block
    data = [extract_info(block) for block in html_blocks]

    # Create a DataFrame
    df = pd.DataFrame(
        data, columns=['Company Name', 'Email', 'State', 'Contact No.'])
    df.to_csv(f'data_page_{p}.csv', index=False)
    p += 1
    dataframes.append(df)


# Combine all DataFrames into a single DataFrame
final_df = pd.concat(dataframes, ignore_index=True)

# Display the combined DataFrame
# print("\nCombined DataFrame:")
# print(final_df)

# Save the combined DataFrame to a single CSV file
final_df.to_csv('exhibitors_combined_data.csv', index=False)
print("Combined DataFrame has been saved to exhibitors_combined_data.csv")
