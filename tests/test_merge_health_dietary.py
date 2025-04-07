"""
Tests for health and dietary data merging functions
"""

import pytest
import pandas as pd
import numpy as np
from src.data_processing.merge_health_dietary import (
    AnalyticalRecord,
    create_lagged_predictors,
    standardize_dietary_metrics
)

@pytest.fixture
def sample_dietary_df():
    """Create a sample dietary metrics DataFrame for testing"""
    return pd.DataFrame({
        'Year': range(2000, 2005),
        'Total_LA_Intake_g_per_capita_day': [10.0] * 5,
        'LA_Intake_percent_calories': [5.0] * 5,
        'Plant_Fat_Ratio': [0.6] * 5,
        'Total_Calorie_Supply': [2500.0] * 5,
        'Total_Fat_Supply_g': [80.0] * 5,
        'Total_Carb_Supply_g': [300.0] * 5,
        'Total_Protein_Supply_g': [70.0] * 5
    })

@pytest.fixture
def sample_health_df():
    """Create a sample health outcomes DataFrame for testing"""
    return pd.DataFrame({
        'Year': range(2000, 2005),
        'Diabetes_Prevalence_Rate_AgeStandardised': [5.0] * 5,
        'Diabetes_Treatment_Rate_AgeStandardised': [3.0] * 5,
        'Obesity_Prevalence_AgeStandardised': [25.0] * 5,
        'Total_Cholesterol_AgeStandardised': [4.5] * 5,
        'NonHDL_Cholesterol_AgeStandardised': [3.0] * 5,
        'CVD_Prevalence_Rate': [15.0] * 5,
        'Dementia_Mortality_Rate_AgeStandardised': [50.0] * 5,
        'Dementia_Estimated_Number': [10000.0] * 5
    })

def test_analytical_record_validation():
    """Test analytical record validation with Pydantic"""
    # Valid record
    valid_record = {
        'Year': 2010,
        'Total_LA_Intake_g_per_capita_day': 10.0,
        'LA_Intake_percent_calories': 5.0,
        'Plant_Fat_Ratio': 0.6,
        'Total_Calorie_Supply': 2500.0,
        'Total_Fat_Supply_g': 80.0,
        'Total_Carb_Supply_g': 300.0,
        'Total_Protein_Supply_g': 70.0,
        'LA_perc_kcal_lag5': 4.5,
        'Diabetes_Prevalence_Rate_AgeStandardised': 5.0,
        'Diabetes_Treatment_Rate_AgeStandardised': 3.0,
        'Obesity_Prevalence_AgeStandardised': 25.0,
        'Total_Cholesterol_AgeStandardised': 4.5,
        'NonHDL_Cholesterol_AgeStandardised': 3.0,
        'CVD_Prevalence_Rate': 15.0,
        'Dementia_Mortality_Rate_AgeStandardised': 50.0,
        'Dementia_Estimated_Number': 10000.0
    }
    record = AnalyticalRecord(**valid_record)
    assert record.Year == 2010
    assert record.Total_LA_Intake_g_per_capita_day == 10.0
    assert record.Total_Carb_Supply_g == 300.0
    assert record.Total_Protein_Supply_g == 70.0
    
    # Test invalid cases
    # Invalid year
    with pytest.raises(ValueError) as exc_info:
        AnalyticalRecord(**{**valid_record, 'Year': 1900})
    assert "greater than or equal to 1961" in str(exc_info.value)
    
    # Invalid LA intake percentage
    with pytest.raises(ValueError) as exc_info:
        AnalyticalRecord(**{**valid_record, 'LA_Intake_percent_calories': 101.0})
    assert "less than or equal to 100" in str(exc_info.value)
    
    # Invalid Plant Fat Ratio
    with pytest.raises(ValueError) as exc_info:
        AnalyticalRecord(**{**valid_record, 'Plant_Fat_Ratio': 1.5})
    assert "less than or equal to 1" in str(exc_info.value)
    
    # Invalid Total Cholesterol
    with pytest.raises(ValueError) as exc_info:
        AnalyticalRecord(**{**valid_record, 'Total_Cholesterol_AgeStandardised': 9.0})
    assert "Total Cholesterol should be between 2 and 8 mmol/L" in str(exc_info.value)
    
    # Invalid Non-HDL Cholesterol
    with pytest.raises(ValueError) as exc_info:
        AnalyticalRecord(**{**valid_record, 'NonHDL_Cholesterol_AgeStandardised': 9.0})
    assert "Non-HDL cholesterol should be between 0 and 8 mmol/L" in str(exc_info.value)
    
    # Test optional fields
    minimal_record = {
        'Year': 2010,
        'Total_LA_Intake_g_per_capita_day': 10.0,
        'LA_Intake_percent_calories': 5.0,
        'Plant_Fat_Ratio': 0.6,
        'Total_Calorie_Supply': 2500.0,
        'Total_Fat_Supply_g': 80.0
    }
    record = AnalyticalRecord(**minimal_record)
    assert record.Total_Carb_Supply_g is None
    assert record.Total_Protein_Supply_g is None
    assert record.Diabetes_Prevalence_Rate_AgeStandardised is None

def test_create_lagged_predictors(sample_dietary_df):
    """Test creation of lagged predictors"""
    lag_years = [1, 2]
    lagged_df = create_lagged_predictors(sample_dietary_df, lag_years)
    
    # Check that original columns are preserved
    assert all(col in lagged_df.columns for col in sample_dietary_df.columns)
    
    # Check that lag columns were created
    for lag in lag_years:
        lag_col = f'LA_perc_kcal_lag{lag}'
        assert lag_col in lagged_df.columns
    
    # Check that lags were calculated correctly
    assert pd.isna(lagged_df.iloc[0]['LA_perc_kcal_lag1'])  # First row should be NaN
    assert lagged_df.iloc[1]['LA_perc_kcal_lag1'] == sample_dietary_df.iloc[0]['LA_Intake_percent_calories']
    
    # Test error cases
    # Missing Year column
    df_no_year = sample_dietary_df.drop('Year', axis=1)
    with pytest.raises(ValueError, match="DataFrame must contain 'Year' column for sorting"):
        create_lagged_predictors(df_no_year, lag_years)
    
    # Missing LA intake column
    df_no_la = sample_dietary_df.drop('LA_Intake_percent_calories', axis=1)
    with pytest.raises(ValueError, match="Column 'LA_Intake_percent_calories' not found for lagging"):
        create_lagged_predictors(df_no_la, lag_years)

def test_standardize_dietary_metrics(sample_dietary_df):
    """Test standardization of dietary metrics"""
    # Test with all columns present
    standardized_df = standardize_dietary_metrics(sample_dietary_df)
    
    # Check that columns were renamed correctly
    expected_cols = {
        'Year',
        'Total_LA_Intake_g_per_capita_day',
        'LA_Intake_percent_calories',
        'Plant_Fat_Ratio',
        'Total_Calorie_Supply',
        'Total_Fat_Supply_g',
        'Total_Carb_Supply_g',
        'Total_Protein_Supply_g'
    }
    assert set(standardized_df.columns) == expected_cols
    
    # Check that values were preserved
    assert standardized_df['Total_LA_Intake_g_per_capita_day'].iloc[0] == sample_dietary_df['Total_LA_Intake_g_per_capita_day'].iloc[0]
    
    # Test with missing carb column
    df_no_carb = sample_dietary_df.drop('Total_Carb_Supply_g', axis=1)
    standardized_no_carb = standardize_dietary_metrics(df_no_carb)
    assert 'Total_Carb_Supply_g' not in standardized_no_carb.columns
    
    # Test with missing Year column
    df_no_year = sample_dietary_df.drop('Year', axis=1)
    with pytest.raises(ValueError, match="Failed to create 'Year' column during dietary metrics standardization"):
        standardize_dietary_metrics(df_no_year) 