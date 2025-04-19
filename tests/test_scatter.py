"""
Unit tests for lagged scatter plot visualisation.

Tests the plot_lagged_scatter function in src/visualisation/scatter.py.
Follows project standards: Pytest, Google-style docstrings, type hints, and mocking.
"""

import pytest
import pandas as pd
from unittest import mock
from src.visualisation.scatter import plot_lagged_scatter, ScatterConfig

@pytest.fixture
def dummy_df():
    """Fixture for a small dummy DataFrame with lagged LA and health outcome metrics."""
    return pd.DataFrame({
        "Year": [2000, 2001, 2002, 2003, 2004],
        "LA_perc_kcal_lag10": [4.5, 5.0, 5.5, 6.0, 6.5],
        "Diabetes_Prevalence_Rate_AgeStandardised": [6.0, 6.2, 6.5, 6.7, 7.0]
    })

def test_plot_lagged_scatter_happy_path(dummy_df):
    """Test that the function runs and saves a figure for valid input."""
    config = ScatterConfig(
        output_dir="figures",
        show_plots=False,
        lag=0
    )
    with mock.patch("matplotlib.figure.Figure.savefig") as mock_savefig:
        fig = plot_lagged_scatter(
            dummy_df,
            x="LA_perc_kcal_lag10",
            y="Diabetes_Prevalence_Rate_AgeStandardised",
            config=config,
            title="Test Lagged Scatter"
        )
        assert fig is not None
        mock_savefig.assert_called_once()
        assert fig.get_axes()[0].get_xlabel() == "LA_perc_kcal_lag10 (lag 0)"

def test_plot_lagged_scatter_missing_column(dummy_df):
    """Test that the function raises KeyError if a required column is missing."""
    config = ScatterConfig(
        output_dir="figures",
        show_plots=False,
        lag=0
    )
    with pytest.raises(KeyError):
        plot_lagged_scatter(
            dummy_df.drop(columns=["LA_perc_kcal_lag10"]),
            x="LA_perc_kcal_lag10",
            y="Diabetes_Prevalence_Rate_AgeStandardised",
            config=config
        )

def test_plot_lagged_scatter_empty_df():
    """Test that the function handles an empty DataFrame gracefully."""
    config = ScatterConfig(
        output_dir="figures",
        show_plots=False,
        lag=0
    )
    empty_df = pd.DataFrame(columns=["Year", "LA_perc_kcal_lag10", "Diabetes_Prevalence_Rate_AgeStandardised"])
    with pytest.raises(ValueError):
        plot_lagged_scatter(
            empty_df,
            x="LA_perc_kcal_lag10",
            y="Diabetes_Prevalence_Rate_AgeStandardised",
            config=config
        )