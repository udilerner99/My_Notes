import pandas as pd
from datetime import datetime

class DataHandler:
    """
    A class to handle data cleaning and processing for a CSV file.
    This class identifies and handles bad records, writes them to separate files,
    and saves the cleaned data into a dedicated file.
    """

    def __init__(self, input_file):
        """
        Initialize the DataHandler with the input file path.
        
        Args:
            input_file (str): Path to the input CSV file.
        """
        self.input_file = input_file
        self.df = None
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def load_data(self):
        """
        Load the data from the input CSV file into a pandas DataFrame.
        Adds an 'dt_audit' column to track the timestamp of processing.
        """
        try:
            self.df = pd.read_csv(self.input_file)
            self.df['dt_audit'] = self.timestamp  # Add audit timestamp column
        except Exception as e:
            raise Exception(f"Error loading data: {e}")

    def handle_duration(self):
        """
        Handle the 'Duration' column by:
        - Writing rows with 'Duration' > 120 to a separate file.
        - Removing those rows from the main DataFrame.
        """
        try:
            # Identify rows with 'Duration' > 120
            df_duration_above_120 = self.df[self.df['Duration'] > 120]
            df_duration_above_120.to_csv('duration_above_120.csv', index=False)  # Save bad records

            # Keep only rows with 'Duration' <= 120
            self.df = self.df[self.df['Duration'] <= 120]
        except KeyError:
            raise Exception("The 'Duration' column is missing in the data.")
        except Exception as e:
            raise Exception(f"Error handling 'Duration': {e}")

    def handle_null_values(self):
        """
        Handle rows with null values in any column:
        - Write rows with null values to a separate file.
        - Remove those rows from the main DataFrame.
        """
        try:
            # Identify rows with null values
            df_null_values = self.df[self.df.isnull().any(axis=1)]
            df_null_values.to_csv('error_loading.csv', index=False)  # Save bad records

            # Remove rows with null values
            self.df = self.df.dropna()
        except Exception as e:
            raise Exception(f"Error handling null values: {e}")

    def save_cleaned_data(self):
        """
        Save the cleaned DataFrame to a dedicated CSV file.
        """
        try:
            self.df.to_csv('data_cleaned.csv', index=False)
        except Exception as e:
            raise Exception(f"Error saving cleaned data: {e}")

    def process_data(self):
        """
        Execute the full data handling pipeline:
        - Load data
        - Handle 'Duration' column
        - Handle null values
        - Save cleaned data
        """
        try:
            self.load_data()
            self.handle_duration()
            self.handle_null_values()
            self.save_cleaned_data()
        except Exception as e:
            print(f"An error occurred during processing: {e}")


# Example usage:
if __name__ == "__main__":
    # Initialize the DataHandler with the input file
    handler = DataHandler('data_dirty.csv')

    # Process the data
    handler.process_data()