# src/analysis/eda.py

"""Exploratory Data Analysis (EDA) functions."""

import pandas as pd
from pydantic import BaseModel, Field, FilePath
import logging
import numpy as np # Import numpy for numeric type checking
from scipy import stats # Import scipy for normality test

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EdaConfig(BaseModel):
    data_path: FilePath = Field(..., description="Path to the input data CSV file.")
    # Add other config options as needed (e.g., columns for analysis)

def calculate_summary_statistics(data: pd.DataFrame) -> pd.DataFrame:
    """Calculates summary statistics for numeric columns in the DataFrame.

    Args:
        data: Input DataFrame.

    Returns:
        DataFrame containing summary statistics (count, mean, std, min, quantiles, max)
        for the numeric columns. Returns an empty DataFrame if no numeric columns are found.
    """
    logger.info("Calculating summary statistics for numeric columns...")

    # Select only columns with numeric data types
    numeric_data = data.select_dtypes(include=np.number)

    if numeric_data.empty:
        logger.warning("No numeric columns found in the provided DataFrame.")
        return pd.DataFrame() # Return empty DataFrame

    summary = numeric_data.describe()
    logger.info("Summary statistics calculated successfully.")
    logger.debug(f"Summary statistics:\n{summary}")
    return summary

def calculate_correlations(data: pd.DataFrame, method: str = 'pearson') -> pd.DataFrame:
    """Calculates pairwise correlation between numeric columns.

    Args:
        data: Input DataFrame.
        method: Correlation method ('pearson', 'kendall', 'spearman').

    Returns:
        DataFrame containing the correlation matrix for numeric columns.
        Returns an empty DataFrame if fewer than two numeric columns are found.
    """
    logger.info(f"Calculating {method} correlations for numeric columns...")

    # Select only columns with numeric data types
    numeric_data = data.select_dtypes(include=np.number)

    if numeric_data.shape[1] < 2:
        logger.warning(f"Need at least two numeric columns for correlation. Found {numeric_data.shape[1]}.")
        return pd.DataFrame() # Return empty DataFrame

    correlations = numeric_data.corr(method=method)
    logger.info("Correlation matrix calculated successfully.")
    logger.debug(f"Correlation matrix:\n{correlations}")
    return correlations

def analyse_missing_data(data: pd.DataFrame) -> pd.DataFrame:
    """Calculates the count and percentage of missing values for each column.

    Args:
        data: Input DataFrame.

    Returns:
        DataFrame summarising missing values per column, sorted by percentage descending.
        Columns: 'Column', 'Missing Count', 'Missing Percentage'.
    """
    logger.info("Analysing missing data...")
    missing_counts = data.isnull().sum()
    missing_percentage = (missing_counts / len(data)) * 100

    missing_summary = pd.DataFrame({
        'Column': data.columns,
        'Missing Count': missing_counts,
        'Missing Percentage': missing_percentage
    })

    # Sort by percentage descending to show most problematic columns first
    missing_summary = missing_summary.sort_values(by='Missing Percentage', ascending=False)

    # Filter out columns with no missing data for brevity, unless all columns have data
    if (missing_summary['Missing Count'] > 0).any():
        missing_summary = missing_summary[missing_summary['Missing Count'] > 0]

    if missing_summary.empty:
        logger.info("No missing data found in any columns.")
    else:
        logger.info("Missing data analysis complete.")
        logger.debug(f"Missing data summary:\n{missing_summary}")

    return missing_summary

def calculate_distribution_stats(data: pd.DataFrame) -> pd.DataFrame:
    """Calculates skewness, kurtosis, and Shapiro-Wilk normality test for numeric columns.

    Args:
        data: Input DataFrame.

    Returns:
        DataFrame summarising distribution statistics per numeric column.
        Columns: 'Column', 'Skewness', 'Kurtosis', 'Shapiro_W', 'Shapiro_p_value'.
        Returns an empty DataFrame if no numeric columns are found.
    """
    logger.info("Calculating distribution statistics (Skewness, Kurtosis, Shapiro-Wilk)...")

    numeric_data = data.select_dtypes(include=np.number)

    if numeric_data.empty:
        logger.warning("No numeric columns found for distribution analysis.")
        return pd.DataFrame()

    results = []
    for col in numeric_data.columns:
        # Drop NaNs for calculations
        col_data = numeric_data[col].dropna()

        # Shapiro-Wilk test requires at least 3 data points
        if len(col_data) < 3:
            logger.warning(f"Skipping Shapiro-Wilk for column '{col}' (needs >= 3 non-NaN values, has {len(col_data)}).")
            shapiro_w, shapiro_p = np.nan, np.nan
        else:
            try:
                shapiro_w, shapiro_p = stats.shapiro(col_data)
            except Exception as e:
                logger.warning(f"Could not calculate Shapiro-Wilk for column '{col}': {e}")
                shapiro_w, shapiro_p = np.nan, np.nan

        skewness = col_data.skew()
        kurt = col_data.kurtosis() # Fisher's definition (normal == 0)

        results.append({
            'Column': col,
            'Skewness': skewness,
            'Kurtosis': kurt,
            'Shapiro_W': shapiro_w,
            'Shapiro_p_value': shapiro_p
        })

    dist_summary = pd.DataFrame(results)
    logger.info("Distribution statistics calculated.")
    logger.debug(f"Distribution summary:\n{dist_summary}")

    return dist_summary

# TODO: Add functions for:
# - Outlier detection
# - Lag analysis calculation 