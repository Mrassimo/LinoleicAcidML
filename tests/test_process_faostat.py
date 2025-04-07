"""
Tests for FAOSTAT data processing functions
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from src.data_processing.process_faostat import (
    FAOSTATRecord,
    convert_to_daily_values,
    harmonize_overlapping_period
)

@pytest.fixture
def sample_faostat_df():
    """Create a sample FAOSTAT DataFrame for testing"""
    return pd.DataFrame({
        'Year': [2010, 2010, 2011],
        'Area': ['Australia'] * 3,
        'Item': ['Wheat'] * 3,
        'Element': ['Food supply quantity'] * 3,
        'Unit': ['kg/capita/yr'] * 3,
        'Value': [100.0, 150.0, 200.0]
    })

@pytest.fixture
def sample_historical_df():
    """Create a sample historical FAOSTAT DataFrame"""
    return pd.DataFrame({
        'Year': [2010, 2011, 2012],
        'Area': ['Australia'] * 3,
        'Item': ['Wheat'] * 3,
        'Element': ['Food supply quantity'] * 3,
        'Unit': ['kg/capita/yr'] * 3,
        'Value': [100.0, 110.0, 120.0]
    })

@pytest.fixture
def sample_modern_df():
    """Create a sample modern FAOSTAT DataFrame"""
    return pd.DataFrame({
        'Year': [2010, 2011, 2013],
        'Area': ['Australia'] * 3,
        'Item': ['Wheat'] * 3,
        'Element': ['Food supply quantity'] * 3,
        'Unit': ['kg/capita/yr'] * 3,
        'Value': [90.0, 100.0, 130.0]
    })

def test_faostat_record_validation():
    """Test FAOSTAT record validation with Pydantic"""
    # Valid record
    valid_record = {
        'Year': 2010,
        'Area': 'Australia',
        'Item': 'Wheat',
        'Element': 'Food supply quantity',
        'Unit': 'kg/capita/yr',
        'Value': 100.0
    }
    record = FAOSTATRecord(**valid_record)
    assert record.Year == 2010
    assert record.Area == 'Australia'
    
    # Invalid year
    with pytest.raises(Exception):
        FAOSTATRecord(**{**valid_record, 'Year': 1900})
    
    # Invalid area
    with pytest.raises(Exception):
        FAOSTATRecord(**{**valid_record, 'Area': 'New Zealand'})
    
    # Invalid value
    with pytest.raises(Exception):
        FAOSTATRecord(**{**valid_record, 'Value': -1.0})

def test_convert_to_daily_values(sample_faostat_df):
    """Test conversion of annual values to daily values"""
    df = convert_to_daily_values(sample_faostat_df)
    
    # Check kg/capita/yr conversion to g/capita/day
    expected_daily_g = 100.0 * 1000 / 365.25
    assert np.isclose(df.iloc[0]['Value'], expected_daily_g)
    assert df.iloc[0]['Unit'] == 'kg/capita/day'
    
    # Check original df wasn't modified
    assert sample_faostat_df.iloc[0]['Unit'] == 'kg/capita/yr'
    assert sample_faostat_df.iloc[0]['Value'] == 100.0

def test_harmonize_overlapping_period(sample_historical_df, sample_modern_df):
    """Test harmonization of overlapping period between historical and modern data"""
    harmonized_df = harmonize_overlapping_period(sample_historical_df, sample_modern_df)
    
    # Check that we have all years
    expected_years = {2010, 2011, 2012, 2013}
    assert set(harmonized_df['Year']) == expected_years
    
    # Check that historical data is used for overlapping years
    overlap_years = {2010, 2011}
    for year in overlap_years:
        historical_value = sample_historical_df[sample_historical_df['Year'] == year]['Value'].iloc[0]
        harmonized_value = harmonized_df[harmonized_df['Year'] == year]['Value'].iloc[0]
        assert historical_value == harmonized_value
    
    # Check that modern data is used for non-overlapping years (2013)
    modern_2013 = sample_modern_df[sample_modern_df['Year'] == 2013]['Value'].iloc[0]
    harmonized_2013 = harmonized_df[harmonized_df['Year'] == 2013]['Value'].iloc[0]
    assert modern_2013 == harmonized_2013 