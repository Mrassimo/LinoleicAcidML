import pytest
from pydantic import ValidationError
from datetime import datetime
from pathlib import Path
import pandas as pd
from src.process_faostat_fbs import (
    FBSBase,
    FoodBalanceSchema,
    validate_fbs_data,
    generate_validation_report,
    InvalidFBSEntry
)

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
        'value': 25000.0,
        'flag': 'X'
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
        'value': -100,  # Invalid
        'flag': 'Z'  # Invalid
    }

def test_fbsbase_valid_data(valid_fbs_data):
    """Test that valid data passes FBSBase validation"""
    record = FBSBase(**valid_fbs_data)
    assert record.area_code == valid_fbs_data['area_code']
    assert record.year == valid_fbs_data['year']

def test_fbsbase_invalid_data(invalid_fbs_data):
    """Test that invalid data fails FBSBase validation"""
    with pytest.raises(ValidationError) as excinfo:
        FBSBase(**invalid_fbs_data)
    
    errors = excinfo.value.errors()
    assert len(errors) > 0
    assert any(e['loc'][0] == 'area_code' for e in errors)
    assert any(e['loc'][0] == 'year' for e in errors)
    assert any(e['loc'][0] == 'value' for e in errors)

def test_foodbalanceschema_item_code_validation(valid_fbs_data):
    """Test item code validation in FoodBalanceSchema"""
    # Test valid item code
    valid_data = valid_fbs_data.copy()
    record = FoodBalanceSchema(**valid_data)
    assert record.item_code == valid_data['item_code']
    
    # Test invalid item code
    invalid_data = valid_fbs_data.copy()
    invalid_data['item_code'] = 99  # Too low
    with pytest.raises(ValidationError) as excinfo:
        FoodBalanceSchema(**invalid_data)
    assert "Item code must be between 1000-9999" in str(excinfo.value)

def test_foodbalanceschema_element_code_validation(valid_fbs_data):
    """Test element code validation in FoodBalanceSchema"""
    # Test valid element code
    valid_data = valid_fbs_data.copy()
    record = FoodBalanceSchema(**valid_data)
    assert record.element_code == valid_data['element_code']
    
    # Test invalid element code
    invalid_data = valid_fbs_data.copy()
    invalid_data['element_code'] = 9999  # Too high
    with pytest.raises(ValidationError) as excinfo:
        FoodBalanceSchema(**invalid_data)
    assert "Element code must be between 100-999" in str(excinfo.value)

def test_validate_fbs_data(valid_fbs_data, invalid_fbs_data):
    """Test the validate_fbs_data function"""
    # Test with valid data
    df_valid = pd.DataFrame([valid_fbs_data])
    errors = validate_fbs_data(df_valid)
    assert not errors
    
    # Test with invalid data
    df_invalid = pd.DataFrame([invalid_fbs_data])
    errors = validate_fbs_data(df_invalid)
    assert len(errors) > 0
    assert 1 in errors  # Row number should be in errors

def test_generate_validation_report(tmp_path):
    """Test the validation report generation"""
    errors = {
        1: ["value must be greater than or equal to 0"],
        2: ["year must be greater than or equal to 1961"]
    }
    report_path = tmp_path / "validation_errors.csv"
    generate_validation_report(errors, str(report_path))
    
    assert report_path.exists()
    df = pd.read_csv(report_path)
    assert len(df) == 2
    assert set(df['error_message']) == set(errors[1] + errors[2])

def test_clean_faostat_fbs_integration(tmp_path):
    """Integration test for the full cleaning and validation process"""
    from src.process_faostat_fbs import clean_faostat_fbs
    
    # Create a minimal test CSV file
    test_data = """area_code,area,item_code,item,element_code,element,unit,y2010,y2010F
10,Australia,2501,Population,511,Total Population,1000 No,22019.17,X"""
    input_path = tmp_path / "test_input.csv"
    output_path = tmp_path / "test_output.csv"
    
    with open(input_path, 'w') as f:
        f.write(test_data)
    
    # Run the cleaning function
    result = clean_faostat_fbs(str(input_path), str(output_path))
    
    # Check outputs
    assert output_path.exists()
    assert len(result) == 1
    assert result.iloc[0]['year'] == 2010
    assert (tmp_path / "reports").exists()  # Reports directory should exist