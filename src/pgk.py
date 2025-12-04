import numpy as np
import pandas as pd


class DataCleaner:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.df = None

    def clean_data(self) -> pd.DataFrame:
        """Load and clean the data from the specified path."""
        self.data = pd.read_csv(self.data_path)
        return self.data

    def remove_nulls(self) -> pd.DataFrame:
        """Remove rows with null values."""
        return self.data.dropna()

    def fill_nulls(self, value) -> pd.DataFrame:
        """Fill null values with a specified value."""
        return self.data.fillna(value)

    def remove_duplicates(self) -> pd.DataFrame:
        """Remove duplicate rows."""
        return self.data.drop_duplicates()
    
    def get_summary(self) -> pd.DataFrame:
        """Get summary statistics of the DataFrame."""
        return self.data.describe()
    
    def get_data(self) -> pd.DataFrame:
        """Return the current state of the DataFrame."""
        return self.data