"""
Unit tests for the ABS population data processing script.
"""

import pytest
import pandas as pd
from pathlib import Path
import os
import logging
from unittest.mock import patch, MagicMock

# Import the function to test (assuming it's callable and runnable)
from src.data_processing.process_abs_population import process_abs_population_data

# Mock the config module before importing the script that uses it
@pytest.fixture(autouse=True)
def mock_config_paths(tmp_path):
    # Create dummy directories for raw, processed, staging
    raw_dir = tmp_path / "data" / "raw"
    processed_dir = tmp_path / "data" / "processed"
    staging_dir = tmp_path / "data" / "staging"
    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)
    staging_dir.mkdir(parents=True, exist_ok=True)

    # Define mock config attributes
    mock_config = MagicMock()
    mock_config.RAW_DATA_DIR = raw_dir
    mock_config.PROCESSED_DATA_DIR = processed_dir
    mock_config.STAGING_DATA_DIR = staging_dir
    mock_config.ABS_POPULATION_FILENAME = "test_abs_pop.xlsx"

    # Use patch to replace the config object in the target module's namespace
    with patch('src.data_processing.process_abs_population.config', mock_config):
        yield # Allow the test to run with the mocked config

# Fixture to create a dummy ABS Excel file for testing
@pytest.fixture
def create_dummy_abs_excel(mock_config_paths):
    raw_file_path = mock_config_paths.RAW_DATA_DIR / mock_config_paths.ABS_POPULATION_FILENAME
    staging_file_path = mock_config_paths.STAGING_DATA_DIR / "abs_population_processed.csv"
    
    # Create a realistic dummy dataframe (including metadata rows and quarterly data)
    header_rows = pd.DataFrame([['Unit', 'Persons', 'Persons']], columns=['A', 'B', 'C']) # Simplified
    metadata_rows = pd.DataFrame([['Series Type', 'Original', 'Original']], columns=['A', 'B', 'C']) # Simplified
    # ... add more metadata rows to total 9 ...
    for i in range(7):
         metadata_rows = pd.concat([metadata_rows, pd.DataFrame([[f'Meta{i}', f'Val{i}', f'Val{i}']], columns=['A', 'B', 'C'])], ignore_index=True)

    data = {
        'Date': pd.to_datetime([
            '2020-06-01', '2020-09-01', '2020-12-01',
            '2021-03-01', '2021-06-01', '2021-09-01', '2021-12-01',
            '2022-03-01', '2022-06-01', '2022-09-01', '2022-12-01', 
            'Bad Date', # Add a bad date to test coercion
            '2023-12-01'
        ]),
        'Other Col': range(13),
        # Need 28 cols total, fill others, place population at index 27
        **{f'Col{i}': range(13) for i in range(2, 28)},
        'Australia Pop': [25000000 + i*1000 for i in range(13)]
    }
    data_df = pd.DataFrame(data)
    # Reorder columns to match expected indices (Date=0, Pop=27)
    cols = list(data_df.columns)
    date_col = cols.pop(cols.index('Date'))
    pop_col = cols.pop(cols.index('Australia Pop'))
    final_cols = [date_col] + cols + [pop_col]
    data_df = data_df[final_cols]
    
    # Concatenate headers and data
    full_df = pd.concat([header_rows, metadata_rows, data_df], ignore_index=True)

    # Save to dummy Excel file with the correct sheet name
    # Note: Using default header=True here to write headers, but process script uses header=None
    with pd.ExcelWriter(raw_file_path, engine='openpyxl') as writer:
        full_df.to_excel(writer, sheet_name='Data1', index=False, header=False) # Write without headers in excel

    return raw_file_path, staging_file_path


def test_process_abs_population_success(create_dummy_abs_excel, caplog):
    """Test successful processing of a valid ABS population file."""
    caplog.set_level(logging.INFO)
    raw_file_path, staging_file_path = create_dummy_abs_excel

    # Run the processor
    process_abs_population_data()

    # Assertions
    assert staging_file_path.exists(), "Staging file should be created"
    log_output = caplog.text
    assert "Successfully processed and saved data" in log_output
    assert "Filtered data to keep only December quarter rows" in log_output

    # Check content of the output CSV
    result_df = pd.read_csv(staging_file_path)
    assert list(result_df.columns) == ['Year', 'Population']
    assert len(result_df) == 4, "Should only contain 4 December rows (2020, 2021, 2022, 2023)"
    assert result_df['Year'].tolist() == [2020, 2021, 2022, 2023]
    # Check population for Dec 2021 (index 6 in original data, pop = 25000000 + 6*1000)
    assert result_df[result_df['Year'] == 2021]['Population'].iloc[0] == 25006000
    # Check population for Dec 2022 (index 10 in original data, pop = 25000000 + 10*1000)
    assert result_df[result_df['Year'] == 2022]['Population'].iloc[0] == 25010000 
    # Check population for Dec 2023 (index 12 in original data, pop = 25000000 + 12*1000)
    assert result_df[result_df['Year'] == 2023]['Population'].iloc[0] == 25012000 
    assert "Coerced 1 non-date values to NaT" in log_output # Check bad date handling

def test_process_abs_population_file_not_found(mock_config_paths, caplog):
    """Test handling when the raw input file is missing."""
    caplog.set_level(logging.ERROR)
    # Ensure file does not exist
    raw_file_path = mock_config_paths.RAW_DATA_DIR / mock_config_paths.ABS_POPULATION_FILENAME
    if raw_file_path.exists():
        raw_file_path.unlink()
        
    process_abs_population_data()
    
    assert "Raw ABS population file not found" in caplog.text
    assert not (mock_config_paths.STAGING_DATA_DIR / "abs_population_processed.csv").exists()

@patch('src.data_processing.process_abs_population.EXPECTED_SHEET_NAME', 'WrongSheetName')
def test_process_abs_population_wrong_sheet(create_dummy_abs_excel, caplog):
    """Test handling when the expected sheet name is incorrect."""
    caplog.set_level(logging.ERROR)
    raw_file_path, staging_file_path = create_dummy_abs_excel

    process_abs_population_data()

    assert "Data processing error: Worksheet named 'WrongSheetName' not found" in caplog.text
    assert not staging_file_path.exists()

# Add more tests for edge cases if needed, e.g.:
# - Test with different header/skiprows combinations if format varies.
# - Test with all dates being invalid.
# - Test with population column having non-numeric data.
# - Test with fewer than expected columns. 