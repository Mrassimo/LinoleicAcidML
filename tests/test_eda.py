"""
Tests for the EDA module.
"""

import os
import pandas as pd
import numpy as np
import pytest
from pathlib import Path
from src.analysis.eda import (
    load_data_for_eda,
    perform_summary_statistics,
    plot_distributions,
    perform_correlation_analysis,
    plot_time_series,
    DIETARY_VARS,
    HEALTH_VARS
)
from src import config

@pytest.fixture
def sample_data():
    """Create a sample DataFrame for testing."""
    np.random.seed(42)
    years = range(1990, 2021)
    n_samples = len(years)
    
    data = {
        'Year': years,
        'LA_Intake_percent_calories': np.random.normal(6, 1, n_samples),
        'LA_perc_kcal_lag5': np.random.normal(5.8, 1, n_samples),
        'LA_perc_kcal_lag10': np.random.normal(5.5, 1, n_samples),
        'Total_Fat_Supply_g': np.random.normal(100, 10, n_samples),
        'Plant_Fat_Ratio': np.random.uniform(0.4, 0.6, n_samples),
        'BMI_AgeStandardised': np.random.normal(25, 2, n_samples),
        'Obesity_Prevalence_AgeStandardised': np.random.normal(30, 5, n_samples),
        'CVD_Mortality_Rate_ASMR': np.random.normal(200, 20, n_samples),
        'CVD_Prevalence_Rate_IHME': np.random.normal(5000, 500, n_samples),
        'Dementia_Mortality_Rate_ASMR': np.random.normal(40, 5, n_samples),
        'Dementia_Prevalence_Rate_IHME': np.random.normal(1000, 100, n_samples)
    }
    
    return pd.DataFrame(data)

@pytest.fixture
def setup_test_dirs(tmp_path):
    """Set up temporary directories for test outputs."""
    reports_dir = tmp_path / 'reports'
    figures_dir = tmp_path / 'figures'
    reports_dir.mkdir()
    figures_dir.mkdir()
    
    # Temporarily override config paths
    original_reports_dir = config.REPORTS_DIR
    original_figures_dir = config.FIGURES_DIR
    config.REPORTS_DIR = reports_dir
    config.FIGURES_DIR = figures_dir
    
    yield {'reports': reports_dir, 'figures': figures_dir}
    
    # Restore original paths
    config.REPORTS_DIR = original_reports_dir
    config.FIGURES_DIR = original_figures_dir

def test_perform_summary_statistics(sample_data, setup_test_dirs):
    """Test summary statistics generation."""
    perform_summary_statistics(sample_data)
    
    # Check if summary files were created
    assert (setup_test_dirs['reports'] / 'eda_summary_statistics.csv').exists()
    assert (setup_test_dirs['reports'] / 'eda_missing_data_summary.csv').exists()
    assert (setup_test_dirs['reports'] / 'eda_summary_ihme.csv').exists()
    assert (setup_test_dirs['reports'] / 'eda_summary_abs.csv').exists()
    assert (setup_test_dirs['reports'] / 'eda_summary_ncd_risc.csv').exists()

def test_plot_distributions(sample_data, setup_test_dirs):
    """Test distribution plot generation."""
    plot_distributions(sample_data)
    
    # Check if distribution plots were created
    assert (setup_test_dirs['figures'] / 'distributions_dietary.png').exists()
    for category in HEALTH_VARS.keys():
        assert (setup_test_dirs['figures'] / f'distributions_health_{category.lower()}.png').exists()

def test_perform_correlation_analysis(sample_data, setup_test_dirs):
    """Test correlation analysis."""
    perform_correlation_analysis(sample_data)
    
    # Check if correlation files were created
    assert (setup_test_dirs['reports'] / 'eda_correlation_matrix.csv').exists()
    assert (setup_test_dirs['reports'] / 'eda_lag_correlations.csv').exists()
    
    # Check if correlation heatmaps were created
    for category in HEALTH_VARS.keys():
        assert (setup_test_dirs['figures'] / f'eda_correlation_heatmap_{category.lower()}.png').exists()

def test_plot_time_series(sample_data, setup_test_dirs):
    """Test time series plot generation."""
    plot_time_series(sample_data)
    
    # Check if time series plots were created
    assert (setup_test_dirs['figures'] / 'time_series_dietary.png').exists()
    for category in HEALTH_VARS.keys():
        assert (setup_test_dirs['figures'] / f'time_series_health_{category.lower()}.png').exists()

def test_load_data_for_eda(tmp_path, monkeypatch):
    """Test data loading function."""
    # Create a temporary CSV file
    test_data = pd.DataFrame({
        'Year': [2020, 2021],
        'LA_Intake_percent_calories': [5.5, 5.7]
    })
    test_file = tmp_path / 'test_data.csv'
    test_data.to_csv(test_file, index=False)
    
    # Patch the config to use our test file
    monkeypatch.setattr(config, 'ANALYTICAL_DATA_FINAL_FILE', test_file)
    
    # Test successful load
    result = load_data_for_eda()
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    
    # Test file not found
    monkeypatch.setattr(config, 'ANALYTICAL_DATA_FINAL_FILE', tmp_path / 'nonexistent.csv')
    result = load_data_for_eda()
    assert result is None

def test_error_handling(setup_test_dirs):
    """Test error handling with invalid input."""
    # Test with None
    perform_summary_statistics(None)
    plot_distributions(None)
    perform_correlation_analysis(None)
    plot_time_series(None)
    
    # Test with empty DataFrame
    empty_df = pd.DataFrame()
    perform_summary_statistics(empty_df)
    plot_distributions(empty_df)
    perform_correlation_analysis(empty_df)
    plot_time_series(empty_df)

def test_variable_groups():
    """Test that variable groups are properly defined."""
    assert isinstance(DIETARY_VARS, list)
    assert isinstance(HEALTH_VARS, dict)
    assert all(isinstance(vars_list, list) for vars_list in HEALTH_VARS.values())
    assert 'BMI' in HEALTH_VARS
    assert 'CVD' in HEALTH_VARS
    assert 'Dementia' in HEALTH_VARS 