# src/initial_data_cleaning.py
import pandas as pd
import re
import os

# List of file paths to process
file_paths = [
    'data/raw/NCD_RisC_Lancet_2024_Diabetes_Australia.csv',
    'data/raw/NCD_RisC_Cholesterol_Australia.csv',
    'data/raw/NCD_RisC_Lancet_2024_BMI_age_standardised_Australia.csv',
    'data/processed/faostat_fbs_australia.csv',
    'data/processed/fire_in_a_bottle_la_content.csv',
    'data/processed/aihw_dementia_prevalence.csv',
    'data/processed/aihw_dementia_mortality.csv',
    'data/processed/aihw_cvd_facts.csv'
]

def standardize_column_name(col_name):
    """Converts column name to lowercase, replaces spaces/special chars with underscores."""
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

print("Starting initial data cleaning analysis...\n")

for file_path in file_paths:
    print(f"--- Processing file: {file_path} ---")

    if not os.path.exists(file_path):
        print(f"!!! File not found: {file_path}. Skipping. !!!\n")
        continue

    try:
        # Load the dataset
        df = pd.read_csv(file_path)

        # --- Column Name Standardization ---
        print("\n1. Standardising Column Names...")
        original_columns = df.columns.tolist()
        df.columns = [standardize_column_name(col) for col in df.columns]
        standardized_columns = df.columns.tolist()

        print("   Original Columns:")
        for col in original_columns:
            print(f"      - '{col}'")
        print("\n   Standardised Columns:")
        for col in standardized_columns:
            print(f"      - '{col}'")

        # --- Missing Value Analysis ---
        print("\n2. Missing Value Analysis (%):")
        missing_percentages = df.isnull().mean() * 100
        if missing_percentages.sum() == 0:
            print("   No missing values found.")
        else:
            for col, percentage in missing_percentages.items():
                if percentage > 0:
                    print(f"   - {col}: {percentage:.2f}%")

        # --- Data Type Check ---
        print("\n3. Data Type Check:")
        print(df.dtypes)
        print("\n" + "-"*50 + "\n")

    except FileNotFoundError:
        print(f"!!! Error: File not found at {file_path}. Skipping. !!!\n")
    except pd.errors.EmptyDataError:
        print(f"!!! Error: File {file_path} is empty. Skipping. !!!\n")
    except Exception as e:
        print(f"!!! An error occurred while processing {file_path}: {e} !!!\n")

print("Initial data cleaning analysis finished.")