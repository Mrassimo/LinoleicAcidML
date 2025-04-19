import logging
# DEBUG LOG: process_aihw_excel should always create an output file, even if empty, and write only headers if no data is present.
# Please confirm this is the intended behaviour before proceeding with code changes.
import logging
"""
logging.basicConfig(level=logging.INFO)
Process AIHW Excel files into standardised CSV format.

This module implements the sheet-by-sheet cleaning approach for AIHW Excel files,
ensuring proper header detection and data transformation before concatenation.
"""

import pandas as pd
import os
from typing import Dict, List, Optional, Tuple
import sys
from pathlib import Path
import numpy as np
import re
import argparse
from datetime import datetime
from enum import Enum

# Add the project root to the Python path
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

# Import models using absolute import
from src.models.aihw_models import AIHWRecord, AIHWDataset, MetricType

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
SHEETS_TO_EXCLUDE = {'Contents', 'Notes', 'Metadata', 'Index'}
TABLE_PATTERN = re.compile(r'(?:Table [A-Z0-9.]+:?\s*(.+?)(?:\s*\(|\s*$)|^[A-Z][a-z\s]+(?:and\s+[A-Z][a-z\s]+)*(?:\s+in\s+Australia)?(?:\s*\(|\s*$))')
YEAR_PATTERN = re.compile(r'(?:19|20)\d{2}(?:[-–]\d{2})?')

def transform_sheet_data(df: pd.DataFrame, sheet_name: str) -> pd.DataFrame:
    """
    Add a 'sex' column to the DataFrame for special sheets if missing.
    For sheets 'S2.4' and 'Table 11', assigns 'sex' as 'persons' if not present.
    This function is used for test purposes and ensures consistent handling
    of sex assignment in special cases, following Australian English conventions.
    """
    if 'sex' not in df.columns and sheet_name in ("S2.4", "Table 11"):
        df = df.copy()
        df['sex'] = 'persons'  # Use 'persons' as default for non-sex-split groups (Australian English standard)'.
    return df

def extract_table_name(df: pd.DataFrame, sheet_name: str) -> Optional[str]:
    """Extract the table name from the first few rows or use sheet name as fallback."""
    # First try to find a table title in the first few rows
    for i in range(min(10, len(df))):
        cell = str(df.iloc[i, 0])
        match = TABLE_PATTERN.search(cell)
        if match:
            title = match.group(1) if match.group(1) else cell
            # Remove date ranges and clean up
            title = re.sub(r'between \d{4} and \d{4}', '', title).strip()
            return title
    
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
            
        # Allow years from 1960 to present
        if 1960 <= year_value <= 2024:
            return year_value
        logger.warning(f"Year {year_value} outside valid range (1960-2024)")
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
    """
    Process a single sheet into AIHW records.

    This function is robust to both raw Excel-like DataFrames (with headers in the first column/row)
    and already-cleaned DataFrames (with proper column names and no header rows in the data).
    Special handling is provided for S2.4, S3.5, and Table 11 (CVD Mortality) sheets.
    All code and comments use Australian English.

    Args:
        df: The input DataFrame, either raw (as read from Excel) or already cleaned.
        sheet_name: The name of the sheet being processed.
        file_name: The name of the file being processed.

    Returns:
        List[AIHWRecord]: List of extracted records.
    """
    table_name = extract_table_name(df, sheet_name)
    logger.info(f"Processing Sheet: '{sheet_name}', Table: '{table_name}'")
    
    # Add debug logging for CVD data
    if "AIHW-CVD-92" in file_name:
        logger.debug(f"Processing CVD data from sheet {sheet_name}")
        logger.debug(f"DataFrame head:\n{df.head()}")
        logger.debug(f"DataFrame columns: {df.columns.tolist()}")
    
    records = []

    # --- Special Handling for Table 11 (CVD Mortality) ---
    if sheet_name == "All CVD" and "AIHW-CVD-92" in file_name:
        logger.info("Applying special handling for CVD Table 11")
        
        # Find Table 11
        table_start_idx = None
        for i in range(len(df)):
            if pd.notna(df.iloc[i, 0]) and "Table 11" in str(df.iloc[i, 0]):
                table_start_idx = i
                break
        
        if table_start_idx is not None:
            # Data starts 3 rows after table title (year, number headers, sex headers)
            data_start_idx = table_start_idx + 3
            
            # Process each row
            for idx in range(data_start_idx, len(df)):
                row = df.iloc[idx]
                
                # Stop if we hit empty row or notes
                if pd.isna(row[0]) or str(row[0]).lower().startswith('note'):
                    break
                
                try:
                    # Extract year
                    year = int(float(row[0]))
                    
                    # Process deaths (columns 1-3)
                    for col_idx, sex in [(1, "men"), (2, "women"), (3, "persons")]:
                        if pd.notna(row[col_idx]):
                            try:
                                value = float(str(row[col_idx]).replace(',', ''))
                                records.append(AIHWRecord(
                                    year=year,
                                    value=value,
                                    metric_type=MetricType.NUMBER,
                                    source_sheet="Table 11",
                                    sex=sex,
                                    age_group="all_ages",
                                    table_name="Cardiovascular disease deaths",
                                    condition="Cardiovascular Disease"
                                ))
                            except (ValueError, TypeError) as e:
                                logger.warning(f"Error converting deaths value in row {idx}, col {col_idx}: {e}")
                    
                    # Process age-standardised rates (columns 7-9)
                    for col_idx, sex in [(7, "men"), (8, "women"), (9, "persons")]:
                        if pd.notna(row[col_idx]):
                            try:
                                value = float(str(row[col_idx]).replace(',', ''))
                                records.append(AIHWRecord(
                                    year=year,
                                    value=value,
                                    metric_type=MetricType.STANDARDISED_RATE,
                                    source_sheet="Table 11",
                                    sex=sex,
                                    age_group="all_ages",
                                    table_name="Cardiovascular disease deaths",
                                    condition="Cardiovascular Disease"
                                ))
                            except (ValueError, TypeError) as e:
                                logger.warning(f"Error converting rate value in row {idx}, col {col_idx}: {e}")
                
                except Exception as e:
                    logger.warning(f"Error processing CVD row {idx}: {e}")
                    continue
            
            logger.info(f"Extracted {len(records)} CVD records from Table 11")
            return records

    # --- Special Handling for S2.4 (Dementia Prevalence) ---
    elif sheet_name == "S2.4" and "AIHW-DEM-02-S2-Prevalence" in file_name:
        logger.info("Applying special handling for Sheet S2.4")
        
        # Find data start (after headers)
        data_start = None
        for i in range(len(df)):
            if pd.notna(df.iloc[i, 0]) and str(df.iloc[i, 0]).strip().isdigit():
                data_start = i
                break
        
        if data_start is not None:
            # Process each row
            for idx in range(data_start, len(df)):
                row = df.iloc[idx]
                
                # Stop if we hit empty row
                if pd.isna(row[0]):
                    break
                
                try:
                    year = int(float(row[0]))
                    # Process men, women, persons (columns 1-3)
                    for col_idx, sex in [(1, "men"), (2, "women"), (3, "persons")]:
                        if pd.notna(row[col_idx]):
                            try:
                                value = float(str(row[col_idx]).replace(',', ''))
                                records.append(AIHWRecord(
                                    year=year,
                                    value=value,
                                    metric_type=MetricType.NUMBER,
                                    source_sheet="S2.4",
                                    sex=sex,
                                    age_group="all_ages",
                                    table_name="Australians living with dementia",
                                    condition="Dementia"
                                ))
                            except (ValueError, TypeError) as e:
                                logger.warning(f"Error converting value in row {idx}, col {col_idx}: {e}")
                
                except Exception as e:
                    logger.warning(f"Error processing dementia prevalence row {idx}: {e}")
                    continue
            
            logger.info(f"Extracted {len(records)} dementia prevalence records from S2.4")
            return records

    # --- Special Handling for S3.5 (Dementia Mortality) ---
    elif sheet_name == "S3.5" and "AIHW-DEM-02-S3-Mortality" in file_name:
        logger.info("Applying special handling for Sheet S3.5")
        
        # Find data start (after headers)
        data_start = None
        for i in range(len(df)):
            if pd.notna(df.iloc[i, 0]) and str(df.iloc[i, 0]).strip().isdigit():
                data_start = i
                break
        
        if data_start is not None:
            # Get column headers from row before data
            headers = df.iloc[data_start-1]
            
            # Process each row
            for idx in range(data_start, len(df)):
                row = df.iloc[idx]
                
                # Stop if we hit empty row
                if pd.isna(row[0]):
                    break
                
                try:
                    year = int(float(row[0]))
                    # Process each type of dementia (columns 4-6)
                    for col_idx in range(4, 7):
                        if pd.notna(row[col_idx]) and pd.notna(headers[col_idx]):
                            try:
                                value = float(str(row[col_idx]).replace(',', ''))
                                dementia_type = str(headers[col_idx]).strip()
                                records.append(AIHWRecord(
                                    year=year,
                                    value=value,
                                    metric_type=MetricType.STANDARDISED_RATE,
                                    source_sheet="S3.5",
                                    sex="persons",
                                    age_group="all_ages",
                                    table_name="Deaths due to dementia",
                                    condition=dementia_type
                                ))
                            except (ValueError, TypeError) as e:
                                logger.warning(f"Error converting value in row {idx}, col {col_idx}: {e}")
                
                except Exception as e:
                    logger.warning(f"Error processing dementia mortality row {idx}: {e}")
                    continue
            
            logger.info(f"Extracted {len(records)} dementia mortality records from S3.5")
            return records

    # --- Standard Processing Logic (Fallback) ---
    logger.info(f"Applying standard processing for Sheet: '{sheet_name}'")
    header_row_idx, col_map = find_header_row(df)

    if header_row_idx is None:
        logger.warning(
            f"Could not determine header row for sheet '{sheet_name}'. Skipping standard processing."
        )
        return records

    data_start_row = header_row_idx + 1
    data_df = df.iloc[data_start_row:].copy()
    data_df.columns = [
        standardize_column_name(col_map.get(i, f"unnamed_{i}"))
        for i in range(len(data_df.columns))
    ]

    year_col = next((col for col in data_df.columns if "year" in col), None)
    default_year = extract_year_from_table(data_df, table_name)

    for idx, row in data_df.iterrows():
        if row.isna().all() or (
            pd.notna(row.iloc[0])
            and str(row.iloc[0]).lower().startswith(("note", "source", "total"))
        ):
            continue

        metadata = extract_row_metadata(row)
        row_year = (
            metadata.get("year")
            or (int(row[year_col]) if year_col and pd.notna(row[year_col]) else None)
            or default_year
        )

        if not row_year:
            logger.debug(
                f"Skipping row {idx+data_start_row} in sheet '{sheet_name}' due to missing year."
            )
            continue

        for col in data_df.columns:
            if col.startswith("value_"):
                metric_type_str = col.split("_", 1)[1]
                try:
                    metric_type = MetricType(metric_type_str.replace("_", "-"))
                    value = pd.to_numeric(row[col], errors="coerce")

                    if pd.notna(value):
                        sex = row.get("sex", metadata.get("sex"))

                        records.append(
                            AIHWRecord(
                                year=row_year,
                                value=float(value),
                                metric_type=metric_type,
                                source_sheet=sheet_name,
                                sex=sex,
                                age_group=row.get(
                                    "age_group", metadata.get("age_group")
                                ),
                                table_name=table_name,
                                condition=extract_condition_from_table(table_name),
                            )
                        )
                except (ValueError, TypeError) as e:
                    logger.warning(
                        f"Sheet {sheet_name}, Row {idx+data_start_row}, Col {col}: Error processing value '{row[col]}'. Error: {e}"
                    )
                except KeyError as e:
                    logger.debug(
                        f"Sheet {sheet_name}, Row {idx+data_start_row}: Missing expected column {e}"
                    )

    logger.info(
        f"Sheet {sheet_name}: Extracted {len(records)} records using standard processing."
    )
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

def parse_age_group(label: str) -> str:
    """
    Parse and normalise an age group label, handling non-integer ranges, composite groups, and non-standard dashes.

    Args:
        label (str): The raw age group label.

    Returns:
        str: The canonicalised age group label, or None if unparseable.

    Notes:
        - Normalises all dash types to standard hyphen.
        - Accepts non-integer ranges (e.g., "65.5–70", "0–4/5–9", "65+").
        - Handles composite groups (e.g., "0–4/5–9", "65+ and over").
        - Logs a warning if parsing fails.
    """
    import re

    if not isinstance(label, str):
        return None

    # Normalise dashes to standard hyphen
    label = label.replace("–", "-").replace("—", "-").replace("−", "-")
    label = label.strip().lower()

    # Remove common extraneous text
    label = re.sub(r"\band over\b|\byears?\b|\byr\b|\byrs\b", "", label)
    label = label.replace("  ", " ").strip()

    # Accept "all ages" or "total"
    if label in {"all ages", "total"}:
        return label

    # Accept single group (e.g., "65+")
    if re.match(r"^\d+(\.\d+)?\+$", label):
        return label

    # Accept range (e.g., "0-4", "65.5-70")
    if re.match(r"^\d+(\.\d+)?-\d+(\.\d+)?$", label):
        return label

    # Accept composite groups separated by "/" or ","
    if "/" in label or "," in label:
        parts = re.split(r"[/,]", label)
        parsed_parts = [parse_age_group(part.strip()) for part in parts]
        if all(parsed_parts):
            return "/".join(parsed_parts)
        else:
            logger.warning(f"Failed to parse composite age group: '{label}'")
            return None

    # Accept "65+ and over" as "65+"
    if re.match(r"^\d+(\.\d+)?\+\s*and\s*over$", label):
        return re.match(r"^(\d+(\.\d+)?\+)", label).group(1)

    logger.warning(f"Unrecognised age group label: '{label}'")
    return None

def extract_row_metadata(row: pd.Series) -> Dict:
    """
    Extract metadata from a row including sex, age group, and year.

    This version uses robust age group parsing and context-aware year validation.
    Logs warnings for any parsing failures but does not halt processing.

    Args:
        row (pd.Series): The row to extract metadata from.

    Returns:
        Dict: Metadata dictionary with possible keys: 'sex', 'age_group', 'year'.
    """
    metadata = {}

    for col, val in row.items():
        try:
            if pd.isna(val):
                continue
            val_str = str(val).strip().lower()
            col_str = str(col).strip().lower()

            # Skip numeric values that aren't actually years
            if isinstance(val, (int, float)) or val_str.replace('.', '', 1).isdigit():
                try:
                    numeric_value = float(val)
                    if numeric_value > 3000:
                        continue
                except Exception:
                    pass
        except Exception:
            continue

        # Check if column name indicates a year column
        if 'year' in col_str:
            try:
                year_match = re.search(r'(?:19|20)\d{2}', val_str)
                if year_match:
                    year_value = int(year_match.group())
                    # Allow years from 1960 to 2060 (context-aware, see below)
                    if 1960 <= year_value <= 2060:
                        metadata['year'] = year_value
                    else:
                        logger.warning(f"Year {year_value} outside valid range (1960-2060) in column '{col_str}'")
                    continue
            except (ValueError, TypeError):
                pass

        # Extract sex
        if val_str in ['m', 'men', 'male', 'males', 'women', 'f', 'female', 'females', 'p', 'person', 'persons', 'people']:
            metadata['sex'] = val_str

        # Extract age group using robust parser
        parsed_age_group = parse_age_group(val_str)
        if parsed_age_group:
            metadata['age_group'] = parsed_age_group

        # Extract year if present in a value
        elif re.match(r'(?:19|20)\d{2}(?:[-–]\d{2})?', val_str):
            try:
                year_value = int(val_str[:4])
                if 1960 <= year_value <= 2060:
                    metadata['year'] = year_value
                else:
                    logger.warning(f"Year {year_value} outside valid range (1960-2060) in value '{val_str}'")
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
        logger.warning("No records were extracted from any sheet. Writing empty output file with headers.")
        # Define the expected columns for the output CSV
        expected_columns = ['year', 'source_sheet', 'sex', 'age_group', 'metric', 'value', 'unit', 'condition', 'source_table']
        empty_df = pd.DataFrame(columns=expected_columns)
        empty_df.to_csv(output_path, index=False)
        logger.info(f"Saved empty output file with headers to {output_path}")
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
        'AIHW-DEM-02-S2-Prevalence.xlsx': 'aihw_dementia_prevalence_australia_processed.csv',
        'AIHW-DEM-02-S3-Mortality-202409.xlsx': 'aihw_dementia_mortality_australia_processed.csv',
        'AIHW-CVD-92-HSVD-facts-data-tables-12122024.xlsx': 'aihw_cvd_metrics_australia_processed.csv'
    }
    
    for excel_file, csv_file in file_mappings.items():
        input_path = os.path.join(raw_dir, excel_file)
        output_path = os.path.join(processed_dir, csv_file)
        
        if os.path.exists(input_path):
            try:
                # Handle specific sheets based on the file
                if 'S2-Prevalence' in excel_file:
                    logger.info(f"Processing only sheet S2.4 from {excel_file}")
                    # Read only sheet S2.4 (dementia prevalence by year)
                    df = pd.read_excel(input_path, sheet_name='S2.4', header=None)
                    
                    # Custom handling for S2.4 which has a specific structure
                    # The sheet has years in rows and separate columns for men/women/persons
                    records = []
                    
                    # Find where the actual data begins by looking for the header row
                    header_row = None
                    for i in range(min(15, len(df))):
                        if pd.notna(df.iloc[i, 0]) and ("Year" in str(df.iloc[i, 0]) or "year" in str(df.iloc[i, 0]).lower()):
                            header_row = i
                            break
                    
                    if header_row is not None:
                        logger.info(f"Found header row at row {header_row}")
                        # Skip the header row and get data rows
                        data_rows = df.iloc[header_row+1:].reset_index(drop=True)
                        
                        # Keep only rows that have a year in the first column
                        valid_rows = []
                        for idx, row in data_rows.iterrows():
                            if pd.notna(row.iloc[0]):
                                try:
                                    # Try to extract a year from the first column
                                    year_val = row.iloc[0]
                                    # Handle both integer and float years
                                    if isinstance(year_val, (int, float)):
                                        year_int = int(year_val)
                                        if 1980 <= year_int <= 2060:  # Allow projections to 2060
                                            valid_rows.append(row)
                                    else:
                                        year_str = str(year_val).strip()
                                        # Handle possible float strings like "2010.0"
                                        if '.' in year_str:
                                            year_str = year_str.split('.')[0]
                                        if year_str.isdigit() and 1980 <= int(year_str) <= 2060:
                                            valid_rows.append(row)
                                except Exception as e:
                                    logger.debug(f"Error parsing year in S2.4 row {idx}: {e}")
                                    continue
                        
                        if valid_rows:
                            # Create a DataFrame from valid rows
                            valid_df = pd.DataFrame(valid_rows).reset_index(drop=True)
                            
                            # Process each valid row
                            for idx, row in valid_df.iterrows():
                                # Handle both integer and float years
                                year_val = row.iloc[0]
                                if isinstance(year_val, (int, float)):
                                    year = int(year_val)
                                else:
                                    year_str = str(year_val).strip()
                                    if '.' in year_str:
                                        year_str = year_str.split('.')[0]
                                    year = int(year_str)
                                
                                # Create records for men (col 1), women (col 2), persons (col 3)
                                for col_idx, sex in [(1, "men"), (2, "women"), (3, "persons")]:
                                    if col_idx < len(row) and pd.notna(row.iloc[col_idx]):
                                        try:
                                            value = float(row.iloc[col_idx])
                                            records.append(AIHWRecord(
                                                year=year,
                                                value=value,
                                                metric_type=MetricType.NUMBER,
                                                source_sheet="S2.4",
                                                sex=sex,
                                                age_group=None,
                                                table_name="Australians living with dementia",
                                                condition="Dementia"
                                            ))
                                        except:
                                            continue
                                            
                            logger.info(f"Extracted {len(records)} prevalence records from sheet S2.4")
                    else:
                        logger.warning("Could not locate header row in sheet S2.4")
                    
                    # Convert records to DataFrame
                    records_data = []
                    for record in records:
                        record_dict = record.model_dump()
                        records_data.append(record_dict)
                    
                    if records_data:
                        df = pd.DataFrame(records_data)
                        # Clean up the DataFrame
                        columns_to_drop = ['region', 'indigenous_status', 'notes']
                        df = df.drop(columns=columns_to_drop, errors='ignore')
                        
                        # Sort by year and clean up
                        if 'year' in df.columns:
                            df = df.sort_values('year')
                        
                        df.to_csv(output_path, index=False)
                        logger.info(f"Successfully saved {len(df)} records to {csv_file}")
                        results[csv_file] = df
                    else:
                        logger.warning(f"No valid records found in sheet S2.4")

                elif 'S3-Mortality' in excel_file:
                    logger.info(f"Processing only sheet S3.5 from {excel_file}")
                    # Read only sheet S3.5 (dementia mortality data)
                    df = pd.read_excel(input_path, sheet_name='S3.5', header=None)
                    # Process only this sheet
                    records = process_sheet(df, 'S3.5', excel_file)
                    
                    # Convert records to DataFrame
                    records_data = []
                    for record in records:
                        record_dict = record.model_dump()
                        records_data.append(record_dict)
                    
                    if records_data:
                        df = pd.DataFrame(records_data)
                        # Clean up the DataFrame
                        columns_to_drop = ['region', 'indigenous_status', 'notes']
                        df = df.drop(columns=columns_to_drop, errors='ignore')
                        
                        # Sort by year and clean up
                        if 'year' in df.columns:
                            df = df.sort_values('year')
                        
                        df.to_csv(output_path, index=False)
                        logger.info(f"Successfully saved {len(df)} records to {csv_file}")
                        results[csv_file] = df
                    else:
                        logger.warning(f"No valid records found in sheet S3.5")
                
                elif 'CVD' in excel_file:
                    logger.info(f"Processing Table 11 (CVD mortality time series from 1980-2022) from {excel_file}")
                    
                    # Read the All CVD sheet
                    df = pd.read_excel(input_path, sheet_name='All CVD', header=None)
                    
                    # Special handling for CVD Table 11 (Cardiovascular disease deaths 1980-2022)
                    records = []
                    # Table 11 starts around row 229 in the Excel file
                    table_start = None
                    table_end = None
                    
                    # Find Table 11 by looking for its header row
                    for i in range(len(df)):
                        if pd.notna(df.iloc[i, 0]) and "Table 11" in str(df.iloc[i, 0]):
                            table_start = i
                            # Find where table ends (looking for empty rows or notes)
                            for j in range(i + 10, len(df)):  # Start at least 10 rows after table header
                                if pd.isna(df.iloc[j, 0]) or str(df.iloc[j, 0]).startswith("Note"):
                                    table_end = j
                                    break
                            break
                    
                    if table_start is not None and table_end is not None:
                        logger.info(f"Found Table 11 from rows {table_start} to {table_end}")
                        # Extract the table data (skip header rows - years start 2-3 rows after table title)
                        data_start = table_start + 3  # Adjust based on the actual structure
                        table_data = df.iloc[data_start:table_end].reset_index(drop=True)
                        
                        # Process each row in the table
                        for idx, row in table_data.iterrows():
                            try:
                                # Year is in column 0
                                year_val = row.iloc[0]
                                if pd.isna(year_val):
                                    continue
                                
                                try:
                                    # Extract year - for CVD data, we want ALL years including 1980s
                                    year = int(str(year_val))
                                    if 1980 <= year <= 2022:  # Allow full historical range
                                        # Create records for each metric
                                        
                                        # Men deaths - col 1
                                        if not pd.isna(row.iloc[1]):
                                            records.append(AIHWRecord(
                                                year=year,
                                                value=float(row.iloc[1]),
                                                metric_type=MetricType.NUMBER,
                                                source_sheet="Table 11",
                                                sex="men",
                                                age_group=None,
                                                table_name="Cardiovascular disease deaths in Australia",
                                                condition="Cardiovascular Disease"
                                            ))
                                        
                                        # Women deaths - col 2
                                        if not pd.isna(row.iloc[2]):
                                            records.append(AIHWRecord(
                                                year=year,
                                                value=float(row.iloc[2]),
                                                metric_type=MetricType.NUMBER,
                                                source_sheet="Table 11",
                                                sex="women",
                                                age_group=None,
                                                table_name="Cardiovascular disease deaths in Australia",
                                                condition="Cardiovascular Disease"
                                            ))
                                        
                                        # Persons deaths - col 3
                                        if not pd.isna(row.iloc[3]):
                                            records.append(AIHWRecord(
                                                year=year,
                                                value=float(row.iloc[3]),
                                                metric_type=MetricType.NUMBER,
                                                source_sheet="Table 11",
                                                sex="persons",
                                                age_group=None,
                                                table_name="Cardiovascular disease deaths in Australia",
                                                condition="Cardiovascular Disease"
                                            ))
                                        
                                        # Crude rates - cols 4-6
                                        for col_idx, sex in [(4, "men"), (5, "women"), (6, "persons")]:
                                            if not pd.isna(row.iloc[col_idx]):
                                                records.append(AIHWRecord(
                                                    year=year,
                                                    value=float(row.iloc[col_idx]),
                                                    metric_type=MetricType.CRUDE_RATE,
                                                    source_sheet="Table 11",
                                                    sex=sex,
                                                    age_group=None,
                                                    table_name="Cardiovascular disease deaths in Australia",
                                                    condition="Cardiovascular Disease"
                                                ))
                                        
                                        # Age-standardised rates - cols 7-9
                                        for col_idx, sex in [(7, "men"), (8, "women"), (9, "persons")]:
                                            if not pd.isna(row.iloc[col_idx]):
                                                records.append(AIHWRecord(
                                                    year=year,
                                                    value=float(row.iloc[col_idx]),
                                                    metric_type=MetricType.STANDARDISED_RATE,
                                                    source_sheet="Table 11",
                                                    sex=sex,
                                                    age_group=None,
                                                    table_name="Cardiovascular disease deaths in Australia",
                                                    condition="Cardiovascular Disease"
                                                ))
                                except (ValueError, TypeError) as e:
                                    logger.warning(f"Error processing year in Table 11 row {idx}: {e}")
                                    continue
                            except Exception as e:
                                logger.warning(f"Error processing Table 11 row {idx}: {e}")
                                continue
                        
                        logger.info(f"Extracted {len(records)} CVD mortality records from Table 11")
                    else:
                        logger.warning("Could not locate Table 11 in the CVD Excel file")
                    
                    # Convert records to DataFrame
                    records_data = []
                    for record in records:
                        record_dict = record.model_dump()
                        records_data.append(record_dict)
                    
                    if records_data:
                        df = pd.DataFrame(records_data)
                        # Clean up the DataFrame
                        columns_to_drop = ['region', 'indigenous_status', 'notes']
                        df = df.drop(columns=columns_to_drop, errors='ignore')
                        
                        # Sort by year
                        if 'year' in df.columns:
                            df = df.sort_values('year')
                        
                        df.to_csv(output_path, index=False)
                        logger.info(f"Successfully saved {len(df)} CVD records to {csv_file}")
                        results[csv_file] = df
                    else:
                        logger.warning(f"No valid records found in Table 11")
                
                else:
                    # Standard processing for other files
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
                        
                        # Allow years outside 2009-2022 for CVD data (if it's the CVD file)
                        if 'year' in df.columns and 'CVD' not in excel_file:
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