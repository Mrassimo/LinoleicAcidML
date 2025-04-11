import pytest
import pandas as pd
from src.data_processing.process_faostat_fbs import process_faostat_data, FAOStatRecord
import os

@pytest.fixture
def sample_data():
    """Create a small sample DataFrame matching FAOSTAT FBS structure."""
    return pd.DataFrame({
        'area_code': [10, 10],
        'area': ['Australia', 'Australia'],
        'item_code': [2501, 2901],
        'item': ['Population', 'Grand Total'],
        'element_code': [511, 664],
        'element': ['Total Population', 'Food supply'],
        'unit': ['1000 No', 'kcal/cap/d'],
        'y2010': [22019.17, 3534.0],
        'y2010F': ['X', 'E'],
        'y2010N': [None, None],
        'y2011': [22357.03, 3516.0],
        'y2011F': ['X', 'E'],
        'y2011N': [None, None]
    })

def test_process_faostat_data_pipeline(sample_data, tmp_path):
    """Test the full processing pipeline with sample data."""
    # Create temp input file
    input_path = os.path.join(tmp_path, 'test_input.csv')
    sample_data.to_csv(input_path, index=False)

    # Process data
    result = process_faostat_data(input_path)

    # Check expected columns (no 'flag' in new schema)
    expected_cols = [
        'area_code', 'area', 'item_code', 'item',
        'element_code', 'element', 'unit', 'year', 'value'
    ]
    assert all(col in result.columns for col in expected_cols)

    # Check year conversion
    assert result['year'].min() == 2010
    assert result['year'].max() == 2011

    # Check area is always 'Australia'
    assert set(result['area'].str.lower()) == {'australia'}

def test_pydantic_validation(sample_data, tmp_path):
    """Test Pydantic model validation using FAOStatRecord."""
    # Process sample data
    input_path = os.path.join(tmp_path, 'test_input.csv')
    sample_data.to_csv(input_path, index=False)
    result = process_faostat_data(input_path)

    # Test validation of good records
    good_record = result.iloc[0].to_dict()
    validated = FAOStatRecord(**good_record)
    assert validated.year == 2010
    assert validated.area.lower() == 'australia'

    # Test validation of bad year (should raise ValueError if year is not int or out of range)
    bad_year = good_record.copy()
    bad_year['year'] = 1950  # Not Australia FBS range
    with pytest.raises(Exception):
        FAOStatRecord(**bad_year)

    # Test validation of negative value
    bad_value = good_record.copy()
    bad_value['value'] = -5
    with pytest.raises(Exception):
        FAOStatRecord(**bad_value)

def test_missing_value_handling(tmp_path):
    """Test that rows with missing values are dropped."""
    test_data = pd.DataFrame({
        'area_code': [10, 10],
        'area': ['Australia', 'Australia'],
        'item_code': [2501, 2901],
        'item': ['Population', 'Grand Total'],
        'element_code': [511, 664],
        'element': ['Total Population', 'Food supply'],
        'unit': ['1000 No', 'kcal/cap/d'],
        'y2010': [22019.17, None],  # One missing value
        'y2010F': ['X', 'E'],
        'y2011': [None, 3516.0],    # One missing value
        'y2011F': ['X', 'E']
    })

    input_path = os.path.join(tmp_path, 'test_input.csv')
    test_data.to_csv(input_path, index=False)

    result = process_faostat_data(input_path)

    # Should have 2 rows (one valid for each year)
    assert len(result) == 2
    assert result['value'].notna().all()

def test_duplicate_removal(tmp_path):
    """Test that duplicate rows are removed during processing."""
    df = pd.DataFrame({
        'area_code': [10, 10],
        'area': ['Australia', 'Australia'],
        'item_code': [2901, 2901],
        'item': ['Grand Total', 'Grand Total'],
        'element_code': [664, 664],
        'element': ['Food supply', 'Food supply'],
        'unit': ['kcal/cap/d', 'kcal/cap/d'],
        'y2010': [3500.0, 3500.0],
        'y2010F': ['E', 'E'],
        'y2011': [3600.0, 3600.0],
        'y2011F': ['E', 'E']
    })
    input_path = os.path.join(tmp_path, 'dup_input.csv')
    df.to_csv(input_path, index=False)

    result = process_faostat_data(input_path)

    # There should be only 2 rows (one per year) after duplicate removal
    # not 4 rows (2 duplicates x 2 years)
    assert len(result) == 2