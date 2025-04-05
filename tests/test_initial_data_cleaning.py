import unittest
import pandas as pd
import numpy as np
import os
import sys
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add the src directory to the system path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.initial_data_cleaning import (
    check_missing_percentage,
    standardise_column_names,
    check_data_types,
    perform_initial_cleaning
)

class TestInitialDataCleaning(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        # Create sample dataframes for testing
        self.test_df_clean = pd.DataFrame({
            'Food Name': ['Oil', 'Butter'],
            'Value (%)': [95.0, 3.0],
            'Year': [2020, 2021]
        })
        
        self.test_df_missing = pd.DataFrame({
            'Food Name': ['Oil', None, 'Butter', None],
            'Value (%)': [95.0, None, 3.0, None],
            'Year': [2020, 2021, None, 2023]
        })
        
        self.test_df_mixed_types = pd.DataFrame({
            'Food Name': ['Oil', 'Butter'],
            'Value (%)': ['95.0%', '3.0%'],
            'Year': ['2020', 2021]
        })

    def test_check_missing_percentage_no_missing(self):
        """Test check_missing_percentage with no missing values"""
        result = check_missing_percentage(self.test_df_clean)
        
        # Verify all columns have 0% missing
        self.assertEqual(result['Food Name'], 0.0)
        self.assertEqual(result['Value (%)'], 0.0)
        self.assertEqual(result['Year'], 0.0)

    def test_check_missing_percentage_with_missing(self):
        """Test check_missing_percentage with missing values"""
        result = check_missing_percentage(self.test_df_missing)
        
        # Verify correct missing percentages
        self.assertEqual(result['Food Name'], 50.0)  # 2 out of 4 are missing
        self.assertEqual(result['Value (%)'], 50.0)  # 2 out of 4 are missing
        self.assertEqual(result['Year'], 25.0)       # 1 out of 4 is missing

    def test_standardise_column_names(self):
        """Test standardise_column_names function"""
        # Create DataFrame with mixed case and spaces
        df = pd.DataFrame({
            'Food Name': ['Oil', 'Butter'],
            'Value (%)': [95.0, 3.0],
            'YEAR': [2020, 2021]
        })
        
        result = standardise_column_names(df)
        
        # Verify column names are standardized
        expected_columns = ['food_name', 'value_percent', 'year']
        self.assertListEqual(list(result.columns), expected_columns)

    def test_check_data_types(self):
        """Test check_data_types function"""
        result = check_data_types(self.test_df_clean)
        
        # Verify data types
        self.assertEqual(result['Food Name'], 'object')
        self.assertEqual(result['Value (%)'], 'float64')
        self.assertEqual(result['Year'], 'int64')

    def test_check_data_types_mixed(self):
        """Test check_data_types with mixed types"""
        result = check_data_types(self.test_df_mixed_types)
        
        # Verify data types
        self.assertEqual(result['Food Name'], 'object')
        self.assertEqual(result['Value (%)'], 'object')  # String values
        self.assertEqual(result['Year'], 'object')       # Mixed int/string

    @patch('pandas.read_csv')
    def test_perform_initial_cleaning_success(self, mock_read_csv):
        """Test perform_initial_cleaning with successful data"""
        # Configure mock to return our test DataFrame
        mock_read_csv.return_value = self.test_df_clean
        
        with patch('builtins.print') as mock_print:
            result = perform_initial_cleaning('dummy_file.csv')
            
            # Verify function was called and returned our DataFrame
            mock_read_csv.assert_called_once()
            self.assertIsInstance(result, pd.DataFrame)
            self.assertEqual(len(result), 2)
            
            # Verify that print was called for output
            mock_print.assert_called()

    @patch('pandas.read_csv')
    def test_perform_initial_cleaning_with_missing(self, mock_read_csv):
        """Test perform_initial_cleaning with missing data"""
        # Configure mock to return DataFrame with missing values
        mock_read_csv.return_value = self.test_df_missing
        
        with patch('builtins.print') as mock_print:
            result = perform_initial_cleaning('dummy_file.csv')
            
            # Verify function was called and returned our DataFrame
            mock_read_csv.assert_called_once()
            self.assertIsInstance(result, pd.DataFrame)
            self.assertEqual(len(result), 4)
            
            # Verify that print was called for missing values
            mock_print.assert_called()

    @patch('pandas.read_csv')
    def test_perform_initial_cleaning_with_mixed_types(self, mock_read_csv):
        """Test perform_initial_cleaning with mixed data types"""
        # Configure mock to return DataFrame with mixed types
        mock_read_csv.return_value = self.test_df_mixed_types
        
        with patch('builtins.print') as mock_print:
            result = perform_initial_cleaning('dummy_file.csv')
            
            # Verify function was called and returned our DataFrame
            mock_read_csv.assert_called_once()
            self.assertIsInstance(result, pd.DataFrame)
            self.assertEqual(len(result), 2)
            
            # Verify that print was called for data types
            mock_print.assert_called()

    @patch('pandas.read_csv', side_effect=Exception("File not found"))
    def test_perform_initial_cleaning_exception(self, mock_read_csv):
        """Test perform_initial_cleaning with exception"""
        with self.assertRaises(Exception):
            perform_initial_cleaning('nonexistent_file.csv')

    def test_standardise_column_names_empty_df(self):
        """Test standardise_column_names with empty DataFrame"""
        empty_df = pd.DataFrame()
        result = standardise_column_names(empty_df)
        
        # Should return an empty DataFrame
        self.assertTrue(result.empty)

    def test_check_missing_percentage_empty_df(self):
        """Test check_missing_percentage with empty DataFrame"""
        empty_df = pd.DataFrame()
        result = check_missing_percentage(empty_df)
        
        # Should return an empty dictionary
        self.assertEqual(result, {})

    def test_check_data_types_empty_df(self):
        """Test check_data_types with empty DataFrame"""
        empty_df = pd.DataFrame()
        result = check_data_types(empty_df)
        
        # Should return an empty dictionary
        self.assertEqual(result, {})

if __name__ == '__main__':
    unittest.main() 