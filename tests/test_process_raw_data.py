import unittest
import pandas as pd
import numpy as np
import os
import sys
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path

# Add the src directory to the system path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.process_raw_data import (
    process_ncdrisc_data, 
    process_aihw_excel_file, 
    process_all_raw_data,
    extract_sheet_data
)

class TestProcessRawData(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.test_ncdrisc_data = pd.DataFrame({
            'Country': ['Australia', 'Australia'],
            'Sex': ['Men', 'Women'],
            'Year': [2000, 2000],
            'Mean BMI': [25.0, 24.0],
            'Lower 95% uncertainty interval': [24.0, 23.0],
            'Upper 95% uncertainty interval': [26.0, 25.0]
        })
        
        # Create sample Excel mock data structure
        self.mock_excel_sheets = {
            'Table 1': pd.DataFrame({
                'Year': [2010, 2011, 2012],
                'Value': [10, 11, 12],
                'Category': ['A', 'B', 'C']
            }),
            'Table 2': pd.DataFrame({
                'Year': [2010, 2011, 2012],
                'Value': [20, 21, 22],
                'Category': ['X', 'Y', 'Z']
            }),
            'Instructions': pd.DataFrame({
                'Notes': ['This is a notes sheet']
            })
        }

    @patch('pandas.read_csv')
    def test_process_ncdrisc_data_success(self, mock_read_csv):
        """Test successful processing of NCD-RisC data"""
        mock_read_csv.return_value = self.test_ncdrisc_data
        
        result = process_ncdrisc_data('dummy_file.csv')
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 2)
        self.assertIn('Mean BMI', result.columns)
        mock_read_csv.assert_called_once()

    @patch('pandas.read_csv')
    def test_process_ncdrisc_data_empty(self, mock_read_csv):
        """Test processing empty NCD-RisC data"""
        mock_read_csv.return_value = pd.DataFrame()
        
        result = process_ncdrisc_data('dummy_file.csv')
        
        self.assertTrue(result.empty)
        mock_read_csv.assert_called_once()

    @patch('pandas.read_csv')
    def test_process_ncdrisc_data_missing_columns(self, mock_read_csv):
        """Test processing NCD-RisC data with missing columns"""
        # DataFrame missing the Mean BMI column
        mock_read_csv.return_value = pd.DataFrame({
            'Country': ['Australia', 'Australia'],
            'Sex': ['Men', 'Women'],
            'Year': [2000, 2000]
        })
        
        result = process_ncdrisc_data('dummy_file.csv')
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertNotIn('Mean BMI', result.columns)
        mock_read_csv.assert_called_once()

    @patch('pandas.ExcelFile')
    def test_extract_sheet_data(self, mock_excel_file):
        """Test extracting data from Excel sheets"""
        # Configure the mock to return our predefined sheets
        mock_excel = MagicMock()
        mock_excel.sheet_names = list(self.mock_excel_sheets.keys())
        mock_excel_file.return_value.__enter__.return_value = mock_excel
        
        # Mock the pd.read_excel function to return our dataframes based on sheet name
        with patch('pandas.read_excel', side_effect=lambda *args, **kwargs: 
                   self.mock_excel_sheets.get(kwargs.get('sheet_name', 'Table 1'))):
            
            result = extract_sheet_data('dummy.xlsx', include_pattern='Table')
            
            # Check that only 'Table' sheets were processed
            self.assertEqual(len(result), 2)  # Two tables should be extracted
            self.assertIn('Table 1', result)
            self.assertIn('Table 2', result)
            self.assertNotIn('Instructions', result)

    @patch('pandas.ExcelFile')
    def test_process_aihw_excel_file_success(self, mock_excel_file):
        """Test successful processing of AIHW Excel file"""
        # Configure the mock to return our predefined sheets
        mock_excel = MagicMock()
        mock_excel.sheet_names = list(self.mock_excel_sheets.keys())
        mock_excel_file.return_value.__enter__.return_value = mock_excel
        
        # Mock the pd.read_excel function
        with patch('pandas.read_excel', side_effect=lambda *args, **kwargs: 
                   self.mock_excel_sheets.get(kwargs.get('sheet_name', 'Table 1'))):
            
            result = process_aihw_excel_file('dummy.xlsx', 'output.csv', 'Table')
            
            # Verify results
            self.assertTrue(os.path.exists('output.csv'))
            mock_excel_file.assert_called_once()

    @patch('pandas.ExcelFile')
    def test_process_aihw_excel_file_no_matching_sheets(self, mock_excel_file):
        """Test processing AIHW Excel file with no matching sheets"""
        # Configure the mock with sheets that don't match the pattern
        mock_excel = MagicMock()
        mock_excel.sheet_names = ['Summary', 'Notes', 'Instructions']
        mock_excel_file.return_value.__enter__.return_value = mock_excel
        
        # Mock the pd.read_excel function
        with patch('pandas.read_excel', return_value=pd.DataFrame()):
            
            # Should return an empty DataFrame if no matching sheets
            result = process_aihw_excel_file('dummy.xlsx', 'output_empty.csv', 'Table')
            
            # Verify results
            self.assertFalse(os.path.exists('output_empty.csv'))  # No file should be written
            mock_excel_file.assert_called_once()

    @patch('src.process_raw_data.process_ncdrisc_data')
    @patch('src.process_raw_data.process_aihw_excel_file')
    def test_process_all_raw_data(self, mock_process_aihw, mock_process_ncdrisc):
        """Test the process_all_raw_data function"""
        # Set up mocks
        mock_process_ncdrisc.return_value = pd.DataFrame({'test': [1, 2, 3]})
        mock_process_aihw.return_value = True
        
        with patch('os.path.exists', return_value=True):
            result = process_all_raw_data()
            
            # Check that the processing functions were called
            self.assertTrue(mock_process_ncdrisc.called)
            self.assertTrue(mock_process_aihw.called)

    @patch('pandas.read_csv', side_effect=Exception("File not found"))
    def test_process_ncdrisc_data_exception(self, mock_read_csv):
        """Test handling of exceptions in process_ncdrisc_data"""
        with self.assertRaises(Exception):
            process_ncdrisc_data('nonexistent_file.csv')

    @patch('pandas.ExcelFile', side_effect=Exception("File not found"))
    def test_process_aihw_excel_file_exception(self, mock_excel_file):
        """Test handling of exceptions in process_aihw_excel_file"""
        with self.assertRaises(Exception):
            process_aihw_excel_file('nonexistent_file.xlsx', 'output.csv', 'Table')

if __name__ == '__main__':
    unittest.main() 