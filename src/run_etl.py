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
from process_raw_data import process_excel_file
from process_faostat_fbs import clean_faostat_fbs
from scrape_fire_in_a_bottle import scrape_la_content, save_to_csv, URL
from process_aihw_data import process_aihw_excel  # Import our new module

# Define paths
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
REPORT_DIR = PROCESSED_DATA_DIR / "reports"

# Ensure directories exist
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
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
    
    # First, check if we need to concatenate the CSV files in the faostat_oceania directory
    faostat_dir = RAW_DATA_DIR / "faostat_oceania"
    combined_csv_path = PROCESSED_DATA_DIR / "faostat_fbs_australia.csv"
    output_clean_path = PROCESSED_DATA_DIR / "faostat_fbs_australia_clean.csv"
    
    # Check if the final clean file already exists
    if output_clean_path.exists() and not force_processing:
        logger.info(f"Using existing cleaned FAOSTAT data (skip processing): {output_clean_path}")
        return
    
    if not faostat_dir.exists():
        logger.warning(f"FAOSTAT directory not found: {faostat_dir}")
        return
        
    # Find all CSV files in the FAOSTAT directory
    csv_files = list(faostat_dir.glob("*.csv"))
    if not csv_files:
        logger.warning("No CSV files found in FAOSTAT directory")
        return
        
    try:
        # Check if we've already combined the CSVs
        if not combined_csv_path.exists() or force_processing:
            logger.info(f"Combining {len(csv_files)} FAOSTAT CSV files")
            
            # Process files one by one to avoid loading all into memory at once
            # First, create an empty combined file with just headers
            combined_df = None
            
            # Keep track of total rows processed and retained
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
                        logger.info(f"  Processing chunk {chunk_num+1} of {csv_file.name}")
                        total_raw_rows += len(chunk)
                        
                        # Filter for just Australia data to reduce size immediately
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
                        
                        # Rename columns
                        column_mapping = {
                            'Area Code': 'area_code',
                            'Area': 'area',
                            'Item Code': 'item_code',
                            'Item': 'item',
                            'Element Code': 'element_code',
                            'Element': 'element',
                            'Year': 'year'
                        }
                        
                        # Apply renaming (only for columns that exist)
                        for old_col, new_col in column_mapping.items():
                            if old_col in chunk.columns:
                                chunk = chunk.rename(columns={old_col: new_col})
                        
                        # Append to file
                        if combined_df is None:
                            # For the first chunk, write with headers
                            chunk.to_csv(combined_csv_path, index=False, mode='w')
                            combined_df = True  # Just a flag to indicate file exists
                        else:
                            # For subsequent chunks, append without headers
                            chunk.to_csv(combined_csv_path, index=False, mode='a', header=False)
                        
                        # Force garbage collection
                        del chunk
                        gc.collect()
                    
                except Exception as e:
                    logger.error(f"  Error processing {csv_file.name}: {e}")
                    continue
            
            logger.info(f"Saved combined FAOSTAT data to {combined_csv_path}")
            logger.info(f"Total raw rows: {total_raw_rows}, retained rows: {total_retained_rows}")
            
        else:
            logger.info(f"Using existing combined FAOSTAT data: {combined_csv_path}")
        
        # Now clean the combined data
        if not output_clean_path.exists() or force_processing:
            logger.info("Cleaning FAOSTAT data")
            
            try:
                # Use clean_faostat_fbs from process_faostat_fbs module
                logger.info("Calling clean_faostat_fbs function")
                clean_faostat_fbs(str(combined_csv_path), str(output_clean_path))
                logger.info(f"Saved cleaned FAOSTAT data to {output_clean_path}")
                
            except Exception as e:
                logger.error(f"Error cleaning FAOSTAT data: {e}")
        else:
            logger.info(f"Using existing cleaned FAOSTAT data: {output_clean_path}")
            
    except Exception as e:
        logger.error(f"Error processing FAOSTAT data: {e}")
    
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
    """Run ETL processes based on command line arguments."""
    args = parse_args()
    
    # If no specific options are provided, run all processes
    run_all = not (args.aihw or args.ncd or args.faostat or args.fire)
    
    logger.info("Starting ETL process")
    
    # First run the download script unless --no-download is specified
    if not args.no_download:
        if not run_downloads():
            logger.error("Download process failed. Exiting.")
            return
    else:
        logger.info("Skipping download step (--no-download specified)")
    
    # Process AIHW Excel files
    if run_all or args.aihw:
        try:
            process_aihw_excel_files()
            gc.collect()  # Force garbage collection between processes
        except Exception as e:
            logger.error(f"Error in AIHW processing: {e}")
    
    # Process NCD-RisC CSV files
    if run_all or args.ncd:
        try:
            process_ncd_risc_csvs()
            gc.collect()  # Force garbage collection between processes
        except Exception as e:
            logger.error(f"Error in NCD-RisC processing: {e}")
    
    # Process FAOSTAT data
    if run_all or args.faostat:
        try:
            process_faostat_data(force_processing=args.force)
            gc.collect()  # Force garbage collection between processes
        except Exception as e:
            logger.error(f"Error in FAOSTAT processing: {e}")
    
    # Process Fire in a Bottle data
    if run_all or args.fire:
        try:
            process_fire_in_bottle_data()
            gc.collect()  # Force garbage collection between processes
        except Exception as e:
            logger.error(f"Error in Fire in a Bottle processing: {e}")
    
    # Print summary of processed files
    try:
        processed_files = list(PROCESSED_DATA_DIR.glob("*.csv"))
        logger.info("\n=== ETL Process Summary ===")
        logger.info(f"Total processed files: {len(processed_files)}")
        for file in sorted(processed_files):
            file_size = os.path.getsize(file) / 1024  # Convert to KB
            logger.info(f"  {file.name} ({file_size:.1f} KB)")
    except Exception as e:
        logger.error(f"Error generating summary: {e}")
    
    logger.info("ETL process completed")

if __name__ == "__main__":
    main() 