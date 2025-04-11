import pytest
import pandas as pd
from src.data_processing.process_faostat_fbs import FAOStatRecord, process_faostat_data

@pytest.fixture
def valid_fbs_data():
    return {
        'area_code': 10,
        'area': 'Australia',
        'item_code': 2501,
        'item': 'Population',
        'element_code': 511,
        'element': 'Total Population',
        'unit': '1000 No',
        'year': 2020,
        'value': 25000.0
    }

@pytest.fixture
def invalid_fbs_data():
    return {
        'area_code': -10,  # Invalid
        'area': 'Australia',
        'item_code': 99,   # Invalid
        'item': 'Invalid',
        'element_code': 9999,  # Invalid
        'element': 'Invalid',
        'unit': 'Invalid',
        'year': 1900,  # Invalid
        'value': -100  # Invalid
    }

def test_faostatrecord_valid_data(valid_fbs_data):
    """Test that valid data passes FAOStatRecord validation"""
    record = FAOStatRecord(**valid_fbs_data)
    assert record.area_code == valid_fbs_data['area_code']
    assert record.year == valid_fbs_data['year']

import pydantic

def test_faostatrecord_invalid_data(invalid_fbs_data):
    """Test that invalid data fails FAOStatRecord validation (should raise pydantic.ValidationError).

    This test ensures that invalid input to FAOStatRecord triggers a validation error, as per Australian data standards.
    """
    with pytest.raises(pydantic.ValidationError):
        FAOStatRecord(**invalid_fbs_data)

# No FoodBalanceSchema in new code; skip item/element code-specific tests.

# No validate_fbs_data or generate_validation_report in new code; skip these tests.

def test_process_faostat_data_integration(tmp_path):
    """Integration test for the full processing pipeline."""
    # Create a minimal test CSV file
    test_data = """area_code,area,item_code,item,element_code,element,unit,y2010,y2010F
10,Australia,2501,Population,511,Total Population,1000 No,22019.17,X"""
    input_path = tmp_path / "test_input.csv"

    with open(input_path, 'w') as f:
        f.write(test_data)

    # Run the processing function
    result = process_faostat_data(str(input_path))

    # Check outputs
    assert len(result) == 1
    assert result.iloc[0]['year'] == 2010
    assert result.iloc[0]['area'].lower() == 'australia'