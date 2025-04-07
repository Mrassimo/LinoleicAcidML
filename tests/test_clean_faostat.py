import pytest
from pathlib import Path
import pandas as pd
from src.data_processing.clean_faostat import FAOStatRecord, clean_faostat_data

def test_faostat_record_validation():
    """Test FAOStatRecord validation."""
    # Valid record
    valid_data = {
        "area_code": 10,
        "area": "Australia",
        "item_code": 2511.0,
        "item": "Wheat and products",
        "element_code": 645.0,
        "element": "Food supply quantity (kg/capita/yr)",
        "unit": "kg/cap",
        "year": 2010.0,
        "value": 77.96,
        "flag": "E"
    }
    record = FAOStatRecord(**valid_data)
    assert record.area == "Australia"
    assert record.value == 77.96

    # Test invalid area
    invalid_area = valid_data.copy()
    invalid_area["area"] = "New Zealand"
    with pytest.raises(ValueError, match="Area must be Australia"):
        FAOStatRecord(**invalid_area)

    # Test invalid value
    invalid_value = valid_data.copy()
    invalid_value["value"] = "E"
    with pytest.raises(ValueError):
        FAOStatRecord(**invalid_value)

def test_clean_faostat_data(tmp_path):
    """Test FAOSTAT data cleaning function."""
    # Create a test input file
    input_data = pd.DataFrame([
        {
            "area_code": 10,
            "area": "Australia",
            "item_code": 2511.0,
            "item": "Wheat and products",
            "element_code": 645.0,
            "element": "Food supply quantity (kg/capita/yr)",
            "unit": "kg/cap",
            "year": 2010.0,
            "value": 77.96,
            "flag": "E"
        },
        {
            "area_code": 10,
            "area": "Australia",
            "item_code": 2511.0,
            "item": "Wheat and products",
            "element_code": 645.0,
            "element": "Food supply quantity (kg/capita/yr)",
            "unit": "kg/cap",
            "year": 2010.0,
            "value": "E",
            "flag": "E"
        }
    ])
    
    input_file = tmp_path / "test_input.csv"
    output_file = tmp_path / "test_output.csv"
    input_data.to_csv(input_file, index=False)
    
    # Run the cleaning function
    clean_faostat_data(input_file, output_file)
    
    # Read and check the output
    output_data = pd.read_csv(output_file)
    assert len(output_data) == 1  # Should have removed the duplicate 'E' row
    assert output_data.iloc[0]['element'] == 'Food supply quantity (g/capita/day)'
    assert output_data.iloc[0]['unit'] == 'g/cap/d'
    
    # Check conversion from kg/year to g/day
    expected_g_per_day = 77.96 * 1000 / 365.25
    assert abs(output_data.iloc[0]['value'] - expected_g_per_day) < 0.01 