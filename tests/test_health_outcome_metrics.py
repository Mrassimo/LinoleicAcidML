import pytest
import pandas as pd
from unittest.mock import patch
from src.data_processing import health_outcome_metrics as hom


@pytest.fixture
def diabetes_df():
    return pd.DataFrame({
        'year': [2000, 2000],
        'sex': ['Men', 'Women'],
        'age-standardised_prevalence_of_diabetes_18+_years_': [0.07, 0.08],
        'age-standardised_proportion_of_people_with_diabetes_who_were_treated_30+_years_': [0.5, 0.6]
    })


@pytest.fixture
def bmi_df():
    return pd.DataFrame({
        'year': [2000, 2000],
        'sex': ['Men', 'Women'],
        'prevalence_of_bmi>=30_kg_m²_obesity_': [0.2, 0.25]
    })


@pytest.fixture
def cholesterol_df():
    return pd.DataFrame({
        'year': [2000, 2000],
        'sex': ['Men', 'Women'],
        'mean_total_cholesterol_mmol_l_': [5.2, 5.0],
        'mean_non-hdl_cholesterol_mmol_l_': [3.5, 3.3]
    })


def test_extract_ncd_risc_metrics_basic(diabetes_df, bmi_df, cholesterol_df):
    """Test extraction and calculation of NCD-RisC metrics with typical data."""
    with patch.object(hom, 'load_and_validate_csv', side_effect=[diabetes_df, bmi_df, cholesterol_df]):
        df = hom.extract_ncd_risc_metrics()
        assert df is not None
        assert 'Diabetes_Prevalence_Rate_AgeStandardised' in df.columns
        assert 'Diabetes_Treatment_Rate_AgeStandardised' in df.columns
        # Check values are percentages
        assert df['Diabetes_Prevalence_Rate_AgeStandardised'].iloc[0] > 0
        assert df['Diabetes_Treatment_Rate_AgeStandardised'].iloc[0] > 0


def test_extract_ncd_risc_metrics_missing_cols(bmi_df, cholesterol_df):
    """Test handling when diabetes data is missing required columns."""
    incomplete_diabetes_df = pd.DataFrame({
        'year': [2000],
        'sex': ['Men'],
        # Missing required columns
    })
    with patch.object(hom, 'load_and_validate_csv', side_effect=[incomplete_diabetes_df, bmi_df, cholesterol_df]):
        df = hom.extract_ncd_risc_metrics()
        # Should still return a DataFrame, but diabetes metrics may be missing or NaN
        assert df is not None


def test_load_and_validate_csv_missing_file(tmp_path):
    """Test load_and_validate_csv returns None if file does not exist."""
    missing_file = tmp_path / "nonexistent.csv"
    result = hom.load_and_validate_csv(missing_file)
    assert result is None


def test_load_and_validate_csv_missing_columns(tmp_path):
    """Test load_and_validate_csv returns None if required columns are missing."""
    file_path = tmp_path / "test.csv"
    df = pd.DataFrame({'a': [1], 'b': [2]})
    df.to_csv(file_path, index=False)
    result = hom.load_and_validate_csv(file_path, required_cols=['a', 'c'])
    assert result is None