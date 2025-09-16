import requests
import pandas as pd

# Define the URL for the API
url = 'https://api.coindesk.com/v1/bpi/currentprice.json'

# Send a GET request to fetch the data
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON data
    data = response.json()
    
    # Extract the 'bpi' data from the JSON response
    bpi_data = data['bpi']
    
    # Convert the 'bpi' data into a DataFrame
    bpi_df = pd.DataFrame.from_dict(bpi_data, orient='index')
    
    # Create the 'sales' DataFrame
    sales_data = [
        {"salesPerson": "Yossi", "sales": 1500, "code": "USD"},
        {"salesPerson": "Danni", "sales": 7500, "code": "GBP"}
    ]
    sales_df = pd.DataFrame(sales_data)
    
    # Merge the 'sales' DataFrame with the 'bpi' DataFrame on the 'code' column
    merged_df = pd.merge(sales_df, bpi_df, how='left', left_on='code', right_index=True)
    
    # Calculate the 'total_sale' by multiplying 'sales' by 'rate_float'
    merged_df['total_sale_in_k'] = (merged_df['sales'] * merged_df['rate_float'])/1000
    
    # Print the resulting DataFrame
    print(merged_df[['salesPerson', 'sales', 'code', 'total_sale_in_k']])
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
