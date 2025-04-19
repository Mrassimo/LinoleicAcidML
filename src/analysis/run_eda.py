# src/analysis/run_eda.py

"""Script to run Exploratory Data Analysis functions."""

import pandas as pd
import logging
from pathlib import Path
import sys

# Ensure the src directory is in the Python path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.analysis.eda import (
    calculate_summary_statistics, calculate_correlations, analyse_missing_data
)
from src.config import ANALYTICAL_DATA_FINAL_FILE, REPORTS_DIR

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Load data and run EDA functions."""
    logger.info("Starting EDA script...")

    # Define output file paths
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    summary_stats_output_path = REPORTS_DIR / "eda_summary_statistics.csv"
    correlation_output_path = REPORTS_DIR / "eda_correlation_matrix.csv"
    missing_data_output_path = REPORTS_DIR / "eda_missing_data_summary.csv"

    # Load data
    try:
        logger.info(f"Loading data from {ANALYTICAL_DATA_FINAL_FILE}")
        data = pd.read_csv(ANALYTICAL_DATA_FINAL_FILE)
        logger.info("Data loaded successfully.")
    except FileNotFoundError:
        logger.error(f"Error: Data file not found at {ANALYTICAL_DATA_FINAL_FILE}")
        return
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        return

    # --- Calculate and print/save summary statistics ---
    logger.info("Calculating summary statistics...")
    summary_stats = calculate_summary_statistics(data)
    if not summary_stats.empty:
        print("\n--- Summary Statistics ---")
        print(summary_stats)
        try:
            summary_stats.to_csv(summary_stats_output_path)
            logger.info(f"Summary statistics saved to {summary_stats_output_path}")
        except Exception as e:
            logger.error(f"Error saving summary statistics: {e}")
    else:
        logger.warning("Summary statistics calculation returned empty results.")

    # --- Calculate and print/save correlation matrix ---
    logger.info("Calculating correlation matrix (Pearson)...")
    correlation_matrix = calculate_correlations(data, method='pearson')
    if not correlation_matrix.empty:
        print("\n--- Correlation Matrix (Pearson) ---")
        print(correlation_matrix)
        try:
            correlation_matrix.to_csv(correlation_output_path)
            logger.info(f"Correlation matrix saved to {correlation_output_path}")
        except Exception as e:
            logger.error(f"Error saving correlation matrix: {e}")
    else:
        logger.warning("Correlation matrix calculation returned empty results.")

    # --- Analyse and print/save missing data ---
    logger.info("Analysing missing data...")
    missing_summary = analyse_missing_data(data)
    if not missing_summary.empty:
        print("\n--- Missing Data Summary ---")
        print(missing_summary)
        try:
            missing_summary.to_csv(missing_data_output_path, index=False)
            logger.info(f"Missing data summary saved to {missing_data_output_path}")
        except Exception as e:
            logger.error(f"Error saving missing data summary: {e}")

    # TODO: Add calls to other EDA functions (distribution checks, missing data analysis) here

    logger.info("EDA script finished.")

if __name__ == "__main__":
    main() 