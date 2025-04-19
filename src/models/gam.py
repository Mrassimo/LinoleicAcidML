# src/models/gam.py
"""
Generalised Additive Model (GAM) functions for the Seed Oils ML project.

This module implements GAMs to analyze non-linear relationships between
LA intake (with various lags) and health outcomes. All code and comments use
Australian English spelling.

Author: SeedoilsML Team
"""

import pandas as pd
import numpy as np
from pygam import LinearGAM, s, f, te  # Added tensor product smooth
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
import logging
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from pydantic import BaseModel, Field

from src import config

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GAMConfig(BaseModel):
    """Configuration for GAM analysis."""
    output_dir: str = Field(..., description="Directory to save GAM outputs")
    standardize: bool = Field(default=True, description="Whether to standardize features")
    cv_folds: int = Field(default=5, description="Number of cross-validation folds")
    random_state: int = Field(default=42, description="Random seed for reproducibility")
    n_splines: List[int] = Field(default=[10], description="Number of splines to try for each feature")
    lam_candidates: List[float] = Field(
        default=[0.1, 1.0, 10.0], 
        description="Smoothing parameter candidates"
    )

def prepare_gam_data(df: pd.DataFrame, feature_columns: list[str], target_column: str):
    """
    Prepares data specifically for pygam by selecting features/target and handling missing values.

    Args:
        df (pd.DataFrame): The input DataFrame.
        feature_columns (list[str]): List of column names to use as features.
        target_column (str): The name of the target column.

    Returns:
        tuple: Tuple containing X (features numpy array) and y (target numpy array), or (None, None) if preparation fails.
    """
    logging.info("Preparing data for GAM...")
    try:
        # Select relevant columns
        selected_cols = feature_columns + [target_column]
        df_selected = df[selected_cols].copy()

        # Handle missing values by dropping rows with NaNs in selected columns
        initial_rows = len(df_selected)
        df_cleaned = df_selected.dropna()
        rows_dropped = initial_rows - len(df_cleaned)
        if rows_dropped > 0:
            logging.warning(f"Dropped {rows_dropped} rows with missing values during GAM data preparation.")

        if df_cleaned.empty:
            logging.error("DataFrame is empty after dropping rows with missing values.")
            return None, None

        # Separate features (X) and target (y)
        X = df_cleaned[feature_columns]
        y = df_cleaned[target_column]

        logging.info(f"Data prepared: X shape {X.shape}, y shape {y.shape}")
        return X.values, y.values # Return numpy arrays as often preferred by pygam

    except KeyError as e:
        logging.error(f"Missing required column in DataFrame: {e}")
        return None, None
    except Exception as e:
        logging.error(f"Error preparing GAM data: {e}")
        return None, None

def select_optimal_gam(X: np.ndarray, y: np.ndarray, feature_names: List[str], config: GAMConfig) -> Tuple[LinearGAM, Dict]:
    """
    Performs cross-validation to select optimal GAM hyperparameters.
    
    Args:
        X: Feature matrix
        y: Target vector
        feature_names: Names of features
        config: GAMConfig object
    
    Returns:
        Tuple of (best GAM model, dict with cv results)
    """
    logger.info("Selecting optimal GAM parameters via cross-validation...")
    
    best_score = -np.inf
    best_params = None
    best_model = None
    cv_results = []
    
    kf = KFold(n_splits=config.cv_folds, shuffle=True, random_state=config.random_state)
    
    for n_splines in config.n_splines:
        for lam in config.lam_candidates:
            # Create terms with current n_splines
            terms = sum(s(i, n_splines=n_splines) for i in range(X.shape[1]))
            
            # Cross-validation
            fold_scores = []
            for train_idx, val_idx in kf.split(X):
                X_train, X_val = X[train_idx], X[val_idx]
                y_train, y_val = y[train_idx], y[val_idx]
                
                try:
                    # Fit GAM
                    gam = LinearGAM(terms=terms, lam=lam)
                    gam.fit(X_train, y_train)
                    
                    # Evaluate
                    y_pred = gam.predict(X_val)
                    score = r2_score(y_val, y_pred)
                    fold_scores.append(score)
                except Exception as e:
                    logger.warning(f"Error in CV fold with n_splines={n_splines}, lam={lam}: {e}")
                    continue
            
            if fold_scores:
                mean_score = np.mean(fold_scores)
                std_score = np.std(fold_scores)
                
                cv_results.append({
                    'n_splines': n_splines,
                    'lambda': lam,
                    'mean_r2': mean_score,
                    'std_r2': std_score
                })
                
                if mean_score > best_score:
                    best_score = mean_score
                    best_params = {'n_splines': n_splines, 'lambda': lam}
    
    if best_params:
        # Fit final model with best parameters
        terms = sum(s(i, n_splines=best_params['n_splines']) for i in range(X.shape[1]))
        best_model = LinearGAM(terms=terms, lam=best_params['lambda'])
        best_model.fit(X, y)
        logger.info(f"Selected optimal parameters: n_splines={best_params['n_splines']}, lambda={best_params['lambda']}")
        logger.info(f"Best cross-validated R² score: {best_score:.3f}")
    else:
        logger.error("Failed to find optimal parameters")
        return None, {'cv_results': cv_results}
    
    return best_model, {
        'cv_results': cv_results,
        'best_params': best_params,
        'best_score': best_score
    }

def analyze_health_outcome(
    df: pd.DataFrame,
    outcome_var: str,
    predictors: List[str],
    config: GAMConfig
) -> Dict:
    """
    Analyzes a single health outcome using GAM.
    
    Args:
        df: Input DataFrame
        outcome_var: Name of the health outcome variable
        predictors: List of predictor variables
        config: GAMConfig object
    
    Returns:
        Dict containing analysis results
    """
    logger.info(f"\nAnalyzing {outcome_var} with GAM...")
    
    # Prepare data
    X, y = prepare_gam_data(df, predictors, outcome_var)
    if X is None or y is None:
        return None
    
    # Select optimal model
    model, cv_results = select_optimal_gam(X, y, predictors, config)
    if model is None:
        return None
    
    # Generate predictions and calculate metrics
    y_pred = model.predict(X)
    r2 = r2_score(y, y_pred)
    mse = mean_squared_error(y, y_pred)
    
    # Generate and save plots
    output_dir = Path(config.output_dir) / 'gam_analysis' / outcome_var.lower()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Plot partial dependence for each predictor
    for i, feature in enumerate(predictors):
        plot_partial_dependence(model, i, feature, output_dir)
    
    # Plot actual vs predicted
    plt.figure(figsize=(10, 6))
    plt.scatter(y, y_pred, alpha=0.5)
    plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', lw=2)
    plt.xlabel('Actual Values')
    plt.ylabel('Predicted Values')
    plt.title(f'Actual vs Predicted: {outcome_var}')
    plt.tight_layout()
    plt.savefig(output_dir / f'actual_vs_predicted.png')
    plt.close()
    
    return {
        'outcome': outcome_var,
        'model': model,
        'r2_score': r2,
        'mse': mse,
        'cv_results': cv_results,
        'n_observations': len(y)
    }

def plot_partial_dependence(gam_model, feature_index: int, feature_name: str, output_dir: Path):
    """
    Generates and saves partial dependence plots (PDPs) for a specified feature.

    Args:
        gam_model: The fitted pygam model object.
        feature_index (int): The index of the feature to plot PDP for.
        feature_name (str): The name of the feature (for labeling).
        output_dir (Path): The directory to save the plots.
    """
    logging.info(f"Generating PDP for feature '{feature_name}'...")
    if gam_model is not None:
        try:
            # Ensure output_dir exists
            output_dir.mkdir(parents=True, exist_ok=True)

            plt.figure(figsize=(10, 6))
            XX = gam_model.generate_X_grid(term=feature_index, n=100)
            pdep, confi = gam_model.partial_dependence(term=feature_index, X=XX, width=0.95)
            
            plt.plot(XX[:, feature_index], pdep, label=f'PDP for {feature_name}')
            plt.fill_between(
                XX[:, feature_index],
                confi[:, 0],
                confi[:, 1],
                alpha=0.2,
                color='grey',
                label='95% CI'
            )
            
            plt.title(f'Partial Dependence Plot: {feature_name}')
            plt.xlabel(feature_name)
            plt.ylabel('Partial Effect')
            plt.legend()
            plt.grid(True)
            
            plot_path = output_dir / f'pdp_{feature_name.lower().replace(" ", "_")}.png'
            plt.savefig(plot_path)
            plt.close()
            
            logging.info(f"Saved PDP for '{feature_name}' to {plot_path}")
        except Exception as e:
            logging.error(f"Error generating PDP for {feature_name}: {e}")
    else:
        logging.warning("GAM model object is None, skipping PDP plots.")

def analyze_all_health_outcomes(df: pd.DataFrame, config: Optional[GAMConfig] = None) -> List[Dict]:
    """
    Analyzes all health outcomes using GAMs.
    
    Args:
        df: Input DataFrame
        config: Optional GAMConfig object
    
    Returns:
        List of dictionaries containing analysis results for each outcome
    """
    if config is None:
        config = GAMConfig(output_dir=str(config.FIGURES_DIR))
    
    # Define health outcomes to analyze
    health_outcomes = {
        'Obesity': ['Obesity_Prevalence_AgeStandardised'],
        'Diabetes': ['Diabetes_Prevalence_Rate_AgeStandardised'],
        'CVD': ['CVD_Mortality_Rate_ASMR', 'CVD_Prevalence_Rate_IHME'],
        'Dementia': ['Dementia_Mortality_Rate_ASMR', 'Dementia_Prevalence_Rate_IHME']
    }
    
    # Define predictors (including lags)
    base_predictors = ['LA_Intake_percent_calories', 'Plant_Fat_Ratio', 'Total_Fat_Supply_g']
    lag_predictors = ['LA_perc_kcal_lag5', 'LA_perc_kcal_lag10', 'LA_perc_kcal_lag15', 'LA_perc_kcal_lag20']
    
    results = []
    
    for category, outcomes in health_outcomes.items():
        logger.info(f"\nAnalyzing {category} outcomes...")
        
        for outcome in outcomes:
            if outcome in df.columns:
                # Run GAM with current LA intake and other dietary factors
                current_result = analyze_health_outcome(
                    df, outcome, base_predictors, config
                )
                if current_result:
                    results.append(current_result)
                
                # Run GAM with lagged LA intake
                lag_result = analyze_health_outcome(
                    df, outcome, lag_predictors, config
                )
                if lag_result:
                    results.append(lag_result)
            else:
                logger.warning(f"Outcome variable {outcome} not found in dataset")
    
    return results

if __name__ == '__main__':
    # Set up logging
    logging.info("Starting GAM analysis...")
    
    try:
        # Load the analytical dataset
        df = pd.read_csv(config.ANALYTICAL_DATA_FINAL_FILE)
        logger.info("Loaded analytical dataset")
        
        # Create output directory if it doesn't exist
        config.FIGURES_DIR.mkdir(parents=True, exist_ok=True)
        
        # Configure GAM analysis
        gam_config = GAMConfig(
            output_dir=str(config.FIGURES_DIR),
            cv_folds=5,
            n_splines=[8, 10, 12],
            lam_candidates=[0.1, 1.0, 10.0]
        )
        
        # Run analyses
        results = analyze_all_health_outcomes(df, gam_config)
        
        # Save summary results
        summary_rows = []
        for result in results:
            if result:  # Skip None results
                summary_rows.append({
                    'Outcome Variable': result['outcome'],
                    'R² Score': result['r2_score'],
                    'MSE': result['mse'],
                    'N': result['n_observations'],
                    'Best CV Score': result['cv_results']['best_score'],
                    'Best n_splines': result['cv_results']['best_params']['n_splines'],
                    'Best lambda': result['cv_results']['best_params']['lambda']
                })
        
        summary_df = pd.DataFrame(summary_rows)
        summary_df.to_csv(config.REPORTS_DIR / 'gam_analysis_summary.csv', index=False)
        logger.info("Analysis complete. Results saved to gam_analysis_summary.csv")
        
    except Exception as e:
        logger.error(f"Error in GAM analysis: {e}")
        raise