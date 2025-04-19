# src/models/regression.py
"""
Linear Regression Models for the Seed Oils ML project.

This module implements linear regression models to analyze relationships between
LA intake (with various lags) and health outcomes. All code and comments use
Australian English spelling.

Author: SeedoilsML Team
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Tuple, Optional
from pathlib import Path
import logging
from pydantic import BaseModel, Field
from src import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RegressionConfig(BaseModel):
    """Configuration for regression analysis."""
    output_dir: str = Field(..., description="Directory to save regression outputs")
    standardize: bool = Field(default=True, description="Whether to standardize features")
    test_size: float = Field(default=0.2, description="Proportion of data to use for testing")
    random_state: int = Field(default=42, description="Random seed for reproducibility")

class RegressionResult(BaseModel):
    """Model for storing regression results."""
    dependent_var: str
    independent_vars: List[str]
    r2_score: float
    coefficients: Dict[str, float]
    p_values: Dict[str, float]
    mse: float
    n_observations: int

def prepare_regression_data(
    df: pd.DataFrame,
    dependent_var: str,
    independent_vars: List[str],
    config: RegressionConfig
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Prepare data for regression analysis.
    
    Args:
        df: Input DataFrame
        dependent_var: Target variable name
        independent_vars: List of predictor variable names
        config: RegressionConfig object
    
    Returns:
        Tuple of X (features) and y (target) arrays
    """
    # Drop rows with missing values
    analysis_vars = [dependent_var] + independent_vars
    analysis_df = df[analysis_vars].dropna()
    
    X = analysis_df[independent_vars].values
    y = analysis_df[dependent_var].values
    
    if config.standardize:
        scaler = StandardScaler()
        X = scaler.fit_transform(X)
    
    return X, y

def fit_linear_regression(
    X: np.ndarray,
    y: np.ndarray,
    feature_names: List[str]
) -> Tuple[LinearRegression, Dict[str, float], Dict[str, float]]:
    """
    Fit linear regression model and calculate statistics.
    
    Args:
        X: Feature matrix
        y: Target vector
        feature_names: Names of features for coefficient mapping
    
    Returns:
        Tuple of (fitted model, coefficients dict, p-values dict)
    """
    model = LinearRegression()
    model.fit(X, y)
    
    # Calculate coefficients
    coefficients = dict(zip(feature_names, model.coef_))
    
    # Calculate p-values using statsmodels
    import statsmodels.api as sm
    X_with_const = sm.add_constant(X)
    model_sm = sm.OLS(y, X_with_const).fit()
    p_values = dict(zip(feature_names, model_sm.pvalues[1:]))  # Skip constant
    
    return model, coefficients, p_values

def plot_regression_results(
    X: np.ndarray,
    y: np.ndarray,
    model: LinearRegression,
    feature_names: List[str],
    dependent_var: str,
    config: RegressionConfig
):
    """
    Generate plots for regression analysis.
    
    Args:
        X: Feature matrix
        y: Target vector
        model: Fitted LinearRegression model
        feature_names: Names of features
        dependent_var: Name of target variable
        config: RegressionConfig object
    """
    # Predicted vs Actual plot
    y_pred = model.predict(X)
    plt.figure(figsize=(10, 6))
    plt.scatter(y, y_pred, alpha=0.5)
    plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', lw=2)
    plt.xlabel('Actual Values')
    plt.ylabel('Predicted Values')
    plt.title(f'Actual vs Predicted: {dependent_var}')
    plt.tight_layout()
    plt.savefig(f"{config.output_dir}/regression_actual_vs_predicted_{dependent_var.lower()}.png")
    plt.close()
    
    # Coefficient plot
    plt.figure(figsize=(12, 6))
    coef_df = pd.DataFrame({
        'Feature': feature_names,
        'Coefficient': model.coef_
    })
    sns.barplot(data=coef_df, x='Feature', y='Coefficient')
    plt.xticks(rotation=45)
    plt.title(f'Feature Coefficients: {dependent_var}')
    plt.tight_layout()
    plt.savefig(f"{config.output_dir}/regression_coefficients_{dependent_var.lower()}.png")
    plt.close()

def run_regression_analysis(
    df: pd.DataFrame,
    dependent_var: str,
    independent_vars: List[str],
    config: Optional[RegressionConfig] = None
) -> RegressionResult:
    """
    Run complete regression analysis for a given dependent variable.
    
    Args:
        df: Input DataFrame
        dependent_var: Target variable name
        independent_vars: List of predictor variable names
        config: Optional RegressionConfig object
    
    Returns:
        RegressionResult object with analysis results
    """
    if config is None:
        config = RegressionConfig(output_dir=str(config.FIGURES_DIR))
    
    logger.info(f"Running regression analysis for {dependent_var}")
    
    # Prepare data
    X, y = prepare_regression_data(df, dependent_var, independent_vars, config)
    
    if len(y) < 10:
        logger.warning(f"Insufficient data points ({len(y)}) for reliable regression")
        return None
    
    # Fit model and get statistics
    model, coefficients, p_values = fit_linear_regression(X, y, independent_vars)
    
    # Calculate metrics
    y_pred = model.predict(X)
    r2 = r2_score(y, y_pred)
    mse = mean_squared_error(y, y_pred)
    
    # Generate plots
    plot_regression_results(X, y, model, independent_vars, dependent_var, config)
    
    # Create and return results
    result = RegressionResult(
        dependent_var=dependent_var,
        independent_vars=independent_vars,
        r2_score=r2,
        coefficients=coefficients,
        p_values=p_values,
        mse=mse,
        n_observations=len(y)
    )
    
    logger.info(f"Regression analysis completed for {dependent_var}")
    logger.info(f"R² score: {r2:.3f}")
    logger.info(f"MSE: {mse:.3f}")
    logger.info(f"Number of observations: {len(y)}")
    
    return result

def analyze_all_health_outcomes(df: pd.DataFrame, config: Optional[RegressionConfig] = None):
    """
    Run regression analyses for all health outcomes against LA intake and its lags.
    
    Args:
        df: Input DataFrame
        config: Optional RegressionConfig object
    """
    if config is None:
        config = RegressionConfig(output_dir=str(config.FIGURES_DIR))
    
    # Define health outcomes to analyze
    health_outcomes = {
        'Obesity': ['Obesity_Prevalence_AgeStandardised'],
        'Diabetes': ['Diabetes_Prevalence_Rate_AgeStandardised'],
        'CVD': ['CVD_Mortality_Rate_ASMR', 'CVD_Prevalence_Rate_GBD'],
        'Dementia': ['Dementia_Mortality_Rate_ASMR', 'Dementia_Prevalence_Rate_GBD']
    }
    
    # Define predictors (including lags)
    base_predictors = ['LA_Intake_percent_calories', 'Plant_Fat_Ratio', 'Total_Fat_Supply_g']
    lag_predictors = ['LA_perc_kcal_lag5', 'LA_perc_kcal_lag10', 'LA_perc_kcal_lag15', 'LA_perc_kcal_lag20']
    
    results = []
    
    for category, outcomes in health_outcomes.items():
        logger.info(f"\nAnalyzing {category} outcomes...")
        
        for outcome in outcomes:
            if outcome in df.columns:
                # Run regression with current LA intake and other dietary factors
                current_result = run_regression_analysis(
                    df, outcome, base_predictors, config
                )
                if current_result:
                    results.append(current_result)
                
                # Run regression with lagged LA intake
                lag_result = run_regression_analysis(
                    df, outcome, lag_predictors, config
                )
                if lag_result:
                    results.append(lag_result)
            else:
                logger.warning(f"Outcome variable {outcome} not found in dataset")
    
    return results

if __name__ == "__main__":
    # Load the analytical dataset
    try:
        df = pd.read_csv(config.ANALYTICAL_DATA_FINAL_FILE)
        logger.info("Loaded analytical dataset")
        
        # Create output directory if it doesn't exist
        config.FIGURES_DIR.mkdir(parents=True, exist_ok=True)
        
        # Run analyses
        regression_config = RegressionConfig(output_dir=str(config.FIGURES_DIR))
        results = analyze_all_health_outcomes(df, regression_config)
        
        # Save summary results
        summary_rows = []
        for result in results:
            summary_rows.append({
                'Dependent Variable': result.dependent_var,
                'R² Score': result.r2_score,
                'MSE': result.mse,
                'N': result.n_observations,
                'Significant Predictors': [f"{var} (p={p:.3f})" 
                                        for var, p in result.p_values.items() 
                                        if p < 0.05]
            })
        
        summary_df = pd.DataFrame(summary_rows)
        summary_df.to_csv(config.REPORTS_DIR / 'regression_summary.csv', index=False)
        logger.info("Analysis complete. Results saved to regression_summary.csv")
        
    except Exception as e:
        logger.error(f"Error in regression analysis: {e}")
        raise