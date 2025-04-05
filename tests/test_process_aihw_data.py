"""Tests for the AIHW data processing module."""

import pytest
import pandas as pd
import os
from datetime import datetime
from src.process_aihw_data import (
    find_header_row,
    clean_column_name,
    transform_sheet_data,
    process_aihw_excel,
    validate_data
)
from src.models.aihw_models import MetricType

@pytest.fixture
def sample_df():
    """Create a sample DataFrame for testing."""
    data = {
        'Column1': ['Header1', 'Value1', 'Value2'],
        'Column2': ['Year', 'Value3', 'Value4'],
        'Column3': ['Sex', 'Value5', 'Value6']
    }
    return pd.DataFrame(data)

@pytest.fixture
def valid_aihw_df():
    """Create a sample DataFrame with valid AIHW data."""
    data = {
        'year': [2020, 2021],
        'value': [5.2, 5.5],
        'metric_type': [MetricType.PREVALENCE, MetricType.PREVALENCE],
        'source_sheet': ['Sheet1', 'Sheet1'],
        'sex': ['male', 'female'],
        'age': ['65+', '65+'],
        'region': ['australia', 'victoria'],
        'rate': [5.2, 5.5]
    }
    return pd.DataFrame(data)

@pytest.fixture
def invalid_aihw_df():
    """Create a sample DataFrame with invalid AIHW data."""
    data = {
        'year': [1800, 2025],  # Invalid years
        'value': ['invalid', 5.5],  # Invalid value type
        'metric_type': ['unknown', MetricType.PREVALENCE],  # Invalid metric type
        'source_sheet': ['Sheet1', 'Sheet1'],
        'sex': ['invalid', 'female'],  # Invalid sex value
        'age': ['65+', '65+'],
        'region': ['invalid', 'victoria'],  # Invalid region
        'rate': [5.2, 5.5]
    }
    return pd.DataFrame(data)

def test_find_header_row(sample_df):
    """Test header row detection."""
    # Should find row 0 as it contains 'Year' and 'Sex'
    assert find_header_row(sample_df) == 0
    
    # Test with no header row
    df_no_header = pd.DataFrame({
        'A': [1, 2, 3],
        'B': [4, 5, 6]
    })
    assert find_header_row(df_no_header) is None

def test_clean_column_name():
    """Test column name cleaning."""
    test_cases = [
        ('Aboriginal and Torres Strait Islander', 'indigenous'),
        ('State/Territory', 'region'),
        ('Age Group', 'age'),
        ('Gender', 'sex'),
        ('Rate (%)', 'rate'),
        ('Number of Deaths', 'number'),
        ('Some Random Column!@#', 'some_random_column'),
        ('  Spaces  Around  ', 'spaces_around')
    ]
    
    for input_name, expected in test_cases:
        assert clean_column_name(input_name) == expected

def test_transform_sheet_data():
    """Test sheet data transformation."""
    # Create a sample DataFrame that mimics an AIHW sheet
    data = {
        'Year': [2020, 2021],
        'Age Group': ['65+', '65+'],
        'Rate (%)': ['5.2%', '5.5%'],
        'Number of Deaths': ['100', '110']
    }
    df = pd.DataFrame(data)
    
    # Transform the data
    result = transform_sheet_data(df, 'Mortality_Sheet')
    
    # Check transformations
    assert 'year' in result.columns
    assert 'age' in result.columns
    assert 'rate' in result.columns
    assert 'number' in result.columns
    assert 'source_sheet' in result.columns
    assert 'metric_type' in result.columns
    assert 'value' in result.columns  # New test for value column
    
    # Check data type conversions
    assert pd.api.types.is_numeric_dtype(result['year'])
    assert pd.api.types.is_numeric_dtype(result['rate'])
    assert pd.api.types.is_numeric_dtype(result['number'])
    assert pd.api.types.is_numeric_dtype(result['value'])
    
    # Check metadata
    assert result['source_sheet'].iloc[0] == 'Mortality_Sheet'
    assert result['metric_type'].iloc[0] == MetricType.MORTALITY

def test_validate_data_valid(valid_aihw_df):
    """Test validation with valid data."""
    result = validate_data(valid_aihw_df, "test.xlsx")
    
    # Check that validation succeeded
    assert len(result.records) == len(valid_aihw_df)
    assert result.source_file == "test.xlsx"
    assert isinstance(result.processed_date, datetime)
    
    # Check that all records were properly validated
    for record in result.records:
        assert record.year >= 1900
        assert isinstance(record.value, float)
        assert record.metric_type == MetricType.PREVALENCE
        assert record.sex in {'male', 'female'}
        assert record.region in {'australia', 'victoria'}

def test_validate_data_invalid(invalid_aihw_df):
    """Test validation with invalid data."""
    result = validate_data(invalid_aihw_df, "test.xlsx")
    
    # Check that invalid records were filtered out
    assert len(result.records) < len(invalid_aihw_df)
    
    # Check that remaining records are valid
    for record in result.records:
        assert record.year >= 1900 and record.year <= datetime.now().year
        assert isinstance(record.value, float)
        assert record.metric_type in MetricType
        if record.sex:
            assert record.sex in {'male', 'female', 'all', 'persons', 'total'}
        if record.region:
            assert record.region in {'victoria', 'australia', 'total'}

@pytest.fixture
def temp_excel_file(tmp_path):
    """Create a temporary Excel file for testing."""
    file_path = tmp_path / "test.xlsx"
    
    # Create test data
    sheet1_data = pd.DataFrame({
        'Year': [2020, 2021],
        'Age Group': ['65+', '65+'],
        'Rate (%)': ['5.2%', '5.5%']
    })
    
    sheet2_data = pd.DataFrame({
        'Year': [2020, 2021],
        'Gender': ['Male', 'Female'],
        'Number of Deaths': [100, 110]
    })
    
    # Create Excel writer object
    with pd.ExcelWriter(file_path) as writer:
        sheet1_data.to_excel(writer, sheet_name='Prevalence', index=False)
        sheet2_data.to_excel(writer, sheet_name='Mortality', index=False)
    
    return file_path

def test_process_aihw_excel(temp_excel_file, tmp_path):
    """Test full Excel file processing."""
    output_path = tmp_path / "output.csv"
    
    # Process the test Excel file
    process_aihw_excel(temp_excel_file, output_path)
    
    # Check that output file exists
    assert os.path.exists(output_path)
    
    # Read and check the output
    result = pd.read_csv(output_path)
    
    # Check that we have data from both sheets
    assert len(result) > 0
    assert 'source_sheet' in result.columns
    assert set(result['source_sheet'].unique()) == {'Prevalence', 'Mortality'}
    
    # Check that column names are standardised
    expected_columns = {'year', 'value', 'metric_type', 'source_sheet', 
                       'sex', 'age', 'rate', 'number'}
    assert expected_columns.issubset(set(result.columns))
    
    # Check that data types are correct
    assert pd.api.types.is_numeric_dtype(result['year'])
    assert pd.api.types.is_numeric_dtype(result['value'])
    if 'rate' in result.columns:
        assert pd.api.types.is_numeric_dtype(result['rate'])
    if 'number' in result.columns:
        assert pd.api.types.is_numeric_dtype(result['number']) 