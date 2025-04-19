# src/models/time_series.py
"""
Time-Series modelling functions (e.g., ARIMA, Prophet) for the Seed Oils ML project.

This module contains functions for:
- Fitting time-series models (ARIMA, Prophet)
- Evaluating model performance on time-series data
- Generating forecasts and forecast plots
"""

import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from prophet import Prophet
import matplotlib.pyplot as plt
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
from pydantic import BaseModel
from sklearn.metrics import mean_squared_error
from pmdarima import auto_arima

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TimeSeriesConfig(BaseModel):
    """Configuration for time-series models."""
    date_column: str
    value_column: str
    test_size: float = 0.2
    forecast_periods: int = 5
    seasonality_mode: str = 'multiplicative'  # For Prophet
    changepoint_prior_scale: float = 0.05  # For Prophet
    max_arima_order: Tuple[int, int, int] = (5, 2, 5)  # For auto_arima

def prepare_time_series_data(
    df: pd.DataFrame,
    config: TimeSeriesConfig
) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """
    Prepares data for time-series modelling by converting date column to datetime,
    setting it as index, selecting the value column, sorting, and splitting into train/test.

    Args:
        df (pd.DataFrame): Input dataframe
        config (TimeSeriesConfig): Model configuration

    Returns:
        Tuple containing full series, training series, and test series
    """
    logging.info(f"Preparing time series data for column: {config.value_column}...")
    try:
        # Ensure date column is datetime type and set as index
        ts_df = df.copy()
        ts_df[config.date_column] = pd.to_datetime(ts_df[config.date_column], format='%Y')
        ts_df = ts_df.set_index(config.date_column)
        ts_series = ts_df[config.value_column].sort_index()
        
        # Handle missing values if necessary (e.g., interpolation)
        ts_series = ts_series.interpolate(method='time')
        
        # Split data
        split_idx = int(len(ts_series) * (1 - config.test_size))
        train_series = ts_series[:split_idx]
        test_series = ts_series[split_idx:]
        
        logging.info(f"Time series data prepared. Train size: {len(train_series)}, Test size: {len(test_series)}")
        return ts_series, train_series, test_series
    
    except Exception as e:
        logging.error(f"Error preparing time series data: {e}")
        raise

def fit_auto_arima(
    train_data: pd.Series,
    config: TimeSeriesConfig
) -> ARIMA:
    """
    Automatically finds the best ARIMA model using pmdarima's auto_arima.

    Args:
        train_data (pd.Series): Training time series data
        config (TimeSeriesConfig): Model configuration

    Returns:
        Best ARIMA model
    """
    logging.info("Finding best ARIMA model parameters...")
    try:
        # Find best parameters
        auto_model = auto_arima(
            train_data,
            start_p=0, start_q=0,
            max_p=config.max_arima_order[0],
            max_d=config.max_arima_order[1],
            max_q=config.max_arima_order[2],
            seasonal=True,
            stepwise=True,
            suppress_warnings=True,
            error_action="ignore"
        )
        
        # Get best order
        best_order = auto_model.order
        logging.info(f"Best ARIMA order found: {best_order}")
        
        # Fit ARIMA with best parameters
        model = ARIMA(train_data, order=best_order)
        model_fit = model.fit()
        logging.info("ARIMA model fitted successfully")
        return model_fit
    
    except Exception as e:
        logging.error(f"Error fitting auto ARIMA model: {e}")
        raise

def fit_prophet_model(
    train_data: pd.Series,
    config: TimeSeriesConfig
) -> Prophet:
    """
    Fits a Prophet model to the time series data.

    Args:
        train_data (pd.Series): Training time series data
        config (TimeSeriesConfig): Model configuration

    Returns:
        Fitted Prophet model
    """
    logging.info("Fitting Prophet model...")
    try:
        # Prepare data for Prophet (requires 'ds' and 'y' columns)
        prophet_df = train_data.reset_index()
        prophet_df.columns = ['ds', 'y']
        
        # Initialize and fit Prophet model
        model = Prophet(
            seasonality_mode=config.seasonality_mode,
            changepoint_prior_scale=config.changepoint_prior_scale
        )
        model.fit(prophet_df)
        logging.info("Prophet model fitted successfully")
        return model
    
    except Exception as e:
        logging.error(f"Error fitting Prophet model: {e}")
        raise

def evaluate_ts_model(
    model: Union[ARIMA, Prophet],
    test_data: pd.Series,
    model_type: str
) -> Dict[str, float]:
    """
    Evaluates a time-series model by calculating RMSE and other metrics on test data.

    Args:
        model: The fitted time-series model
        test_data (pd.Series): The actual test time series data
        model_type (str): Type of model ('arima' or 'prophet')

    Returns:
        Dictionary containing evaluation metrics
    """
    logging.info(f"Evaluating {model_type} model...")
    try:
        if model_type.lower() == 'arima':
            predictions = model.predict(start=test_data.index.min(), end=test_data.index.max())
        else:  # Prophet
            future_df = pd.DataFrame({'ds': test_data.index})
            forecast = model.predict(future_df)
            predictions = pd.Series(forecast['yhat'].values, index=test_data.index)
        
        # Calculate metrics
        metrics = {
            'rmse': np.sqrt(mean_squared_error(test_data, predictions)),
            'mape': np.mean(np.abs((test_data - predictions) / test_data)) * 100,
            'r2': 1 - np.sum((test_data - predictions) ** 2) / np.sum((test_data - test_data.mean()) ** 2)
        }
        
        logging.info(f"Model evaluation metrics: {metrics}")
        return metrics
    
    except Exception as e:
        logging.error(f"Error evaluating {model_type} model: {e}")
        raise

def plot_forecast(
    model: Union[ARIMA, Prophet],
    ts_data: pd.Series,
    config: TimeSeriesConfig,
    output_dir: Path,
    model_type: str
):
    """
    Generates and saves forecast plots for a time-series model.

    Args:
        model: The fitted time-series model
        ts_data (pd.Series): The original time series data
        config (TimeSeriesConfig): Model configuration
        output_dir (Path): The directory to save the plot
        model_type (str): Type of model ('arima' or 'prophet')
    """
    logging.info(f"Generating forecast plot for {model_type}...")
    try:
        # Ensure output_dir exists
        output_dir.mkdir(parents=True, exist_ok=True)
        
        plt.figure(figsize=(12, 6))
        
        # Plot actual data
        plt.plot(ts_data.index, ts_data, label='Observed', color='blue')
        
        if model_type.lower() == 'arima':
            # Get forecast
            forecast_obj = model.get_forecast(steps=config.forecast_periods)
            forecast_values = forecast_obj.predicted_mean
            conf_int = forecast_obj.conf_int(alpha=0.05)
            
            # Plot forecast
            plt.plot(forecast_values.index, forecast_values, label='Forecast', color='red')
            plt.fill_between(
                conf_int.index,
                conf_int.iloc[:, 0],
                conf_int.iloc[:, 1],
                color='red',
                alpha=0.1,
                label='95% Confidence Interval'
            )
        else:  # Prophet
            # Create future dates
            future_dates = pd.date_range(
                start=ts_data.index.max(),
                periods=config.forecast_periods + 1,
                freq='Y'
            )[1:]
            future_df = pd.DataFrame({'ds': future_dates})
            
            # Get forecast
            forecast = model.predict(future_df)
            
            # Plot forecast
            plt.plot(future_dates, forecast['yhat'], label='Forecast', color='red')
            plt.fill_between(
                future_dates,
                forecast['yhat_lower'],
                forecast['yhat_upper'],
                color='red',
                alpha=0.1,
                label='95% Confidence Interval'
            )
        
        plt.title(f'{model_type} Forecast')
        plt.xlabel('Date')
        plt.ylabel('Value')
        plt.legend()
        plt.grid(True)
        
        # Save and close plot
        plot_path = output_dir / f'forecast_{model_type.lower()}.png'
        plt.savefig(plot_path)
        plt.close()
        logging.info(f"Forecast plot saved to {plot_path}")
        
    except Exception as e:
        logging.error(f"Error generating forecast plot for {model_type}: {e}")
        raise

if __name__ == '__main__':
    logging.info("Running time-series models example...")
    
    # Create dummy time series data
    dates = pd.date_range(start='2000', end='2020', freq='Y')
    values = pd.Series(
        np.linspace(10, 30, len(dates)) + np.random.randn(len(dates)) * 2 +
        5 * np.sin(np.linspace(0, 4*np.pi, len(dates))),  # Add seasonality
        index=dates
    )
    dummy_df = pd.DataFrame({
        'Year': dates,
        'Value': values
    })
    
    # Configure model
    config = TimeSeriesConfig(
        date_column='Year',
        value_column='Value',
        test_size=0.2,
        forecast_periods=5
    )
    
    try:
        # Prepare data
        ts_data, train_data, test_data = prepare_time_series_data(dummy_df, config)
        
        # Fit and evaluate ARIMA
        arima_model = fit_auto_arima(train_data, config)
        arima_metrics = evaluate_ts_model(arima_model, test_data, 'arima')
        
        # Fit and evaluate Prophet
        prophet_model = fit_prophet_model(train_data, config)
        prophet_metrics = evaluate_ts_model(prophet_model, test_data, 'prophet')
        
        # Generate forecasts
        output_dir = Path("./figures/time_series_forecasts")
        plot_forecast(arima_model, ts_data, config, output_dir, 'ARIMA')
        plot_forecast(prophet_model, ts_data, config, output_dir, 'Prophet')
        
        logging.info("Time-series models example completed successfully")
        
    except Exception as e:
        logging.error(f"Error in time-series models example: {e}")