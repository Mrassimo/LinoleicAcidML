# src/models/regression.py

"""Linear Regression modelling functions."""

import pandas as pd
import statsmodels.api as sm
from pydantic import BaseModel, Field, FilePath
from typing import List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RegressionConfig(BaseModel):
    data_path: FilePath = Field(..., description="Path to the input data CSV file.")
    dependent_var: str = Field(..., description="Name of the dependent variable.")
    independent_vars: List[str] = Field(..., description="List of independent variable names.")
    add_constant: bool = Field(True, description="Whether to add a constant (intercept) to the model.")
    # Add other config options as needed (e.g., output paths)

def fit_linear_regression(config: RegressionConfig) -> sm.regression.linear_model.RegressionResultsWrapper:
    """Fits a linear regression model based on the provided configuration.

    Args:
        config: A RegressionConfig object specifying model parameters.

    Returns:
        The fitted model results object from statsmodels.
    """
    logger.info(f"Fitting linear regression for {config.dependent_var} ~ {' + '.join(config.independent_vars)}")

    try:
        data = pd.read_csv(config.data_path)
    except FileNotFoundError:
        logger.error(f"Input data file not found: {config.data_path}")
        raise
    except Exception as e:
        logger.error(f"Error reading data file {config.data_path}: {e}")
        raise

    # Select relevant columns and drop rows with NaNs in those columns
    cols_to_use = [config.dependent_var] + config.independent_vars
    model_data = data[cols_to_use].dropna()

    if model_data.empty:
        logger.error("No data available for modelling after dropping NaNs.")
        raise ValueError("No data available for modelling after dropping NaNs.")

    Y = model_data[config.dependent_var]
    X = model_data[config.independent_vars]

    if config.add_constant:
        X = sm.add_constant(X)

    model = sm.OLS(Y, X)
    results = model.fit()

    logger.info("Linear regression fitting complete.")
    logger.debug(results.summary())

    return results

# TODO: Add functions for model evaluation, assumption checking (VIF, residuals), prediction etc. 