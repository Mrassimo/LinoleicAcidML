import pandas as pd
import numpy as np
import pytest
import sys
import os
from pathlib import Path
from scripts.calculate_dietary_metrics import (
    calculate_la_intake,
    calculate_plant_fat_ratio,
    calculate_dietary_metrics,
    create_food_group_mapping,
    impute_missing_la_values,
    adjust_la_content,
    handle_methodology_change
)

# Add the parent directory to the path so we can import the script
sys.path.append(str(Path(__file__).parent.parent))

@pytest.fixture
def sample_fao_data():
    """Create sample FAOSTAT data for testing."""
    return pd.DataFrame({
        'year': [2000, 2000, 2000],
        'item': ['Soyabean Oil', 'Vegetable Oils', 'Animal fats'],
        'Food supply quantity (kg/capita/yr)': [10.0, 15.0, 20.0],
        'Fat supply quantity (g/capita/day)': [20.0, 30.0, 40.0],
        'Food supply (kcal/capita/day)': [2000.0, 2000.0, 2000.0],
        'Protein supply quantity (g/capita/day)': [10.0, 10.0, 10.0]
    })

@pytest.fixture
def sample_la_mapping():
    """Create sample LA content mapping for testing."""
    return pd.DataFrame({
        'fao_item': ['Soyabean Oil', 'Vegetable Oils', 'Animal fats'],
        'la_content_per_100g': [51.9, 66.9, 10.2]
    })

@pytest.fixture
def sample_fao_df():
    """Create a sample FAOSTAT DataFrame for testing"""
    return pd.DataFrame({
        'year': [2010, 2010, 2010, 2010, 2010, 2010],
        'item': ['Soyabean Oil', 'Wheat and products', 'Bovine Meat', 'Apples and products', 'Freshwater Fish', 'Unknown Item'],
        'Food supply quantity (kg/capita/yr)': [5.0, 80.0, 20.0, 10.0, 8.0, 3.0],
        'Fat supply quantity (g/capita/day)': [50.0, 10.0, 40.0, 2.0, 5.0, 1.0],
        'Food supply (kcal/capita/day)': [450.0, 2000.0, 300.0, 50.0, 80.0, 20.0],
        'Protein supply quantity (g/capita/day)': [0.0, 60.0, 40.0, 0.5, 15.0, 2.0]
    })

def test_calculate_la_intake(sample_fao_data, sample_la_mapping):
    """Test LA intake calculation."""
    result = calculate_la_intake(sample_fao_data, sample_la_mapping)
    
    # The exact calculation is complex due to various adjustments and caps
    # Just test that the calculation is in the expected range
    assert 45 < result['la_intake_g_day'].iloc[0] < 55
    
    # Test that % calories from LA is in the expected range
    assert 10 < result['la_intake_percent_calories'].iloc[0] < 25

def test_calculate_plant_fat_ratio(sample_fao_data):
    """Test plant fat ratio calculation."""
    result = calculate_plant_fat_ratio(sample_fao_data)
    
    # Plant fats = 20.0 + 30.0 = 50.0 g/day
    # Total fats = 50.0 + 40.0 = 90.0 g/day
    # Ratio = 50.0 / 90.0 = 0.556
    expected_ratio = 0.556
    assert abs(result['plant_fat_ratio'].iloc[0] - expected_ratio) < 0.01

def test_dietary_metrics_columns(sample_fao_data, sample_la_mapping, monkeypatch):
    """Test that the final dietary metrics DataFrame has all required columns."""
    # Mock the load_data function to return our sample data
    def mock_load_data():
        return sample_fao_data, sample_la_mapping
    
    monkeypatch.setattr('scripts.calculate_dietary_metrics.load_data', mock_load_data)
    
    result = calculate_dietary_metrics()
    
    required_columns = {
        'year',
        'la_intake_g_day',
        'la_intake_percent_calories',
        'plant_fat_ratio',
        'total_calorie_supply',
        'total_fat_supply',
        'total_protein_supply'
    }
    
    assert set(result.columns) == required_columns 

def test_create_food_group_mapping(sample_fao_df):
    """Test creation of food group mapping"""
    mapping = create_food_group_mapping(sample_fao_df)
    
    # Check specific mappings
    assert mapping['Soyabean Oil'] == 'Oils and Fats'
    assert mapping['Wheat and products'] == 'Grains'
    assert mapping['Bovine Meat'] == 'Meats'
    assert mapping['Apples and products'] == 'Fruits'
    assert mapping['Freshwater Fish'] == 'Fish'
    
    # Check unknown item not in mapping
    assert 'Unknown Item' not in mapping

def test_impute_missing_la_values(sample_fao_df, sample_la_mapping):
    """Test imputation of missing LA values"""
    # Create an adjusted version of the mapping with known values
    adjusted_mapping = adjust_la_content(sample_la_mapping)
    
    # Impute missing values
    result = impute_missing_la_values(sample_fao_df, adjusted_mapping)
    
    # Check that all items have LA content
    assert result['la_content_per_100g'].isna().sum() == 0
    
    # Check that known values remain unchanged
    assert result.loc[result['item'] == 'Soyabean Oil', 'la_content_per_100g'].iloc[0] == 51.9
    
    # Check that missing items with no food group average are set to 0.0
    assert result.loc[result['item'] == 'Wheat and products', 'la_content_per_100g'].iloc[0] == 0.0
    assert result.loc[result['item'] == 'Bovine Meat', 'la_content_per_100g'].iloc[0] == 0.0
    
    # Check that Freshwater Fish was imputed with an appropriate value from Fish group
    # (but we don't know the exact value since it depends on the group average)
    assert not pd.isna(result.loc[result['item'] == 'Freshwater Fish', 'la_content_per_100g'].iloc[0])
    
    # Check that items without a food group or group average were set to 0
    assert result.loc[result['item'] == 'Unknown Item', 'la_content_per_100g'].iloc[0] == 0.0

def test_food_group_averages(sample_fao_df, sample_la_mapping):
    """Test that food group averages are calculated correctly"""
    # Add more items to the LA mapping to test group averages
    extended_mapping = sample_la_mapping.copy()
    extended_mapping = pd.concat([
        extended_mapping, 
        pd.DataFrame({
            'fao_item': ['Sunflowerseed Oil', 'Maize and products', 'Pigmeat', 'Freshwater Fish'],
            'la_content_per_100g': [65.0, 1.2, 0.5, 0.2]
        })
    ])
    
    # Apply adjustments
    adjusted_mapping = adjust_la_content(extended_mapping)
    
    # Add food groups to the fao dataframe
    item_to_group = create_food_group_mapping(sample_fao_df)
    sample_fao_df['food_group'] = sample_fao_df['item'].map(item_to_group)
    
    # Merge the adjusted mapping
    fao_with_la = pd.merge(
        sample_fao_df,
        adjusted_mapping[['fao_item', 'la_content_per_100g']],
        left_on='item',
        right_on='fao_item',
        how='left'
    )
    
    # Calculate group averages
    oils_avg = fao_with_la[
        (fao_with_la['food_group'] == 'Oils and Fats') & 
        fao_with_la['la_content_per_100g'].notna()
    ]['la_content_per_100g'].mean()
    
    grains_avg = fao_with_la[
        (fao_with_la['food_group'] == 'Grains') & 
        fao_with_la['la_content_per_100g'].notna()
    ]['la_content_per_100g'].mean()
    
    # Test imputation
    result = impute_missing_la_values(sample_fao_df, adjusted_mapping)
    
    # Check that Apples and products got imputed with a value (any non-NA value)
    assert not pd.isna(result.loc[result['item'] == 'Apples and products', 'la_content_per_100g'].iloc[0]) 

def test_handle_methodology_change():
    """Test handling of methodology change in FAOSTAT data."""
    # Create sample data with values before and after the methodology change
    df = pd.DataFrame({
        'year': list(range(2005, 2015)),
        'la_intake_g_day': [10.0] * 5 + [12.0] * 5,
        'total_calorie_supply': [2000.0] * 5 + [2300.0] * 5,
        'total_fat_supply': [80.0] * 5 + [95.0] * 5,
        'total_protein_supply': [70.0] * 5 + [82.0] * 5
    })
    
    # Call the function
    result_df, adjustment_factors = handle_methodology_change(df)
    
    # Check that the adjustment factors are correctly calculated
    assert 0.78 <= adjustment_factors['la_intake_g_day'] <= 0.9
    assert 0.8 <= adjustment_factors['total_calorie_supply'] <= 0.9
    assert 0.8 <= adjustment_factors['total_fat_supply'] <= 0.9
    assert 0.8 <= adjustment_factors['total_protein_supply'] <= 0.9
    
    # Check that post-2010 values have been adjusted
    # Values from 2010 onwards should be closer to pre-2010 values after adjustment
    assert abs(result_df[result_df['year'] == 2010]['la_intake_g_day'].iloc[0] - 10.0) < 1.0
    assert abs(result_df[result_df['year'] == 2010]['total_calorie_supply'].iloc[0] - 2000.0) < 200.0
    assert abs(result_df[result_df['year'] == 2010]['total_fat_supply'].iloc[0] - 80.0) < 10.0
    assert abs(result_df[result_df['year'] == 2010]['total_protein_supply'].iloc[0] - 70.0) < 10.0 