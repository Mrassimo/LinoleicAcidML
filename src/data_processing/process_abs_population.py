"""
Processes the raw ABS National, State and Territory Population data.

Reads the downloaded Excel file, selects the relevant sheet and columns
(Year and Australian Population), standardises column names, and saves
the result to the staging directory.
"""

import pandas as pd
from pathlib import Path
import logging
from src import config

# --- Configuration ---
RAW_POPULATION_FILE = config.RAW_DATA_DIR / config.ABS_POPULATION_FILENAME
# STAGING_POPULATION_FILE = config.STAGING_DATA_DIR / "abs_population_processed.csv" # Old path
PROCESSED_POPULATION_FILE = config.ABS_POPULATION_PROCESSED_FILE # Use the config var for processed path

# --- Expected Structure (Update if script fails) ---
# Common ABS sheet names: 'Data1', 'Table 1', 'Table 3', etc.
EXPECTED_SHEET_NAME = 'Data1' # Confirmed from successful pandas read
# Common time columns: 'Financial year', 'Year', 'Date', or often part of a multi-index header
# TIME_COLUMN_HEADER = 'Unnamed: 0' # First column containing dates, likely needs skipping rows
# POPULATION_COLUMN_HEADER = 'Estimated Resident Population ;  Persons ;  Australia ;' # Confirmed from script output
DATE_COLUMN_INDEX = 0
POPULATION_COLUMN_INDEX = 27 # Last column in the 28-column sheet

# Standardised Output Column Names
OUTPUT_DATE_COLUMN = 'Date' # Temporary name before extracting year
OUTPUT_YEAR_COLUMN = 'Year'
OUTPUT_POPULATION_COLUMN = 'Population'

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_abs_population_data():
    """Loads, cleans, and saves the ABS population data."""
    logging.info(f"Starting processing of ABS population data: {RAW_POPULATION_FILE}")

    try:
        # Attempt to read the specific sheet
        # Skip the first 9 metadata rows, use default integer headers
        df = pd.read_excel(RAW_POPULATION_FILE, sheet_name=EXPECTED_SHEET_NAME, skiprows=9, header=None)
        logging.info(f"Successfully read sheet '{EXPECTED_SHEET_NAME}' from {RAW_POPULATION_FILE.name} (skipped first 9 rows, using integer headers)")
        # logging.info(f"Original columns after skipping rows: {df.columns.tolist()}") # Less useful with int headers

        # --- Data Selection and Cleaning ---
        # Select columns by index
        if df.shape[1] <= max(DATE_COLUMN_INDEX, POPULATION_COLUMN_INDEX):
            logging.error(f"Error: Expected at least {max(DATE_COLUMN_INDEX, POPULATION_COLUMN_INDEX) + 1} columns after skipping rows, but found only {df.shape[1]}. Cannot select by index.")
            raise ValueError("Incorrect number of columns found.")

        df_processed = df[[DATE_COLUMN_INDEX, POPULATION_COLUMN_INDEX]].copy()
        # Assign standard names
        df_processed.columns = [OUTPUT_DATE_COLUMN, OUTPUT_POPULATION_COLUMN]

        # Convert time column to Year (handle potential datetime objects)
        try:
             # Convert to datetime, coercing errors to NaT
             original_date_col = df_processed[OUTPUT_DATE_COLUMN]
             df_processed[OUTPUT_DATE_COLUMN] = pd.to_datetime(original_date_col, errors='coerce')
             
             # Log how many rows had parsing errors
             nat_count = df_processed[OUTPUT_DATE_COLUMN].isna().sum()
             if nat_count > 0:
                  logging.warning(f"Coerced {nat_count} non-date values to NaT in the date column. Original problematic values head:\n{original_date_col[df_processed[OUTPUT_DATE_COLUMN].isna()].head()}")
             
             # Drop rows where date conversion failed
             df_processed.dropna(subset=[OUTPUT_DATE_COLUMN], inplace=True)
             
             # Filter for December quarter data to get annual figures
             df_processed = df_processed[df_processed[OUTPUT_DATE_COLUMN].dt.month == 12].copy()
             logging.info(f"Filtered data to keep only December quarter rows. Shape after filtering: {df_processed.shape}")

             # Extract year
             df_processed[OUTPUT_YEAR_COLUMN] = df_processed[OUTPUT_DATE_COLUMN].dt.year
             logging.info(f"Extracted year from '{OUTPUT_DATE_COLUMN}' column after coercing errors.")
             
        except Exception as e:
             logging.error(f"Failed to extract year from '{OUTPUT_DATE_COLUMN}' (index {DATE_COLUMN_INDEX}) even after coercing. Error: {e}")
             raise ValueError(f"Could not process date column.")

        # Rename population column - already done above
        # df_processed = df_processed.rename(columns={POPULATION_COLUMN_HEADER: OUTPUT_POPULATION_COLUMN})

        # Keep only Year and Population
        df_processed = df_processed[[OUTPUT_YEAR_COLUMN, OUTPUT_POPULATION_COLUMN]]

        # Ensure Population is numeric, coercing errors
        df_processed[OUTPUT_POPULATION_COLUMN] = pd.to_numeric(df_processed[OUTPUT_POPULATION_COLUMN], errors='coerce')
        
        # Drop rows where population is NaN after coercion (optional, depends on data quality)
        df_processed.dropna(subset=[OUTPUT_POPULATION_COLUMN], inplace=True)
        
        # Convert Population to integer
        df_processed[OUTPUT_POPULATION_COLUMN] = df_processed[OUTPUT_POPULATION_COLUMN].astype(int)


        # --- Save Processed Data ---
        # Ensure the processed directory exists
        PROCESSED_POPULATION_FILE.parent.mkdir(parents=True, exist_ok=True)
        # config.STAGING_DATA_DIR.mkdir(parents=True, exist_ok=True)
        # df_processed.to_csv(STAGING_POPULATION_FILE, index=False)
        df_processed.to_csv(PROCESSED_POPULATION_FILE, index=False)
        # logging.info(f"Successfully processed and saved data to {STAGING_POPULATION_FILE}")
        logging.info(f"Successfully processed and saved data to {PROCESSED_POPULATION_FILE}")
        logging.info(f"Processed data shape: {df_processed.shape}")
        logging.info(f"Processed data head:\n{df_processed.head()}")


    except FileNotFoundError:
        logging.error(f"Error: Raw ABS population file not found at {RAW_POPULATION_FILE}")
        logging.error("Please ensure the file has been downloaded correctly using download_data.py and saved with the expected filename.")
    except ValueError as ve:
        logging.error(f"Data processing error: {ve}")
        logging.error(f"Please check the constants EXPECTED_SHEET_NAME ('{EXPECTED_SHEET_NAME}') and the skiprows=9 parameter in this script. Also verify column indices DATE_COLUMN_INDEX ({DATE_COLUMN_INDEX}) and POPULATION_COLUMN_INDEX ({POPULATION_COLUMN_INDEX}) match the actual structure.")
        # Log available sheet names if possible (requires openpyxl to be installed)
        try:
            import openpyxl
            workbook = openpyxl.load_workbook(RAW_POPULATION_FILE, read_only=True)
            logging.info(f"Available sheet names in the workbook: {workbook.sheetnames}")
            # Try reading header from the correct sheet to help debug
            try:
                df_head_debug = pd.read_excel(RAW_POPULATION_FILE, sheet_name=EXPECTED_SHEET_NAME, header=0, nrows=15)
                logging.info(f"First 15 rows of sheet '{EXPECTED_SHEET_NAME}' for debugging headers:\n{df_head_debug}")
            except Exception as debug_e:
                logging.warning(f"Could not read header rows for debugging: {debug_e}")
            workbook.close()
        except ImportError:
             logging.warning("Cannot list sheet names because 'openpyxl' is not installed. Install it with 'pip install openpyxl'.")

    except Exception as e:
        logging.error(f"An unexpected error occurred during ABS population data processing: {e}")
        import traceback
        logging.error(traceback.format_exc())

if __name__ == "__main__":
    process_abs_population_data() 