"""
Process AIHW Excel files into standardised CSV format.

This module implements the sheet-by-sheet cleaning approach for AIHW Excel files,
ensuring proper header detection and data transformation before concatenation.
"""

import pandas as pd
import os
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime
import sys
from pathlib import Path
import numpy as np
import re

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))
from src.models.aihw_models import AIHWRecord, AIHWDataset, MetricType

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
SHEETS_TO_EXCLUDE = {'Contents', 'Notes', 'Metadata', 'Index'}
TABLE_PATTERN = re.compile(r'(?:Table [A-Z0-9.]+:?\s*(.+?)(?:\s*\(|\s*$)|^[A-Z][a-z\s]+(?:and\s+[A-Z][a-z\s]+)*(?:\s+in\s+Australia)?(?:\s*\(|\s*$))')
YEAR_PATTERN = re.compile(r'(?:19|20)\d{2}(?:[-–]\d{2})?')

def extract_table_name(df: pd.DataFrame, sheet_name: str) -> Optional[str]:
    """Extract the table name from the first few rows or use sheet name as fallback."""
    # First try to find a table title in the first few rows
    for i in range(min(10, len(df))):
        cell = str(df.iloc[i, 0])
        match = TABLE_PATTERN.search(cell)
        if match:
            title = match.group(1) if match.group(1) else cell
            return title.strip()
    
    # If no table title found, use the sheet name as the title
    title = sheet_name.replace('_', ' ').title()
    if title in ['AF', 'PAD', 'RHD', 'CHD']:
        # Expand common abbreviations
        expansions = {
            'AF': 'Atrial Fibrillation',
            'PAD': 'Peripheral Arterial Disease',
            'RHD': 'Rheumatic Heart Disease',
            'CHD': 'Coronary Heart Disease'
        }
        title = expansions.get(title, title)
    return f"{title} in Australia"

def extract_year(text: str) -> Optional[int]:
    """Extract year from text, handling ranges and financial years."""
    match = YEAR_PATTERN.search(str(text))
    if match:
        year_str = match.group(0)
        if '-' in year_str or '–' in year_str:
            # For ranges like 2022-23, take the first year
            return int(year_str.split('-')[0].split('–')[0])
        return int(year_str)
    return None

def find_header_row(df: pd.DataFrame) -> Tuple[int, Dict[str, str]]:
    """Find the header row and column mappings in a DataFrame."""
    header_indicators = {'sex', 'age', 'year', 'number', 'rate', 'total', 'male', 'female'}
    
    # Look for header row in first 10 rows
    for i in range(min(10, len(df))):
        row_values = set(str(x).lower().strip() for x in df.iloc[i])
        if any(x in row_values for x in header_indicators):
            # Check if next row provides additional context
            col_names = {}
            for j, col in enumerate(df.columns):
                name = str(df.iloc[i, j]).strip()
                if i + 1 < len(df):
                    subname = str(df.iloc[i + 1, j]).strip()
                    if subname and subname.lower() != 'nan':
                        name = f"{name} ({subname})"
                col_names[col] = name
            return i, col_names
    
    return 0, {col: str(col) for col in df.columns}

def standardize_column_name(name: str) -> str:
    """Convert column name to standard format."""
    name = str(name).lower().strip()
    name = re.sub(r'[^a-z0-9]+', '_', name)
    name = re.sub(r'_+', '_', name)
    name = name.strip('_')
    return name or 'unnamed'

def process_sheet(df: pd.DataFrame, sheet_name: str, file_name: str) -> List[AIHWRecord]:
    """Process a single sheet into AIHW records."""
    records = []
    
    # Extract table name and year
    table_name = extract_table_name(df, sheet_name)
    if not table_name:
        logger.warning(f"Could not find table name in sheet {sheet_name}")
        return records
    
    # Find header row and get column mappings
    header_row, col_names = find_header_row(df)
    if header_row > 0:
        df = df.iloc[header_row:].reset_index(drop=True)
    
    # Standardize column names
    df.columns = [standardize_column_name(name) for name in col_names.values()]
    
    # Drop empty columns that provide no value
    columns_to_drop = ['region', 'indigenous_status', 'notes']
    df = df.drop(columns=columns_to_drop, errors='ignore')
    
    # Extract year from table name or data
    year = None
    year_match = extract_year(table_name)
    if year_match:
        year = year_match
    
    # Process each row
    for _, row in df.iterrows():
        # Skip rows that are all NaN or contain notes
        if row.isna().all() or str(row.iloc[0]).lower().startswith(('note', 'source')):
            continue
            
        try:
            # Extract sex and age group if present
            sex = None
            age_group = None
            for col in df.columns:
                val = str(row[col]).strip()
                if val.lower() in ['men', 'male', 'males', 'women', 'female', 'females', 'persons', 'all']:
                    sex = val
                elif re.match(r'\d+[-–]\d+|\d+\+|total|all ages', val.lower()):
                    age_group = val
            
            # Look for numeric values and their associated metadata
            for col in df.columns:
                try:
                    val = pd.to_numeric(row[col])
                    if pd.isna(val) or val == 0:
                        continue
                        
                    # Determine metric type based on column name and value
                    metric_type = MetricType.NUMBER
                    col_lower = col.lower()
                    if 'rate' in col_lower:
                        metric_type = MetricType.RATE
                    elif 'percent' in col_lower or '%' in col_lower or (0 <= val <= 100 and 'proportion' in col_lower):
                        metric_type = MetricType.PERCENTAGE
                    elif 'crude' in col_lower:
                        metric_type = MetricType.CRUDE_RATE
                    elif 'standardised' in col_lower or 'standardized' in col_lower:
                        metric_type = MetricType.STANDARDISED_RATE
                    
                    # Try to extract year from column name if not found in table
                    if not year:
                        year_match = extract_year(col)
                        if year_match:
                            year = year_match
                    
                    # Create record without empty columns
                    record = AIHWRecord(
                        year=year or datetime.now().year,
                        value=float(val),
                        metric_type=metric_type,
                        source_sheet=sheet_name,
                        sex=sex,
                        age_group=age_group,
                        table_name=table_name,
                        condition=re.sub(r'Table [A-Z0-9.]+:', '', table_name).split('(')[0].strip()
                    )
                    records.append(record)
                except (ValueError, TypeError):
                    continue
                    
        except Exception as e:
            logger.warning(f"Error processing row in sheet {sheet_name}: {e}")
            continue
            
    return records

def process_aihw_excel(file_path: str, output_path: str) -> AIHWDataset:
    """
    Process an AIHW Excel file into a standardised dataset and save to CSV.
    
    Args:
        file_path: Path to input Excel file
        output_path: Path to save processed CSV file
    """
    logger.info(f"Processing {Path(file_path).name}")
    
    # Read Excel file
    xl = pd.ExcelFile(file_path)
    sheets = [s for s in xl.sheet_names if s not in SHEETS_TO_EXCLUDE]
    logger.info(f"Sheet names: {xl.sheet_names}")
    logger.info(f"Data sheets identified: {sheets}")
    
    all_records = []
    for sheet in sheets:
        logger.info(f"Loading sheet: '{sheet}' with header=4")
        try:
            df = pd.read_excel(file_path, sheet_name=sheet, header=None)
            if df.empty or df.isna().all().all():
                logger.info(f"Sheet '{sheet}' is empty or contains only NaN values. Skipping.")
                continue
            logger.info(f"Successfully loaded sheet '{sheet}'. Shape: {df.shape}")
            
            records = process_sheet(df, sheet, Path(file_path).name)
            all_records.extend(records)
            
        except Exception as e:
            logger.error(f"Error processing sheet {sheet}: {e}")
            continue
    
    # Convert records to DataFrame
    records_data = []
    for record in all_records:
        record_dict = record.dict()
        records_data.append(record_dict)
    
    df = pd.DataFrame(records_data)
    
    # Drop empty columns that provide no value
    columns_to_drop = ['region', 'indigenous_status', 'notes']
    df = df.drop(columns=columns_to_drop, errors='ignore')
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    logger.info(f"Combined DataFrame shape: {df.shape}")
    logger.info(f"Saving combined data to: {output_path}")
    
    return AIHWDataset(
        records=all_records,
        source_file=Path(file_path).name,
        processed_date=datetime.now()
    )

def validate_data(df, source_file):
    """Validate data using Pydantic models."""
    valid_records = []
    
    for _, row in df.iterrows():
        try:
            # Convert row to dict
            record_dict = row.to_dict()
            
            # Determine metric type based on sheet name
            sheet_name = record_dict.get('source_sheet', '').lower()
            if 'mortality' in sheet_name:
                metric_type = MetricType.MORTALITY
            elif 'incidence' in sheet_name:
                metric_type = MetricType.INCIDENCE
            else:
                metric_type = MetricType.PREVALENCE
            
            record_dict['metric_type'] = metric_type
            
            # Create and validate record
            record = AIHWRecord(**record_dict)
            valid_records.append(record)
        except Exception as e:
            logging.warning(f"Failed to validate record: {record_dict}")
            logging.warning(f"Error: {e}")
            continue
    
    # Create dataset
    dataset = AIHWDataset(
        records=valid_records,
        source_file=str(source_file),
        processed_date=datetime.now()
    )
    
    logging.info(f"Successfully validated {len(valid_records)} records")
    
    # Convert back to DataFrame
    if valid_records:
        return pd.DataFrame([record.dict() for record in valid_records])
    return pd.DataFrame()

def process_all_aihw_files(raw_dir, processed_dir):
    """Process all AIHW Excel files in the raw directory."""
    results = {}
    
    # Define file mappings
    file_mappings = {
        'AIHW-DEM-02-S2-Prevalence.xlsx': 'aihw_dementia_prevalence.csv',
        'AIHW-DEM-02-S3-Mortality-202409.xlsx': 'aihw_dementia_mortality.csv',
        'AIHW-CVD-92-HSVD-facts-data-tables-12122024.xlsx': 'aihw_cvd_all_facts.csv'
    }
    
    for excel_file, csv_file in file_mappings.items():
        input_path = os.path.join(raw_dir, excel_file)
        output_path = os.path.join(processed_dir, csv_file)
        
        if os.path.exists(input_path):
            try:
                # Process the Excel file
                dataset = process_aihw_excel(input_path, output_path)
                
                # Convert records to DataFrame
                records_data = []
                for record in dataset.records:
                    record_dict = record.model_dump()
                    records_data.append(record_dict)
                
                if records_data:
                    df = pd.DataFrame(records_data)
                    # Drop empty columns that provide no value
                    columns_to_drop = ['region', 'indigenous_status', 'notes']
                    df = df.drop(columns=columns_to_drop, errors='ignore')
                    df.to_csv(output_path, index=False)
                    logger.info(f"Successfully saved {len(records_data)} records to {csv_file}")
                    results[csv_file] = df
                else:
                    logger.warning(f"No valid records found in {excel_file}")
                    
            except Exception as e:
                logger.error(f"Error processing {excel_file}: {e}")
                continue
                
        else:
            logger.warning(f"File not found: {input_path}")
            
    return results

if __name__ == "__main__":
    process_all_aihw_files() 