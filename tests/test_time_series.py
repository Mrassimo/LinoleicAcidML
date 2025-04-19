"""
Unit tests for dual-axis time series visualisation.

Tests the plot_dual_axis_time_series function in src/visualisation/time_series.py.
Follows project standards: Pytest, Google-style docstrings, type hints, and mocking.
"""

import pytest
import pandas as pd
from unittest import mock
from src.visualisation.time_series import plot_dual_axis_time_series, TimeSeriesConfig

@pytest.fixture
def dummy_df():
    """Fixture for a small dummy DataFrame with LA and health outcome metrics."""
    return pd.DataFrame({
        "Year": [2000, 2001, 2002, 2003, 2004],
        "LA_Intake_percent_calories": [5.0, 5.5, 6.0, 6.2, 6.5],
        "Obesity_Prevalence_AgeStandardised": [20.0, 21.0, 22.5, 23.0, 24.0]
    })

def test_plot_dual_axis_time_series_happy_path(dummy_df):
    """Test that the function runs and saves a figure for valid input."""
    config = TimeSeriesConfig(
        output_dir="figures",
        show_plots=False,
        date_col="Year",
        variables=None
    )
    with mock.patch("matplotlib.figure.Figure.savefig") as mock_savefig:
        fig = plot_dual_axis_time_series(
            dummy_df,
            config,
            la_col="LA_Intake_percent_calories",
            health_col="Obesity_Prevalence_AgeStandardised",
            title="Test Dual Axis",
            la_label="LA Intake",
            health_label="Obesity Prevalence",
            annotate=True,
        )
        assert fig is not None
        mock_savefig.assert_called_once()
        assert fig.get_axes()[0].get_ylabel() == "LA Intake"

def test_plot_dual_axis_time_series_custom_filename(dummy_df):
    """Test that the function saves the figure with a custom output filename when provided."""
    config = TimeSeriesConfig(
        output_dir="figures",
        show_plots=False,
        date_col="Year",
        variables=None
    )
    with mock.patch("matplotlib.figure.Figure.savefig") as mock_savefig:
        fig = plot_dual_axis_time_series(
            dummy_df,
            config,
            la_col="LA_Intake_percent_calories",
            health_col="Obesity_Prevalence_AgeStandardised",
            title="Test Custom Filename",
            la_label="LA Intake",
            health_label="Obesity Prevalence",
            annotate=True,
            output_filename="impact_LA_vs_Health_timeseries.png",
        )
        assert fig is not None
        mock_savefig.assert_called_once()
        args, kwargs = mock_savefig.call_args
        assert "impact_LA_vs_Health_timeseries.png" in args[0]


def test_plot_dual_axis_time_series_missing_column(dummy_df):
    """Test that the function raises KeyError if a required column is missing."""
    config = TimeSeriesConfig(
        output_dir="figures",
        show_plots=False,
        date_col="Year",
        variables=None
    )
    with pytest.raises(KeyError):
        plot_dual_axis_time_series(
            dummy_df.drop(columns=["LA_Intake_percent_calories"]),
            config,
            la_col="LA_Intake_percent_calories",
            health_col="Obesity_Prevalence_AgeStandardised"
        )

def test_plot_dual_axis_time_series_empty_df():
    """Test that the function handles an empty DataFrame gracefully."""
    config = TimeSeriesConfig(
        output_dir="figures",
        show_plots=False,
        date_col="Year",
        variables=None
    )
    empty_df = pd.DataFrame(columns=["Year", "LA_Intake_percent_calories", "Obesity_Prevalence_AgeStandardised"])
    with pytest.raises(ValueError):
        plot_dual_axis_time_series(
            empty_df,
            config,
            la_col="LA_Intake_percent_calories",
            health_col="Obesity_Prevalence_AgeStandardised"
        )