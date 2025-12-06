import os
import numpy as np
import pandas as pd


class DataCleaner:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.df = None
        self.df_uk = None

    def load_data(self) -> pd.DataFrame:
        """
        Load the dataset from the specified path.

        Returns:
            pd.DataFrame: Loaded DataFrame.
        """
        dtype = dict(
            InvoiceNo=np.object_,
            StovkCode=np.object_,
            Description=np.object_,
            Quantity=np.int64,
            # InvoiceDate=np.object_,
            UnitPrice=np.float64,
            CustomerID=np.object_,
            Country=np.object_
        )

        print(self.data_path)

        self.df = pd.read_csv(
            self.data_path,
            encoding='ISO-8859-1',
            parse_dates=['InvoiceDate'],
            dtype=dtype
        )

        print(f"Data loaded with shape: {self.df.shape}")
        print(f"Data loaded has samples: {len(self.df)}")

        return self.df

    def clean_data(self) -> pd.DataFrame:
        """
        Clean the dataset by remove invalid samples and filter UK customer.

        Returns:
            pd.DataFrame: Cleaned UK DataFrame.
        """
        # Calculate TotalPrice
        self.df['TotalPrice'] = self.df['Quantity'] * self.df['UnitPrice']
        
        # Remove canceled orders
        self.df = self.df[~self.df['InvoiceNo'].astype(str).str.startswith('C')]
        print(f"Data after removing canceled orders: {self.df.shape}")

        # Renmove samples with non-positive Quantity or UnitPrice
        self.df = self.df[(self.df['Quantity'] > 0) & (self.df['UnitPrice'] > 0)]
        print(f"Data after removing non-positive Quantity or UnitPrice: {self.df.shape}")

        # Remove samples with null CustomerID
        self.df = self.df[self.df['CustomerID'].notnull()]
        # Standardize CustomerID format
        self.df['CustomerID'] = (
            self.df['CustomerID']
            .astype(float)
            .astype(np.int64)
            .astype(str)
            .str.zfill(6)
        )
        print(f"Data after removing null CustomerID: {self.df.shape}")

        # Filter UK customers
        self.df_uk = self.df[self.df['Country'] == 'United Kingdom'].copy()
        print(f"Data after filtering UK customers: {self.df_uk.shape}")

        return self.df_uk

    def create_time_features(self) -> None:
        """
        Create additional time-based features.
        """
        self.df_uk['InvoiceDayOfWeek'] = self.df_uk['InvoiceDate'].dt.day_of_week
        self.df_uk['InvoiceHour'] = self.df_uk['InvoiceDate'].dt.hour

    def remove_duplicates(self) -> pd.DataFrame:
        """Remove duplicate rows."""
        return self.data.drop_duplicates()
    
    def get_summary(self) -> pd.DataFrame:
        """Get summary statistics of the DataFrame."""
        return self.data.describe()
    
    def get_data(self) -> pd.DataFrame:
        """Return the current state of the DataFrame."""
        return self.data
    
if __name__ == "__main__":
    print(pd.read_csv("data/online_retail.csv").head())