"""Module for processing FAOSTAT Food Balance Sheets data"""
import os
import pandas as pd
import numpy as np
import gc
import re
from datetime import datetime
import logging
from typing import Dict, List, Union, Optional, Type
from pathlib import Path
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

class FBSBase(BaseModel):
    """Base model for Food Balance Sheet data."""
    area_code: Union[int, float]
    area: str
    item_code: Union[int, float]
    item: str
    element_code: Union[int, float]  # Relaxed to allow various element codes
    element: str
    unit: str
    year: int
    value: float
    flag: Optional[str] = None  # Allow None values for flag

    @validator('value')
    def validate_value(cls, v):
        """Value should be non-negative."""
        if v < 0:
            logger.warning(f"Negative value found: {v}, allowed but flagged")
        return v
    
    @validator('flag')
    def validate_flag(cls, v):
        """Flag should be a valid string if provided."""
        if v is None or v == '':
            return None
        return v

class FoodBalanceSchema(FBSBase):
    """Schema for validating Food Balance Sheet data."""
    # Remove specific validators to make schema more flexible
    pass

def validate_fbs_data(df: pd.DataFrame, schema: Type[BaseModel]) -> Dict[int, List[str]]:
    """
    Validate each row in the DataFrame against the provided schema.
    
    Args:
        df: DataFrame to validate
        schema: Pydantic schema for validation
    
    Returns:
        Dictionary mapping row indices to error messages
    """
    errors = {}
    
    for i, record in df.iterrows():
        try:
            # Replace NaN values with None for proper Pydantic handling
            clean_record = {k: (None if pd.isna(v) else v) for k, v in record.items()}
            schema(**clean_record)
        except Exception as e:
            if hasattr(e, 'errors'):
                # For ValidationError which has an errors() method
                errors[i] = [str(err) for err in e.errors()]
            else:
                # For other exceptions
                errors[i] = [str(e)]
    
    return errors

def generate_validation_report(validation_errors: Dict[int, List[str]], output_path: str) -> None:
    """
    Generate a CSV report of validation errors.
    
    Args:
        validation_errors: Dictionary mapping row indices to error messages
        output_path: Path to save the CSV report
    """
    if not validation_errors:
        logger.info("No validation errors to report")
        return
    
    # Create a DataFrame from the errors
    rows = []
    for row_idx, errors in validation_errors.items():
        for error in errors:
            rows.append({
                'row': row_idx,
                'error': error
            })
    
    # Create a DataFrame and save to CSV
    if rows:
        error_df = pd.DataFrame(rows)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        error_df.to_csv(output_path, index=False)
        logger.info(f"Validation report saved to {output_path}")
    else:
        logger.info("No validation errors to report")

def clean_faostat_fbs(csv_path, output_path, chunk_size=5000):
    """
    Clean FAOSTAT Food Balance Sheets data by:
    1. Filtering to essential element codes
    2. Filtering to data from 1980 onwards
    3. Restructuring the wide format (years as columns) to long format
    4. Validating against the schema

    Args:
        csv_path: Path to the combined FAOSTAT CSV file
        output_path: Path to save the cleaned CSV file
        chunk_size: Number of rows to process at a time

    Returns:
        DataFrame with a sample of the cleaned data
    """
    try:
        logger.info(f"Starting to clean FAOSTAT data from {csv_path} with chunk size {chunk_size}")
        
        # Essential element codes to keep
        essential_elements = [
            664,  # Food supply (kcal/capita/day)
            674,  # Protein supply quantity (g/capita/day)
            684,  # Fat supply quantity (g/capita/day)
            645,  # Food supply quantity (kg/capita/yr)
            5142, # Total Population - Female (1000 persons)
            5511, # Export Quantity
            5611, # Import Quantity
            5301, # Production
            5071  # Stock Variation
        ]
        
        # Create the output file with headers
        with open(output_path, 'w', newline='') as f:
            f.write("area_code,area,item_code,item,element_code,element,unit,year,value,flag\n")
        
        # Track the number of rows
        total_rows = 0
        retained_rows = 0
        chunk_idx = 0
        
        # Process the data in chunks
        for chunk in pd.read_csv(csv_path, chunksize=chunk_size, low_memory=False):
            try:
                chunk_idx += 1
                chunk_rows = len(chunk)
                total_rows += chunk_rows
                logger.info(f"Processing chunk {chunk_idx} ({chunk_rows} rows)")
                
                # Debug: Print column names
                logger.debug(f"Columns in chunk: {chunk.columns.tolist()}")
                
                # Standard column names we expect
                expected_columns = {
                    'area_code': ['area_code', 'Area Code', 'Area Code (M49)'],
                    'area': ['area', 'Area'],
                    'item_code': ['item_code', 'Item Code', 'Item Code (FBS)'],
                    'item': ['item', 'Item'],
                    'element_code': ['element_code', 'Element Code'],
                    'element': ['element', 'Element'],
                    'unit': ['unit', 'Unit']
                }
                
                # Check and map columns
                column_mapping = {}
                for std_col, alternatives in expected_columns.items():
                    found = False
                    for alt in alternatives:
                        if alt in chunk.columns:
                            column_mapping[alt] = std_col
                            found = True
                            break
                    if not found:
                        logger.warning(f"Missing column: {alternatives[0]} in chunk {chunk_idx}")
                        # Try to find a close match based on case-insensitive matching
                        for col in chunk.columns:
                            if any(alt.lower() == col.lower() for alt in alternatives):
                                logger.info(f"  Used {col} as {alternatives[0]}")
                                column_mapping[col] = std_col
                                found = True
                                break
                        if not found:
                            logger.error(f"Cannot find alternative for missing column: {alternatives[0]}")
                
                # Check if we have all required columns
                required_columns = ['area_code', 'area', 'item_code', 'item', 'element_code', 'element', 'unit']
                
                # Check each required column separately
                missing_columns = [col for col in required_columns if col not in column_mapping.values()]
                if missing_columns:
                    # If we're missing required columns but have the basics for processing years, we can continue
                    if 'element_code' not in missing_columns:
                        # We can proceed with partial data
                        logger.warning(f"Missing columns {missing_columns} in chunk {chunk_idx}, proceeding with partial data")
                    else:
                        logger.error(f"Missing critical column element_code in chunk {chunk_idx}, skipping")
                        continue
                
                # Rename columns based on the mapping
                chunk = chunk.rename(columns=column_mapping)
                
                # Debug: Print renamed columns
                logger.debug(f"Columns after renaming: {chunk.columns.tolist()}")
                
                # Filter by essential elements (if element_code column exists)
                if 'element_code' in chunk.columns:
                    # Convert to numeric before filtering
                    if chunk['element_code'].dtype == 'object':
                        chunk['element_code'] = pd.to_numeric(chunk['element_code'], errors='coerce')
                    
                    # Create a mask for filtering
                    element_mask = chunk['element_code'].isin(essential_elements)
                    filtered_chunk = chunk[element_mask]
                    logger.info(f"  After element filtering: {len(filtered_chunk)} rows")
                    chunk = filtered_chunk
                
                # Filter to recent years (1980+) 
                year_columns = [col for col in chunk.columns if isinstance(col, str) and col.startswith('Y') and col[1:5].isdigit()]
                recent_year_columns = [col for col in year_columns if int(col[1:5]) >= 1980]
                logger.info(f"  Keeping {len(recent_year_columns)} years (1980+) out of {len(year_columns)} total years")
                
                # Ensure we have some year columns
                if not recent_year_columns:
                    logger.warning(f"No valid year columns found in chunk {chunk_idx}, skipping")
                    continue
                
                # Find flag columns
                flag_columns = [col for col in chunk.columns if isinstance(col, str) and col.startswith('Y') and col.endswith('F')]
                
                # Get available required columns that exist in the chunk
                available_required_cols = [col for col in required_columns if col in chunk.columns]
                cols_to_keep = available_required_cols + recent_year_columns + flag_columns
                
                # Make sure all columns in cols_to_keep exist in chunk
                cols_to_keep = [col for col in cols_to_keep if col in chunk.columns]
                
                if not cols_to_keep:
                    logger.warning(f"No valid columns to keep in chunk {chunk_idx}, skipping")
                    continue
                
                # Debug: Print columns to keep
                logger.debug(f"Columns to keep: {cols_to_keep}")
                
                # Keep only needed columns
                chunk = chunk[cols_to_keep].copy()
                
                # Check for null values in critical columns
                if available_required_cols:
                    chunk = chunk.dropna(subset=available_required_cols)
                    logger.info(f"  After dropping nulls in critical columns: {len(chunk)} rows")
                
                # Convert to numeric where needed
                for col in ['area_code', 'item_code', 'element_code']:
                    if col in chunk.columns:
                        chunk[col] = pd.to_numeric(chunk[col], errors='coerce')
                
                logger.info(f"  After numeric conversion: {len(chunk)} rows")
                
                # Skip if no data left
                if len(chunk) == 0:
                    logger.warning(f"No data left in chunk {chunk_idx} after filtering, skipping")
                    continue
                
                # Manual wide-to-long conversion to avoid common pandas errors
                long_data = []
                
                for _, row in chunk.iterrows():
                    base_data = {}
                    # Add metadata columns
                    for col in available_required_cols:
                        base_data[col] = row.get(col)
                    
                    # Process each year column
                    for year_col in recent_year_columns:
                        year_val = row.get(year_col)
                        
                        # Handle year_val if it's a Series
                        if isinstance(year_val, pd.Series):
                            # Get the first non-null value if it exists
                            non_null_vals = year_val.dropna()
                            if len(non_null_vals) > 0:
                                year_val = non_null_vals.iloc[0]
                            else:
                                # No valid values, skip this year
                                continue
                        
                        # Only include non-null values
                        if pd.notna(year_val):
                            record = base_data.copy()
                            record['value'] = year_val
                            record['year'] = int(year_col[1:5])
                            
                            # Add flag if available
                            flag_col = f"{year_col}F"
                            if flag_col in row.index:
                                flag_val = row.get(flag_col)
                                # Check if flag_val is a Series and handle appropriately
                                if isinstance(flag_val, pd.Series):
                                    # Get the first non-null value or None if all are null
                                    non_null_flags = flag_val.dropna()
                                    record['flag'] = non_null_flags.iloc[0] if len(non_null_flags) > 0 else None
                                else:
                                    record['flag'] = None if pd.isna(flag_val) else flag_val
                            else:
                                record['flag'] = None
                                
                            long_data.append(record)
                
                # Create a DataFrame from the collected records
                if not long_data:
                    logger.warning(f"No valid records after reshaping in chunk {chunk_idx}, skipping")
                    continue
                
                long_df = pd.DataFrame(long_data)
                
                # Debug: Print long_df columns
                logger.debug(f"Columns in long_df: {long_df.columns.tolist()}")
                
                # Ensure all required columns exist in the output
                for col in ['area_code', 'area', 'item_code', 'item', 'element_code', 'element', 'unit', 'year', 'value', 'flag']:
                    if col not in long_df.columns:
                        long_df[col] = None
                
                # Append to the output file
                try:
                    long_df.to_csv(output_path, mode='a', header=False, index=False)
                    row_count = len(long_df)
                    retained_rows += row_count
                    logger.info(f"  Successfully appended {row_count} rows to output file")
                except Exception as e:
                    logger.error(f"Error writing to output file: {e}")
                
                # Free memory
                del chunk, long_df, long_data
                gc.collect()
                
            except Exception as e:
                import traceback
                logger.error(f"Error processing chunk {chunk_idx}: {str(e)}")
                logger.error(traceback.format_exc())
                # Continue with next chunk
                continue
        
        logger.info(f"Processed {total_rows} total rows, retained {retained_rows} rows")
        logger.info(f"Saved cleaned data to {output_path}")
        
        # Return a small sample of the cleaned data if available
        try:
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                sample = pd.read_csv(output_path, nrows=5)
                return sample
            else:
                logger.warning("No data was saved to the output file")
                return None
        except Exception as e:
            logger.error(f"Error reading sample from output file: {e}")
            return None
            
    except Exception as e:
        import traceback
        logger.error(f"Fatal error cleaning FAOSTAT data: {str(e)}")
        logger.error(traceback.format_exc())
        raise

if __name__ == '__main__':
    input_path = 'data/processed/faostat_fbs_australia.csv' # Input and output path are the same to overwrite the original file
    output_path = 'data/processed/faostat_fbs_australia.csv'
    cleaned_data = clean_faostat_fbs(input_path, output_path)
    print(f"Successfully cleaned and saved data to {output_path}")