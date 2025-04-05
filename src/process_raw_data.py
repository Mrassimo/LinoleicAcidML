import pandas as pd
import os
import re
from pathlib import Path

# Define base paths
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"

# Ensure the processed data directory exists
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Define file paths for manually downloaded data
aihw_prevalence_file = RAW_DATA_DIR / "AIHW-DEM-02-S2-Prevalence.xlsx"
aihw_mortality_file = RAW_DATA_DIR / "AIHW-DEM-02-S3-Mortality-202409.xlsx"
aihw_cvd_facts_file = RAW_DATA_DIR / "AIHW-CVD-92-HSVD-facts-data-tables-12122024.xlsx"

# Define output paths for processed AIHW files
output_aihw_prevalence_csv = PROCESSED_DATA_DIR / "aihw_dementia_prevalence.csv"
output_aihw_mortality_csv = PROCESSED_DATA_DIR / "aihw_dementia_mortality.csv"
output_aihw_cvd_facts_csv = PROCESSED_DATA_DIR / "aihw_cvd_all_facts.csv"

def standardize_column_name(col_name):
    """Converts column name to lowercase, replaces spaces/special chars with underscores."""
    if not isinstance(col_name, str):
        return f"unnamed_{col_name}" if pd.isna(col_name) else str(col_name)
    
    # Convert to lowercase
    new_name = col_name.lower()
    # Replace spaces and specific special characters with underscores
    new_name = re.sub(r'[ /()]+', '_', new_name)
    # Remove any characters that are not alphanumeric or underscore
    new_name = re.sub(r'[^a-z0-9_]', '', new_name)
    # Remove leading/trailing underscores
    new_name = new_name.strip('_')
    # Handle potential multiple underscores resulting from replacements
    new_name = re.sub(r'_+', '_', new_name)
    return new_name

def perform_cleaning_analysis(df, file_name):
    """Perform initial cleaning analysis on a DataFrame."""
    print(f"\n--- Cleaning Analysis for {file_name} ---")
    
    # Standardise column names
    print("\n1. Standardising Column Names:")
    original_columns = df.columns.tolist()
    df.columns = [standardize_column_name(col) for col in df.columns]
    print("   Original Columns:", original_columns)
    print("   Standardised Columns:", df.columns.tolist())
    
    # Missing value analysis
    print("\n2. Missing Value Analysis (%):")
    missing_percentages = df.isnull().mean() * 100
    if missing_percentages.sum() == 0:
        print("   No missing values found.")
    else:
        for col, percentage in missing_percentages.items():
            if percentage > 0:
                print(f"   - {col}: {percentage:.2f}%")
    
    # Data type check
    print("\n3. Data Type Check:")
    print(df.dtypes)

def is_data_sheet(sheet_name):
    """Determine if a sheet is likely a data sheet vs. a cover/summary/notes sheet."""
    # Common names for non-data sheets
    non_data_sheets = ['contents', 'notes', 'cover', 'sheet1', 'summary', 'introduction']
    
    # Check if the sheet name is in the list of non-data sheets
    if sheet_name.lower() in non_data_sheets:
        return False
    
    # Assume sheets with alphanumeric pattern (S1.1, S2.3, etc.) are data sheets
    if re.match(r'^S\d+\.\d+$', sheet_name):
        return True
    
    # For CVD document, these are all data sheets
    if sheet_name in ['All CVD', 'CHD', 'Stroke', 'Heart failure', 'AF', 'PAD', 'RHD', 'Congenital', 
                      'Comorbidity', 'Treatment & management', 'Impact', 'Risk factors']:
        return True
    
    # Default to True for other sheet names that don't match non-data patterns
    return True

def process_excel_file(excel_path, csv_output_path):
    """
    Process an Excel file by reading all relevant data sheets and combining them.
    
    Args:
        excel_path: Path to the Excel file
        csv_output_path: Path to save the combined CSV result
        
    Returns:
        Combined DataFrame from all data sheets
    """
    print(f"\n--- Processing: {excel_path.name} ---")
    
    if not excel_path.exists():
        print(f"File not found: {excel_path}")
        return None
    
    try:
        # List all sheet names
        xls = pd.ExcelFile(excel_path)
        sheet_names = xls.sheet_names
        print(f"Sheet names in {excel_path.name}: {sheet_names}")
        
        # Filter for data sheets
        data_sheets = [sheet for sheet in sheet_names if is_data_sheet(sheet)]
        print(f"Data sheets identified: {data_sheets}")
        
        if not data_sheets:
            print(f"No data sheets found in {excel_path.name}")
            return None
        
        # Read all data sheets
        all_dfs = []
        for sheet_name in data_sheets:
            print(f"Loading sheet: '{sheet_name}' with header=4")
            try:
                df = pd.read_excel(excel_path, sheet_name=sheet_name, header=4)
                
                # Add a column to indicate the source sheet
                df['source_sheet'] = sheet_name
                
                # Basic data check - skip if completely empty
                if df.empty or df.dropna().empty:
                    print(f"Sheet '{sheet_name}' is empty or contains only NaN values. Skipping.")
                    continue
                
                all_dfs.append(df)
                print(f"Successfully loaded sheet '{sheet_name}'. Shape: {df.shape}")
                
            except Exception as e:
                print(f"Error loading sheet '{sheet_name}': {e}")
        
        if not all_dfs:
            print(f"No valid data found in any sheets of {excel_path.name}")
            return None
        
        # Combine all DataFrames
        combined_df = pd.concat(all_dfs, ignore_index=True)
        print(f"Combined DataFrame shape: {combined_df.shape}")
        
        # Save the combined DataFrame to CSV
        print(f"Saving combined data to: {csv_output_path}")
        combined_df.to_csv(csv_output_path, index=False)
        print(f"Successfully saved {csv_output_path.name}")
        
        # Perform cleaning analysis on the combined DataFrame
        perform_cleaning_analysis(combined_df, csv_output_path.name)
        
        return combined_df
        
    except Exception as e:
        print(f"Error processing {excel_path.name}: {e}")
        return None

print("--- Starting Manual Data Processing ---")

# Process AIHW Excel Files and Convert to CSV
aihw_files_to_process = {
    aihw_prevalence_file: output_aihw_prevalence_csv,
    aihw_mortality_file: output_aihw_mortality_csv,
    aihw_cvd_facts_file: output_aihw_cvd_facts_csv
}

for excel_path, csv_output_path in aihw_files_to_process.items():
    process_excel_file(excel_path, csv_output_path)

print("\n--- Manual Data Processing Finished ---")