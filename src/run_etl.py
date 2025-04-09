#!/usr/bin/env python3
"""
Main ETL script to process all datasets in the project.
This script orchestrates the processing of all data files, including:
- AIHW Excel files
- FAOSTAT Food Balance Sheets
- NCD-RisC health datasets
- Fire in a Bottle linoleic acid data

Usage:
  python src/run_etl.py [--aihw] [--ncd] [--faostat] [--fire]
  
  Options:
    --aihw     Process only AIHW data
    --ncd      Process only NCD-RisC data
    --faostat  Process only FAOSTAT data
    --fire     Process only Fire in a Bottle data
    --no-download  Skip the download step (assume files exist)
    
  If no options are provided, all datasets will be processed.
"""

import os
import sys
import pandas as pd
import logging
from pathlib import Path
import subprocess
import re
import glob
import argparse
import gc  # Garbage collector
import importlib.util

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import project modules
from .data_processing.process_faostat_fbs import clean_faostat_data
from .data_processing.scrape_fire_in_bottle import scrape_la_content, save_to_csv, URL
from .data_processing.process_aihw_data import process_aihw_excel
from .data_processing.validation_utils import get_la_content_for_item
from .data_processing.update_validation import create_validation_data
from .data_processing.calculate_dietary_metrics import calculate_dietary_metrics as calculate_dietary_metrics_main
from .data_processing.health_outcome_metrics import main as health_outcome_metrics_main
from .data_processing.merge_health_dietary import main as merge_health_dietary_main
try:
    from . import download_data
except ImportError:
    download_data = None


# Define paths
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
STAGING_DATA_DIR = BASE_DIR / "data" / "staging"  # Add staging directory
REPORT_DIR = PROCESSED_DATA_DIR / "reports"

# Ensure directories exist
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
STAGING_DATA_DIR.mkdir(parents=True, exist_ok=True)  # Create staging directory
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def run_downloads():
    """Run the download script to fetch all raw data files."""
    logger.info("=== Downloading raw data files ===")
    if download_data is None:
        logger.error("download_data module not found.")
        return False
    try:
        download_data.main()
        logger.info("Download process completed")
        return True
    except Exception as e:
        logger.error(f"Error during download process: {e}")
        return False

def process_ncd_risc_csvs():
    """Process NCD-RisC CSV files."""
    logger.info("=== Processing NCD-RisC datasets ===")
    
    ncd_files = [
        ("NCD_RisC_Lancet_2024_Diabetes_Australia.csv", "ncdrisc_diabetes_australia_processed.csv"),
        ("NCD_RisC_Cholesterol_Australia.csv", "ncdrisc_cholesterol_australia_processed.csv"),
        ("NCD_RisC_Lancet_2024_BMI_age_standardised_Australia.csv", "ncdrisc_bmi_australia_processed.csv")
    ]
    for input_filename, output_filename in ncd_files:
        input_path = RAW_DATA_DIR / input_filename
        output_path = PROCESSED_DATA_DIR / output_filename
        
        if not input_path.exists():
            logger.warning(f"File not found: {input_path}")
            continue
            
        if os.path.getsize(input_path) == 0:
            logger.warning(f"Skipping empty file: {input_path}")
            continue
            
        try:
            logger.info(f"Processing {input_filename}")
            df = pd.read_csv(input_path)
            
            # Basic cleaning
            # Standardize column names
            df.columns = [re.sub(r'[ /()]+', '_', col.lower()) for col in df.columns]
            
            # Add source_file column
            df['source_file'] = input_filename
            
            # Save processed data
            df.to_csv(output_path, index=False)
            logger.info(f"Saved processed data to {output_path}")
            
            # Log basic stats
            logger.info(f"  Rows: {len(df)}")
            logger.info(f"  Columns: {len(df.columns)}")
            
            # Force garbage collection
            del df
            gc.collect()
            
        except Exception as e:
            logger.error(f"Error processing {input_filename}: {e}")

def process_aihw_excel_files():
    """Process AIHW Excel files using the new sheet-by-sheet approach."""
    logger.info("=== Processing AIHW Excel files ===")
    
    aihw_files = [
        ("AIHW-DEM-02-S2-Prevalence.xlsx", "aihw_dementia_prevalence_australia_processed.csv"),
        ("AIHW-DEM-02-S3-Mortality-202409.xlsx", "aihw_dementia_mortality_australia_processed.csv"),
        ("AIHW-CVD-92-HSVD-facts-data-tables-12122024.xlsx", "aihw_cvd_metrics_australia_processed.csv")
    ]
    for input_filename, output_filename in aihw_files:
        input_path = RAW_DATA_DIR / input_filename
        output_path = PROCESSED_DATA_DIR / output_filename
        
        if not input_path.exists():
            logger.warning(f"File not found: {input_path}")
            continue
            
        try:
            logger.info(f"Processing {input_filename}")
            # Use our new AIHW processing module
            process_aihw_excel(str(input_path), str(output_path))
            
            # Log success and basic stats
            if output_path.exists():
                df = pd.read_csv(output_path)
                logger.info(f"Successfully processed {input_filename}")
                logger.info(f"  Shape: {df.shape}")
                logger.info(f"  Columns: {', '.join(df.columns)}")
                
                # Force garbage collection
                del df
                gc.collect()
                
        except Exception as e:
            logger.error(f"Error processing {input_filename}: {e}")

def process_faostat_data(force_processing: bool = False):
    """
    Process FAOSTAT data by directly cleaning raw data directories.

    Args:
        force_processing: If True, process the data even if output file already exists
    """
    logger.info("=== Processing FAOSTAT data ===")

    faostat_dir = RAW_DATA_DIR / "faostat_oceania"
    faostat_historic_dir = RAW_DATA_DIR / "faostat_historic_oceania"
    final_output_path = PROCESSED_DATA_DIR / "faostat_fbs_australia_processed.csv"

    logger.debug(f"Checking FAOSTAT skip: force={force_processing}, exists={final_output_path.exists()}")
    if not force_processing and final_output_path.exists():
        logger.info(f"Using existing cleaned FAOSTAT data: {final_output_path}")
        return

    # Gather all CSV files from FAOSTAT directories
    input_files = []
    if faostat_dir.exists():
        input_files.extend(list(faostat_dir.glob("*.csv")))
    else:
        logger.warning(f"FAOSTAT directory not found: {faostat_dir}")

    if faostat_historic_dir.exists():
        input_files.extend(list(faostat_historic_dir.glob("*.csv")))
    else:
        logger.warning(f"FAOSTAT historical directory not found: {faostat_historic_dir}")

    if not input_files:
        logger.error("No FAOSTAT data directories found to process")
        return

    try:
        logger.info("Cleaning FAOSTAT data from raw directories")
        clean_faostat_data(
            input_files=[str(f) for f in input_files],
            output_file=str(final_output_path)
        )
        logger.info(f"Saved final cleaned FAOSTAT data to {final_output_path}")
    except Exception as e:
        logger.error(f"Error cleaning FAOSTAT data: {e}")


def process_fire_in_bottle_data():
    """Process Fire in a Bottle linoleic acid data using the scraper."""
    logger.info("=== Processing Fire in a Bottle data ===")
    
    output_path = PROCESSED_DATA_DIR / "la_content_fireinabottle_processed.csv"
    
    try:
        logger.info(f"Scraping Fire in a Bottle data from {URL}")
        df = scrape_la_content(URL)
        
        if df is not None and not df.empty:
            logger.info(f"Successfully scraped Fire in a Bottle data")
            
            # Save to CSV in the processed directory
            save_to_csv(df, str(output_path))
            logger.info(f"Saved processed data to {output_path}")
            logger.info(f"  Shape: {df.shape}")
            
            # Force garbage collection
            del df
            gc.collect()
        else:
            logger.error("Failed to scrape Fire in a Bottle data")
    except Exception as e:
        logger.error(f"Error processing Fire in a Bottle data: {e}")

def process_semantic_validation():
    """Process semantic validation between FAOSTAT and LA content data."""
    logger.info("=== Processing Semantic Validation ===")
    
    try:
        # Load LA content data
        la_content_path = PROCESSED_DATA_DIR / 'la_content_fireinabottle_processed.csv'
        if not la_content_path.exists():
            logger.error("LA content data not found. Please process Fire in a Bottle data first.")
            return False
            
        la_df = pd.read_csv(la_content_path)
        
        # Create validation DataFrame
        logger.info("Creating validation DataFrame")
        validation_df = create_validation_data()
        
        # Add LA content information
        logger.info("Adding LA content information")
        validation_df['la_content_per_100g'] = validation_df['matched_la_item'].apply(
            lambda x: get_la_content_for_item(x, la_df) if pd.notna(x) else None
        )
        
        # Save final mapping
        output_path = PROCESSED_DATA_DIR / 'fao_la_mapping_validated.csv'
        validation_df.to_csv(output_path, index=False)
        logger.info(f"Saved final mapping to {output_path}")
        
        # Print validation statistics
        total = len(validation_df)
        approved = (validation_df['validation_status'] == 'APPROVED').sum()
        no_match = (validation_df['validation_status'] == 'NO_MATCH').sum()
        has_la = validation_df['la_content_per_100g'].notna().sum()
        
        logger.info("\nValidation Statistics:")
        logger.info(f"Total FAOSTAT items: {total}")
        logger.info(f"Approved matches: {approved}")
        logger.info(f"No appropriate match: {no_match}")
        logger.info(f"Items with LA content: {has_la}")
        logger.info(f"Match rate: {(approved/total)*100:.1f}%")
        
        return True
        
    except Exception as e:
        logger.error(f"Error during semantic validation: {e}")
        return False

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Process various datasets.')
    parser.add_argument('--aihw', action='store_true', help='Process only AIHW data')
    parser.add_argument('--ncd', action='store_true', help='Process only NCD-RisC data')
    parser.add_argument('--faostat', action='store_true', help='Process only FAOSTAT data')
    parser.add_argument('--fire', action='store_true', help='Process only Fire in a Bottle data')
    parser.add_argument('--force', action='store_true', help='Force processing even if output files exist')
    parser.add_argument('--no-download', action='store_true', help='Skip the download step')
    return parser.parse_args()

def main():
    """Main ETL function."""
    args = parse_args()
    
    # Skip download if --no-download flag is set
    if not args.no_download:
        if not run_downloads():
            logger.error("Download process failed. Exiting.")
            sys.exit(1)
    
    # Process each dataset based on flags
    if args.aihw or not any([args.ncd, args.faostat, args.fire]):
        process_aihw_excel_files()
    
    if args.ncd or not any([args.aihw, args.faostat, args.fire]):
        process_ncd_risc_csvs()
    
    if args.faostat or not any([args.aihw, args.ncd, args.fire]):
        process_faostat_data(force_processing=args.force)
    
    if args.fire or not any([args.aihw, args.ncd, args.faostat]):
        process_fire_in_bottle_data()
        
    # Always run semantic validation after Fire in a Bottle and FAOSTAT data are processed
    if (args.fire or args.faostat) or not any([args.aihw, args.ncd]):
        if not process_semantic_validation():
            logger.error("Semantic validation failed.")
            sys.exit(1)
    
    logger.info("=== Calculating dietary metrics ===")
    calculate_dietary_metrics_main()

    logger.info("=== Calculating health outcome metrics ===")
    health_outcome_metrics_main()

    logger.info("=== Merging health and dietary datasets ===")
    merge_health_dietary_main()

    logger.info("ETL process completed successfully")

if __name__ == "__main__":
    main() 