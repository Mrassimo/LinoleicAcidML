# tests/test_gam.py
"""
Tests for the GAM module.

Tests the functionality of the Generalised Additive Model implementation
including data preparation, model fitting, evaluation, and plotting.
"""

import pytest
import numpy as np
import pandas as pd
from pathlib import Path
import tempfile
import shutil
from pygam import LinearGAM

from src.models.gam import (
    GAMConfig,
    prepare_gam_data,
    select_optimal_gam,
    analyze_health_outcome,
    plot_partial_dependence,
    analyze_all_health_outcomes
)

@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    np.random.seed(42)
    n_samples = 100
    
    # Create non-linear relationships
    x1 = np.linspace(0, 10, n_samples)
    x2 = np.linspace(-5, 5, n_samples)
    x3 = np.random.normal(0, 1, n_samples)
    
    # Create target with non-linear relationships
    y = (
        np.sin(x1) +  # Non-linear relationship with x1
        0.5 * x2**2 +  # Quadratic relationship with x2
        0.1 * x3 +  # Linear relationship with x3
        np.random.normal(0, 0.1, n_samples)  # Some noise
    )
    
    df = pd.DataFrame({
        'LA_Intake_percent_calories': x1,
        'Plant_Fat_Ratio': x2,
        'Total_Fat_Supply_g': x3,
        'Obesity_Prevalence_AgeStandardised': y
    })
    
    return df

@pytest.fixture
def temp_output_dir():
    """Create a temporary directory for test outputs."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)

@pytest.fixture
def gam_config(temp_output_dir):
    """Create a GAMConfig for testing."""
    return GAMConfig(
        output_dir=str(temp_output_dir),
        cv_folds=3,  # Smaller number for testing
        n_splines=[5, 8],  # Fewer options for testing
        lam_candidates=[0.1, 1.0]  # Fewer options for testing
    )

def test_prepare_gam_data(sample_data):
    """Test data preparation function."""
    feature_cols = ['LA_Intake_percent_calories', 'Plant_Fat_Ratio', 'Total_Fat_Supply_g']
    target_col = 'Obesity_Prevalence_AgeStandardised'
    
    X, y = prepare_gam_data(sample_data, feature_cols, target_col)
    
    assert X is not None
    assert y is not None
    assert X.shape[1] == len(feature_cols)
    assert X.shape[0] == y.shape[0]
    assert not np.any(np.isnan(X))
    assert not np.any(np.isnan(y))

def test_prepare_gam_data_missing_column(sample_data):
    """Test data preparation with missing column."""
    feature_cols = ['NonExistentColumn']
    target_col = 'Obesity_Prevalence_AgeStandardised'
    
    X, y = prepare_gam_data(sample_data, feature_cols, target_col)
    assert X is None
    assert y is None

def test_prepare_gam_data_with_missing_values(sample_data):
    """Test data preparation with missing values."""
    # Add some missing values
    sample_data.loc[0, 'LA_Intake_percent_calories'] = np.nan
    
    feature_cols = ['LA_Intake_percent_calories', 'Plant_Fat_Ratio']
    target_col = 'Obesity_Prevalence_AgeStandardised'
    
    X, y = prepare_gam_data(sample_data, feature_cols, target_col)
    
    assert X is not None
    assert y is not None
    assert X.shape[0] == y.shape[0]
    assert X.shape[0] == len(sample_data) - 1  # One row should be dropped

def test_select_optimal_gam(sample_data, gam_config):
    """Test GAM model selection."""
    feature_cols = ['LA_Intake_percent_calories', 'Plant_Fat_Ratio']
    target_col = 'Obesity_Prevalence_AgeStandardised'
    
    X, y = prepare_gam_data(sample_data, feature_cols, target_col)
    model, results = select_optimal_gam(X, y, feature_cols, gam_config)
    
    assert isinstance(model, LinearGAM)
    assert 'cv_results' in results
    assert 'best_params' in results
    assert 'best_score' in results
    assert len(results['cv_results']) > 0
    assert all(r['mean_r2'] <= 1.0 for r in results['cv_results'])

def test_analyze_health_outcome(sample_data, gam_config):
    """Test health outcome analysis."""
    predictors = ['LA_Intake_percent_calories', 'Plant_Fat_Ratio']
    outcome = 'Obesity_Prevalence_AgeStandardised'
    
    result = analyze_health_outcome(sample_data, outcome, predictors, gam_config)
    
    assert result is not None
    assert 'outcome' in result
    assert 'model' in result
    assert 'r2_score' in result
    assert 'mse' in result
    assert 'cv_results' in result
    assert 'n_observations' in result
    assert isinstance(result['model'], LinearGAM)
    assert 0 <= result['r2_score'] <= 1.0

def test_plot_partial_dependence(sample_data, gam_config, temp_output_dir):
    """Test partial dependence plotting."""
    predictors = ['LA_Intake_percent_calories']
    outcome = 'Obesity_Prevalence_AgeStandardised'
    
    result = analyze_health_outcome(sample_data, outcome, predictors, gam_config)
    assert result is not None
    
    plot_partial_dependence(result['model'], 0, predictors[0], temp_output_dir)
    
    # Check if plot was saved
    plot_file = temp_output_dir / f'pdp_{predictors[0].lower().replace(" ", "_")}.png'
    assert plot_file.exists()

def test_analyze_all_health_outcomes(sample_data, gam_config):
    """Test analysis of all health outcomes."""
    # Add some IHME metrics to the sample data
    sample_data['CVD_Mortality_Rate_ASMR'] = np.random.normal(50, 10, len(sample_data))
    sample_data['CVD_Prevalence_Rate_IHME'] = np.random.normal(200, 20, len(sample_data))
    
    results = analyze_all_health_outcomes(sample_data, gam_config)
    
    assert results is not None
    assert len(results) > 0
    
    # Check that we have results for both base predictors and lag predictors
    outcomes_analyzed = set(r['outcome'] for r in results if r is not None)
    assert 'Obesity_Prevalence_AgeStandardised' in outcomes_analyzed
    
    # Check that each result has the expected structure
    for result in results:
        if result is not None:
            assert 'outcome' in result
            assert 'model' in result
            assert 'r2_score' in result
            assert 'mse' in result
            assert 'cv_results' in result
            assert 'n_observations' in result

def test_gam_config_validation():
    """Test GAMConfig validation."""
    # Test valid config
    valid_config = GAMConfig(
        output_dir="/tmp",
        cv_folds=5,
        n_splines=[8, 10],
        lam_candidates=[0.1, 1.0]
    )
    assert valid_config.cv_folds == 5
    
    # Test default values
    default_config = GAMConfig(output_dir="/tmp")
    assert default_config.standardize is True
    assert default_config.cv_folds == 5
    assert default_config.random_state == 42
    assert len(default_config.n_splines) > 0
    assert len(default_config.lam_candidates) > 0