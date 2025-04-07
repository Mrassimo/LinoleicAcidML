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
from data_processing.process_raw_data import process_excel_file
from data_processing.process_faostat_fbs import clean_faostat_data
from data_processing.scrape_fire_in_bottle import scrape_la_content, save_to_csv, URL
from data_processing.process_aihw_data import process_aihw_excel
from data_processing.validation_utils import get_la_content_for_item
from data_processing.update_validation import create_validation_data

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
    try:
        # Import the download_data module
        spec = importlib.util.spec_from_file_location(
            "download_data", 
            os.path.join(os.path.dirname(__file__), "download_data.py")
        )
        download_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(download_module)
        
        # Run the download script
        download_module.main()
        logger.info("Download process completed")
        return True
    except Exception as e:
        logger.error(f"Error during download process: {e}")
        return False

def process_ncd_risc_csvs():
    """Process NCD-RisC CSV files."""
    logger.info("=== Processing NCD-RisC datasets ===")
    
    ncd_files = [
        ("NCD_RisC_Lancet_2024_Diabetes_Australia.csv", "ncd_risc_diabetes.csv"),
        ("NCD_RisC_Cholesterol_Australia.csv", "ncd_risc_cholesterol.csv"),
        ("NCD_RisC_Lancet_2024_BMI_age_standardised_Australia.csv", "ncd_risc_bmi_adult.csv")
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
        ("AIHW-DEM-02-S2-Prevalence.xlsx", "aihw_dementia_prevalence.csv"),
        ("AIHW-DEM-02-S3-Mortality-202409.xlsx", "aihw_dementia_mortality.csv"),
        ("AIHW-CVD-92-HSVD-facts-data-tables-12122024.xlsx", "aihw_cvd_all_facts.csv")
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

def process_faostat_data(force_processing=False):
    """
    Process FAOSTAT data.
    
    Args:
        force_processing: If True, process the data even if output files already exist
    """
    logger.info("=== Processing FAOSTAT data ===")
    
    # Define paths for both current and historical data
    faostat_dir = RAW_DATA_DIR / "faostat_oceania"
    faostat_historic_dir = RAW_DATA_DIR / "faostat_historic_oceania"
    
    # Staging paths for intermediate files
    combined_current_staging = STAGING_DATA_DIR / "faostat_fbs_current_combined.csv"
    combined_historic_staging = STAGING_DATA_DIR / "faostat_fbs_historic_combined.csv"
    
    # Final output path - single cleaned file containing all FAOSTAT data
    final_output_path = PROCESSED_DATA_DIR / "faostat_food_balance_sheets.csv"
    
    if not force_processing and final_output_path.exists():
        logger.info(f"Using existing cleaned FAOSTAT data: {final_output_path}")
        return
    
    # Process current FAOSTAT data
    if not faostat_dir.exists():
        logger.warning(f"FAOSTAT directory not found: {faostat_dir}")
    else:
        process_faostat_directory(
            faostat_dir,
            combined_current_staging,
            data_type="current"
        )
    
    # Process historical FAOSTAT data
    if not faostat_historic_dir.exists():
        logger.warning(f"FAOSTAT historical directory not found: {faostat_historic_dir}")
    else:
        process_faostat_directory(
            faostat_historic_dir,
            combined_historic_staging,
            data_type="historical"
        )
    
    # Combine and clean both datasets
    success = False
    try:
        logger.info("Combining and cleaning all FAOSTAT data")
        
        # Read and combine both datasets
        dfs = []
        for file in [combined_current_staging, combined_historic_staging]:
            if file.exists():
                logger.info(f"Reading {file.name}")
                df = pd.read_csv(file)
                dfs.append(df)
                del df  # Free memory
                gc.collect()
        
        if not dfs:
            logger.error("No FAOSTAT data found to process")
            return
            
        # Clean and save final output
        logger.info("Cleaning combined FAOSTAT data")
        clean_faostat_data(
            input_files=[str(f) for f in [combined_current_staging, combined_historic_staging] if f.exists()],
            output_file=str(final_output_path)
        )
        
        logger.info(f"Saved final cleaned FAOSTAT data to {final_output_path}")
        success = True
                
    except Exception as e:
        logger.error(f"Error combining and cleaning FAOSTAT data: {e}")
    
    finally:
        # Only clean up staging files if processing was successful
        if success:
            # Clean up staging files
            for file in [combined_current_staging, combined_historic_staging]:
                if file.exists():
                    file.unlink()
                    logger.info(f"Cleaned up staging file: {file}")
        else:
            logger.info("Keeping staging files for debugging due to processing error")

def process_faostat_directory(input_dir: Path, output_path: Path, data_type: str):
    """
    Process FAOSTAT data from a specific directory.
    
    Args:
        input_dir: Directory containing FAOSTAT CSV files
        output_path: Path for combined CSV output
        data_type: Type of data being processed ('current' or 'historical')
    """
    logger.info(f"Processing {data_type} FAOSTAT data from {input_dir}")
    
    # Find all CSV files in the directory
    csv_files = list(input_dir.glob("*.csv"))
    if not csv_files:
        logger.warning(f"No CSV files found in {data_type} FAOSTAT directory")
        return
        
    try:
        logger.info(f"Combining {len(csv_files)} {data_type} FAOSTAT CSV files")
        
        # Process files one by one to avoid loading all into memory at once
        combined_df = None
        total_raw_rows = 0
        total_retained_rows = 0
        
        # Essential elements to keep - focus only on important food supply metrics
        essential_elements = [
            'Food supply (kcal/capita/day)',
            'Fat supply quantity (g/capita/day)', 
            'Protein supply quantity (g/capita/day)',
            'Food supply quantity (kg/capita/yr)'
        ]
        
        # Use smaller chunk size to reduce memory pressure
        chunk_size = 5000
        
        for i, csv_file in enumerate(csv_files):
            try:
                logger.info(f"Processing file {i+1}/{len(csv_files)}: {csv_file.name}")
                
                # Read in chunks to reduce memory usage
                chunks = pd.read_csv(csv_file, chunksize=chunk_size)
                
                for chunk_num, chunk in enumerate(chunks):
                    logger.info(f"  Processing chunk {chunk_num+1} of {csv_file.name} with {len(chunk)} rows")
                    total_raw_rows += len(chunk)
                    
                    # Check for historical data format (has columns like Y1961, Y1962, etc.)
                    year_columns = [col for col in chunk.columns if re.match(r'^Y\d{4}$', col)]
                    if year_columns:
                        logger.info(f"  Detected historical data format with {len(year_columns)} year columns")
                        # Historical data is handled differently and will be processed 
                        # in clean_faostat_data function
                        # We still need to filter for Australia though
                        if 'Area' in chunk.columns:
                            australia_mask = chunk['Area'] == 'Australia'
                            chunk = chunk[australia_mask]
                    else:
                        # Filter for just Australia data to reduce size immediately (current format)
                        if 'Area' in chunk.columns:
                            australia_mask = chunk['Area'] == 'Australia'
                            chunk = chunk[australia_mask]
                            
                            # Also filter for essential elements immediately
                            if 'Element' in chunk.columns:
                                element_mask = chunk['Element'].isin(essential_elements)
                                chunk = chunk[element_mask]
                    
                    # Skip processing if no rows left after filtering
                    if len(chunk) == 0:
                        logger.info(f"  No Australia data in this chunk, skipping")
                        continue
                        
                    # Count retained rows
                    total_retained_rows += len(chunk)
                    
                    # Rename columns - only for modern format
                    # Historical format will be handled in clean_faostat_data
                    if not year_columns:
                        column_mapping = {
                            'Area Code': 'area_code',
                            'Area': 'area',
                            'Item Code': 'item_code',
                            'Item': 'item',
                            'Element Code': 'element_code',
                            'Element': 'element',
                            'Year': 'year',
                            'Value': 'value'  # Value to value mapping
                        }
                        
                        # Apply renaming (only for columns that exist)
                        for old_col, new_col in column_mapping.items():
                            if old_col in chunk.columns:
                                chunk = chunk.rename(columns={old_col: new_col})
                    
                    # Add data type column
                    chunk['data_type'] = data_type
                    
                    # Append to file
                    if combined_df is None:
                        # For the first chunk, write with headers
                        chunk.to_csv(output_path, index=False, mode='w')
                        combined_df = True  # Just a flag to indicate file exists
                    else:
                        # For subsequent chunks, append without headers
                        chunk.to_csv(output_path, index=False, mode='a', header=False)
                    
                    # Force garbage collection
                    del chunk
                    gc.collect()
                
            except Exception as e:
                logger.error(f"  Error processing {csv_file.name}: {e}")
                continue
        
        logger.info(f"Saved combined {data_type} FAOSTAT data to {output_path}")
        logger.info(f"Total raw rows: {total_raw_rows}, retained rows: {total_retained_rows}")
        
    except Exception as e:
        logger.error(f"Error processing {data_type} FAOSTAT data: {e}")
    
    # Force garbage collection at the end
    gc.collect()

def process_fire_in_bottle_data():
    """Process Fire in a Bottle linoleic acid data using the scraper."""
    logger.info("=== Processing Fire in a Bottle data ===")
    
    output_path = PROCESSED_DATA_DIR / "fire_in_a_bottle_la_content.csv"
    
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
        la_content_path = PROCESSED_DATA_DIR / 'fire_in_a_bottle_la_content.csv'
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
        output_path = PROCESSED_DATA_DIR / 'fao_la_mapping_final.csv'
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
        process_faostat_data()
    
    if args.fire or not any([args.aihw, args.ncd, args.faostat]):
        process_fire_in_bottle_data()
        
    # Always run semantic validation after Fire in a Bottle and FAOSTAT data are processed
    if (args.fire or args.faostat) or not any([args.aihw, args.ncd]):
        if not process_semantic_validation():
            logger.error("Semantic validation failed.")
            sys.exit(1)
    
    logger.info("ETL process completed successfully")

if __name__ == "__main__":
    main() 