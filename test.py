from bs4 import BeautifulSoup
import pandas as pd

# Your HTML blocks
html_blocks = [
    '''
    <div class="col-md-3">
        <!-- ... (Block 1 content) ... -->
    </div>
    ''',
    '''
    <div class="col-md-3">
        <!-- ... (Block 2 content) ... -->
    </div>
    '''
    # Add more blocks if needed
]

# Function to extract information from each HTML block
def extract_info(html_block):
    soup = BeautifulSoup(html_block, 'html.parser')
    
    company_name = soup.find('h4').text.strip()
    email = soup.find('p', string='Email :').find_next('p').text.strip()
    state = soup.find('p', string='State :').find_next('p').text.strip()

    return company_name, email, state

# Create a list of tuples containing information from each block
data = [extract_info(block) for block in html_blocks]

# Create a DataFrame
df = pd.DataFrame(data, columns=['Company Name', 'Email', 'State'])

# Display the DataFrame
print(df)
