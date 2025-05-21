import unittest
import pandas as pd
import numpy as np
from pathlib import Path
from utils import validate_dataframe, load_cleaned_data

class TestDataValidation(unittest.TestCase):
    def setUp(self):
        # Create sample data for testing
        self.valid_data = pd.DataFrame({
            'GHI': [100, 200, 300],
            'DNI': [150, 250, 350],
            'DHI': [50, 150, 250]
        })
        
        self.invalid_data = pd.DataFrame({
            'GHI': [100, -200, 300],  # Contains negative value
            'DNI': [150, np.nan, 350],  # Contains missing value
            'DHI': [50, 150, 250]
        })
    
    def test_validate_dataframe_valid(self):
        """Test validation with valid data"""
        result = validate_dataframe(self.valid_data, "Test Country")
        self.assertTrue(result)
    
    def test_validate_dataframe_invalid(self):
        """Test validation with invalid data"""
        result = validate_dataframe(self.invalid_data, "Test Country")
        self.assertFalse(result)
    
    def test_validate_dataframe_missing_columns(self):
        """Test validation with missing required columns"""
        invalid_data = self.valid_data.drop('GHI', axis=1)
        result = validate_dataframe(invalid_data, "Test Country")
        self.assertFalse(result)

class TestDataLoading(unittest.TestCase):
    def test_load_cleaned_data(self):
        """Test loading of cleaned data"""
        try:
            data = load_cleaned_data()
            self.assertIsInstance(data, dict)
            self.assertTrue(all(isinstance(df, pd.DataFrame) for df in data.values()))
            self.assertTrue(all('GHI' in df.columns for df in data.values()))
        except FileNotFoundError:
            self.skipTest("Data files not found")

if __name__ == '__main__':
    unittest.main() 