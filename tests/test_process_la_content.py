"""
Tests for Linoleic Acid content data processing functions
"""

import pytest
import pandas as pd
from pathlib import Path
from src.data_processing.process_la_content import (
    LAContentRecord,
    clean_la_content_data
)

@pytest.fixture
def sample_la_df():
    """Create a sample LA content DataFrame for testing"""
    return pd.DataFrame({
        'food_item': ['Soybean Oil', 'Olive Oil', 'Butter'],
        'linoleic_acid_g_per_100g': [50.0, 10.0, 2.0],
        'extra_column': ['ignore', 'this', 'column']
    })

def test_la_content_record_validation():
    """Test LA content record validation with Pydantic"""
    # Valid record
    valid_record = {
        'food_item': 'Soybean Oil',
        'linoleic_acid_g_per_100g': 50.0
    }
    record = LAContentRecord(**valid_record)
    assert record.food_item == 'Soybean Oil'
    assert record.linoleic_acid_g_per_100g == 50.0
    
    # Invalid food item (empty)
    with pytest.raises(Exception):
        LAContentRecord(**{**valid_record, 'food_item': ''})
    
    # Invalid LA content (negative)
    with pytest.raises(Exception):
        LAContentRecord(**{**valid_record, 'linoleic_acid_g_per_100g': -1.0})
    
    # Invalid LA content (over 100%)
    with pytest.raises(Exception):
        LAContentRecord(**{**valid_record, 'linoleic_acid_g_per_100g': 101.0})

def test_clean_la_content_data(tmp_path, sample_la_df):
    """Test cleaning and validation of LA content data"""
    # Save sample data to temp file
    input_path = tmp_path / 'test_la_content.csv'
    sample_la_df.to_csv(input_path, index=False)
    
    # Process the data
    clean_df = clean_la_content_data(input_path)
    
    # Check that only required columns are present
    expected_cols = {'food_item', 'linoleic_acid_g_per_100g'}
    assert set(clean_df.columns) == expected_cols
    
    # Check that data is sorted by LA content
    assert clean_df['linoleic_acid_g_per_100g'].is_monotonic_decreasing
    
    # Check that all values are present and correct
    assert len(clean_df) == 3
    assert clean_df.iloc[0]['food_item'] == 'Soybean Oil'
    assert clean_df.iloc[0]['linoleic_acid_g_per_100g'] == 50.0

def test_clean_la_content_data_missing_columns(tmp_path):
    """Test handling of missing required columns"""
    # Create DataFrame with missing column
    df = pd.DataFrame({
        'food_item': ['Soybean Oil'],
        'wrong_column': [50.0]
    })
    
    # Save to temp file
    input_path = tmp_path / 'test_la_content_missing_cols.csv'
    df.to_csv(input_path, index=False)
    
    # Check that processing raises error
    with pytest.raises(ValueError, match="Missing required columns"):
        clean_la_content_data(input_path)

def test_clean_la_content_data_missing_values(tmp_path):
    """Test handling of missing values"""
    # Create DataFrame with NaN values
    df = pd.DataFrame({
        'food_item': ['Soybean Oil', None, 'Butter'],
        'linoleic_acid_g_per_100g': [50.0, 10.0, None]
    })
    
    # Save to temp file
    input_path = tmp_path / 'test_la_content_missing_vals.csv'
    df.to_csv(input_path, index=False)
    
    # Process the data
    clean_df = clean_la_content_data(input_path)
    
    # Check that rows with NaN values were dropped
    assert len(clean_df) == 1
    assert clean_df.iloc[0]['food_item'] == 'Soybean Oil' 