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
import argparse

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
    # Skip numeric values that aren't actually years (e.g., data values)
    if isinstance(text, (int, float)) or (isinstance(text, str) and text.replace('.', '', 1).isdigit()):
        numeric_value = float(text)
        # If it's a large number that could be a count/value rather than a year, skip it
        if numeric_value > 3000:  # Arbitrary threshold higher than realistic year values
            return None
    
    match = YEAR_PATTERN.search(str(text))
    if match:
        year_str = match.group(0)
        if '-' in year_str or '–' in year_str:
            # For ranges like 2022-23, take the first year
            year_value = int(year_str.split('-')[0].split('–')[0])
        else:
            year_value = int(year_str)
            
        # More restrictive validation: only allow years between 2009 and 2022
        # This matches our known dataset time range
        if 2009 <= year_value <= 2022:
            return year_value
        return None
    return None

def find_header_row(df: pd.DataFrame) -> Tuple[int, Dict[str, str]]:
    """Find the header row and column mappings in a DataFrame."""
    header_indicators = {
        'sex', 'age', 'year', 'number', 'rate', 'total', 'male', 'female', 'persons',
        'deaths', 'mortality', 'prevalence', 'men', 'women'
    }
    
    # Look for header row in first 15 rows
    for i in range(min(15, len(df))):
        row_values = set(str(x).lower().strip() for x in df.iloc[i] if pd.notna(x))
        
        # Check if this row contains header indicators
        if any(x in row_values for x in header_indicators):
            # Initialize column names
            col_names = {}
            
            # Check next few rows for potential subheaders
            max_subheader_rows = min(i + 3, len(df))
            subheaders = []
            
            for j in range(i, max_subheader_rows):
                row = df.iloc[j]
                if not row.isna().all():  # Skip empty rows
                    subheaders.append(row)
            
            # Combine headers if multiple header rows found
            if len(subheaders) > 1:
                for col_idx in range(len(df.columns)):
                    col_parts = []
                    for subheader in subheaders:
                        val = str(subheader.iloc[col_idx]).strip()
                        if pd.notna(val) and val.lower() not in ('nan', ''):
                            col_parts.append(val)
                    col_names[df.columns[col_idx]] = ' '.join(col_parts)
            else:
                # Single header row
                for j, col in enumerate(df.columns):
                    name = str(df.iloc[i, j]).strip()
                    col_names[col] = name if name.lower() not in ('nan', '') else f'column_{j}'
            
            # Clean up column names
            col_names = {k: v.replace('\n', ' ').strip() for k, v in col_names.items()}
            
            return i, col_names
    
    # If no header row found, use default column names
    return 0, {col: f'column_{i}' for i, col in enumerate(df.columns)}

def standardize_column_name(name: str) -> str:
    """Convert column name to standard format."""
    name = str(name).lower().strip()
    name = re.sub(r'[^a-z0-9]+', '_', name)
    name = re.sub(r'_+', '_', name)
    name = name.strip('_')
    return name or 'unnamed'

def process_sheet(df: pd.DataFrame, sheet_name: str, file_name: str) -> List[AIHWRecord]:
    """Process a single sheet into AIHW records."""
    # Find the table title for this sheet
    table_name = extract_table_name(df, sheet_name)
    logger.debug(f"Table name: {table_name}")
    
    records = []
    
    # Special handling for S3.3 sheet (known time series sheet with years 2009-2022)
    if sheet_name == 'S3.3' and 'AIHW-DEM-02-S3-Mortality' in file_name:
        logger.info(f"Using special handling for time series sheet {sheet_name}")
        try:
            # This sheet has years 2009-2022 in column A
            # Data starts approximately at row 10
            data_rows = df.iloc[10:].reset_index(drop=True)
            data_rows = data_rows.dropna(how='all')
            year_idx = 0  # Year is in column A (index 0)
            # Years 2009-2022 are in rows 4-17 (index 3-16)
            
            for idx, row in data_rows.iterrows():
                try:
                    # Extract year
                    year_val = row.iloc[year_idx]
                    if pd.isna(year_val):
                        continue
                        
                    try:
                        year = extract_year(str(year_val))
                        if year and 2009 <= year <= 2022:
                            # Create records for each metric
                            # Men deaths - col 1
                            if not pd.isna(row.iloc[1]):
                                records.append(AIHWRecord(
                                    year=year,
                                    value=float(row.iloc[1]),
                                    metric_type=MetricType.NUMBER,
                                    source_sheet=sheet_name,
                                    sex="men",
                                    age_group=None,
                                    table_name="Deaths due to dementia in Australia",
                                    condition="Dementia"
                                ))
                            
                            # Women deaths - col 2
                            if not pd.isna(row.iloc[2]):
                                records.append(AIHWRecord(
                                    year=year,
                                    value=float(row.iloc[2]),
                                    metric_type=MetricType.NUMBER,
                                    source_sheet=sheet_name,
                                    sex="women",
                                    age_group=None,
                                    table_name="Deaths due to dementia in Australia",
                                    condition="Dementia"
                                ))
                                
                            # Persons deaths - col 3
                            if not pd.isna(row.iloc[3]):
                                records.append(AIHWRecord(
                                    year=year,
                                    value=float(row.iloc[3]),
                                    metric_type=MetricType.NUMBER,
                                    source_sheet=sheet_name,
                                    sex="persons",
                                    age_group=None,
                                    table_name="Deaths due to dementia in Australia",
                                    condition="Dementia"
                                ))
                                
                            # Age-standardised rates - cols 4-6
                            for col_idx, sex in [(4, "men"), (5, "women"), (6, "persons")]:
                                if not pd.isna(row.iloc[col_idx]):
                                    records.append(AIHWRecord(
                                        year=year,
                                        value=float(row.iloc[col_idx]),
                                        metric_type=MetricType.STANDARDISED_RATE,
                                        source_sheet=sheet_name,
                                        sex=sex,
                                        age_group=None,
                                        table_name="Deaths due to dementia in Australia",
                                        condition="Dementia"
                                    ))
                                    
                            # Crude rates - cols 7-9
                            for col_idx, sex in [(7, "men"), (8, "women"), (9, "persons")]:
                                if not pd.isna(row.iloc[col_idx]):
                                    records.append(AIHWRecord(
                                        year=year,
                                        value=float(row.iloc[col_idx]),
                                        metric_type=MetricType.CRUDE_RATE,
                                        source_sheet=sheet_name,
                                        sex=sex,
                                        age_group=None,
                                        table_name="Deaths due to dementia in Australia",
                                        condition="Dementia"
                                    ))
                        else:
                            logger.warning(f"Invalid year {year_val} in S3.3 row {idx} - outside valid range 2009-2022")
                    except (ValueError, TypeError) as e:
                        logger.warning(f"Error processing year in S3.3 row {idx}: {e}")
                        continue
                except Exception as e:
                    logger.warning(f"Error processing S3.3 row {idx}: {e}")
                    continue
                    
            logger.info(f"Successfully extracted {len(records)} time series records from {sheet_name}")
            if records:
                return records
            # Fall back to standard processing if no records were extracted
        except Exception as e:
            logger.error(f"Error in special handling for {sheet_name}: {e}")
            # Fall back to standard processing
    
    # Special handling for known S3.5 sheet
    if sheet_name == 'S3.5':
        logger.info(f"Using direct extraction for known time series sheet: {sheet_name}")
        try:
            # Similar approach for S3.5 which also contains Years 2009-2022 but different metrics
            # The structure is consistent: Year in col 0, metrics in cols 1-6
            year_idx = 0
            
            # We know headers are at row 3 (index 2)
            df.columns = [f"col_{i}" for i in range(len(df.columns))]
            data_rows = df.iloc[3:17]  # Years 2009-2022 are in rows 4-17 (index 3-16)
            
            for idx, row in data_rows.iterrows():
                try:
                    # Extract year
                    year_val = row.iloc[year_idx]
                    if pd.isna(year_val):
                        continue
                        
                    try:
                        year = int(str(year_val)[:4])
                        if 1900 <= year <= datetime.now().year:
                            # Create records for each metric - S3.5 has different structure
                            # Columns might be different, adjust as needed
                            # Age-standardised rates - assuming cols 1-3
                            for col_idx, sex in [(1, "men"), (2, "women"), (3, "persons")]:
                                if col_idx < len(row) and not pd.isna(row.iloc[col_idx]):
                                    records.append(AIHWRecord(
                                        year=year,
                                        value=float(row.iloc[col_idx]),
                                        metric_type=MetricType.STANDARDISED_RATE,
                                        source_sheet=sheet_name,
                                        sex=sex,
                                        age_group=None,
                                        table_name="Alzheimer deaths in Australia",
                                        condition="Alzheimer's Disease"
                                    ))
                    except (ValueError, TypeError) as e:
                        logger.warning(f"Error processing year in S3.5 row {idx}: {e}")
                        continue
                except Exception as e:
                    logger.warning(f"Error processing S3.5 row {idx}: {e}")
                    continue
                    
            logger.info(f"Successfully extracted {len(records)} time series records from {sheet_name}")
            if records:
                return records
            # Fall back to standard processing if no records were extracted
        except Exception as e:
            logger.error(f"Error in special handling for {sheet_name}: {e}")
            # Fall back to standard processing
    
    # Find tables in the sheet (standard approach)
    tables = find_tables_in_sheet(df)
    
    for table_info in tables:
        try:
            # Extract table data
            table_df = df.iloc[table_info['start_row']:table_info['end_row']].copy()
            table_name = table_info['title']
            is_time_series = table_info.get('is_time_series', False)
            
            # Find header row within the table
            header_row, col_names = find_header_row(table_df)
            if header_row > 0:
                table_df = table_df.iloc[header_row:].reset_index(drop=True)
                table_df.columns = [standardize_column_name(name) for name in col_names.values()]
            
            # Check if this is a time series table (has a year column)
            has_year_column = any('year' in str(col).lower() for col in table_df.columns)
            
            # Flag as time series if either condition is true
            is_time_series = is_time_series or has_year_column
            
            # Extract default year from table name if not a time series
            default_year = None if is_time_series else extract_year_from_table(table_df, table_name)
            
            # Log the detection of a time series
            if is_time_series:
                logger.info(f"Detected time series data in sheet '{sheet_name}', table: '{table_name}'")
                
                # Special handling for clear time series data with year in first column
                if has_year_column and len(table_df) > 0:
                    # Find the year column index
                    year_col_idx = -1
                    for i, col in enumerate(table_df.columns):
                        if 'year' in str(col).lower():
                            year_col_idx = i
                            break
                    
                    if year_col_idx >= 0:
                        logger.info(f"Using special time series handler for sheet '{sheet_name}'")
                        sex_values = ["men", "women", "persons"]
                        # Process each row (skipping header rows and note rows)
                        for idx, row in table_df.iterrows():
                            # Skip empty rows or rows with notes
                            if row.isna().all() or (not pd.isna(row.iloc[0]) and str(row.iloc[0]).lower().startswith(('note', 'source', 'year'))):
                                continue
                                
                            try:
                                # Extract year from the year column
                                year_val = row.iloc[year_col_idx]
                                if pd.isna(year_val):
                                    continue
                                
                                try:
                                    # Try to convert to numeric year
                                    year = int(str(year_val)[:4])
                                    
                                    # Check if it's a valid year
                                    if 1900 <= year <= datetime.now().year:
                                        # Process the numeric columns that follow the year
                                        for col_idx, col_name in enumerate(table_df.columns):
                                            if col_idx == year_col_idx:  # Skip the year column
                                                continue
                                                
                                            val = row.iloc[col_idx]
                                            
                                            # Skip non-numeric values
                                            try:
                                                val_numeric = pd.to_numeric(str(val).strip().replace('%', ''))
                                                if pd.isna(val_numeric) or val_numeric == 0:
                                                    continue
                                            except (ValueError, TypeError):
                                                continue
                                                
                                            # Determine sex from column position (common pattern)
                                            sex = None
                                            if 0 < col_idx <= 3:  # Men, Women, Persons in columns 1,2,3
                                                sex_idx = (col_idx - 1) % 3
                                                sex = sex_values[sex_idx] if sex_idx < len(sex_values) else None
                                            elif 3 < col_idx <= 6:  # Rate columns 4,5,6
                                                sex_idx = (col_idx - 4) % 3
                                                sex = sex_values[sex_idx] if sex_idx < len(sex_values) else None
                                            elif 6 < col_idx <= 9:  # Rate columns 7,8,9
                                                sex_idx = (col_idx - 7) % 3
                                                sex = sex_values[sex_idx] if sex_idx < len(sex_values) else None
                                                
                                            metric_type = determine_metric_type(col_name, val_numeric)
                                            
                                            # Create record
                                            record = AIHWRecord(
                                                year=year,
                                                value=float(val_numeric),
                                                metric_type=metric_type,
                                                source_sheet=sheet_name,
                                                sex=sex,
                                                age_group=None,
                                                table_name=table_name,
                                                condition=extract_condition_from_table(table_name)
                                            )
                                            records.append(record)
                                            
                                except (ValueError, TypeError):
                                    continue
                            except Exception as e:
                                logger.debug(f"Error processing time series row: {e}")
                                continue
                                
                        # Skip the regular processing for these specially handled tables
                        continue
            
            # Process each row in the table (standard method)
            for _, row in table_df.iterrows():
                try:
                    # Skip rows that are all NaN or contain notes/sources
                    if row.isna().all() or any(str(row.iloc[0]).lower().startswith(x) for x in ('note', 'source')):
                        continue
                    
                    # Extract metadata (sex, age_group, etc.)
                    metadata = extract_row_metadata(row)
                    
                    # For time series data, require a year to be present
                    if is_time_series and 'year' not in metadata:
                        # Try harder to find a year in the row
                        for val in row:
                            if pd.isna(val):
                                continue
                            try:
                                val_str = str(val).strip()
                                year_match = re.search(r'(?:19|20)\d{2}', val_str)
                                if year_match:
                                    metadata['year'] = int(year_match.group())
                                    break
                            except (ValueError, TypeError):
                                continue
                    
                    # Determine the year for this row
                    row_year = metadata.get('year') or default_year or datetime.now().year
                    
                    # Process numeric values in the row
                    for col in table_df.columns:
                        try:
                            # Skip year columns for value extraction
                            if 'year' in str(col).lower():
                                continue
                                
                            # Try to convert to numeric, handling percentage strings
                            val_str = str(row[col]).strip().replace('%', '')
                            val = pd.to_numeric(val_str)
                            
                            if pd.isna(val) or val == 0:
                                continue
                            
                            metric_type = determine_metric_type(col, val)
                            
                            # Create record with the correct year
                            record = AIHWRecord(
                                year=row_year,
                                value=float(val),
                                metric_type=metric_type,
                                source_sheet=sheet_name,
                                sex=metadata.get('sex'),
                                age_group=metadata.get('age_group'),
                                table_name=table_name,
                                condition=extract_condition_from_table(table_name)
                            )
                            records.append(record)
                        except (ValueError, TypeError):
                            continue
                except Exception as e:
                    logger.debug(f"Error processing row in table: {e}")
                    continue
                    
        except Exception as e:
            logger.warning(f"Error processing table in sheet {sheet_name}: {e}")
            continue
    
    return records

def find_tables_in_sheet(df: pd.DataFrame) -> List[Dict]:
    """Find tables within a sheet based on headers and content."""
    tables = []
    current_table = None
    
    for i, row in df.iterrows():
        # Convert row values to string, handling non-string types
        row_text = ' '.join(str(x).strip() for x in row if pd.notna(x))
        
        # Check for table headers
        if ('Table' in row_text or 
            any(x in row_text.lower() for x in ['deaths', 'rates', 'prevalence', 'mortality', 'number of', 
                                             'age-specific', 'age-standardised', 'year', 'period', 
                                             'over the period', 'time series']) or
            re.search(r'(?:19|20)\d{2}[-–](?:19|20)\d{2}', row_text) or  # Look for year ranges
            (i == 0 and not row.isna().all())):  # First non-empty row might be a header
            
            if current_table:
                current_table['end_row'] = i
                tables.append(current_table)
            
            current_table = {
                'start_row': i,
                'title': row_text.strip(),
                'end_row': None,
                'is_time_series': any(x in row_text.lower() for x in ['year', 'period', 'over the period']) or
                                  re.search(r'(?:19|20)\d{2}[-–](?:19|20)\d{2}', row_text)
            }
        
        # Check for end of table markers
        elif current_table and (
            row.isna().all() or 
            any(str(x).lower().startswith(('note', 'source')) for x in row if pd.notna(x)) or
            i == len(df) - 1
        ):
            current_table['end_row'] = i
            tables.append(current_table)
            current_table = None
    
    # Handle last table if it exists
    if current_table:
        current_table['end_row'] = len(df)
        tables.append(current_table)
    
    # Filter out too-small tables and merge adjacent tables if they look related
    filtered_tables = []
    for i, table in enumerate(tables):
        # Skip tables that are too small
        if table['end_row'] - table['start_row'] < 2:
            continue
            
        # Check if this table should be merged with the previous one
        if filtered_tables and i > 0:
            prev_table = filtered_tables[-1]
            if (table['start_row'] - prev_table['end_row'] <= 2 and  # Tables are close
                not any(str(x).lower().startswith(('note', 'source')) 
                       for x in df.iloc[prev_table['end_row']:table['start_row']].values.flatten() 
                       if pd.notna(x))):  # No notes between tables
                # Merge tables
                prev_table['end_row'] = table['end_row']
                # If either table is a time series, the merged table is a time series
                prev_table['is_time_series'] = prev_table.get('is_time_series', False) or table.get('is_time_series', False)
                continue
                
        filtered_tables.append(table)
    
    return filtered_tables

def extract_row_metadata(row: pd.Series) -> Dict:
    """Extract metadata from a row including sex, age group, and year."""
    metadata = {}
    
    for col, val in row.items():
        # Convert to string, handling non-string types
        try:
            if pd.isna(val):
                continue
            val_str = str(val).strip().lower()
            col_str = str(col).strip().lower()
            
            # Skip numeric values that aren't actually years
            if isinstance(val, (int, float)) or val_str.replace('.', '', 1).isdigit():
                try:
                    numeric_value = float(val)
                    # If it's a large number, it's probably a count/value rather than a year
                    if numeric_value > 3000:
                        continue
                except:
                    pass
        except:
            continue
        
        # Check if column name indicates a year column
        if 'year' in col_str:
            try:
                # Extract year directly from a year column
                year_match = re.search(r'(?:19|20)\d{2}', val_str)
                if year_match:
                    year_value = int(year_match.group())
                    # More restrictive validation: only allow years between 2009 and 2022
                    if 2009 <= year_value <= 2022:
                        metadata['year'] = year_value
                    continue
            except (ValueError, TypeError):
                pass
        
        # Extract sex
        if val_str in ['m', 'men', 'male', 'males', 'women', 'f', 'female', 'females', 'p', 'person', 'persons', 'people', 'all']:
            metadata['sex'] = val_str
        
        # Extract age group
        elif re.match(r'\d+[-–]\d+|\d+\+|total|all ages', val_str):
            metadata['age_group'] = val_str
        
        # Extract year if present in a value - with validation
        elif re.match(r'(?:19|20)\d{2}(?:[-–]\d{2})?', val_str):
            try:
                year_value = int(val_str[:4])
                # More restrictive validation: only allow years between 2009 and 2022
                if 2009 <= year_value <= 2022:
                    metadata['year'] = year_value
            except ValueError:
                continue
    
    return metadata

def determine_metric_type(column_name: str, value: float) -> MetricType:
    """Determine the metric type based on column name and value."""
    col_lower = column_name.lower()
    
    if 'rate' in col_lower:
        if 'crude' in col_lower:
            return MetricType.CRUDE_RATE
        elif 'standardised' in col_lower or 'standardized' in col_lower:
            return MetricType.STANDARDISED_RATE
        return MetricType.RATE
    elif 'percent' in col_lower or '%' in col_lower or (0 <= value <= 100 and 'proportion' in col_lower):
        return MetricType.PERCENTAGE
    elif 'number' in col_lower or 'deaths' in col_lower:
        return MetricType.NUMBER
    
    return MetricType.NUMBER

def extract_year_from_table(df: pd.DataFrame, table_name: str) -> Optional[int]:
    """Extract year from table name or data."""
    
    # Try table name first
    year_match = re.search(r'(?:19|20)\d{2}(?:[-–]\d{2})?', table_name)
    if year_match:
        year_value = int(year_match.group()[:4])
        # More restrictive validation: only allow years between 2009 and 2022
        if 2009 <= year_value <= 2022:
            return year_value
    
    # Try column names
    for col in df.columns:
        col_str = str(col)
        # Skip numeric values that aren't actually years
        if isinstance(col, (int, float)) or (isinstance(col_str, str) and col_str.replace('.', '', 1).isdigit()):
            try:
                numeric_value = float(col)
                # If it's a large number, it's probably a count/value rather than a year
                if numeric_value > 3000:
                    continue
            except:
                pass
                
        year_match = re.search(r'(?:19|20)\d{2}(?:[-–]\d{2})?', col_str)
        if year_match:
            year_value = int(year_match.group()[:4])
            # More restrictive validation: only allow years between 2009 and 2022
            if 2009 <= year_value <= 2022:
                return year_value
    
    return None

def extract_condition_from_table(table_name: str) -> str:
    """Extract the health condition from the table name."""
    # Remove table number if present
    cleaned_name = re.sub(r'Table [A-Z0-9.]+:', '', table_name)
    # Remove year ranges
    cleaned_name = re.sub(r'(?:19|20)\d{2}(?:[-–]\d{2})?', '', cleaned_name)
    # Remove parenthetical content
    cleaned_name = re.sub(r'\([^)]*\)', '', cleaned_name)
    return cleaned_name.split('in Australia')[0].strip()

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
    logger.info(f"Found {len(sheets)} data sheets: {sheets}")
    
    all_records = []
    
    # Process each sheet
    for sheet in sheets:
        try:
            # Read the sheet without assuming header row
            logger.info(f"Loading sheet: '{sheet}'")
            df = pd.read_excel(file_path, sheet_name=sheet, header=None)
            
            # Skip empty sheets
            if df.empty or df.isna().all().all():
                logger.info(f"Sheet '{sheet}' is empty. Skipping.")
                continue
                
            logger.info(f"Processing sheet '{sheet}'. Shape: {df.shape}")
            
            # Process the sheet
            records = process_sheet(df, sheet, Path(file_path).name)
            if records:
                logger.info(f"Extracted {len(records)} records from sheet '{sheet}'")
                all_records.extend(records)
            else:
                logger.warning(f"No records extracted from sheet '{sheet}'")
            
        except Exception as e:
            logger.error(f"Error processing sheet {sheet}: {e}")
            continue
    
    if not all_records:
        logger.error("No records were extracted from any sheet")
        return AIHWDataset(
            records=[],
            source_file=Path(file_path).name,
            processed_date=datetime.now()
        )
    
    # Convert records to DataFrame
    records_data = []
    for record in all_records:
        try:
            # Use model_dump instead of dict
            record_dict = record.model_dump()
            records_data.append(record_dict)
        except Exception as e:
            logger.warning(f"Invalid record: {e}")
            continue
    
    df = pd.DataFrame(records_data)
    
    # Clean up the DataFrame
    if not df.empty:
        # Filter by valid year range (2009-2022 only)
        # This is a strict range for which we know we have real data
        if 'year' in df.columns:
            original_count = len(df)
            df = df[(df['year'] >= 2009) & (df['year'] <= 2022)]
            filtered_count = original_count - len(df)
            if filtered_count > 0:
                logger.info(f"Filtered out {filtered_count} records with years outside 2009-2022 range")
        
        # Sort by year and other relevant columns
        sort_cols = ['year', 'source_sheet', 'sex', 'age_group']
        sort_cols = [col for col in sort_cols if col in df.columns]
        if sort_cols:
            df = df.sort_values(sort_cols)
        
        # Drop any empty columns
        df = df.dropna(axis=1, how='all')
        
        # Drop duplicate records
        df = df.drop_duplicates()
        
        # Save to CSV
        df.to_csv(output_path, index=False)
        logger.info(f"Saved {len(df)} records to {output_path}")
        logger.info(f"DataFrame shape: {df.shape}")
        logger.info(f"Columns: {', '.join(df.columns)}")
    else:
        logger.error("No valid records to save")
    
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
                    
                    # FINAL SAFETY CHECK: Filter only 2009-2022 years regardless of what earlier filtering did
                    if 'year' in df.columns:
                        original_count = len(df)
                        df = df[(df['year'] >= 2009) & (df['year'] <= 2022)]
                        filtered_count = original_count - len(df)
                        if filtered_count > 0:
                            logger.info(f"Final filtering: removed {filtered_count} records with invalid years from {csv_file}")
                    
                    df.to_csv(output_path, index=False)
                    logger.info(f"Successfully saved {len(df)} records to {csv_file}")
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
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Process AIHW Excel files into standardized CSV format.')
    parser.add_argument('raw_dir', help='Directory containing raw AIHW Excel files')
    parser.add_argument('processed_dir', help='Directory to save processed CSV files')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Process files
    process_all_aihw_files(args.raw_dir, args.processed_dir) 