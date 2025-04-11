"""
Extract standardized health outcome metrics from various processed data sources.
Merges NCD-RisC and specific AIHW metrics into a single yearly dataset.
"""

import pandas as pd
from pathlib import Path
from src import config
import logging
from typing import Dict, List, Optional

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Use centralised processed data directory from config

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
    diabetes_df = load_and_validate_csv(config.PROCESSED_DATA_DIR / 'ncdrisc_diabetes_australia_processed.csv', ['year', 'sex', 'age-standardised_prevalence_of_diabetes_18+_years_', 'age-standardised_proportion_of_people_with_diabetes_who_were_treated_30+_years_'])
    bmi_df = load_and_validate_csv(config.PROCESSED_DATA_DIR / 'ncdrisc_bmi_australia_processed.csv', ['year', 'sex', 'prevalence_of_bmi>=30_kg_m²_obesity_'])
    cholesterol_df = load_and_validate_csv(config.PROCESSED_DATA_DIR / 'ncdrisc_cholesterol_australia_processed.csv', ['year', 'sex', 'mean_total_cholesterol_mmol_l_', 'mean_non-hdl_cholesterol_mmol_l_'])

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
    prev_df = load_and_validate_csv(config.AIHW_PREVALENCE_PROCESSED_FILE, ['year', 'value', 'source_sheet', 'sex'])
    if prev_df is not None:
        # Log unique sex values before filtering Dementia Prevalence
        logger.debug(f"Dementia Prevalence - unique 'sex' values before filtering: {prev_df['sex'].unique().tolist()}")
        # Filter specifically for sheet S2.4 and persons
        dementia_prev = prev_df[
            (prev_df['source_sheet'] == 'S2.4') &
            (prev_df['sex'] == 'persons')
        ].copy()
        # Log shape after filtering Dementia Prevalence
        logger.debug(f"Dementia Prevalence - filtered dataframe shape: {dementia_prev.shape}")
        if not dementia_prev.empty:
            dementia_prev = dementia_prev[['year', 'value']].rename(columns={'year': 'Year', 'value': 'Dementia_Prevalence_Number'})
            # Ensure no duplicate years
            dementia_prev = dementia_prev.drop_duplicates(subset=['Year'], keep='first')
            all_aihw_metrics.append(dementia_prev)
            logger.info(f"Extracted Dementia Prevalence (Number): {dementia_prev.shape[0]} rows")
        else:
            logger.warning("No 'persons' data found in aihw_dementia_prevalence_australia_processed.csv from sheet S2.4.")

    # Dementia Mortality (Age-Standardised Rate) - From S3.5
    mort_df = load_and_validate_csv(config.AIHW_MORTALITY_PROCESSED_FILE, ['year', 'value', 'source_sheet', 'metric_type', 'sex'])
    if mort_df is not None:
        # Log unique sex values before filtering Dementia Mortality
        logger.debug(f"Dementia Mortality - unique 'sex' values before filtering: {mort_df['sex'].unique().tolist()}")
        # Filter specifically for sheet S3.5, standardised rate, and persons
        dementia_mort = mort_df[
            (mort_df['source_sheet'] == 'S3.5') &
            (mort_df['metric_type'] == 'standardised_rate') &
            (mort_df['sex'] == 'persons')
        ].copy()
        # Log shape after filtering Dementia Mortality
        logger.debug(f"Dementia Mortality - filtered dataframe shape: {dementia_mort.shape}")
        if not dementia_mort.empty:
            dementia_mort = dementia_mort[['year', 'value']].rename(columns={'year': 'Year', 'value': 'Dementia_Mortality_Rate_ASMR'})
            dementia_mort = dementia_mort.drop_duplicates(subset=['Year'], keep='first')
            all_aihw_metrics.append(dementia_mort)
            logger.info(f"Extracted Dementia Mortality (ASMR): {dementia_mort.shape[0]} rows")
        else:
            logger.warning("No 'persons' standardised rate data found in aihw_dementia_mortality_australia_processed.csv from sheet S3.5.")


    # CVD Mortality (Age-Standardised Rate) - From Table 11 in aihw_cvd_all_facts.csv
    cvd_df = load_and_validate_csv(config.AIHW_CVD_PROCESSED_FILE, ['year', 'value', 'source_sheet', 'metric_type', 'sex'])
    if cvd_df is not None:
        # Log unique sex values before filtering CVD Mortality
        logger.debug(f"CVD Mortality - unique 'sex' values before filtering: {cvd_df['sex'].unique().tolist()}")
        # Filter specifically for Table 11, standardised rate, and persons
        cvd_mort = cvd_df[
            (cvd_df['source_sheet'] == 'Table 11') &
            (cvd_df['metric_type'] == 'standardised_rate') &
            (cvd_df['sex'] == 'persons')
        ].copy()
        # Log shape after filtering CVD Mortality
        logger.debug(f"CVD Mortality - filtered dataframe shape: {cvd_mort.shape}")
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

    aihw_merged_df = all_aihw_metrics[0]
    for df in all_aihw_metrics[1:]:
        aihw_merged_df = pd.merge(aihw_merged_df, df, on='Year', how='outer')

    logger.info(f"Processed AIHW metrics. Shape: {aihw_merged_df.shape}")
    return aihw_merged_df

def main():
    """
    Main function to extract and merge all health metrics.
    """
    logger.info("Starting health metrics consolidation...")

    ncd_metrics = extract_ncd_risc_metrics()
    aihw_metrics = extract_aihw_metrics()

    # Merge NCD and AIHW metrics
    if ncd_metrics is not None and aihw_metrics is not None:
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
    output_path = config.HEALTH_METRICS_FILE
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