import os
import sys
import pandas as pd
import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add src directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.process_raw_data import is_data_sheet, process_excel_file

class TestExcelProcessing:
    """Tests for Excel file processing functionality"""
    
    def setup_method(self):
        """Set up test environment before each test."""
        # Create temporary directories for test data
        self.temp_dir = tempfile.mkdtemp()
        self.raw_dir = Path(self.temp_dir) / "raw"
        self.processed_dir = Path(self.temp_dir) / "processed"
        self.raw_dir.mkdir(exist_ok=True)
        self.processed_dir.mkdir(exist_ok=True)
        
    def teardown_method(self):
        """Clean up after each test."""
        # Remove temporary directory
        shutil.rmtree(self.temp_dir)

    def test_is_data_sheet(self):
        """Test the is_data_sheet function identifies data sheets correctly."""
        # Test sheets that should be identified as data sheets
        assert is_data_sheet("S2.1") is True
        assert is_data_sheet("S3.5") is True
        assert is_data_sheet("All CVD") is True
        assert is_data_sheet("Stroke") is True
        assert is_data_sheet("Heart failure") is True
        assert is_data_sheet("Impact") is True
        
        # Test sheets that should be identified as non-data sheets
        assert is_data_sheet("Contents") is False
        assert is_data_sheet("CONTENTS") is False
        assert is_data_sheet("notes") is False
        assert is_data_sheet("Notes") is False
        assert is_data_sheet("cover") is False
        assert is_data_sheet("Summary") is False
        assert is_data_sheet("sheet1") is False
        assert is_data_sheet("introduction") is False

    @patch('pandas.read_excel')
    @patch('pandas.ExcelFile')
    def test_process_excel_file_multiple_sheets(self, mock_excel_file, mock_read_excel):
        """Test processing multiple sheets from an Excel file."""
        # Set up mock for ExcelFile to list sheet names
        mock_excel_file_instance = MagicMock()
        mock_excel_file_instance.sheet_names = ['Contents', 'S2.1', 'S2.2', 'S2.3']
        mock_excel_file.return_value = mock_excel_file_instance
        
        # Set up mock DataFrames for each sheet
        df1 = pd.DataFrame({
            'Age': ['65-69', '70-74'],
            'Count': [100, 200],
            'Rate': [10.5, 20.5]
        })
        df2 = pd.DataFrame({
            'Region': ['NSW', 'VIC'],
            'Male': [150, 160],
            'Female': [170, 180]
        })
        df3 = pd.DataFrame({
            'Year': [2020, 2021],
            'Total': [300, 350]
        })
        
        # Configure mock read_excel to return different DataFrames for different sheets
        def side_effect(excel_path, sheet_name, header):
            if sheet_name == 'S2.1':
                return df1
            elif sheet_name == 'S2.2':
                return df2
            elif sheet_name == 'S2.3':
                return df3
            return pd.DataFrame()  # Empty DataFrame for non-matching sheets
            
        mock_read_excel.side_effect = side_effect
        
        # Create a test Excel file path
        test_excel_path = Path(self.raw_dir) / "test_data.xlsx"
        with open(test_excel_path, 'w') as f:
            f.write("dummy content")  # Create dummy file
            
        test_csv_path = Path(self.processed_dir) / "test_output.csv"
        
        # Call the function
        result_df = process_excel_file(test_excel_path, test_csv_path)
        
        # Verify ExcelFile was called correctly
        mock_excel_file.assert_called_once_with(test_excel_path)
        
        # Verify read_excel was called for each data sheet
        assert mock_read_excel.call_count == 3
        
        # Verify each sheet was read with the correct parameters
        data_sheets = ['S2.1', 'S2.2', 'S2.3']
        for i, sheet in enumerate(data_sheets):
            call_args = mock_read_excel.call_args_list[i][0]
            call_kwargs = mock_read_excel.call_args_list[i][1]
            assert call_args[0] == test_excel_path
            assert call_kwargs['sheet_name'] == sheet
            assert call_kwargs['header'] == 4
        
        # Verify each DataFrame has the source_sheet column added
        assert 'source_sheet' in result_df.columns
        assert set(result_df['source_sheet'].unique()) == set(data_sheets)
        
        # Verify the total number of rows is the sum of rows from each sheet
        assert len(result_df) == len(df1) + len(df2) + len(df3)

    @patch('pandas.read_excel')
    @patch('pandas.ExcelFile')
    def test_process_excel_file_skips_empty_sheets(self, mock_excel_file, mock_read_excel):
        """Test that empty sheets are skipped during processing."""
        # Set up mock for ExcelFile to list sheet names
        mock_excel_file_instance = MagicMock()
        mock_excel_file_instance.sheet_names = ['Contents', 'S2.1', 'S2.2', 'Empty']
        mock_excel_file.return_value = mock_excel_file_instance
        
        # Set up mock DataFrames - one normal, one empty
        df1 = pd.DataFrame({
            'Age': ['65-69', '70-74'],
            'Count': [100, 200],
            'Rate': [10.5, 20.5]
        })
        df2 = pd.DataFrame({
            'Region': ['NSW', 'VIC'],
            'Male': [150, 160],
            'Female': [170, 180]
        })
        empty_df = pd.DataFrame()  # Empty DataFrame
        
        # Configure mock read_excel to return different DataFrames for different sheets
        def side_effect(excel_path, sheet_name, header):
            if sheet_name == 'S2.1':
                return df1
            elif sheet_name == 'S2.2':
                return df2
            elif sheet_name == 'Empty':
                return empty_df
            return pd.DataFrame()
            
        mock_read_excel.side_effect = side_effect
        
        # Create a test Excel file path
        test_excel_path = Path(self.raw_dir) / "test_data.xlsx"
        with open(test_excel_path, 'w') as f:
            f.write("dummy content")  # Create dummy file
            
        test_csv_path = Path(self.processed_dir) / "test_output.csv"
        
        # Call the function
        result_df = process_excel_file(test_excel_path, test_csv_path)
        
        # Verify read_excel was called for each data sheet (3 times, including the Empty sheet)
        assert mock_read_excel.call_count == 3
        
        # Verify only non-empty sheets appear in the source_sheet column
        assert 'source_sheet' in result_df.columns
        assert set(result_df['source_sheet'].unique()) == {'S2.1', 'S2.2'}
        
        # Verify the total number of rows is only the sum of non-empty sheets
        assert len(result_df) == len(df1) + len(df2)
