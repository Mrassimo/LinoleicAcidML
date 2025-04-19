# src/analysis/run_eda.py

"""
Script to run Exploratory Data Analysis (EDA) for the Seed Oils ML project.
This script executes the EDA functions defined in eda.py and generates reports and visualisations.
"""

import logging
from pathlib import Path
import sys
from datetime import datetime

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.analysis.eda import (
    load_data_for_eda,
    perform_summary_statistics,
    plot_distributions,
    perform_correlation_analysis,
    plot_time_series
)

def main():
    """
    Main function to run the EDA process.
    """
    # Set up logging with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / f"eda_run_{timestamp}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    logging.info("Starting EDA process...")

    # Load the data
    df = load_data_for_eda()
    if df is None:
        logging.error("Failed to load data. Exiting...")
        return

    try:
        # Perform summary statistics
        logging.info("Generating summary statistics...")
        perform_summary_statistics(df)

        # Generate distribution plots
        logging.info("Creating distribution plots...")
        plot_distributions(df)

        # Perform correlation analysis
        logging.info("Performing correlation analysis...")
        perform_correlation_analysis(df)

        # Create time series plots
        logging.info("Creating time series plots...")
        plot_time_series(df)

        logging.info("EDA process completed successfully!")
        logging.info(f"Log file saved to: {log_file}")
        logging.info("Check the reports/ and figures/ directories for outputs.")

    except Exception as e:
        logging.error(f"Error during EDA process: {e}")
        raise

if __name__ == "__main__":
    main() 