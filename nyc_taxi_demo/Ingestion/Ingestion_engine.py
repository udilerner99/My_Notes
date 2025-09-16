import requests
import os
from datetime import datetime, timedelta

def download_file(url, folder_path):
    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Extract the file name from the URL
    file_name = url.split("/")[-1]

    # Set the path for the downloaded file
    file_path = os.path.join(folder_path, file_name)

    try:
        # Send a GET request to the URL
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for non-success status codes

        # Save the file
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"Downloaded: {file_name}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading the file: {e}")


# Example usage
base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_"
folder_path = "/Users/udilerner/prsnl_projects/My_Notes/nyc_taxi_demo/nyc_taxi_raw_source"

start_date = datetime(2009, 1, 1)
end_date = datetime(2023, 4, 1)
delta = timedelta(days=30)  # Assuming each month has 30 days for simplicity

current_date = start_date
while current_date < end_date:
    # Format the date as "YYYY-MM"
    year_month = current_date.strftime("%Y-%m")
    
    # Construct the URL for the specific month
    url = f"{base_url}{year_month}.parquet"

    # Download the file
    download_file(url, folder_path)

    # Move to the next month
    current_date += delta
