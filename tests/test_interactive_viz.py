"""
Tests for the interactive visualisation module.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.graph_objects as go
from src.visualisation.interactive import (
    create_time_series_plot,
    create_correlation_heatmap,
    create_scatter_with_trend,
    create_feature_importance_plot,
    create_model_comparison_plot,
    create_gam_partial_dependence_plot,
    save_interactive_plots
)

@pytest.fixture
def sample_df():
    """Create a sample DataFrame for testing."""
    dates = pd.date_range(start='1980', end='2020', freq='Y')
    np.random.seed(42)
    
    return pd.DataFrame({
        'Year': dates,
        'LA_Intake_percent_calories': np.random.normal(6, 1, len(dates)),
        'Diabetes_Prevalence_Rate': np.random.normal(5, 0.5, len(dates)),
        'CVD_Mortality_Rate': np.random.normal(200, 20, len(dates)),
        'Total_Fat_Supply_g': np.random.normal(100, 10, len(dates))
    }).set_index('Year')

@pytest.fixture
def sample_model_results():
    """Create sample model results for testing."""
    return {
        'feature_importance': pd.DataFrame({
            'feature': ['LA_Intake', 'Total_Fat', 'Year'],
            'importance': [0.5, 0.3, 0.2]
        }),
        'model_metrics': pd.DataFrame({
            'R2': [0.8, 0.75, 0.7],
            'RMSE': [0.1, 0.15, 0.2]
        }, index=['GAM', 'Random Forest', 'XGBoost']),
        'gam_results': {
            'LA_Intake': {
                'x_values': np.linspace(4, 8, 100),
                'y_values': np.sin(np.linspace(4, 8, 100)),
                'confidence_intervals': (
                    np.sin(np.linspace(4, 8, 100)) - 0.2,
                    np.sin(np.linspace(4, 8, 100)) + 0.2
                )
            }
        }
    }

def test_create_time_series_plot(sample_df):
    """Test time series plot creation."""
    y_cols = ['LA_Intake_percent_calories', 'Diabetes_Prevalence_Rate']
    fig = create_time_series_plot(sample_df, y_cols)
    
    assert isinstance(fig, go.Figure)
    assert len(fig.data) == len(y_cols)
    assert fig.layout.title.text == "Time Series Analysis"

def test_create_correlation_heatmap(sample_df):
    """Test correlation heatmap creation."""
    corr_matrix = sample_df.corr()
    fig = create_correlation_heatmap(corr_matrix)
    
    assert isinstance(fig, go.Figure)
    assert isinstance(fig.data[0], go.Heatmap)
    assert fig.layout.title.text == "Correlation Analysis"

def test_create_scatter_with_trend(sample_df):
    """Test scatter plot creation."""
    fig = create_scatter_with_trend(
        sample_df,
        'LA_Intake_percent_calories',
        'Diabetes_Prevalence_Rate'
    )
    
    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 2  # Scatter points and trend line

def test_create_feature_importance_plot(sample_model_results):
    """Test feature importance plot creation."""
    fig = create_feature_importance_plot(
        sample_model_results['feature_importance']
    )
    
    assert isinstance(fig, go.Figure)
    assert isinstance(fig.data[0], go.Bar)
    assert len(fig.data[0].x) == 3  # Number of features

def test_create_model_comparison_plot(sample_model_results):
    """Test model comparison plot creation."""
    fig = create_model_comparison_plot(
        sample_model_results['model_metrics']
    )
    
    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 2  # Number of metrics
    assert len(fig.data[0].x) == 3  # Number of models

def test_create_gam_partial_dependence_plot(sample_model_results):
    """Test GAM partial dependence plot creation."""
    gam_data = sample_model_results['gam_results']['LA_Intake']
    fig = create_gam_partial_dependence_plot(
        gam_data['x_values'],
        gam_data['y_values'],
        gam_data['confidence_intervals'],
        'LA_Intake'
    )
    
    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 2  # Main line and confidence interval

def test_save_interactive_plots(tmp_path, sample_df, sample_model_results):
    """Test saving all interactive plots."""
    output_dir = tmp_path / "figures" / "interactive"
    save_interactive_plots(sample_df, output_dir, sample_model_results)
    
    # Check if files were created
    assert (output_dir / "health_metrics_time_series.html").exists()
    assert (output_dir / "dietary_metrics_time_series.html").exists()
    assert (output_dir / "correlation_heatmap.html").exists()
    assert (output_dir / "feature_importance.html").exists()
    assert (output_dir / "model_comparison.html").exists()
    
    # Check for scatter plots
    scatter_plots = list(output_dir.glob("scatter_*.html"))
    assert len(scatter_plots) > 0
    
    # Check for GAM plots
    gam_plots = list(output_dir.glob("gam_pdp_*.html"))
    assert len(gam_plots) > 0 