import requests
from bs4 import BeautifulSoup
import pandas as pd

# Make a GET request to the URL
url = "https://ihgfdelhifair.in/mis/Exhibitors/index/2250"
response = requests.get(url)
print(response.text)
# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all blocks with class "col-md-3"
    html_blocks = soup.find_all('div', class_='col-md-3')

    # Function to extract information from each HTML block
    def extract_info(html_block):
        company_name = html_block.find('h4').text.strip()
        email = html_block.find(
            'p', string='Email :').find_next('p').text.strip()
        state = html_block.find(
            'p', string='State :').find_next('p').text.strip()
        return company_name, email, state

    # Create a list of tuples containing information from each block
    data = [extract_info(block) for block in html_blocks]

    # Create a DataFrame
    df = pd.DataFrame(data, columns=['Company Name', 'Email', 'State'])

    # Display the DataFrame
    # print(df)

    # Save the DataFrame to a CSV file
    df.to_csv('exhibitors_data.csv', index=False)
    print("DataFrame has been saved to exhibitors_data.csv")


else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
