# tests/test_time_series.py
"""
Unit tests for the Time-Series modelling functions in src/models/time_series.py.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
# Import the functions to be tested
from src.models.time_series import (
    prepare_time_series_data,
    fit_arima_model,
    # fit_prophet_model, # Uncomment if testing Prophet
    evaluate_ts_model,
    plot_forecast
)
# Import statsmodels types if needed for assertions later
# from statsmodels.tsa.arima.model import ARIMAResultsWrapper

# --- Fixtures (Optional Placeholders - Define later) ---

@pytest.fixture
def sample_time_series_df():
    """
    Provides a sample DataFrame for time-series testing.
    """
    dates = pd.to_datetime(pd.date_range(start='2000-01-01', periods=36, freq='YS')) # Yearly frequency
    data = {
        'Year': dates.year,
        'Value': np.random.rand(36) * 100 + np.linspace(0, 50, 36) # Add trend
    }
    df = pd.DataFrame(data)
    # Add potential issues like missing dates or values if needed
    # df = df.drop(index=5) # Example: drop a row
    # df.loc[10, 'Value'] = np.nan # Example: add NaN
    return df

@pytest.fixture
def sample_prepared_ts(sample_time_series_df):
    """ Provides a sample prepared time series (output of prepare_time_series_data). """
    # This fixture depends on the actual implementation of prepare_time_series_data
    # For placeholder, create a simple Series
    df = sample_time_series_df
    ts = pd.Series(df['Value'].values, index=pd.to_datetime(df['Year'], format='%Y'), name='Value')
    ts = ts.sort_index()
    # Apply basic interpolation if needed for testing fit functions
    # ts = ts.interpolate(method='time')
    return ts

# --- Test Functions ---

def test_prepare_time_series_data_success(sample_time_series_df):
    """ Test successful preparation of time series data. """
    df = sample_time_series_df
    ts = prepare_time_series_data(df, date_column='Year', value_column='Value')
    assert ts is not None
    assert isinstance(ts, pd.Series)
    assert isinstance(ts.index, pd.DatetimeIndex)
    # Assuming prepare_time_series_data handles NaNs (e.g., interpolation or dropping)
    # If not, this assertion might need adjustment based on the actual implementation
    # assert not ts.isnull().any()
    assert ts.index.is_monotonic_increasing

def test_prepare_time_series_data_invalid_column(sample_time_series_df):
    """ Test preparation with invalid column names. """
    df = sample_time_series_df
    ts = prepare_time_series_data(df, date_column='InvalidDate', value_column='Value')
    assert ts is None
    ts = prepare_time_series_data(df, date_column='Year', value_column='InvalidValue')
    assert ts is None

def test_fit_arima_model_success(sample_prepared_ts):
    """ Test successful fitting of an ARIMA model. """
    ts = sample_prepared_ts
    # Use a simple order for testing. Wrap in pytest.warns for convergence issues.
    # Need to import ConvergenceWarning from statsmodels.tools.sm_exceptions
    # from statsmodels.tools.sm_exceptions import ConvergenceWarning
    # with pytest.warns(ConvergenceWarning):
    model_fit = fit_arima_model(ts, order=(1,1,0))
    assert model_fit is not None
    # Add check for model type if possible/needed
    # assert isinstance(model_fit, ARIMAResultsWrapper)

def test_fit_arima_model_none_input():
    """ Test fitting ARIMA with None input. """
    model_fit = fit_arima_model(None, order=(1,1,0))
    assert model_fit is None

# Add tests for fit_prophet_model if implemented

def test_evaluate_ts_model_success(sample_prepared_ts):
    """ Test successful evaluation of a time-series model. """
    # Requires fitting a model and having test data
    ts = sample_prepared_ts
    # Ensure enough data for split and fitting
    if len(ts) < 10:
        pytest.skip("Not enough data in sample_prepared_ts for train/test split and model fitting.")

    train_ts = ts[:-5] # Example split
    test_ts = ts[-5:]
    # Need to import ConvergenceWarning from statsmodels.tools.sm_exceptions
    # from statsmodels.tools.sm_exceptions import ConvergenceWarning
    # with pytest.warns(ConvergenceWarning):
    model_fit = fit_arima_model(train_ts, order=(1,1,0))
    assert model_fit is not None # Ensure model fitted first
    metrics = evaluate_ts_model(model_fit, test_ts)
    assert metrics is not None
    assert isinstance(metrics, dict)
    assert 'rmse' in metrics # Or other relevant metric like 'mae', 'mse'

def test_evaluate_ts_model_none_input():
    """ Test evaluation with None model input. """
    metrics = evaluate_ts_model(None, pd.Series([1,2])) # Provide dummy test data
    assert metrics is None

def test_plot_forecast_runs(sample_prepared_ts, tmp_path):
    """ Test that plot_forecast runs without errors and saves a file. """
    ts = sample_prepared_ts
    # Ensure enough data for fitting
    if len(ts) < 5:
         pytest.skip("Not enough data in sample_prepared_ts for model fitting.")

    # Need to import ConvergenceWarning from statsmodels.tools.sm_exceptions
    # from statsmodels.tools.sm_exceptions import ConvergenceWarning
    # with pytest.warns(ConvergenceWarning):
    model_fit = fit_arima_model(ts, order=(1,1,0))
    assert model_fit is not None

    output_dir = tmp_path / "ts_forecasts"
    model_name = "ARIMA_test"
    steps = 5
    plot_forecast(model_fit, ts, steps, output_dir, model_name)
    assert output_dir.is_dir()
    assert (output_dir / f'forecast_{model_name}.png').is_file()

def test_plot_forecast_none_input(tmp_path):
    """ Test plot_forecast handles None model input gracefully. """
    output_dir = tmp_path / "ts_forecasts_none"
    # Provide dummy data for the time series argument
    dummy_ts = pd.Series([1, 2, 3, 4, 5], index=pd.to_datetime(pd.date_range(start='2020-01-01', periods=5, freq='D')))
    plot_forecast(None, dummy_ts, 5, output_dir, "NoneTest")
    # Assert it ran without error, and the output directory was not created
    assert not output_dir.exists()