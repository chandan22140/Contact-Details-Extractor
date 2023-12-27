from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd

# Set up Chrome options to run headless (without opening a browser window)
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_driver_path = 'chromedriver.exe'


def extract_info(html_block):
    company_name = html_block.find(
        'h4').text.strip() if html_block.find('h4') else None
    email = html_block.find('p', string='Email :').find_next(
        'p').text.strip() if html_block.find('p', string='Email :') else None
    state = html_block.find('p', string='State :').find_next(
        'p').text.strip() if html_block.find('p', string='State :') else None
    return company_name, email, state


# Create a new instance of the Chrome driver
driver = webdriver.Chrome(
    executable_path=chrome_driver_path, options=chrome_options)


# URL to scrape
p = 2
x = (p-1)*50
url = f"https://ihgfdelhifair.in/mis/Exhibitors/index/{x}"

# Load the webpage
driver.get(url)

# Wait for some time to allow dynamic content to load (you may need to adjust this)
t = 10
print(f"Waiting for {t} seconds...")
driver.implicitly_wait(t)

# Get the updated page source after dynamic content has loaded
html_content = driver.page_source

# Close the browser window
driver.quit()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find all blocks with class "col-md-3"
html_blocks = soup.find_all('div', class_='col-md-3')

# Function to extract information from each HTML block

# Create a list of tuples containing information from each block
data = [extract_info(block) for block in html_blocks]

# Create a DataFrame
df = pd.DataFrame(data, columns=['Company Name', 'Email', 'State'])

# Display the DataFrame
print(df)

# Save the DataFrame to a CSV file
df.to_csv('exhibitors_data.csv', index=False)
print("DataFrame has been saved to exhibitors_data.csv")
