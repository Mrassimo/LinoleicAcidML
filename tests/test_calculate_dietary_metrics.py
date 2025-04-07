"""
Tests for dietary metrics calculation functions
"""

import pytest
import pandas as pd
import numpy as np
from src.data_processing.calculate_dietary_metrics import (
    DietaryMetrics,
    classify_fat_source,
    calculate_la_intake,
    calculate_plant_fat_ratio,
    calculate_nutrient_supply
)

@pytest.fixture
def sample_faostat_df():
    """Create a sample FAOSTAT DataFrame for testing"""
    return pd.DataFrame({
        'Year': [2010, 2010, 2010, 2010],
        'Item': ['Soybean Oil', 'Butter', 'Wheat', 'Beef'],
        'Element': [
            'Food supply quantity (g/capita/day)',
            'Fat supply quantity (g/capita/day)',
            'Food supply (kcal/capita/day)',
            'Protein supply quantity (g/capita/day)'
        ],
        'Value': [10.0, 20.0, 2000.0, 30.0]
    })

@pytest.fixture
def sample_la_content_df():
    """Create a sample LA content DataFrame for testing"""
    return pd.DataFrame({
        'food_item': ['Soybean Oil', 'Butter'],
        'linoleic_acid_g_per_100g': [50.0, 2.0]
    })

@pytest.fixture
def sample_mapping_df():
    """Create a sample mapping DataFrame for testing"""
    return pd.DataFrame({
        'fao_item': ['Soybean Oil', 'Butter'],
        'matched_la_item': ['Soybean Oil', 'Butter'],
        'similarity_score': [0.95, 0.90],
        'manual_validation_status': ['CONFIRMED', 'CONFIRMED']
    })

def test_dietary_metrics_validation():
    """Test dietary metrics validation with Pydantic"""
    # Valid metrics
    valid_metrics = {
        'Year': 2010,
        'Total_LA_Intake_g_per_capita_day': 5.0,
        'LA_Intake_percent_calories': 2.0,
        'Plant_Fat_Ratio': 0.6,
        'Total_Calorie_Supply': 2500.0,
        'Total_Fat_Supply_g': 80.0,
        'Total_Carb_Supply_g': 300.0,
        'Total_Protein_Supply_g': 70.0
    }
    metrics = DietaryMetrics(**valid_metrics)
    assert metrics.Year == 2010
    assert metrics.Total_LA_Intake_g_per_capita_day == 5.0
    
    # Invalid year
    with pytest.raises(Exception):
        DietaryMetrics(**{**valid_metrics, 'Year': 1900})
    
    # Invalid LA intake (negative)
    with pytest.raises(Exception):
        DietaryMetrics(**{**valid_metrics, 'Total_LA_Intake_g_per_capita_day': -1.0})
    
    # Invalid plant fat ratio (> 1)
    with pytest.raises(Exception):
        DietaryMetrics(**{**valid_metrics, 'Plant_Fat_Ratio': 1.1})

def test_classify_fat_source():
    """Test classification of fat sources"""
    # Animal sources
    assert classify_fat_source('Butter') == 'Animal'
    assert classify_fat_source('Beef Fat') == 'Animal'
    assert classify_fat_source('Fish Oil') == 'Animal'
    assert classify_fat_source('Egg') == 'Animal'
    
    # Plant sources
    assert classify_fat_source('Soybean Oil') == 'Plant'
    assert classify_fat_source('Olive Oil') == 'Plant'
    assert classify_fat_source('Corn') == 'Plant'
    assert classify_fat_source('Nuts') == 'Plant'

def test_calculate_la_intake(sample_faostat_df, sample_la_content_df, sample_mapping_df):
    """Test calculation of LA intake"""
    la_intake_df = calculate_la_intake(sample_faostat_df, sample_la_content_df, sample_mapping_df)
    
    # Check structure
    assert 'Year' in la_intake_df.columns
    assert 'Total_LA_Intake_g_per_capita_day' in la_intake_df.columns
    
    # Check calculations
    # Soybean Oil: 10 g/day * 50% LA = 5 g LA/day
    assert np.isclose(la_intake_df.iloc[0]['Total_LA_Intake_g_per_capita_day'], 5.0)

def test_calculate_plant_fat_ratio(sample_faostat_df):
    """Test calculation of plant fat ratio"""
    plant_fat_df = calculate_plant_fat_ratio(sample_faostat_df)
    
    # Check structure
    assert 'Year' in plant_fat_df.columns
    assert 'Plant_Fat_Ratio' in plant_fat_df.columns
    
    # Check ratio is between 0 and 1
    assert all(0 <= ratio <= 1 for ratio in plant_fat_df['Plant_Fat_Ratio'])

def test_calculate_nutrient_supply(sample_faostat_df):
    """Test calculation of nutrient supply"""
    nutrient_df = calculate_nutrient_supply(sample_faostat_df)
    
    # Check all required columns are present
    required_cols = [
        'Total_Calorie_Supply',
        'Total_Fat_Supply_g',
        'Total_Protein_Supply_g',
        'Total_Carb_Supply_g'
    ]
    assert all(col in nutrient_df.columns for col in required_cols)
    
    # Check all values are non-negative
    assert all(nutrient_df[col].min() >= 0 for col in required_cols) 