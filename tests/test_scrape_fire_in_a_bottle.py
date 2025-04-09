import unittest
import pandas as pd
import os
import sys
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path

# Add the src directory to the system path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_processing.scrape_fire_in_bottle import (
    parse_markdown_content,
    extract_food_data,
    process_linoleic_acid_data,
    save_to_csv
)

class TestScrapeFireInABottle(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.sample_markdown = """
# Foods Highest and Lowest in Linoleic Acid (n-6 PUFA)

## Foods Highest in LA

| Food | LA Cal | Total Cal | % Cal from LA |
|------|--------|-----------|---------------|
| Sunflower Oil | 120 | 124 | 97% |
| Corn Oil | 95 | 120 | 79% |

## Foods Lowest in LA

| Food | LA Cal | Total Cal | % Cal from LA |
|------|--------|-----------|---------------|
| Butter | 3 | 100 | 3% |
| Beef Tallow | 4 | 120 | 3.3% |
"""
        
        self.expected_high_foods = [
            {'food_name': 'Sunflower Oil', 'la_cal': 120, 'cal': 124, 'la_perc': 97.0},
            {'food_name': 'Corn Oil', 'la_cal': 95, 'cal': 120, 'la_perc': 79.0}
        ]
        
        self.expected_low_foods = [
            {'food_name': 'Butter', 'la_cal': 3, 'cal': 100, 'la_perc': 3.0},
            {'food_name': 'Beef Tallow', 'la_cal': 4, 'cal': 120, 'la_perc': 3.3}
        ]

    def test_parse_markdown_content_success(self):
        """Test successful parsing of markdown content"""
        with patch('builtins.open', mock_open(read_data=self.sample_markdown)):
            high_foods, low_foods = parse_markdown_content('dummy_file.md')
            
            # Verify high foods data
            self.assertEqual(len(high_foods), 2)
            self.assertIn('| Sunflower Oil | 120 | 124 | 97% |', high_foods)
            self.assertIn('| Corn Oil | 95 | 120 | 79% |', high_foods)
            
            # Verify low foods data
            self.assertEqual(len(low_foods), 2)
            self.assertIn('| Butter | 3 | 100 | 3% |', low_foods)
            self.assertIn('| Beef Tallow | 4 | 120 | 3.3% |', low_foods)

    def test_parse_markdown_content_empty_file(self):
        """Test parsing of empty markdown file"""
        with patch('builtins.open', mock_open(read_data="")):
            high_foods, low_foods = parse_markdown_content('dummy_file.md')
            
            # Both lists should be empty
            self.assertEqual(len(high_foods), 0)
            self.assertEqual(len(low_foods), 0)

    def test_parse_markdown_content_missing_sections(self):
        """Test parsing of markdown with missing sections"""
        markdown_missing_sections = """
# Foods Highest and Lowest in Linoleic Acid (n-6 PUFA)

Some text without tables.
"""
        with patch('builtins.open', mock_open(read_data=markdown_missing_sections)):
            high_foods, low_foods = parse_markdown_content('dummy_file.md')
            
            # Both lists should be empty since no tables are present
            self.assertEqual(len(high_foods), 0)
            self.assertEqual(len(low_foods), 0)

    def test_extract_food_data_success(self):
        """Test successful extraction of food data from table rows"""
        sample_rows = [
            '| Food | LA Cal | Total Cal | % Cal from LA |',
            '|------|--------|-----------|---------------|',
            '| Sunflower Oil | 120 | 124 | 97% |',
            '| Corn Oil | 95 | 120 | 79% |'
        ]
        
        result = extract_food_data(sample_rows)
        
        # Verify result
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['food_name'], 'Sunflower Oil')
        self.assertEqual(result[0]['la_cal'], 120)
        self.assertEqual(result[0]['cal'], 124)
        self.assertEqual(result[0]['la_perc'], 97.0)
        
        self.assertEqual(result[1]['food_name'], 'Corn Oil')
        self.assertEqual(result[1]['la_cal'], 95)
        self.assertEqual(result[1]['cal'], 120)
        self.assertEqual(result[1]['la_perc'], 79.0)

    def test_extract_food_data_empty_rows(self):
        """Test extraction of food data from empty rows"""
        result = extract_food_data([])
        
        # Result should be an empty list
        self.assertEqual(len(result), 0)

    def test_extract_food_data_invalid_format(self):
        """Test extraction of food data from invalid format rows"""
        invalid_rows = [
            '| Food | LA Cal | Total Cal |',  # Missing column
            '|------|--------|-----------|',
            '| Sunflower Oil | 120 | 124 |'
        ]
        
        result = extract_food_data(invalid_rows)
        
        # Result should be empty as format is invalid
        self.assertEqual(len(result), 0)

    def test_process_linoleic_acid_data_success(self):
        """Test successful processing of linoleic acid data"""
        with patch('src.scrape_fire_in_a_bottle.parse_markdown_content') as mock_parse:
            # Configure mock to return our predefined data
            mock_parse.return_value = (
                self.expected_high_foods,
                self.expected_low_foods
            )
            
            result_df = process_linoleic_acid_data('dummy_file.md')
            
            # Verify result
            self.assertIsInstance(result_df, pd.DataFrame)
            self.assertEqual(len(result_df), 4)  # 2 high + 2 low foods
            self.assertTrue(all(col in result_df.columns for col in ['food_name', 'la_cal', 'cal', 'la_perc']))
            
            # Check if high and low foods are correctly included
            self.assertTrue('Sunflower Oil' in result_df['food_name'].values)
            self.assertTrue('Butter' in result_df['food_name'].values)

    def test_process_linoleic_acid_data_empty(self):
        """Test processing when no data is available"""
        with patch('src.scrape_fire_in_a_bottle.parse_markdown_content') as mock_parse:
            # Configure mock to return empty data
            mock_parse.return_value = ([], [])
            
            result_df = process_linoleic_acid_data('dummy_file.md')
            
            # Result should be an empty DataFrame
            self.assertIsInstance(result_df, pd.DataFrame)
            self.assertTrue(result_df.empty)

    def test_save_to_csv_success(self):
        """Test successful saving of data to CSV"""
        test_df = pd.DataFrame(self.expected_high_foods + self.expected_low_foods)
        
        with patch('pandas.DataFrame.to_csv') as mock_to_csv:
            save_to_csv(test_df, 'output.csv')
            
            # Verify that to_csv was called once with the correct arguments
            mock_to_csv.assert_called_once()
            # Check that the first positional arg (file path) is 'output.csv'
            self.assertEqual(mock_to_csv.call_args[0][0], 'output.csv')

    def test_save_to_csv_empty_dataframe(self):
        """Test saving an empty DataFrame to CSV"""
        empty_df = pd.DataFrame()
        
        with patch('pandas.DataFrame.to_csv') as mock_to_csv:
            save_to_csv(empty_df, 'output_empty.csv')
            
            # Verify that to_csv was called once
            mock_to_csv.assert_called_once()

    def test_data_validation(self):
        """Test data validation for processed data"""
        # Create a DataFrame with valid and invalid data
        test_data = pd.DataFrame([
            {'food_name': 'Sunflower Oil', 'la_cal': 120, 'cal': 124, 'la_perc': 97.0},  # Valid
            {'food_name': 'Invalid Oil', 'la_cal': -5, 'cal': 0, 'la_perc': 150.0},      # Invalid
            {'food_name': '', 'la_cal': None, 'cal': 100, 'la_perc': 10.0}               # Invalid
        ])
        
        # Filter out invalid entries
        valid_data = test_data[
            (test_data['food_name'] != '') & 
            (test_data['la_cal'] > 0) & 
            (test_data['cal'] > 0) & 
            (test_data['la_perc'] >= 0) & 
            (test_data['la_perc'] <= 100)
        ]
        
        # Verify only valid data remains
        self.assertEqual(len(valid_data), 1)
        self.assertEqual(valid_data.iloc[0]['food_name'], 'Sunflower Oil')

if __name__ == '__main__':
    unittest.main() 