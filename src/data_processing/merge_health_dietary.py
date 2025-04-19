"""
Merge health outcomes data with dietary metrics.
Creates the final analytical dataset with lagged predictors.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from src import config
from pydantic import BaseModel, Field, field_validator
import logging
from typing import List, Dict, Optional
from .health_outcome_metrics import main as generate_health_metrics

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnalyticalRecord(BaseModel):
    """Pydantic model for validating analytical records.
    All field names and comments use Australian English.
    """
    Year: int = Field(..., ge=1961, le=2024)
    # Dietary metrics (current year)
    Total_LA_Intake_g_per_capita_day: float = Field(..., ge=0)
    LA_Intake_percent_calories: float = Field(..., ge=0, le=100)
    Plant_Fat_Ratio: float = Field(..., ge=0, le=1)
    Total_Calorie_Supply: float = Field(..., ge=0)
    Total_Fat_Supply_g: float = Field(..., ge=0)
    Total_Carb_Supply_g: Optional[float] = Field(None, ge=0)
    Total_Protein_Supply_g: Optional[float] = Field(None, ge=0)
    Population: Optional[float] = Field(None, ge=0, description="Estimated population for the year (used for per capita calculations)")
    # Health outcomes (optional, from NCD-RisC and AIHW datasets)
    Diabetes_Prevalence_Rate_AgeStandardised: Optional[float] = Field(None)
    Diabetes_Treatment_Rate_AgeStandardised: Optional[float] = Field(None)
    Obesity_Prevalence_AgeStandardised: Optional[float] = Field(None)
    BMI_AgeStandardised: Optional[float] = Field(None, ge=0, description="Body Mass Index, age-standardised")
    Total_Cholesterol_AgeStandardised: Optional[float] = Field(None)
    NonHDL_Cholesterol_AgeStandardised: Optional[float] = Field(None)
    # Updated AIHW metrics
    Dementia_Prevalence_Number: Optional[float] = Field(None)
    Dementia_Mortality_Rate_ASMR: Optional[float] = Field(None)
    CVD_Mortality_Rate_ASMR: Optional[float] = Field(None)
    # Lagged LA intake (optional)
    LA_perc_kcal_lag5: Optional[float] = Field(None)
    LA_perc_kcal_lag10: Optional[float] = Field(None)
    LA_perc_kcal_lag15: Optional[float] = Field(None)
    LA_perc_kcal_lag20: Optional[float] = Field(None)

    # Validators for optional fields
    @field_validator('*')
    def check_non_negative_optional(cls, v, info):
        # List of fields that should be non-negative if present
        non_negative_fields = [
            'Total_LA_Intake_g_per_capita_day', 'LA_Intake_percent_calories', 'Plant_Fat_Ratio',
            'Total_Calorie_Supply', 'Total_Fat_Supply_g', 'Total_Carb_Supply_g', 'Total_Protein_Supply_g',
            'Diabetes_Prevalence_Rate_AgeStandardised', 'Diabetes_Treatment_Rate_AgeStandardised',
            'Obesity_Prevalence_AgeStandardised', 'Dementia_Prevalence_Number',
            'Dementia_Mortality_Rate_ASMR', 'CVD_Mortality_Rate_ASMR',
            'LA_perc_kcal_lag5', 'LA_perc_kcal_lag10', 'LA_perc_kcal_lag15', 'LA_perc_kcal_lag20',
            'NonHDL_Cholesterol_AgeStandardised'
        ]
        if info.field_name in non_negative_fields and v is not None and not pd.isna(v):
            if v < 0:
                raise ValueError(f"{info.field_name} should be non-negative: {v}")
        return v

    @field_validator('LA_Intake_percent_calories', 'LA_perc_kcal_lag5', 'LA_perc_kcal_lag10', 'LA_perc_kcal_lag15', 'LA_perc_kcal_lag20')
    def validate_la_percent(cls, v):
        if v is not None and not pd.isna(v):
            if not (0 <= v <= 100):
                raise ValueError(f"LA percentage should be between 0 and 100: {v}")
        return v

    @field_validator('Total_Cholesterol_AgeStandardised')
    def validate_cholesterol(cls, v):
        if v is not None and not pd.isna(v):
            if not (2 <= v <= 8):
                raise ValueError(f"Total Cholesterol should be between 2 and 8 mmol/L: {v}")
        return v

    @field_validator('NonHDL_Cholesterol_AgeStandardised')
    def validate_nonhdl_cholesterol(cls, v):
        if v is not None and not pd.isna(v):
            if not (0 <= v <= 8):
                raise ValueError(f"Non-HDL cholesterol should be between 0 and 8 mmol/L: {v}")
        return v

    @field_validator('Plant_Fat_Ratio')
    def validate_ratio(cls, v):
        if v is not None and not pd.isna(v):
            if not (0 <= v <= 1):
                raise ValueError(f"Plant Fat Ratio must be between 0 and 1: {v}")
        return v

    @field_validator('Dementia_Mortality_Rate_ASMR', 'CVD_Mortality_Rate_ASMR')
    def check_asmr_non_negative(cls, v, info):
        if v is not None and not pd.isna(v):
            if v < 0:
                raise ValueError(f"{info.field_name} should be non-negative: {v}")
        return v

def create_lagged_predictors(df: pd.DataFrame, lag_years: List[int]) -> pd.DataFrame:
    """
    Create lagged versions of LA intake percentage
    """
    df = df.copy()
    # Ensure data is sorted by year before lagging
    if 'Year' not in df.columns:
        raise ValueError("DataFrame must contain 'Year' column for sorting.")
    df = df.sort_values('Year')

    target_col = 'LA_Intake_percent_calories'
    if target_col not in df.columns:
        raise ValueError(f"Column '{target_col}' not found for lagging.")

    for lag in lag_years:
        col_name = f'LA_perc_kcal_lag{lag}'
        df[col_name] = df[target_col].shift(lag)
        logger.info(f"Created lagged column: {col_name}")

    return df

def standardize_dietary_metrics(dietary_df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize dietary metrics column names to match the AnalyticalRecord schema.
    """
    df = dietary_df.copy()
    # Define mapping based on the output of scripts/calculate_dietary_metrics.py
    # and the target AnalyticalRecord schema
    column_mapping = {
        'year': 'Year',
        'la_intake_g_day': 'Total_LA_Intake_g_per_capita_day',
        'la_intake_percent_calories': 'LA_Intake_percent_calories',
        'plant_fat_ratio': 'Plant_Fat_Ratio',
        'total_fat_supply': 'Total_Fat_Supply_g',
        'total_protein_supply': 'Total_Protein_Supply_g',
        'total_calorie_supply': 'Total_Calorie_Supply'
    }

    # Check if carb column exists in input
    carb_col_input = None
    for potential_carb_col in ['total_carb_supply', 'Total_Carb_Supply_g']:
        if potential_carb_col in df.columns:
            carb_col_input = potential_carb_col
            break
    if carb_col_input:
        column_mapping[carb_col_input] = 'Total_Carb_Supply_g'
    else:
        logger.warning("Carbohydrate supply column not found in dietary metrics input. It will be missing.")

    # Apply renaming only for columns that exist
    actual_renames = {old: new for old, new in column_mapping.items() if old in df.columns}
    df = df.rename(columns=actual_renames)
    logger.info(f"Renamed dietary metrics columns: {actual_renames}")

    # Ensure 'Year' column exists after renaming
    if 'Year' not in df.columns:
        raise ValueError("Failed to create 'Year' column during dietary metrics standardization.")

    return df

def main():
    # Set up paths
    # Use centralised processed data directory from config
    processed_dir = config.PROCESSED_DATA_DIR

    # Load dietary metrics
    dietary_metrics_path = config.DIETARY_METRICS_FILE
    if not dietary_metrics_path.exists():
        logger.error(f"Dietary metrics file not found: {dietary_metrics_path}")
        return
    logger.info(f"Loading dietary metrics from {dietary_metrics_path}...")
    dietary_df = pd.read_csv(dietary_metrics_path)
    dietary_df = standardize_dietary_metrics(dietary_df)

    # Create lagged predictors
    logger.info("Creating lagged predictors...")
    lag_years = [5, 10, 15, 20]
    try:
        dietary_df = create_lagged_predictors(dietary_df, lag_years)
    except ValueError as e:
        logger.error(f"Error creating lagged predictors: {e}")
        return
    
    # Load health outcome metrics from the consolidated file
    logger.info("Loading health outcome metrics...")
    health_metrics_path = config.HEALTH_METRICS_FILE
    
    # Check if health_metrics_australia_combined.csv exists, if not, generate it
    if not health_metrics_path.exists():
        logger.info("Health outcome metrics file not found. Generating now...")
        try:
            generate_health_metrics()
        except Exception as e:
            logger.error(f"Failed to generate health metrics: {e}")
            return
    
    # Now load the health metrics file
    if not health_metrics_path.exists():
        logger.error("Failed to create health metrics file.")
        return
    
    try:
        health_df = pd.read_csv(health_metrics_path)
        logger.info(f"Loaded health metrics: {health_df.shape[0]} rows, {health_df.shape[1]} columns")
    except Exception as e:
        logger.error(f"Error loading health metrics file: {e}")
        # Create an empty DataFrame with just Year if loading fails
        health_df = pd.DataFrame({'Year': dietary_df['Year'].unique()})

    # --- Load Population Data ---
    logger.info("Loading processed population data...")
    population_data_path = config.ABS_POPULATION_PROCESSED_FILE
    if not population_data_path.exists():
        logger.warning(f"Processed population data file not found: {population_data_path}. Population column will be empty.")
        # Create an empty DataFrame with 'Year' to avoid merge errors later
        population_df = pd.DataFrame({'Year': [], 'Population': []})
    else:
        try:
            population_df = pd.read_csv(population_data_path)
            # Ensure columns are correct ('Year', 'Population')
            if 'Year' not in population_df.columns or 'Population' not in population_df.columns:
                 raise ValueError("Population data CSV missing required 'Year' or 'Population' columns.")
            population_df = population_df[['Year', 'Population']] # Keep only relevant columns
            logger.info(f"Loaded population data: {population_df.shape[0]} rows")
        except Exception as e:
            logger.error(f"Error loading or processing population data file {population_data_path}: {e}")
            population_df = pd.DataFrame({'Year': [], 'Population': []}) # Empty DF on error

    # Merge dietary metrics (with lags) and health outcomes
    logger.info("Merging dietary and health data...")
    # Ensure 'Year' is integer type for merging
    try:
        dietary_df['Year'] = dietary_df['Year'].astype(int)
        health_df['Year'] = health_df['Year'].astype(int)
        population_df['Year'] = population_df['Year'].astype(int) # Also convert population year
    except Exception as e:
        logger.error(f"Could not convert Year columns to integer for merging: {e}")
        logger.info(f"Dietary Year Dtype: {dietary_df['Year'].dtype}")
        logger.info(f"Health Year Dtype: {health_df['Year'].dtype}")
        return

    merged_df = pd.merge(dietary_df, health_df, on='Year', how='left')
    logger.info(f"Merged data shape after health data: {merged_df.shape}")

    # --- Merge Population Data ---
    logger.info("Merging population data...")
    merged_df = pd.merge(merged_df, population_df, on='Year', how='left')
    logger.info(f"Merged data shape after population data: {merged_df.shape}")

    # --- Data Type Conversion and NaN Handling BEFORE Validation ---
    # Convert all potentially numeric columns to float, coercing errors
    numeric_cols = [col for col in merged_df.columns if col != 'Year']
    for col in numeric_cols:
        if col in merged_df:
            merged_df[col] = pd.to_numeric(merged_df[col], errors='coerce')

    # Replace Pandas NaN with None for Pydantic validation
    merged_df = merged_df.replace({np.nan: None})
    logger.info("Replaced NaN with None for validation.")

    # Validate records using Pydantic
    logger.info("Validating merged records...")
    validated_records = []
    invalid_count = 0
    validation_errors = {}

    for i, record_dict in enumerate(merged_df.to_dict('records')):
        try:
            validated_record = AnalyticalRecord(**record_dict)
            validated_records.append(validated_record.model_dump())
        except Exception as e:
            invalid_count += 1
            year = record_dict.get('Year', f'Unknown_Row_{i+1}')
            error_details = {
                "Year": year,
                "ErrorType": type(e).__name__,
                "ErrorMessage": str(e),
                "InvalidFields": getattr(e, 'errors', lambda: "N/A")() if hasattr(e, 'errors') else str(e)
            }
            # Log more detailed field errors if available (from pydantic.ValidationError)
            if hasattr(e, 'errors'):
                 field_errors = {err['loc'][0]: err['msg'] for err in e.errors() if 'loc' in err and err['loc']}
                 error_details["FieldErrors"] = field_errors
                 logger.error(f"Validation error for Year {year}: {field_errors}")
            else:
                 logger.error(f"Validation error for Year {year}: {type(e).__name__} - {str(e)}")

            # Store error details for reporting
            if year not in validation_errors:
                validation_errors[year] = []
            validation_errors[year].append(error_details)

    logger.info(f"Validation completed. Total records: {len(merged_df)}, Valid records: {len(validated_records)}, Invalid records: {invalid_count}")

    # --- Save Validated Data and Errors ---
    if validated_records:
        final_df = pd.DataFrame(validated_records)
        # Re-establish desired column order based on the Pydantic model fields
        final_df = final_df[list(AnalyticalRecord.model_fields.keys())]

        # --- Final Dataset Completeness Check ---
        logger.info("--- Final Dataset Completeness ---")
        total_rows = len(final_df)
        for col in final_df.columns:
            if col != 'Year': # Exclude Year column from completeness check
                completeness = final_df[col].notna().sum()
                completeness_perc = (completeness / total_rows) * 100
                logger.info(f"{col}: {completeness_perc:.1f}% complete ({completeness}/{total_rows})")

        # Save the final validated DataFrame
        final_output_path = config.ANALYTICAL_DATA_FINAL_FILE
        final_df.to_csv(final_output_path, index=False)
        logger.info(f"Final analytical dataset saved successfully to {final_output_path}")
        logger.info(f"Final dataset covers years {final_df['Year'].min()} to {final_df['Year'].max()}")
        logger.info(f"Total validated records: {len(final_df)}")

    else:
        logger.warning("No valid records found after validation. Final dataset not saved.")

    # Save validation errors if any occurred
    if validation_errors:
        error_df = pd.DataFrame(list(validation_errors.items()), columns=['Year_or_Row', 'Error'])
        error_path = config.ANALYTICAL_DATA_VALIDATION_ERRORS_FILE
        error_df.to_csv(error_path, index=False)
        logger.warning(f"Detailed validation errors saved to {error_path}")

if __name__ == "__main__":
    main() 