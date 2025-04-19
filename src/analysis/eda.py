# src/analysis/eda.py
"""
Exploratory Data Analysis (EDA) functions for the Seed Oils ML project.

This module contains functions for:
- Summary statistics
- Distribution analysis
- Correlation analysis
- Time series analysis
- Visualisation helpers for EDA
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Optional, Dict
import logging
from src import config

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define key variable groups for analysis
DIETARY_VARS = [
    'LA_Intake_percent_calories',
    'LA_perc_kcal_lag5',
    'LA_perc_kcal_lag10',
    'LA_perc_kcal_lag15',
    'LA_perc_kcal_lag20',
    'Total_Fat_Supply_g',
    'Plant_Fat_Ratio'
]

HEALTH_VARS = {
    'BMI': ['BMI_AgeStandardised', 'Obesity_Prevalence_AgeStandardised'],
    'Diabetes': ['Diabetes_Prevalence_Rate_AgeStandardised'],
    'CVD': [
        'CVD_Mortality_Rate_ASMR',
        'CVD_Prevalence_Rate_IHME',
        'CVD_Incidence_Rate_IHME',
        'CVD_Death_Rate_IHME'
    ],
    'Dementia': [
        'Dementia_Mortality_Rate_ASMR',
        'Dementia_Prevalence_Rate_IHME',
        'Dementia_Incidence_Rate_IHME',
        'Dementia_Death_Rate_IHME'
    ]
}

def load_data_for_eda() -> pd.DataFrame | None:
    """
    Loads the final analytical dataset for EDA.
    """
    filepath = config.ANALYTICAL_DATA_FINAL_FILE
    try:
        df = pd.read_csv(filepath)
        logging.info(f"Successfully loaded data from {filepath}")
        return df
    except FileNotFoundError:
        logging.error(f"EDA data file not found at {filepath}")
        return None
    except Exception as e:
        logging.error(f"Error loading data from {filepath}: {e}")
        return None

def perform_summary_statistics(df: pd.DataFrame):
    """
    Calculates and saves descriptive statistics and missing value counts.
    Also generates summary by data source (IHME, ABS, NCD-RisC).
    """
    if df is not None:
        logging.info("Calculating summary statistics...")

        # Ensure reports directory exists
        os.makedirs(config.REPORTS_DIR, exist_ok=True)

        # Descriptive statistics
        summary_stats = df.describe().T
        summary_stats_path = config.REPORTS_DIR / 'eda_summary_statistics.csv'
        summary_stats.to_csv(summary_stats_path)
        logging.info(f"Descriptive statistics saved to {summary_stats_path}")

        # Missing value counts and percentages
        missing_values = pd.DataFrame({
            'missing_count': df.isnull().sum(),
            'missing_percentage': (df.isnull().sum() / len(df) * 100).round(2)
        })
        missing_values_path = config.REPORTS_DIR / 'eda_missing_data_summary.csv'
        missing_values.to_csv(missing_values_path)
        logging.info(f"Missing value analysis saved to {missing_values_path}")

        # Summary by data source
        source_summary = {}
        
        # IHME metrics
        ihme_cols = [col for col in df.columns if 'IHME' in col]
        if ihme_cols:
            source_summary['IHME'] = df[ihme_cols].describe()
            source_path = config.REPORTS_DIR / 'eda_summary_ihme.csv'
            source_summary['IHME'].to_csv(source_path)
            logging.info(f"IHME summary statistics saved to {source_path}")
        
        # ABS metrics (ASMR)
        abs_cols = [col for col in df.columns if 'ASMR' in col]
        if abs_cols:
            source_summary['ABS'] = df[abs_cols].describe()
            source_path = config.REPORTS_DIR / 'eda_summary_abs.csv'
            source_summary['ABS'].to_csv(source_path)
            logging.info(f"ABS summary statistics saved to {source_path}")
        
        # NCD-RisC metrics
        ncd_cols = [col for col in df.columns if 'AgeStandardised' in col]
        if ncd_cols:
            source_summary['NCD_RisC'] = df[ncd_cols].describe()
            source_path = config.REPORTS_DIR / 'eda_summary_ncd_risc.csv'
            source_summary['NCD_RisC'].to_csv(source_path)
            logging.info(f"NCD-RisC summary statistics saved to {source_path}")
    else:
        logging.warning("DataFrame is None, skipping summary statistics.")

def plot_distributions(df: pd.DataFrame):
    """
    Generates and saves distribution plots for numerical columns,
    grouped by variable type (dietary vs health outcomes).
    """
    if df is not None:
        logging.info("Generating distribution plots...")

        # Ensure figures directory exists
        os.makedirs(config.FIGURES_DIR, exist_ok=True)

        # Plot dietary variables
        plt.figure(figsize=(15, 10))
        for i, col in enumerate(DIETARY_VARS, 1):
            if col in df.columns:
                plt.subplot(3, 3, i)
                sns.histplot(df[col].dropna(), kde=True)
                plt.title(f'Distribution of {col}')
                plt.xlabel(col)
                plt.ylabel('Frequency')
        plt.tight_layout()
        plt.savefig(config.FIGURES_DIR / 'distributions_dietary.png')
        plt.close()

        # Plot health variables by category
        for category, vars_list in HEALTH_VARS.items():
            plt.figure(figsize=(15, 10))
            for i, col in enumerate(vars_list, 1):
                if col in df.columns:
                    plt.subplot(3, 3, i)
                    sns.histplot(df[col].dropna(), kde=True)
                    plt.title(f'Distribution of {col}')
                    plt.xlabel(col)
                    plt.ylabel('Frequency')
            plt.tight_layout()
            plt.savefig(config.FIGURES_DIR / f'distributions_health_{category.lower()}.png')
            plt.close()
        
        logging.info("Distribution plots saved to figures directory")
    else:
        logging.warning("DataFrame is None, skipping distribution plotting.")

def perform_correlation_analysis(df: pd.DataFrame):
    """
    Calculates and saves correlation analyses:
    - Overall correlation matrix
    - Correlation heatmaps by health outcome category
    - Lag analysis for LA intake vs health outcomes
    """
    if df is not None:
        logging.info("Performing correlation analysis...")

        # Select only numerical columns
        numerical_df = df.select_dtypes(include='number')

        # Calculate correlation matrix
        correlation_matrix = numerical_df.corr()

        # Ensure reports directory exists
        os.makedirs(config.REPORTS_DIR, exist_ok=True)

        # Save full correlation matrix to CSV
        correlation_matrix_path = config.REPORTS_DIR / 'eda_correlation_matrix.csv'
        correlation_matrix.to_csv(correlation_matrix_path)
        logging.info(f"Full correlation matrix saved to {correlation_matrix_path}")

        # Generate correlation heatmaps by health category
        for category, health_vars in HEALTH_VARS.items():
            # Combine dietary variables with specific health outcome variables
            vars_to_plot = DIETARY_VARS + [var for var in health_vars if var in df.columns]
            
            # Filter correlation matrix for these variables
            correlation_subset = correlation_matrix.loc[vars_to_plot, vars_to_plot]

            plt.figure(figsize=(12, 10))
            sns.heatmap(correlation_subset, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
            plt.title(f'Correlation Heatmap: Dietary Factors vs {category} Outcomes')
            plt.tight_layout()
            heatmap_path = config.FIGURES_DIR / f'eda_correlation_heatmap_{category.lower()}.png'
            plt.savefig(heatmap_path)
            plt.close()
            logging.info(f"Correlation heatmap for {category} saved to {heatmap_path}")

        # Perform lag analysis
        lag_correlations = {}
        lag_vars = [col for col in df.columns if 'lag' in col.lower()]
        health_outcome_vars = [var for sublist in HEALTH_VARS.values() for var in sublist]
        
        for lag_var in lag_vars:
            lag_correlations[lag_var] = {}
            for outcome_var in health_outcome_vars:
                if outcome_var in df.columns:
                    lag_correlations[lag_var][outcome_var] = df[lag_var].corr(df[outcome_var])
        
        # Save lag analysis results
        lag_df = pd.DataFrame(lag_correlations)
        lag_df.to_csv(config.REPORTS_DIR / 'eda_lag_correlations.csv')
        logging.info("Lag correlation analysis saved to reports directory")

    else:
        logging.warning("DataFrame is None, skipping correlation analysis.")

def plot_time_series(df: pd.DataFrame):
    """
    Generates time series plots for key variables.
    """
    if df is not None and 'Year' in df.columns:
        logging.info("Generating time series plots...")

        # Plot dietary variables over time
        plt.figure(figsize=(15, 10))
        for var in DIETARY_VARS:
            if var in df.columns:
                plt.plot(df['Year'], df[var], label=var)
        plt.title('Dietary Variables Over Time')
        plt.xlabel('Year')
        plt.ylabel('Value')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.savefig(config.FIGURES_DIR / 'time_series_dietary.png')
        plt.close()

        # Plot health variables by category
        for category, vars_list in HEALTH_VARS.items():
            plt.figure(figsize=(15, 10))
            for var in vars_list:
                if var in df.columns:
                    plt.plot(df['Year'], df[var], label=var)
            plt.title(f'{category} Outcomes Over Time')
            plt.xlabel('Year')
            plt.ylabel('Value')
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.tight_layout()
            plt.savefig(config.FIGURES_DIR / f'time_series_health_{category.lower()}.png')
            plt.close()
        
        logging.info("Time series plots saved to figures directory")
    else:
        logging.warning("DataFrame is None or missing Year column, skipping time series plotting.")

if __name__ == '__main__':
    logging.info("Starting EDA process...")
    data = load_data_for_eda()
    if data is not None:
        perform_summary_statistics(data)
        plot_distributions(data)
        perform_correlation_analysis(data)
        plot_time_series(data)
        logging.info("EDA process completed successfully.")
    else:
        logging.error("Failed to load data. EDA process aborted.")