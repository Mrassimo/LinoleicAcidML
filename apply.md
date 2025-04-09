Okay, the log looks much better! The ETL completed successfully, and importantly, Total_Carb_Supply_g is now 100% complete. The validation passed with 0 invalid records.

However, we still have the issue where Dementia_Prevalence_Number and CVD_Mortality_Rate_ASMR are 0% complete. Let's fix that.

Looking at the logs again:

WARNING - No 'persons' data found in aihw_dementia_prevalence.csv from sheet S2.4.

ERROR - Missing required columns in data/processed/aihw_cvd_metrics_australia_processed.csv: ['sex']

These clearly point to problems in how we are processing or filtering the AIHW data.

Issue 1 (Dementia Prevalence): The filtering in health_outcome_metrics.py for sex == 'persons' on the S2.4 data is failing. This means either the process_aihw_data.py script isn't correctly assigning 'persons' to the sex column for that specific sheet, or the column name/value is slightly different.

Issue 2 (CVD Mortality): The aihw_cvd_metrics_australia_processed.csv file is missing the sex column entirely, which breaks the filtering in health_outcome_metrics.py. We need to ensure process_aihw_data.py adds the sex column correctly when processing Table 11 from the CVD file.

Let's fix process_aihw_data.py to correctly handle the sex column assignment for these specific cases.

Step 1: Correct Sex Assignment in process_aihw_data.py

We need to adjust the special handling sections for S2.4 and Table 11 to explicitly assign the correct sex based on the column index from which the value is being extracted.

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

# Fix the import path issue
# Use relative import within the package
from ..models.aihw_models import AIHWRecord, AIHWDataset, MetricType

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
        cell_value = df.iloc[i, 0]
        if pd.notna(cell_value):
            cell = str(cell_value)
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
    return f"{title} in Australia" # Assume Australia context

def extract_year(text: str) -> Optional[int]:
    """Extract year from text, handling ranges and financial years."""
    if pd.isna(text):
        return None

    text_str = str(text)

    # Skip clearly non-year numeric values
    if text_str.replace('.', '', 1).isdigit():
        try:
            numeric_value = float(text_str)
            # Allow years but filter out large numbers likely data points
            if numeric_value > 2100 or numeric_value < 1900: # Check if outside plausible year range
                return None
        except ValueError:
            pass # Not a simple number

    match = YEAR_PATTERN.search(text_str)
    if match:
        year_str = match.group(0)
        # Handle ranges like '2022-23' or '2022–23' -> take the first year
        year_value = int(re.split(r'[-–]', year_str)[0])

        # Validate year range (adjust if needed for projections)
        if 1960 <= year_value <= 2060: # Allow years from 1960 up to projections
            return year_value
    return None


def find_header_row(df: pd.DataFrame) -> Tuple[Optional[int], Optional[Dict[str, str]]]:
    """Find the header row and column mappings in a DataFrame."""
    header_indicators = {
        'sex', 'age', 'year', 'number', 'rate', 'total', 'male', 'female', 'persons',
        'deaths', 'mortality', 'prevalence', 'men', 'women', 'condition', 'table', 'metric'
    }

    for i in range(min(15, len(df))):
        row_values_set = set()
        row_values_list = []
        is_potential_header = False
        for x in df.iloc[i]:
            if pd.notna(x):
                val_str = str(x).lower().strip()
                row_values_set.add(val_str)
                row_values_list.append(val_str)
                if val_str in header_indicators:
                    is_potential_header = True

        # Require at least 2 indicators or 'year' to be considered a header
        if is_potential_header and (len(row_values_set.intersection(header_indicators)) >= 2 or 'year' in row_values_set):
            logger.debug(f"Potential header found at row {i}: {row_values_list}")
            # Basic column mapping from this row
            col_names = {}
            for j, col_header in enumerate(df.iloc[i]):
                 col_names[j] = str(col_header).strip() if pd.notna(col_header) else f'unnamed_{j}'

            # Refine with potential subheaders (simple approach: check next row)
            if i + 1 < len(df):
                next_row = df.iloc[i+1]
                if not next_row.isna().all() and len(next_row.dropna()) > 1: # Check if next row has content
                    for j, sub_header in enumerate(next_row):
                        if pd.notna(sub_header) and str(sub_header).strip():
                             # Prepend subheader if it exists
                             col_names[j] = f"{str(sub_header).strip()} {col_names[j]}"

            # Clean up names
            col_names = {f'col_{k}': v.replace('\n', ' ').strip() for k, v in col_names.items()}
            return i, col_names # Return index and mapped names

    logger.warning("No distinct header row found based on indicators.")
    return None, None # Indicate no header found

def standardize_column_name(name: str) -> str:
    """Convert column name to standard format."""
    name = str(name).lower().strip()
    # Handle specific known variations first
    if name in ['males', 'male', 'men']: return 'sex_male'
    if name in ['females', 'female', 'women']: return 'sex_female'
    if name in ['persons', 'people', 'total', 'all']: return 'sex_persons'
    if 'age group' in name or name == 'age': return 'age_group'
    if 'year' in name: return 'year'
    if 'number' in name: return 'value_number'
    if 'rate' in name:
        if 'crude' in name: return 'value_crude_rate'
        if 'standardised' in name or 'standardized' in name: return 'value_standardised_rate'
        return 'value_rate'
    if 'percent' in name or '%' in name: return 'value_percentage'

    # General cleaning
    name = re.sub(r'[^a-z0-9_]+', '_', name)
    name = re.sub(r'_+', '_', name)
    name = name.strip('_')
    return name or 'unnamed'

def process_sheet(df: pd.DataFrame, sheet_name: str, file_name: str) -> List[AIHWRecord]:
    """Process a single sheet into AIHW records."""
    table_name = extract_table_name(df, sheet_name)
    logger.info(f"Processing Sheet: '{sheet_name}', Table: '{table_name}'")
    records = []

    # --- Special Handling for S2.4 (Dementia Prevalence) ---
    if sheet_name == 'S2.4' and 'AIHW-DEM-02-S2-Prevalence' in file_name:
        logger.info(f"Applying special handling for Sheet S2.4")
        header_row_idx = None
        for i in range(min(15, len(df))):
            # Look for 'Year' in the first column to identify the header row
            if pd.notna(df.iloc[i, 0]) and "Year" in str(df.iloc[i, 0]):
                header_row_idx = i
                break

        if header_row_idx is not None:
            logger.info(f"Found header row at row {header_row_idx} in S2.4")
            data_start_row = header_row_idx + 1
            data_df = df.iloc[data_start_row:].copy()
            # Assign temporary column names for easier access: col_0=Year, col_1=Men, col_2=Women, col_3=Persons
            data_df.columns = [f'col_{j}' for j in range(len(data_df.columns))]

            for idx, row in data_df.iterrows():
                year_val = row['col_0']
                year = extract_year(year_val) # Use the updated extract_year

                if year: # Check if year is valid
                    # Men (col 1), Women (col 2), Persons (col 3) - based on Excel structure
                    for col_idx, sex in [(1, "male"), (2, "female"), (3, "persons")]: # Corrected sex values
                         col_key = f'col_{col_idx}'
                         if col_key in row and pd.notna(row[col_key]):
                             try:
                                 value = float(row[col_key])
                                 # Create record with CORRECT sex value
                                 records.append(AIHWRecord(
                                     year=year,
                                     value=value,
                                     metric_type=MetricType.NUMBER, # This sheet contains numbers
                                     source_sheet=sheet_name,
                                     sex=sex, # Use the determined sex
                                     age_group='all_ages', # This table is for all ages
                                     table_name=table_name, # Use extracted table name
                                     condition="Dementia"
                                 ))
                             except (ValueError, TypeError) as e:
                                 logger.warning(f"Sheet {sheet_name}, Row {idx+data_start_row}, Col {col_idx}: Could not convert value '{row[col_key]}' to float. Error: {e}")
                # else: logger.debug(f"Sheet {sheet_name}, Row {idx+data_start_row}: Invalid or out-of-range year '{year_val}'")
            logger.info(f"Sheet {sheet_name}: Extracted {len(records)} records using special handling.")
            return records # Return early after special handling
        else:
            logger.warning(f"Could not find header row for special handling in Sheet {sheet_name}.")
            # Fall through to standard processing if special handling fails

    # --- Special Handling for S3.5 (Dementia Mortality - Alzheimer's) ---
    elif sheet_name == 'S3.5' and 'AIHW-DEM-02-S3-Mortality' in file_name:
        logger.info(f"Applying special handling for Sheet S3.5")
        header_row_idx = None
        for i in range(min(15, len(df))):
            if pd.notna(df.iloc[i, 0]) and "Year" in str(df.iloc[i, 0]):
                header_row_idx = i
                break

        if header_row_idx is not None:
            logger.info(f"Found header row at row {header_row_idx} in S3.5")
            data_start_row = header_row_idx + 1
            # Data seems to end before notes, find the last valid year row
            last_data_row = data_start_row
            for i in range(data_start_row, len(df)):
                 if pd.isna(df.iloc[i, 0]) or not str(df.iloc[i, 0]).strip().isdigit():
                      break
                 last_data_row = i + 1

            data_df = df.iloc[data_start_row:last_data_row].copy()
            data_df.columns = [f'col_{j}' for j in range(len(data_df.columns))] # Assign temp names

            for idx, row in data_df.iterrows():
                year_val = row['col_0']
                year = extract_year(year_val) # Use updated extract_year

                if year: # Check if year is valid
                    # Age-standardised rates: Men (col 1), Women (col 2), Persons (col 3)
                    for col_idx, sex in [(1, "male"), (2, "female"), (3, "persons")]: # Corrected sex values
                        col_key = f'col_{col_idx}'
                        if col_key in row and pd.notna(row[col_key]):
                            try:
                                value = float(row[col_key])
                                records.append(AIHWRecord(
                                    year=year,
                                    value=value,
                                    metric_type=MetricType.STANDARDISED_RATE, # This sheet is rates
                                    source_sheet=sheet_name,
                                    sex=sex, # Use determined sex
                                    age_group='all_ages', # Assuming all ages unless specified
                                    table_name=table_name, # Use extracted table name
                                    condition="Alzheimer's Disease" # Specific to S3.5
                                ))
                            except (ValueError, TypeError) as e:
                                logger.warning(f"Sheet {sheet_name}, Row {idx+data_start_row}, Col {col_idx}: Could not convert value '{row[col_key]}' to float. Error: {e}")
                # else: logger.debug(f"Sheet {sheet_name}, Row {idx+data_start_row}: Invalid or out-of-range year '{year_val}'")
            logger.info(f"Sheet {sheet_name}: Extracted {len(records)} records using special handling.")
            return records # Return early
        else:
            logger.warning(f"Could not find header row for special handling in Sheet {sheet_name}.")
            # Fall through

    # --- Special Handling for Table 11 (CVD Mortality) ---
    elif sheet_name == 'All CVD' and 'AIHW-CVD-92' in file_name:
        logger.info(f"Applying special handling for CVD Table 11")
        table_start_idx, table_end_idx = None, None
        for i in range(len(df)):
            # Find the start of Table 11
            if pd.notna(df.iloc[i, 0]) and "Table 11" in str(df.iloc[i, 0]):
                table_start_idx = i
                # Find end row (look for notes or empty row after some data)
                for j in range(i + 5, len(df)): # Start looking a few rows down
                    if pd.isna(df.iloc[j, 0]) or str(df.iloc[j, 0]).lower().strip().startswith("note"):
                        table_end_idx = j
                        break
                if table_end_idx is None: table_end_idx = len(df) # If no end marker, take rest of sheet
                break

        if table_start_idx is not None and table_end_idx is not None:
            logger.info(f"Found Table 11 from rows {table_start_idx} to {table_end_idx}")
            # Header seems to be 2 rows below title based on inspection
            header_row_idx = table_start_idx + 2
            data_start_row = header_row_idx + 1
            table_df = df.iloc[data_start_row:table_end_idx].copy()
            table_df.columns = [f'col_{j}' for j in range(len(table_df.columns))] # Temp names

            for idx, row in table_df.iterrows():
                year_val = row['col_0']
                # For CVD, allow full range 1980-2022
                year_match = re.search(r'^(19[89]\d|20[01]\d|202[0-2])$', str(year_val).strip())
                if year_match:
                    year = int(year_match.group(0))
                    # Map column index to metric type and sex
                    metrics_map = {
                        1: (MetricType.NUMBER, "male"), 2: (MetricType.NUMBER, "female"), 3: (MetricType.NUMBER, "persons"),
                        4: (MetricType.CRUDE_RATE, "male"), 5: (MetricType.CRUDE_RATE, "female"), 6: (MetricType.CRUDE_RATE, "persons"),
                        7: (MetricType.STANDARDISED_RATE, "male"), 8: (MetricType.STANDARDISED_RATE, "female"), 9: (MetricType.STANDARDISED_RATE, "persons")
                    }
                    for col_idx, (metric_type, sex) in metrics_map.items():
                        col_key = f'col_{col_idx}'
                        if col_key in row and pd.notna(row[col_key]):
                            try:
                                value = float(row[col_key])
                                # Create record with CORRECT sex value
                                records.append(AIHWRecord(
                                    year=year, value=value, metric_type=metric_type,
                                    source_sheet="Table 11", sex=sex, # Assign sex here
                                    age_group='all_ages', # This table is all ages
                                    table_name="Cardiovascular disease deaths", condition="Cardiovascular Disease"
                                ))
                            except (ValueError, TypeError) as e:
                                logger.warning(f"Sheet {sheet_name}, Table 11, Row {idx+data_start_row}, Col {col_idx}: Could not convert value '{row[col_key]}' to float. Error: {e}")
                # else: logger.debug(f"Sheet {sheet_name}, Table 11, Row {idx+data_start_row}: Invalid or out-of-range year '{year_val}'")
            logger.info(f"Sheet {sheet_name}, Table 11: Extracted {len(records)} records using special handling.")
            return records # Return early
        else:
            logger.warning(f"Could not locate Table 11 structure in Sheet {sheet_name}.")
            # Fall through

    # --- Standard Processing Logic (Fallback) ---
    logger.info(f"Applying standard processing for Sheet: '{sheet_name}'")
    header_row_idx, col_map = find_header_row(df)

    if header_row_idx is None:
        logger.warning(f"Could not determine header row for sheet '{sheet_name}'. Skipping standard processing.")
        return records # Return any records found by special handling

    data_start_row = header_row_idx + 1
    data_df = df.iloc[data_start_row:].copy()
    # Use standardized names based on detected header
    data_df.columns = [standardize_column_name(col_map.get(i, f'unnamed_{i}')) for i in range(len(data_df.columns))]

    year_col = next((col for col in data_df.columns if 'year' in col), None)
    default_year = extract_year_from_table(data_df, table_name)

    for idx, row in data_df.iterrows():
        if row.isna().all() or (pd.notna(row.iloc[0]) and str(row.iloc[0]).lower().startswith(('note', 'source', 'total'))):
            continue # Skip note/source/total rows

        metadata = extract_row_metadata(row)
        row_year = metadata.get('year') or (int(row[year_col]) if year_col and pd.notna(row[year_col]) else None) or default_year

        if not row_year: # Skip if year cannot be determined
             logger.debug(f"Skipping row {idx+data_start_row} in sheet '{sheet_name}' due to missing year.")
             continue

        # Extract values based on standardized column names
        for col in data_df.columns:
            if col.startswith('value_'): # Standardized value columns
                metric_type_str = col.split('_', 1)[1] # e.g., number, crude_rate
                try:
                    metric_type = MetricType(metric_type_str.replace('_', '-')) # Convert to enum format
                    value = pd.to_numeric(row[col], errors='coerce')

                    if pd.notna(value):
                         # Determine sex - check if a sex column exists, otherwise check metadata
                         sex = row.get('sex', metadata.get('sex')) # Prioritize column if exists

                         records.append(AIHWRecord(
                             year=row_year, value=float(value), metric_type=metric_type,
                             source_sheet=sheet_name, sex=sex,
                             age_group=row.get('age_group', metadata.get('age_group')),
                             table_name=table_name, condition=extract_condition_from_table(table_name)
                         ))
                except (ValueError, TypeError) as e:
                     logger.warning(f"Sheet {sheet_name}, Row {idx+data_start_row}, Col {col}: Error processing value '{row[col]}'. Error: {e}")
                except KeyError as e:
                     logger.debug(f"Sheet {sheet_name}, Row {idx+data_start_row}: Missing expected column {e}")


    logger.info(f"Sheet {sheet_name}: Extracted {len(records)} records using standard processing.")
    return records

# --- Helper functions remain largely the same, ensure they are robust ---

def find_tables_in_sheet(df: pd.DataFrame) -> List[Dict]:
    """Find tables within a sheet based on headers and content."""
    # (Keep existing robust logic, ensure it handles edge cases)
    tables = []
    current_table = None
    in_table = False

    for i, row in df.iterrows():
        row_text = ' '.join(str(x).strip() for x in row if pd.notna(x))
        is_note_or_source = any(str(x).lower().strip().startswith(('note', 'source')) for x in row if pd.notna(x))
        is_empty = row.isna().all()

        # Potential start of a table (Look for 'Table' or common header words)
        if not in_table and not is_empty and not is_note_or_source and ('Table' in row_text or any(kw in row_text.lower() for kw in ['year', 'rate', 'number', 'prevalence'])):
            if current_table: # End previous table if we hit a new potential header
                 current_table['end_row'] = i
                 tables.append(current_table)

            current_table = {
                'start_row': i,
                'title': extract_table_name(df.iloc[i:], f"Sheet_{i}"), # Try to get title from here
                'end_row': None,
                'is_time_series': any(x in row_text.lower() for x in ['year', 'period'])
            }
            in_table = True
            logger.debug(f"Potential table start at row {i}, Title: {current_table['title']}")

        # Potential end of a table
        elif in_table and (is_empty or is_note_or_source):
            if current_table:
                current_table['end_row'] = i
                tables.append(current_table)
                logger.debug(f"Table ended at row {i}")
            current_table = None
            in_table = False

    # Add the last table if the sheet ends while in a table
    if current_table:
        current_table['end_row'] = len(df)
        tables.append(current_table)
        logger.debug(f"Final table ended at end of sheet (row {len(df)})")

    # Filter and potentially merge tables (Keep existing logic)
    filtered_tables = []
    # ... (rest of the filtering/merging logic) ...
    return tables # Return potentially overlapping tables for now, let process_sheet handle extraction


def extract_row_metadata(row: pd.Series) -> Dict:
    """Extract metadata from a row including sex, age group, and year."""
    metadata = {}
    # Prioritize columns named 'sex', 'age_group', 'year' if they exist
    if 'sex' in row.index and pd.notna(row['sex']):
        metadata['sex'] = str(row['sex']).strip().lower()
    if 'age_group' in row.index and pd.notna(row['age_group']):
         metadata['age_group'] = str(row['age_group']).strip().lower()
    if 'year' in row.index and pd.notna(row['year']):
         year = extract_year(row['year'])
         if year: metadata['year'] = year

    # Fallback: check other columns for keywords if primary columns missing/empty
    for col, val in row.items():
        if pd.isna(val): continue
        val_str = str(val).strip().lower()
        col_str = str(col).strip().lower()

        if 'sex' not in metadata and val_str in ['m', 'men', 'male', 'males', 'women', 'f', 'female', 'females', 'p', 'person', 'persons', 'people', 'all']:
             metadata['sex'] = val_str
        elif 'age_group' not in metadata and re.match(r'\d+[-–]\d+|\d+\+|total|all ages', val_str):
             metadata['age_group'] = val_str
        elif 'year' not in metadata: # Only look for year if not already found
             year = extract_year(val_str)
             if year: metadata['year'] = year

    # Standardize extracted values
    if 'sex' in metadata:
        s = metadata['sex']
        if s in ['m', 'male', 'males', 'men']: metadata['sex'] = 'male'
        elif s in ['f', 'female', 'females', 'women']: metadata['sex'] = 'female'
        elif s in ['p', 'person', 'persons', 'people', 'all']: metadata['sex'] = 'persons'
    if 'age_group' in metadata:
        ag = metadata['age_group']
        if ag == 'total': metadata['age_group'] = 'all_ages'
        metadata['age_group'] = ag.replace(' ', '').replace('–', '-')

    return metadata


def determine_metric_type(column_name: str, value: float) -> MetricType:
    """Determine the metric type based on column name and value."""
    col_lower = str(column_name).lower().strip() # Ensure it's string and lower

    # Check for specific keywords in column name
    if 'standardised_rate' in col_lower or 'standardized_rate' in col_lower or 'asmr' in col_lower:
        return MetricType.STANDARDISED_RATE
    if 'crude_rate' in col_lower:
        return MetricType.CRUDE_RATE
    if 'rate' in col_lower: # General rate if not crude/standardised
        return MetricType.RATE
    if 'percent' in col_lower or '%' in col_lower or 'proportion' in col_lower:
         # Check value range for percentage/proportion
         if 0 <= value <= 100:
             return MetricType.PERCENTAGE
         else: # If value is > 100, it's likely a number despite the name
              logger.debug(f"Column '{column_name}' suggests percentage/proportion but value {value} is outside 0-100. Treating as NUMBER.")
              return MetricType.NUMBER
    if 'number' in col_lower or 'deaths' in col_lower or 'count' in col_lower or 'prevalence_number' in col_lower:
        return MetricType.NUMBER

    # Default guess based on value range if name is ambiguous
    if 0 <= value <= 1:
        # Could be a rate (per 1) or proportion, default to RATE for now
        # Or could be a very small number. Hard to tell without context.
        logger.debug(f"Ambiguous metric type for column '{column_name}', value {value}. Defaulting to RATE.")
        return MetricType.RATE
    if 1 < value <= 100 and isinstance(value, float) and not value.is_integer():
        # Could be percentage or rate per 100. Defaulting to PERCENTAGE.
         logger.debug(f"Ambiguous metric type for column '{column_name}', value {value}. Defaulting to PERCENTAGE.")
         return MetricType.PERCENTAGE

    # Default to NUMBER if no other clues
    logger.debug(f"Ambiguous metric type for column '{column_name}', value {value}. Defaulting to NUMBER.")
    return MetricType.NUMBER


def extract_year_from_table(df: pd.DataFrame, table_name: str) -> Optional[int]:
    """Extract year from table name or data."""
    # Try table name first
    year = extract_year(table_name)
    if year: return year

    # Try column names
    for col in df.columns:
        year = extract_year(str(col))
        if year: return year

    # Try first few rows of data
    for i in range(min(5, len(df))):
        for cell in df.iloc[i]:
            year = extract_year(cell)
            if year: return year

    return None


def extract_condition_from_table(table_name: str) -> str:
    """Extract the health condition from the table name."""
    # Remove table number if present
    cleaned_name = re.sub(r'Table [A-Z0-9.]+[:\s]*', '', table_name, flags=re.IGNORECASE).strip()
    # Remove year ranges/specific years
    cleaned_name = re.sub(r'\s*\b(?:19|20)\d{2}(?:[-–](?:19|20)?\d{2})?\b', '', cleaned_name).strip()
    # Remove parenthetical content
    cleaned_name = re.sub(r'\s*\([^)]*\)', '', cleaned_name).strip()
    # Remove trailing prepositions like 'in Australia', 'by sex', 'by age'
    cleaned_name = re.sub(r'\s*\b(in|by|among|over)\b.*$', '', cleaned_name, flags=re.IGNORECASE).strip()
    # Specific known conditions
    if 'dementia' in cleaned_name.lower(): return 'Dementia'
    if 'alzheimer' in cleaned_name.lower(): return "Alzheimer's Disease"
    if 'cardiovascular' in cleaned_name.lower() or 'cvd' in cleaned_name.lower(): return 'Cardiovascular Disease'
    if 'coronary heart disease' in cleaned_name.lower() or 'chd' in cleaned_name.lower(): return 'Coronary Heart Disease'
    if 'stroke' in cleaned_name.lower(): return 'Stroke'
    # Fallback to the cleaned name
    return cleaned_name.strip().rstrip(',') or "Unknown Condition"


def process_aihw_excel(file_path: str, output_path: str) -> Optional[AIHWDataset]:
    """
    Process an AIHW Excel file into a standardised dataset and save to CSV.

    Args:
        file_path: Path to input Excel file
        output_path: Path to save processed CSV file
    """
    logger.info(f"Processing {Path(file_path).name}")

    try:
        xl = pd.ExcelFile(file_path)
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return None
    except Exception as e:
        logger.error(f"Error opening Excel file {file_path}: {e}")
        return None

    sheets = [s for s in xl.sheet_names if s not in SHEETS_TO_EXCLUDE]
    logger.info(f"Found {len(sheets)} potential data sheets: {sheets}")

    all_records = []

    # Process each sheet
    for sheet in sheets:
        try:
            logger.info(f"Loading sheet: '{sheet}'")
            df = pd.read_excel(file_path, sheet_name=sheet, header=None)

            if df.empty or df.isna().all().all():
                logger.info(f"Sheet '{sheet}' is empty or all NaN. Skipping.")
                continue

            logger.info(f"Processing sheet '{sheet}'. Shape: {df.shape}")
            records = process_sheet(df, sheet, Path(file_path).name)
            if records:
                logger.info(f"Extracted {len(records)} records from sheet '{sheet}'")
                all_records.extend(records)
            else:
                logger.warning(f"No records extracted from sheet '{sheet}'")

        except Exception as e:
            logger.error(f"Error processing sheet {sheet}: {e}", exc_info=True) # Log traceback
            continue

    if not all_records:
        logger.error("No records were extracted from any sheet.")
        # Still create the dataset object, but with empty records
        return AIHWDataset(records=[], source_file=Path(file_path).name, processed_date=datetime.now())


    # Convert records to DataFrame for final cleaning and saving
    records_data = []
    valid_records_count = 0
    invalid_records_count = 0
    for record in all_records:
        try:
            # Re-validate before dumping (optional but good practice)
            validated_record = AIHWRecord(**record.model_dump())
            records_data.append(validated_record.model_dump())
            valid_records_count += 1
        except Exception as e:
            logger.warning(f"Final validation failed for record: {record.model_dump()}. Error: {e}")
            invalid_records_count += 1
            continue

    logger.info(f"Final validation: {valid_records_count} valid, {invalid_records_count} invalid records.")

    if not records_data:
         logger.error("No valid records remained after final validation.")
         return AIHWDataset(records=[], source_file=Path(file_path).name, processed_date=datetime.now())


    df_final = pd.DataFrame(records_data)

    # Final cleanup
    if not df_final.empty:
        # Drop columns that might have been added but are usually empty/not needed
        cols_to_drop = ['region', 'indigenous_status', 'notes']
        df_final = df_final.drop(columns=[col for col in cols_to_drop if col in df_final.columns], errors='ignore')

        # Filter by valid year range (1980-2022) - Allow older years for CVD
        if 'year' in df_final.columns:
            original_count = len(df_final)
            df_final = df_final[(df_final['year'] >= 1980) & (df_final['year'] <= 2022)]
            filtered_count = original_count - len(df_final)
            if filtered_count > 0:
                logger.info(f"Filtered out {filtered_count} records with years outside 1980-2022 range.")

        # Sort for consistency
        sort_cols = ['year', 'source_sheet', 'condition', 'sex', 'age_group']
        sort_cols = [col for col in sort_cols if col in df_final.columns]
        if sort_cols:
            df_final = df_final.sort_values(by=sort_cols).reset_index(drop=True)

        # Drop exact duplicate rows
        initial_rows = len(df_final)
        df_final = df_final.drop_duplicates()
        dropped_duplicates = initial_rows - len(df_final)
        if dropped_duplicates > 0:
            logger.info(f"Removed {dropped_duplicates} duplicate records.")

        # Save to CSV
        try:
            df_final.to_csv(output_path, index=False)
            logger.info(f"Saved {len(df_final)} processed records to {output_path}")
            logger.info(f"Final DataFrame shape: {df_final.shape}")
            logger.info(f"Final Columns: {', '.join(df_final.columns)}")
        except Exception as e:
            logger.error(f"Failed to save processed data to {output_path}: {e}")
            return None # Indicate failure

    else:
        logger.error("DataFrame became empty after final processing steps.")
        # Optionally save an empty file or handle as needed
        # pd.DataFrame().to_csv(output_path, index=False)
        return None

    # Return the Pydantic Dataset object
    # Recreate records from the final cleaned DataFrame
    final_records_data = df_final.to_dict('records')
    return AIHWDataset(
        records=[AIHWRecord(**r) for r in final_records_data],
        source_file=Path(file_path).name,
        processed_date=datetime.now()
    )


def process_all_aihw_files(raw_dir, processed_dir):
    """Process all AIHW Excel files in the raw directory."""
    results = {}

    # Define file mappings using the new standardized names
    file_mappings = {
        'AIHW-DEM-02-S2-Prevalence.xlsx': 'aihw_dementia_prevalence_australia_processed.csv',
        'AIHW-DEM-02-S3-Mortality-202409.xlsx': 'aihw_dementia_mortality_australia_processed.csv',
        'AIHW-CVD-92-HSVD-facts-data-tables-12122024.xlsx': 'aihw_cvd_metrics_australia_processed.csv'
    }

    processed_dir_path = Path(processed_dir)
    processed_dir_path.mkdir(parents=True, exist_ok=True) # Ensure dir exists

    for excel_file, csv_file in file_mappings.items():
        input_path = Path(raw_dir) / excel_file
        output_path = processed_dir_path / csv_file

        if input_path.exists():
            try:
                # The process_aihw_excel function now handles sheet selection internally
                dataset_obj = process_aihw_excel(str(input_path), str(output_path))
                if dataset_obj and dataset_obj.records:
                    # Convert back to DataFrame for results dict (optional)
                    results[csv_file] = pd.DataFrame([r.model_dump() for r in dataset_obj.records])
                    logger.info(f"Successfully processed and saved {excel_file} to {csv_file}")
                elif dataset_obj:
                     logger.warning(f"Processed {excel_file}, but no valid records were extracted or saved.")
                else:
                     logger.error(f"Processing failed for {excel_file}.")

            except Exception as e:
                logger.error(f"Unhandled error processing {excel_file}: {e}", exc_info=True)
                continue
        else:
            logger.warning(f"AIHW input file not found: {input_path}")

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


Step 2: Add Debugging in health_outcome_metrics.py

"""
Extract standardized health outcome metrics from various processed data sources.
Merges NCD-RisC and specific AIHW metrics into a single yearly dataset.
"""

import pandas as pd
from pathlib import Path
import logging
from typing import Dict, List, Optional

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define base paths
PROCESSED_DATA_DIR = Path("data/processed")

def load_and_validate_csv(file_path: Path, required_cols: Optional[List[str]] = None) -> Optional[pd.DataFrame]:
    """Loads a CSV file and performs basic validation."""
    if not file_path.exists():
        logger.warning(f"File not found: {file_path}")
        return None
    try:
        df = pd.read_csv(file_path)
        if df.empty:
            logger.warning(f"File is empty: {file_path}")
            return None
        if required_cols:
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                logger.error(f"Missing required columns in {file_path}: {missing_cols}")
                return None
        logger.info(f"Loaded {file_path.name}: {df.shape[0]} rows, {df.shape[1]} columns")
        return df
    except Exception as e:
        logger.error(f"Error loading {file_path}: {e}")
        return None

def extract_ncd_risc_metrics() -> Optional[pd.DataFrame]:
    """Extracts and standardizes metrics from NCD-RisC files."""
    logger.info("Processing NCD-RisC data...")
    diabetes_df = load_and_validate_csv(PROCESSED_DATA_DIR / 'ncdrisc_diabetes_australia_processed.csv', ['year', 'sex', 'age-standardised_prevalence_of_diabetes_18+_years_', 'age-standardised_proportion_of_people_with_diabetes_who_were_treated_30+_years_'])
    bmi_df = load_and_validate_csv(PROCESSED_DATA_DIR / 'ncdrisc_bmi_australia_processed.csv', ['year', 'sex', 'prevalence_of_bmi>=30_kg_m²_obesity_'])
    cholesterol_df = load_and_validate_csv(PROCESSED_DATA_DIR / 'ncdrisc_cholesterol_australia_processed.csv', ['year', 'sex', 'mean_total_cholesterol_mmol_l_', 'mean_non-hdl_cholesterol_mmol_l_'])

    metrics_list = []

    # Diabetes
    if diabetes_df is not None:
        # Create separate pivot tables for prevalence and treatment rate
        diabetes_prev_pivot = diabetes_df.pivot_table(
            index='year',
            columns='sex',
            values='age-standardised_prevalence_of_diabetes_18+_years_'
        ).reset_index()

        diabetes_treat_pivot = diabetes_df.pivot_table(
            index='year',
            columns='sex',
            values='age-standardised_proportion_of_people_with_diabetes_who_were_treated_30+_years_'
        ).reset_index()

        # Calculate prevalence rate
        if 'Men' in diabetes_prev_pivot.columns and 'Women' in diabetes_prev_pivot.columns:
            diabetes_prev_pivot['Diabetes_Prevalence_Rate_AgeStandardised'] = diabetes_prev_pivot[['Men', 'Women']].mean(axis=1) * 100  # Convert to percentage
            logger.info("Successfully calculated diabetes prevalence rate")
        else:
            logger.warning("Could not find 'Men' and 'Women' columns in diabetes prevalence data for averaging.")
            logger.info(f"Available columns in diabetes_prev_pivot: {diabetes_prev_pivot.columns.tolist()}")

        # Calculate treatment rate
        if 'Men' in diabetes_treat_pivot.columns and 'Women' in diabetes_treat_pivot.columns:
            diabetes_treat_pivot['Diabetes_Treatment_Rate_AgeStandardised'] = diabetes_treat_pivot[['Men', 'Women']].mean(axis=1) * 100  # Convert to percentage
            logger.info("Successfully calculated diabetes treatment rate")
        else:
            logger.warning("Could not find 'Men' and 'Women' columns in diabetes treatment data for averaging.")
            logger.info(f"Available columns in diabetes_treat_pivot: {diabetes_treat_pivot.columns.tolist()}")

            # Alternative approach: if columns exist but have different case or formatting
            men_col = next((col for col in diabetes_treat_pivot.columns if 'men' in col.lower()), None)
            women_col = next((col for col in diabetes_treat_pivot.columns if 'women' in col.lower()), None)

            if men_col and women_col:
                logger.info(f"Found alternative columns: {men_col} and {women_col}")
                diabetes_treat_pivot['Diabetes_Treatment_Rate_AgeStandardised'] = diabetes_treat_pivot[[men_col, women_col]].mean(axis=1) * 100  # Convert to percentage
                logger.info("Successfully calculated diabetes treatment rate using alternative columns")
            elif len(diabetes_treat_pivot.columns) > 1:  # At least one data column plus 'year'
                # Get all non-year columns and average them
                data_cols = [col for col in diabetes_treat_pivot.columns if col != 'year']
                if data_cols:
                    logger.info(f"Using all available data columns: {data_cols}")
                    diabetes_treat_pivot['Diabetes_Treatment_Rate_AgeStandardised'] = diabetes_treat_pivot[data_cols].mean(axis=1) * 100
                    logger.info("Successfully calculated diabetes treatment rate by averaging all available data")

        # Merge prevalence and treatment rates
        diabetes_metrics = pd.DataFrame({
            'Year': diabetes_prev_pivot['year'],
            'Diabetes_Prevalence_Rate_AgeStandardised': diabetes_prev_pivot.get('Diabetes_Prevalence_Rate_AgeStandardised', None),
            'Diabetes_Treatment_Rate_AgeStandardised': diabetes_treat_pivot.get('Diabetes_Treatment_Rate_AgeStandardised', None)
        })
        metrics_list.append(diabetes_metrics)
        logger.info(f"Processed diabetes metrics. Shape: {diabetes_metrics.shape}")
    else:
        logger.warning("Could not process diabetes data.")

    # BMI/Obesity
    if bmi_df is not None:
        bmi_pivot = bmi_df.pivot_table(
            index='year',
            columns='sex',
            values='prevalence_of_bmi>=30_kg_m²_obesity_'
        ).reset_index()
        if 'Men' in bmi_pivot.columns and 'Women' in bmi_pivot.columns:
            bmi_pivot['Obesity_Prevalence_AgeStandardised'] = bmi_pivot[['Men', 'Women']].mean(axis=1) * 100 # Convert to percentage
            metrics_list.append(bmi_pivot[['year', 'Obesity_Prevalence_AgeStandardised']].rename(columns={'year': 'Year'}))
        else:
            logger.warning("Could not find 'Men' and 'Women' columns in BMI data for averaging.")

    # Cholesterol
    if cholesterol_df is not None:
        chol_pivot_total = cholesterol_df.pivot_table(
            index='year',
            columns='sex',
            values='mean_total_cholesterol_mmol_l_'
        ).reset_index()
        chol_pivot_nonhdl = cholesterol_df.pivot_table(
            index='year',
            columns='sex',
            values='mean_non-hdl_cholesterol_mmol_l_'
        ).reset_index()

        chol_metrics = pd.DataFrame({'Year': chol_pivot_total['year']})
        if 'Men' in chol_pivot_total.columns and 'Women' in chol_pivot_total.columns:
            chol_metrics['Total_Cholesterol_AgeStandardised'] = chol_pivot_total[['Men', 'Women']].mean(axis=1)
        if 'Men' in chol_pivot_nonhdl.columns and 'Women' in chol_pivot_nonhdl.columns:
            chol_metrics['NonHDL_Cholesterol_AgeStandardised'] = chol_pivot_nonhdl[['Men', 'Women']].mean(axis=1)

        metrics_list.append(chol_metrics)

    # Merge NCD-RisC metrics
    if not metrics_list:
        logger.warning("No NCD-RisC metrics could be processed.")
        return None

    ncd_merged_df = metrics_list[0]
    for df in metrics_list[1:]:
        ncd_merged_df = pd.merge(ncd_merged_df, df, on='Year', how='outer')

    logger.info(f"Processed NCD-RisC metrics. Shape: {ncd_merged_df.shape}")
    return ncd_merged_df

def extract_aihw_metrics() -> Optional[pd.DataFrame]:
    """Extracts and standardizes metrics from processed AIHW files."""
    logger.info("Processing AIHW data...")
    all_aihw_metrics = []

    # Dementia Prevalence (Number) - From S2.4
    prev_df = load_and_validate_csv(PROCESSED_DATA_DIR / 'aihw_dementia_prevalence_australia_processed.csv', ['year', 'value', 'source_sheet', 'sex'])
    if prev_df is not None:
        # --- Debugging Log ---
        logger.info(f"AIHW Dementia Prevalence - Unique source sheets: {prev_df['source_sheet'].unique()}")
        logger.info(f"AIHW Dementia Prevalence - Unique sex values: {prev_df['sex'].unique()}")
        # --- End Debugging Log ---
        # Filter specifically for sheet S2.4 and persons
        dementia_prev = prev_df[
            (prev_df['source_sheet'] == 'S2.4') &
            (prev_df['sex'] == 'persons') # Check if 'persons' is the correct value
        ].copy()
        # --- Debugging Log ---
        logger.info(f"AIHW Dementia Prevalence - Shape after filtering for S2.4 & persons: {dementia_prev.shape}")
        # --- End Debugging Log ---
        if not dementia_prev.empty:
            dementia_prev = dementia_prev[['year', 'value']].rename(columns={'year': 'Year', 'value': 'Dementia_Prevalence_Number'})
            # Ensure no duplicate years
            dementia_prev = dementia_prev.drop_duplicates(subset=['Year'], keep='first')
            all_aihw_metrics.append(dementia_prev)
            logger.info(f"Extracted Dementia Prevalence (Number): {dementia_prev.shape[0]} rows")
        else:
            logger.warning("No 'persons' data found in aihw_dementia_prevalence_australia_processed.csv from sheet S2.4.")

    # Dementia Mortality (Age-Standardised Rate) - From S3.5
    mort_df = load_and_validate_csv(PROCESSED_DATA_DIR / 'aihw_dementia_mortality_australia_processed.csv', ['year', 'value', 'source_sheet', 'metric_type', 'sex'])
    if mort_df is not None:
        # --- Debugging Log ---
        logger.info(f"AIHW Dementia Mortality - Unique source sheets: {mort_df['source_sheet'].unique()}")
        logger.info(f"AIHW Dementia Mortality - Unique metric types: {mort_df['metric_type'].unique()}")
        logger.info(f"AIHW Dementia Mortality - Unique sex values: {mort_df['sex'].unique()}")
        # --- End Debugging Log ---
        # Filter specifically for sheet S3.5, standardised rate, and persons
        dementia_mort = mort_df[
            (mort_df['source_sheet'] == 'S3.5') &
            (mort_df['metric_type'] == 'standardised_rate') &
            (mort_df['sex'] == 'persons') # Check if 'persons' is the correct value
        ].copy()
        # --- Debugging Log ---
        logger.info(f"AIHW Dementia Mortality - Shape after filtering for S3.5, standardised_rate & persons: {dementia_mort.shape}")
        # --- End Debugging Log ---
        if not dementia_mort.empty:
            dementia_mort = dementia_mort[['year', 'value']].rename(columns={'year': 'Year', 'value': 'Dementia_Mortality_Rate_ASMR'})
            dementia_mort = dementia_mort.drop_duplicates(subset=['Year'], keep='first')
            all_aihw_metrics.append(dementia_mort)
            logger.info(f"Extracted Dementia Mortality (ASMR): {dementia_mort.shape[0]} rows")
        else:
            logger.warning("No 'persons' standardised rate data found in aihw_dementia_mortality_australia_processed.csv from sheet S3.5.")


    # CVD Mortality (Age-Standardised Rate) - From Table 11 in aihw_cvd_metrics_australia_processed.csv
    cvd_df = load_and_validate_csv(PROCESSED_DATA_DIR / 'aihw_cvd_metrics_australia_processed.csv', ['year', 'value', 'source_sheet', 'metric_type', 'sex'])
    if cvd_df is not None:
        # --- Debugging Log ---
        logger.info(f"AIHW CVD Metrics - Unique source sheets: {cvd_df['source_sheet'].unique()}")
        logger.info(f"AIHW CVD Metrics - Unique metric types: {cvd_df['metric_type'].unique()}")
        logger.info(f"AIHW CVD Metrics - Unique sex values: {cvd_df['sex'].unique()}")
        # --- End Debugging Log ---
        # Filter specifically for Table 11, standardised rate, and persons
        cvd_mort = cvd_df[
            (cvd_df['source_sheet'] == 'Table 11') &
            (cvd_df['metric_type'] == 'standardised_rate') &
            (cvd_df['sex'] == 'persons') # Check if 'persons' is the correct value
        ].copy()
        # --- Debugging Log ---
        logger.info(f"AIHW CVD Metrics - Shape after filtering for Table 11, standardised_rate & persons: {cvd_mort.shape}")
        # --- End Debugging Log ---
        if not cvd_mort.empty:
            cvd_mort = cvd_mort[['year', 'value']].rename(columns={'year': 'Year', 'value': 'CVD_Mortality_Rate_ASMR'})
            cvd_mort = cvd_mort.drop_duplicates(subset=['Year'], keep='first')
            all_aihw_metrics.append(cvd_mort)
            logger.info(f"Extracted CVD Mortality (ASMR): {cvd_mort.shape[0]} rows")
        else:
             logger.warning("No 'persons' standardised rate data found in aihw_cvd_metrics_australia_processed.csv from Table 11.")


    # Merge AIHW metrics
    if not all_aihw_metrics:
        logger.warning("No AIHW metrics could be processed.")
        return None

    # Start with an empty DataFrame with 'Year' to ensure all years are covered
    if ncd_metrics is not None:
         all_years = pd.DataFrame({'Year': range(ncd_metrics['Year'].min(), ncd_metrics['Year'].max() + 1)})
    else:
         # Fallback if NCD metrics failed (less ideal)
         min_year = min(df['Year'].min() for df in all_aihw_metrics if not df.empty)
         max_year = max(df['Year'].max() for df in all_aihw_metrics if not df.empty)
         all_years = pd.DataFrame({'Year': range(min_year, max_year + 1)})

    aihw_merged_df = all_years
    for df in all_aihw_metrics:
        aihw_merged_df = pd.merge(aihw_merged_df, df, on='Year', how='left')

    logger.info(f"Processed AIHW metrics. Shape: {aihw_merged_df.shape}")
    return aihw_merged_df

def main():
    """
    Main function to extract and merge all health metrics.
    """
    logger.info("=== Calculating health outcome metrics ===") # Changed log message

    ncd_metrics = extract_ncd_risc_metrics()
    aihw_metrics = extract_aihw_metrics()

    # Merge NCD and AIHW metrics
    if ncd_metrics is not None and aihw_metrics is not None:
        # Use outer merge to keep all years from both datasets
        merged_health_df = pd.merge(ncd_metrics, aihw_metrics, on='Year', how='outer')
    elif ncd_metrics is not None:
        merged_health_df = ncd_metrics
    elif aihw_metrics is not None:
        merged_health_df = aihw_metrics
    else:
        logger.error("Failed to process any health metrics. Exiting.")
        return

    # Sort by year
    merged_health_df = merged_health_df.sort_values('Year').reset_index(drop=True)

    # Save the merged health metrics
    output_path = PROCESSED_DATA_DIR / 'health_metrics_australia_combined.csv'
    try:
        merged_health_df.to_csv(output_path, index=False)
        logger.info(f"Merged health metrics saved successfully to {output_path}")
    except Exception as e:
        logger.error(f"Failed to save merged health metrics: {e}")
        return

    # Log final summary
    logger.info(f"Final health metrics dataset shape: {merged_health_df.shape}")
    logger.info(f"Years covered: {merged_health_df['Year'].min()} to {merged_health_df['Year'].max()}")
    logger.info(f"Columns: {', '.join(merged_health_df.columns)}")

    # Log completeness
    logger.info("--- Health Metrics Completeness ---")
    for col in merged_health_df.columns:
        if col != 'Year':
            completeness = merged_health_df[col].notna().mean() * 100
            logger.info(f"{col}: {completeness:.1f}% complete")

if __name__ == "__main__":
    main()
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Python name=src/data_processing/health_outcome_metrics.py
IGNORE_WHEN_COPYING_END

Step 3: Re-run ETL and Verify

Action: Delete data/processed/*.

Action: Run python -m src.run_etl --force --no-download.

Action: Examine the logs. Specifically check:

The debug logs added in health_outcome_metrics.py should now show 'persons' in the unique sex values for the relevant dataframes.

The shape of dementia_prev and cvd_mort after filtering should be greater than 0.

The final completeness report should show > 0% for Dementia_Prevalence_Number and CVD_Mortality_Rate_ASMR.

Action: Check data/processed/analytical_data_australia_final.csv to confirm the columns are populated.

Let's see if these targeted fixes resolve the missing AIHW data.