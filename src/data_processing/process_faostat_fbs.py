"""Module for processing FAOSTAT Food Balance Sheets data"""
import os
import pandas as pd
import numpy as np
import gc
import re
from datetime import datetime
import logging
from typing import Dict, List, Union, Optional, Type, Tuple
from pathlib import Path
from pydantic import BaseModel, Field, field_validator
from pydantic import BaseModel, validator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class InvalidFBSEntry(Exception):
    """Custom exception for invalid FBS entries"""
    pass

class FAOStatRecord(BaseModel):
    area_code: int
    area: str
    item_code: int
    item: str
    element_code: int
    element: str
    unit: str
    year: int
    value: float

    @field_validator('area')
    def area_must_be_australia(cls, v):
        if v.lower() != 'australia':
            raise ValueError('Area must be Australia')
        return v

    @field_validator('value')
    def value_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('Value must be non-negative')
        return v

def identify_year_columns(df: pd.DataFrame) -> List[str]:
    """Identify year columns in the dataset."""
    year_pattern = r'^Y\d{4}$'
    return [col for col in df.columns if re.match(year_pattern, col, re.IGNORECASE)]

def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Clean column names to lowercase and remove special characters."""
    df.columns = df.columns.str.lower()
    return df

def filter_australia_data(df: pd.DataFrame) -> pd.DataFrame:
    """Filter data for Australia only."""
    return df[df['area'].str.lower() == 'australia'].copy()

def melt_year_columns(df: pd.DataFrame, year_cols: List[str]) -> pd.DataFrame:
    """Melt year columns into long format."""
    id_vars = [col for col in df.columns if col not in year_cols and not col.endswith(('f', 'n'))]
    df_melted = pd.melt(
        df,
        id_vars=id_vars,
        value_vars=year_cols,
        var_name='year',
        value_name='value'
    )
    return df_melted

def convert_year_format(df: pd.DataFrame) -> pd.DataFrame:
    """Convert year format from 'Y2010' to 2010."""
    df['year'] = df['year'].str.extract(r'(\d{4})').astype(int)
    return df

def convert_units(df: pd.DataFrame) -> pd.DataFrame:
    """Convert units where necessary (e.g., kg/year to g/day)."""
    # Convert food supply from kg/year to g/day for relevant elements
    mask = (df['element'] == 'Food supply quantity (kg/capita/yr)')
    df.loc[mask, 'value'] = df.loc[mask, 'value'] * 1000 / 365
    df.loc[mask, 'unit'] = 'g/cap/d'
    
    return df

def validate_records(df: pd.DataFrame) -> pd.DataFrame:
    """Validate each record using the Pydantic model."""
    valid_records = []
    for _, row in df.iterrows():
        try:
            record = FAOStatRecord(
                area_code=row['area_code'],
                area=row['area'],
                item_code=row['item_code'],
                item=row['item'],
                element_code=row['element_code'],
                element=row['element'],
                unit=row['unit'],
                year=row['year'],
                value=row['value']
            )
            valid_records.append(record.dict())
        except Exception as e:
            logger.warning(f"Invalid record: {row}, Error: {e}")
            continue
    
    return pd.DataFrame(valid_records)

def process_faostat_data(input_file: Path, is_historical: bool = False) -> pd.DataFrame:
    """Process FAOSTAT data, handling both historical and modern formats.

    Ensures rows with missing values are dropped and duplicates are removed.
    All code and comments use Australian English.
    """
    logger.info(f"Reading FAOSTAT data from {input_file}")

    # Read data in chunks to handle large files
    chunk_size = 10000
    chunks = []

    for chunk in pd.read_csv(input_file, chunksize=chunk_size):
        # Clean column names
        chunk = clean_column_names(chunk)

        # Filter for Australia
        chunk = filter_australia_data(chunk)

        # Identify year columns
        year_cols = identify_year_columns(chunk)

        # Melt year columns
        chunk = melt_year_columns(chunk, year_cols)

        # Convert year format
        chunk = convert_year_format(chunk)

        # Convert units
        chunk = convert_units(chunk)

        # Drop rows with missing values in the 'value' column
        chunk = chunk.dropna(subset=['value'])

        # Remove duplicate rows based on all columns except 'value'
        dedup_columns = [col for col in chunk.columns if col != 'value']
        chunk = chunk.drop_duplicates(subset=dedup_columns, keep='first')

        chunks.append(chunk)

    # Combine all chunks
    df = pd.concat(chunks, ignore_index=True)

    # Validate records
    df = validate_records(df)

    return df

def harmonize_overlapping_years(historical_df: pd.DataFrame, modern_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Harmonize data for overlapping years (2010-2013) between historical and modern datasets."""
    overlap_years = set(historical_df['year']).intersection(set(modern_df['year']))
    logger.info(f"Harmonizing overlapping years: {sorted(overlap_years)}")
    
    # Calculate adjustment factors for each element based on overlapping years
    adjustment_factors = {}
    for element in modern_df['element'].unique():
        hist_data = historical_df[
            (historical_df['element'] == element) & 
            (historical_df['year'].isin(overlap_years))
        ]['value'].mean()
        
        modern_data = modern_df[
            (modern_df['element'] == element) & 
            (modern_df['year'].isin(overlap_years))
        ]['value'].mean()
        
        if hist_data > 0 and modern_data > 0:
            adjustment_factors[element] = modern_data / hist_data
            logger.info(f"Adjustment factor for {element}: {adjustment_factors[element]:.3f}")
    
    # Apply adjustment factors to historical data
    for element, factor in adjustment_factors.items():
        historical_df.loc[historical_df['element'] == element, 'value'] *= factor
    
    return historical_df, modern_df

def clean_faostat_data(input_files: list, output_file: str):
    """
    Clean and combine FAOSTAT food balance sheet data.
    
    Args:
        input_files: List of input CSV files to process
        output_file: Path to save the cleaned output
    """
    dfs = []
    
    # Process each input file
    for file in input_files:
        if not Path(file).exists():
            logger.warning(f"Input file not found: {file}")
            continue
            
        try:
            logger.info(f"Processing {file}")
            # Read data in chunks to manage memory
            chunks = pd.read_csv(file, chunksize=5000)
            
            file_dfs = []
            # Define required columns for a valid processed chunk
            required_chunk_cols = ['area', 'item', 'element', 'year', 'value', 'unit']
            for chunk in chunks:
                logger.info(f"Processing chunk with {len(chunk)} rows")
                # Basic cleaning
                chunk = chunk.copy()
                
                # Check if this is historical data by looking for year columns (Y1961, Y1962, etc.)
                year_cols = [col for col in chunk.columns if re.match(r'^Y\d{4}$', col)]
                
                # Handle historical data format 
                if year_cols:
                    logger.info(f"Detected historical data format with {len(year_cols)} year columns")
                    # Keep only essential non-year columns for melting
                    id_vars = [col for col in chunk.columns 
                              if not re.match(r'^Y\d{4}$', col) 
                              and not col.endswith(('F', 'N'))]
                    
                    # Melt year columns into rows
                    chunk = pd.melt(
                        chunk,
                        id_vars=id_vars,
                        value_vars=year_cols,
                        var_name='year',
                        value_name='value'
                    )
                    
                    # Extract year number from 'Y1961' format
                    chunk['year'] = chunk['year'].str.extract(r'Y(\d{4})').astype(int)
                
                # Ensure column names are standardized (after potential melting)
                chunk.columns = [col.lower() for col in chunk.columns]
                
                # Keep only essential columns
                # Filter for Australia only
                if 'area' in chunk.columns:
                    chunk = chunk[chunk['area'].str.lower() == 'australia']

                # Filter columns after all processing to avoid dropping added columns prematurely
                
                    
                
                # Skip empty chunks
                if len(chunk) == 0:
                    continue
                    
                if not chunk.empty and all(col in chunk.columns for col in required_chunk_cols):
                    file_dfs.append(chunk)
                else:
                    logger.warning(f"Skipping chunk from {file} due to missing required columns after processing. Columns present: {chunk.columns.tolist()}")
            
            if file_dfs:
                df = pd.concat(file_dfs, ignore_index=True)
                if not df.empty:
                    dfs.append(df)
                    logger.info(f"Added {len(df)} rows from {file}")
                
        except Exception as e:
            logger.error(f"Error processing {file}: {e}")
            continue
    
    if not dfs:
        logger.error("No data to process after reading input files")
        # Create empty output file to indicate processing was attempted
        pd.DataFrame().to_csv(output_file, index=False)
        return
    
    try:
        # Combine all data
        combined_df = pd.concat(dfs, ignore_index=True)
        logger.info(f"Combined data shape: {combined_df.shape}")
        
        # Convert year to int
        combined_df['year'] = pd.to_numeric(combined_df['year'], errors='coerce').astype('Int64')
        
        # Convert value to float
        combined_df['value'] = pd.to_numeric(combined_df['value'], errors='coerce')
        
        # Drop rows with missing essential data
        combined_df = combined_df.dropna(subset=['year', 'value', 'element'])
        logger.info(f"After dropping NA, data shape: {combined_df.shape}")
        # Log columns present before sorting and duplicate removal for debugging missing 'data_type' issues
        logger.info(f"Columns before FAOSTAT duplicate removal: {combined_df.columns.tolist()}")

        # Sort and remove duplicates based on year, item, and element to ensure data integrity before pivoting
        combined_df.sort_values(by=['year', 'item', 'element'], inplace=True)
        before_dedup_len = len(combined_df)
        combined_df.drop_duplicates(subset=['year', 'item', 'element'], keep='first', inplace=True)
        duplicates_removed = before_dedup_len - len(combined_df)
        logger.info(f"Removed {duplicates_removed} duplicate records from FAOSTAT data")
        
        # Create pivot table for easier analysis
        pivot_df = combined_df.pivot_table(
            index=['year', 'item'],
            columns='element',
            values='value',
            aggfunc='first'
        ).reset_index()
        
        # Save to CSV
        pivot_df.to_csv(output_file, index=False)
        logger.info(f"Successfully saved cleaned data to {output_file}")
        
    except Exception as e:
        logger.error(f"Error creating final output: {e}")
        raise

if __name__ == "__main__":
    data_dir = Path("data/processed")
    # Deprecated intermediate files removed from processing pipeline
    # Final processed FAOSTAT FBS data is now saved elsewhere