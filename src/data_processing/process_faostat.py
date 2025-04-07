"""
Process FAOSTAT data for Australia from the pre-processed food balance sheets.
"""

import pandas as pd
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_processed_faostat() -> pd.DataFrame:
    """
    Load the pre-processed FAOSTAT food balance sheets data
    """
    try:
        data_dir = Path('data')
        processed_dir = data_dir / 'processed'
        file_path = processed_dir / 'faostat_food_balance_sheets.csv'
        
        df = pd.read_csv(file_path)
        logger.info(f"Successfully loaded processed FAOSTAT data from {file_path}")
        return df
        
    except Exception as e:
        logger.error(f"Error loading processed FAOSTAT data: {e}")
        raise

def main():
    # Load the pre-processed FAOSTAT data
    faostat_df = load_processed_faostat()
    logger.info(f"Loaded {len(faostat_df)} records from processed FAOSTAT data")

if __name__ == "__main__":
    main() 