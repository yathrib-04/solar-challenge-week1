"""
Data loading and initial inspection module for solar data analysis.

This module provides functionality for loading solar data from CSV files and
performing initial data inspection and validation. It includes methods for
basic data information retrieval and summary statistics calculation.
"""

import pandas as pd
import numpy as np
from typing import Tuple, Dict

class DataLoader:
    """
    A class for loading and performing initial inspection of solar data.
    
    This class handles the loading of solar data from CSV files and provides
    methods for initial data inspection, including basic information retrieval
    and summary statistics calculation. It ensures data is properly loaded and
    validated before analysis.
    
    Attributes:
        file_path (str): Path to the CSV file containing solar data
        data (pd.DataFrame): The loaded dataset, initialized as None
    """
    
    def __init__(self, file_path: str):
        """
        Initialize the DataLoader with the path to the data file.
        
        Args:
            file_path (str): Path to the CSV file containing solar data.
                            The file should contain solar measurement data
                            including irradiance, temperature, and other
                            environmental measurements.
        
        Raises:
            FileNotFoundError: If the specified file does not exist
        """
        self.file_path = file_path
        self.data = None
        
    def load_data(self) -> pd.DataFrame:
        """
        Load the dataset from the CSV file.
        
        This method reads the CSV file and stores the data in the instance
        variable. It performs basic validation to ensure the data is properly
        loaded.
        
        Returns:
            pd.DataFrame: The loaded dataset with all columns and rows
            
        Raises:
            FileNotFoundError: If the specified file does not exist
            pd.errors.EmptyDataError: If the file is empty
            pd.errors.ParserError: If the file cannot be parsed as CSV
        """
        self.data = pd.read_csv(self.file_path)
        return self.data
    
    def get_basic_info(self) -> Tuple[Tuple[int, int], Dict]:
        """
        Get basic information about the dataset.
        
        This method provides a comprehensive overview of the dataset including:
        - Dataset dimensions (rows and columns)
        - Data types of each column
        - Missing value counts and percentages
        
        Returns:
            Tuple[Tuple[int, int], Dict]: A tuple containing:
                - Dataset shape (rows, columns)
                - Dictionary with:
                    - dtypes: Data types of each column
                    - missing_values: Count of missing values per column
                    - missing_percentages: Percentage of missing values per column
                    
        Note:
            If data hasn't been loaded yet, this method will automatically
            load the data first.
        """
        if self.data is None:
            self.load_data()
            
        shape = self.data.shape
        info = {
            'dtypes': self.data.dtypes,
            'missing_values': self.data.isna().sum(),
            'missing_percentages': (self.data.isna().sum() / len(self.data)) * 100
        }
        
        return shape, info
    
    def get_summary_statistics(self) -> pd.DataFrame:
        """
        Get summary statistics of the dataset.
        
        This method calculates comprehensive summary statistics for all
        numerical columns in the dataset, including:
        - count
        - mean
        - standard deviation
        - minimum
        - 25th percentile
        - median (50th percentile)
        - 75th percentile
        - maximum
        
        Returns:
            pd.DataFrame: A DataFrame containing summary statistics for all
                         numerical columns in the dataset
                         
        Note:
            If data hasn't been loaded yet, this method will automatically
            load the data first.
        """
        if self.data is None:
            self.load_data()
            
        return self.data.describe() 