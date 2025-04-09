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
    table_name = extract_table_name(df, sheet_name)
    logger.info(f"Processing Sheet: '{sheet_name}', Table: '{table_name}'")
    records = []

    # --- Special Handling for S2.4 (Dementia Prevalence) ---
    if sheet_name == "S2.4" and "AIHW-DEM-02-S2-Prevalence" in file_name:
        logger.info("Applying special handling for Sheet S2.4")
        header_row_idx = None
        for i in range(min(15, len(df))):
            if pd.notna(df.iloc[i, 0]) and "Year" in str(df.iloc[i, 0]):
                header_row_idx = i
                break

        if header_row_idx is not None:
            logger.info(f"Found header row at row {header_row_idx} in S2.4")
            data_start_row = header_row_idx + 1
            data_df = df.iloc[data_start_row:].copy()
            data_df.columns = [f"col_{j}" for j in range(len(data_df.columns))]

            for idx, row in data_df.iterrows():
                year_val = row["col_0"]
                year = extract_year(year_val)

                if year:
                    for col_idx, sex in [(1, "male"), (2, "female"), (3, "persons")]:
                        col_key = f"col_{col_idx}"
                        if col_key in row and pd.notna(row[col_key]):
                            try:
                                value = float(row[col_key])
                                records.append(
                                    AIHWRecord(
                                        year=year,
                                        value=value,
                                        metric_type=MetricType.NUMBER,
                                        source_sheet=sheet_name,
                                        sex=sex,
                                        age_group="all_ages",
                                        table_name=table_name,
                                        condition="Dementia",
                                    )
                                )
                            except (ValueError, TypeError) as e:
                                logger.warning(
                                    f"Sheet {sheet_name}, Row {idx+data_start_row}, Col {col_idx}: Could not convert value '{row[col_key]}' to float. Error: {e}"
                                )
            logger.info(
                f"Sheet {sheet_name}: Extracted {len(records)} records using special handling."
            )
            return records
        else:
            logger.warning(
                f"Could not find header row for special handling in Sheet {sheet_name}."
            )
            # Fall through to standard processing if special handling fails

    # --- Special Handling for S3.5 (Dementia Mortality) ---
    elif sheet_name == "S3.5" and "AIHW-DEM-02-S3-Mortality" in file_name:
        logger.info("Applying special handling for Sheet S3.5")

        # Targeted header detection for column A (index 0)
        header_rows = []
        max_search_rows = min(20, len(df))
        for i in range(max_search_rows):
            cell = str(df.iloc[i, 0]).strip().lower()  # Only check first column
            if "year" in cell:
                logger.debug(f"Found year header candidate at row {i}: {cell}")
                # Use current row and next row as headers (A2:A3)
                header_rows = [i, i+1] if i+1 < len(df) else [i]
                break

        if not header_rows:
            logger.warning("Could not find year header in column A, using rows 0-1")
            header_rows = [0, 1]

        logger.debug(f"Final header rows: {header_rows}")

        logger.info(
            f"S3.5: Using header rows at indices {header_rows[0]} and {header_rows[1]}"
        )

        # Combine headers from both rows
        composite_headers = []
        # Build composite headers from A2:A3
        composite_headers = []
        for col_idx in range(len(df.columns)):
            if col_idx == 0:  # Special handling for year column
                # Combine both header rows for column A
                year_header = " ".join([
                    str(df.iloc[row_idx, col_idx]).strip()
                    for row_idx in header_rows
                    if pd.notna(df.iloc[row_idx, col_idx])
                ]).lower().replace(" ", "_")
                composite_headers.append(year_header)
            else:
                # For other columns, use single header row
                primary = str(df.iloc[header_rows[0], col_idx]).strip()
                secondary = str(df.iloc[header_rows[-1], col_idx]).strip() if len(header_rows) > 1 else ""
                header = f"{secondary}_{primary}".lower().replace(" ", "_") if secondary else primary.lower().replace(" ", "_")
                composite_headers.append(header)

        logger.debug(f"Composite headers: {composite_headers}")

        data_start_row = header_rows[1] + 1
        data_df = df.iloc[data_start_row:].copy()
        
        # Debug: Log first 5 rows of parsed data
        logger.debug("S3.5 - First 5 rows of parsed data:")
        for i in range(min(5, len(data_df))):
            logger.debug(f"Row {i}: {data_df.iloc[i].to_dict()}")
        data_df.columns = composite_headers

        # Process each year row
        parsed_years = []
        for idx, row in data_df.iterrows():
            # Extract year from first column with strict validation
            year_cell = str(row.iloc[0]).strip()
            logger.debug(f"Raw year value: {year_cell}")
            
            # Handle Excel's merged cell formatting (e.g., "2009.")
            year_cell = year_cell.rstrip('.').split()[0]
            
            year = extract_year(year_cell)
            logger.debug(f"Parsed year: {year} from '{year_cell}'")
            if year:
                parsed_years.append(year)
            else:
                continue

            # Process each rate column
            for col in [
                "alzheimer’s_disease_age-standardised_rate_(per_100,000_people)",
                "unspecified_dementia_age-standardised_rate_(per_100,000_people)",
                "vascular_dementia_age-standardised_rate_(per_100,000_people)",
            ]:
                if col in row and pd.notna(row[col]):
                    try:
                        records.append(
                            AIHWRecord(
                                year=year,
                                value=float(row[col]),
                                metric_type=MetricType.STANDARDISED_RATE,
                                source_sheet=sheet_name,
                                sex="persons",  # Aggregated data
                                age_group="all_ages",
                                table_name=table_name,
                                condition=col.split("_")[0].title(),
                            )
                        )
                    except (ValueError, TypeError) as e:
                        logger.warning(f"Error processing {col}: {e}")

        logger.info(
            f"S3.5: Successfully parsed {len(parsed_years)} years. Sample: {parsed_years[:5]} (Total unique: {len(set(parsed_years))})"
        )
        logger.info(
            f"Sheet {sheet_name}: Extracted {len(records)} dementia mortality records"
        )
        return records

    # --- Special Handling for Table 11 (CVD Mortality) ---
    elif sheet_name == "All CVD" and "AIHW-CVD-92" in file_name:
        logger.info("Applying special handling for CVD Table 11")
        table_start_idx, table_end_idx = None, None
        for i in range(len(df)):
            if pd.notna(df.iloc[i, 0]) and "Table 11" in str(df.iloc[i, 0]):
                table_start_idx = i
                for j in range(i + 5, len(df)):
                    if pd.isna(df.iloc[j, 0]) or str(df.iloc[j, 0]).lower().strip().startswith("note"):
                        table_end_idx = j
                        break
                if table_end_idx is None:
                    table_end_idx = len(df)
                break

        if table_start_idx is not None and table_end_idx is not None:
            logger.info(f"Found Table 11 from rows {table_start_idx} to {table_end_idx}")
            header_row_idx = table_start_idx + 2
            data_start_row = header_row_idx + 1
            table_df = df.iloc[data_start_row:table_end_idx].copy()
            table_df.columns = [f"col_{j}" for j in range(len(table_df.columns))]

            for idx, row in table_df.iterrows():
                year_val = row["col_0"]
                year_match = re.search(
                    r"^(19[89]\d|20[01]\d|202[0-2])$", str(year_val).strip()
                )
                if year_match:
                    year = int(year_match.group(0))
                    metrics_map = {
                        1: (MetricType.NUMBER, "male"),
                        2: (MetricType.NUMBER, "female"),
                        3: (MetricType.NUMBER, "persons"),
                        4: (MetricType.CRUDE_RATE, "male"),
                        5: (MetricType.CRUDE_RATE, "female"),
                        6: (MetricType.CRUDE_RATE, "persons"),
                        7: (MetricType.STANDARDISED_RATE, "male"),
                        8: (MetricType.STANDARDISED_RATE, "female"),
                        9: (MetricType.STANDARDISED_RATE, "persons"),
                    }
                    for col_idx, (metric_type, sex) in metrics_map.items():
                        col_key = f"col_{col_idx}"
                        if col_key in row and pd.notna(row[col_key]):
                            try:
                                raw_value = str(row[col_key]).strip()
                                # Clean numeric values
                                clean_value = re.sub(r"[^\d.]", "", raw_value)
                                logger.debug(f"Raw: {raw_value} | Cleaned: {clean_value}")
                                value = float(clean_value) if clean_value else None
                                records.append(
                                    AIHWRecord(
                                        year=year,
                                        value=value,
                                        metric_type=metric_type,
                                        source_sheet="Table 11",
                                        sex=sex,
                                        age_group="all_ages",
                                        table_name="Cardiovascular disease deaths",
                                        condition="Cardiovascular Disease",
                                    )
                                )
                            except (ValueError, TypeError) as e:
                                logger.warning(
                                    f"Sheet {sheet_name}, Table 11, Row {idx+data_start_row}, Col {col_idx}: Could not convert value '{row[col_key]}' to float. Error: {e}"
                                )
            logger.info(
                f"Sheet {sheet_name}, Table 11: Extracted {len(records)} records using special handling."
            )
            return records
        else:
            logger.warning(
                f"Could not locate Table 11 structure in Sheet {sheet_name}."
            )
            # Fall through

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