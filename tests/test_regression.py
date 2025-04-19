# tests/test_regression.py
"""
Tests for the regression module.
All tests use Australian English spelling.

Author: SeedoilsML Team
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from src.models.regression import (
    RegressionConfig,
    RegressionResult,
    prepare_regression_data,
    fit_linear_regression,
    run_regression_analysis,
    analyze_all_health_outcomes
)

@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    np.random.seed(42)
    n_samples = 100
    
    # Create predictors
    X1 = np.random.normal(6, 1, n_samples)  # LA intake
    X2 = np.random.uniform(0.4, 0.6, n_samples)  # Plant Fat Ratio
    X3 = np.random.normal(100, 10, n_samples)  # Total Fat Supply
    
    # Create response variables with known relationships
    y1 = 2*X1 + 0.5*X2 + 0.1*X3 + np.random.normal(0, 1, n_samples)  # Obesity
    y2 = 1.5*X1 - 0.3*X2 + 0.2*X3 + np.random.normal(0, 1, n_samples)  # Diabetes
    
    # Create lagged versions
    X1_lag5 = np.roll(X1, 5)
    X1_lag10 = np.roll(X1, 10)
    
    data = {
        'LA_Intake_percent_calories': X1,
        'Plant_Fat_Ratio': X2,
        'Total_Fat_Supply_g': X3,
        'LA_perc_kcal_lag5': X1_lag5,
        'LA_perc_kcal_lag10': X1_lag10,
        'Obesity_Prevalence_AgeStandardised': y1,
        'Diabetes_Prevalence_Rate_AgeStandardised': y2
    }
    
    return pd.DataFrame(data)

@pytest.fixture
def regression_config(tmp_path):
    """Create a RegressionConfig instance for testing."""
    return RegressionConfig(
        output_dir=str(tmp_path),
        standardize=True,
        test_size=0.2,
        random_state=42
    )

def test_prepare_regression_data(sample_data, regression_config):
    """Test data preparation for regression."""
    dependent_var = 'Obesity_Prevalence_AgeStandardised'
    independent_vars = ['LA_Intake_percent_calories', 'Plant_Fat_Ratio']
    
    X, y = prepare_regression_data(sample_data, dependent_var, independent_vars, regression_config)
    
    assert X.shape[1] == len(independent_vars)
    assert len(y) == len(sample_data)
    assert not np.any(np.isnan(X))
    assert not np.any(np.isnan(y))
    
    if regression_config.standardize:
        assert np.abs(X.mean(axis=0)).max() < 1e-10
        assert np.abs(X.std(axis=0) - 1).max() < 1e-10

def test_fit_linear_regression(sample_data, regression_config):
    """Test linear regression model fitting."""
    dependent_var = 'Obesity_Prevalence_AgeStandardised'
    independent_vars = ['LA_Intake_percent_calories', 'Plant_Fat_Ratio']
    
    X, y = prepare_regression_data(sample_data, dependent_var, independent_vars, regression_config)
    model, coefficients, p_values = fit_linear_regression(X, y, independent_vars)
    
    assert len(coefficients) == len(independent_vars)
    assert len(p_values) == len(independent_vars)
    assert all(isinstance(v, float) for v in coefficients.values())
    assert all(isinstance(v, float) for v in p_values.values())
    assert all(0 <= v <= 1 for v in p_values.values())

def test_run_regression_analysis(sample_data, regression_config):
    """Test complete regression analysis pipeline."""
    dependent_var = 'Obesity_Prevalence_AgeStandardised'
    independent_vars = ['LA_Intake_percent_calories', 'Plant_Fat_Ratio']
    
    result = run_regression_analysis(sample_data, dependent_var, independent_vars, regression_config)
    
    assert isinstance(result, RegressionResult)
    assert result.dependent_var == dependent_var
    assert result.independent_vars == independent_vars
    assert 0 <= result.r2_score <= 1
    assert result.mse >= 0
    assert result.n_observations == len(sample_data)
    assert len(result.coefficients) == len(independent_vars)
    assert len(result.p_values) == len(independent_vars)

def test_analyze_all_health_outcomes(sample_data, regression_config):
    """Test analysis of all health outcomes."""
    results = analyze_all_health_outcomes(sample_data, regression_config)
    
    assert isinstance(results, list)
    assert len(results) > 0
    assert all(isinstance(r, RegressionResult) for r in results)
    
    # Check that we have results for both current and lagged analyses
    outcome_vars = set(r.dependent_var for r in results)
    assert 'Obesity_Prevalence_AgeStandardised' in outcome_vars
    assert 'Diabetes_Prevalence_Rate_AgeStandardised' in outcome_vars

def test_regression_with_missing_data(sample_data, regression_config):
    """Test regression handling of missing data."""
    # Introduce some missing values
    sample_data.loc[0:10, 'LA_Intake_percent_calories'] = np.nan
    
    result = run_regression_analysis(
        sample_data,
        'Obesity_Prevalence_AgeStandardised',
        ['LA_Intake_percent_calories', 'Plant_Fat_Ratio'],
        regression_config
    )
    
    assert result is not None
    assert result.n_observations == len(sample_data) - 11  # Accounting for removed NaN rows

def test_regression_with_insufficient_data(regression_config):
    """Test regression handling of insufficient data."""
    # Create very small dataset
    small_data = pd.DataFrame({
        'Obesity_Prevalence_AgeStandardised': range(5),
        'LA_Intake_percent_calories': range(5),
        'Plant_Fat_Ratio': range(5)
    })
    
    result = run_regression_analysis(
        small_data,
        'Obesity_Prevalence_AgeStandardised',
        ['LA_Intake_percent_calories', 'Plant_Fat_Ratio'],
        regression_config
    )
    
    assert result is None  # Should return None for insufficient data

def test_regression_config_validation():
    """Test RegressionConfig validation."""
    # Test valid config
    valid_config = RegressionConfig(
        output_dir="/tmp",
        standardize=True,
        test_size=0.2,
        random_state=42
    )
    assert valid_config.test_size == 0.2
    
    # Test invalid test_size
    with pytest.raises(ValueError):
        RegressionConfig(
            output_dir="/tmp",
            test_size=1.5  # Invalid value
        )

def test_regression_result_validation():
    """Test RegressionResult validation."""
    valid_result = RegressionResult(
        dependent_var="test",
        independent_vars=["var1", "var2"],
        r2_score=0.8,
        coefficients={"var1": 1.0, "var2": 2.0},
        p_values={"var1": 0.01, "var2": 0.05},
        mse=0.1,
        n_observations=100
    )
    assert valid_result.r2_score == 0.8
    
    # Test invalid r2_score
    with pytest.raises(ValueError):
        RegressionResult(
            dependent_var="test",
            independent_vars=["var1"],
            r2_score=1.5,  # Invalid value
            coefficients={"var1": 1.0},
            p_values={"var1": 0.01},
            mse=0.1,
            n_observations=100
        )