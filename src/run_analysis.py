"""
Central analysis script for generating refined visualisations and statistical analyses.

This script orchestrates the analysis pipeline by:
1. Loading the final analytical dataset
2. Applying any necessary data transformations
3. Calling visualisation functions with appropriate configurations
4. Adding statistical annotations and refinements to plots

Note: This is the main entry point for analysis, not visualisation implementation.
The actual plotting functions live in src/visualisation/ modules.
"""
from pathlib import Path
from typing import Optional

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm

from src.config import PROCESSED_DATA_DIR, FIGURES_DIR, ANALYTICAL_DATA_FINAL_FILE
from src.visualisation import (
    time_series,
    scatter,
    correlation,
    regression,
    utils
)
from src.visualisation.utils import DatasetConfig, set_plot_style
from scipy import stats


def load_analytical_data() -> pd.DataFrame:
    """Load the final analytical dataset with basic validation.
    
    Returns:
        pd.DataFrame: The processed analytical dataset
        
    Raises:
        FileNotFoundError: If the data file doesn't exist
        ValueError: If the data fails basic validation checks
    """
    if not ANALYTICAL_DATA_FINAL_FILE.exists():
        raise FileNotFoundError(
            f"Analytical data file not found at {ANALYTICAL_DATA_FINAL_FILE}. "
            "Please run the ETL pipeline first."
        )
    
    df = pd.read_csv(ANALYTICAL_DATA_FINAL_FILE)
    
    # Basic validation
    if df.empty:
        raise ValueError("Loaded analytical dataset is empty")
    
    required_cols = {"Year", "Total_LA_Intake_g_per_capita_day"}
    if not required_cols.issubset(df.columns):
        missing = required_cols - set(df.columns)
        raise ValueError(f"Dataset missing required columns: {missing}")
    
    return df


def main():
    """Main analysis execution function."""
    # Initialise plot style and output directory
    set_plot_style()
    FIGURES_DIR.mkdir(exist_ok=True)
    
    try:
        # Load the analytical dataset
        df = load_analytical_data()
        print(f"Successfully loaded dataset with {len(df)} records")
        
        # === Data Preparation Section ===
        # Create decade column for visualisation
        df['Decade'] = (df['Year'] // 10 * 10).astype(str) + 's'
        
        # Print data availability info
        print("\nData availability:")
        for col in ['LA_Intake_percent_calories', 'Obesity_Prevalence_AgeStandardised', 
                   'Diabetes_Prevalence_Rate_AgeStandardised', 'CVD_Mortality_Rate_ASMR']:
            valid_count = df[col].notna().sum()
            print(f"{col}: {valid_count} records")
        
        # === Time Series Analysis ===
        # Configure visualisation settings
        ts_config = time_series.TimeSeriesConfig(
            output_dir=str(FIGURES_DIR),
            show_plots=False,
            date_col="Year"
        )
        
        # 1. Enhanced LA trend plot with annotations
        time_series.plot_la_trend(df, ts_config)
        
        # 2. Faceted trends plot for available data
        health_vars = [
            "LA_Intake_percent_calories",
            "Obesity_Prevalence_AgeStandardised",
            "Diabetes_Prevalence_Rate_AgeStandardised"
        ]
        titles = [
            "LA Intake (% Calories)",
            "Obesity Prevalence (%)",
            "Diabetes Prevalence (%)"
        ]
        time_series.plot_faceted_trends(df, ts_config, health_vars, titles)
        
        # === Correlation Analysis ===
        # Prepare correlation dataset (exclude columns with too many NaN values)
        corr_vars = [
            'LA_Intake_percent_calories',
            'Obesity_Prevalence_AgeStandardised',
            'Diabetes_Prevalence_Rate_AgeStandardised',
            'Total_Cholesterol_AgeStandardised'
        ]
        df_corr = df[corr_vars].dropna()
        
        if len(df_corr) > 2:  # Only proceed if we have enough data
            corr_config = correlation.CorrelationConfig(
                output_dir=str(FIGURES_DIR),
                show_plots=False
            )
            
            # Enhanced correlation heatmap
            correlation.plot_correlation_heatmap(
                df_corr,
                config=corr_config,
                title="Health Outcomes vs. LA Intake Correlations",
                caption="Note: Shows overall linear correlations for available data points only."
            )
        
        # === Scatter Plot Analysis ===
        # Prepare datasets for each analysis
        obesity_data = df.dropna(subset=['LA_perc_kcal_lag10', 'Obesity_Prevalence_AgeStandardised', 'Decade'])
        diabetes_data = df.dropna(subset=['LA_perc_kcal_lag10', 'Diabetes_Prevalence_Rate_AgeStandardised', 'Decade'])
        
        scatter_config = scatter.ScatterConfig(
            output_dir=str(FIGURES_DIR),
            show_plots=False,
            lag=0  # Using pre-computed lag columns
        )
        
        # Plot scatter plots only if we have enough data
        if len(obesity_data) > 2:
            scatter.plot_lagged_scatter(
                obesity_data,
                x="LA_perc_kcal_lag10",
                y="Obesity_Prevalence_AgeStandardised",
                config=scatter_config,
                hue="Decade",
                title="Obesity Prevalence vs. 10-Year Lagged LA Intake"
            )
        
        if len(diabetes_data) > 2:
            scatter.plot_lagged_scatter(
                diabetes_data,
                x="LA_perc_kcal_lag10",
                y="Diabetes_Prevalence_Rate_AgeStandardised",
                config=scatter_config,
                hue="Decade",
                title="Diabetes Prevalence vs. 10-Year Lagged LA Intake"
            )
        
        print("\nAnalysis completed successfully")
        
    except Exception as e:
        print(f"Analysis failed: {str(e)}")
        raise


if __name__ == "__main__":
    main()