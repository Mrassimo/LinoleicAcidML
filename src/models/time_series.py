# src/models/time_series.py

"""Time Series Modelling functions (Optional)."""

import pandas as pd
# Consider using statsmodels.tsa or prophet
# from statsmodels.tsa.arima.model import ARIMA
# from prophet import Prophet
from pydantic import BaseModel, Field
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TimeSeriesConfig(BaseModel):
    target_var: str = Field(..., description="Name of the time series variable to model/forecast.")
    date_col: str = Field(..., description="Name of the date/time column.")
    # Add model-specific config (e.g., ARIMA order, Prophet params)


def fit_time_series_model(data: pd.DataFrame, config: TimeSeriesConfig):
    """Fits a time series model based on the provided config."""
    logger.info(f"Fitting time series model for {config.target_var}...")

    # TODO: Ensure data is sorted by date
    # data = data.sort_values(by=config.date_col)
    # data = data.set_index(config.date_col)

    # TODO: Implement time series model fitting (e.g., ARIMA, Prophet)
    # Example structure:
    # series = data[config.target_var]
    # model = ... # Initialize chosen model (ARIMA, Prophet, etc.)
    # results = model.fit()
    # logger.info("Time series model fitting complete.")
    # return results

    logger.warning("Time series modelling not yet implemented.")
    return None

# TODO: Add functions for forecasting, evaluation, diagnostics etc. 