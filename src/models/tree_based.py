"""
Tree-based models for the Seed Oils ML project.

This module implements tree-based models (Random Forest, XGBoost) for analysing
relationships between dietary patterns and health outcomes.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score
import xgboost as xgb
import matplotlib.pyplot as plt
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TreeModelConfig(BaseModel):
    """Configuration for tree-based models."""
    target_variable: str
    feature_columns: List[str]
    test_size: float = 0.2
    random_state: int = 42
    n_estimators: int = 100
    max_depth: Optional[int] = None
    cv_folds: int = 5

def prepare_tree_data(
    df: pd.DataFrame,
    config: TreeModelConfig
) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
    """
    Prepares data for tree-based models by splitting features and target,
    and creating train/test splits respecting time series nature of data.

    Args:
        df (pd.DataFrame): Input dataframe
        config (TreeModelConfig): Model configuration

    Returns:
        Tuple containing X_train, y_train, X_test, y_test
    """
    logging.info(f"Preparing data for tree-based models, target: {config.target_variable}")
    try:
        # Sort by year to respect time series nature
        df = df.sort_index()
        
        # Split features and target
        X = df[config.feature_columns]
        y = df[config.target_variable]
        
        # Calculate split point
        split_idx = int(len(df) * (1 - config.test_size))
        
        # Split data
        X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
        y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
        
        logging.info(f"Data prepared. Train size: {len(X_train)}, Test size: {len(X_test)}")
        return X_train, y_train, X_test, y_test
    
    except Exception as e:
        logging.error(f"Error preparing tree data: {e}")
        raise

def fit_random_forest(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    config: TreeModelConfig
) -> RandomForestRegressor:
    """
    Fits a Random Forest model to the training data.

    Args:
        X_train (pd.DataFrame): Training features
        y_train (pd.Series): Training target
        config (TreeModelConfig): Model configuration

    Returns:
        Fitted Random Forest model
    """
    logging.info("Fitting Random Forest model...")
    try:
        model = RandomForestRegressor(
            n_estimators=config.n_estimators,
            max_depth=config.max_depth,
            random_state=config.random_state
        )
        model.fit(X_train, y_train)
        logging.info("Random Forest model fitted successfully")
        return model
    
    except Exception as e:
        logging.error(f"Error fitting Random Forest model: {e}")
        raise

def fit_xgboost(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    config: TreeModelConfig
) -> xgb.XGBRegressor:
    """
    Fits an XGBoost model to the training data.

    Args:
        X_train (pd.DataFrame): Training features
        y_train (pd.Series): Training target
        config (TreeModelConfig): Model configuration

    Returns:
        Fitted XGBoost model
    """
    logging.info("Fitting XGBoost model...")
    try:
        model = xgb.XGBRegressor(
            n_estimators=config.n_estimators,
            max_depth=config.max_depth if config.max_depth else 6,
            random_state=config.random_state
        )
        model.fit(X_train, y_train)
        logging.info("XGBoost model fitted successfully")
        return model
    
    except Exception as e:
        logging.error(f"Error fitting XGBoost model: {e}")
        raise

def evaluate_tree_model(
    model: Union[RandomForestRegressor, xgb.XGBRegressor],
    X_test: pd.DataFrame,
    y_test: pd.Series,
    model_name: str
) -> Dict[str, float]:
    """
    Evaluates a tree-based model using various metrics.

    Args:
        model: Fitted tree-based model
        X_test (pd.DataFrame): Test features
        y_test (pd.Series): Test target
        model_name (str): Name of the model for logging

    Returns:
        Dictionary of evaluation metrics
    """
    logging.info(f"Evaluating {model_name}...")
    try:
        # Make predictions
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        metrics = {
            'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
            'r2': r2_score(y_test, y_pred)
        }
        
        logging.info(f"{model_name} evaluation metrics: {metrics}")
        return metrics
    
    except Exception as e:
        logging.error(f"Error evaluating {model_name}: {e}")
        raise

def plot_feature_importance(
    model: Union[RandomForestRegressor, xgb.XGBRegressor],
    feature_names: List[str],
    output_dir: Path,
    model_name: str
):
    """
    Plots and saves feature importance for tree-based models.

    Args:
        model: Fitted tree-based model
        feature_names (List[str]): List of feature names
        output_dir (Path): Directory to save the plot
        model_name (str): Name of the model for the plot title
    """
    logging.info(f"Plotting feature importance for {model_name}...")
    try:
        # Ensure output directory exists
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Get feature importance
        if isinstance(model, RandomForestRegressor):
            importance = model.feature_importances_
        else:  # XGBoost
            importance = model.feature_importances_
            
        # Create DataFrame for plotting
        importance_df = pd.DataFrame({
            'feature': feature_names,
            'importance': importance
        }).sort_values('importance', ascending=True)
        
        # Plot
        plt.figure(figsize=(10, 6))
        plt.barh(importance_df['feature'], importance_df['importance'])
        plt.title(f'Feature Importance - {model_name}')
        plt.xlabel('Importance')
        
        # Save plot
        plot_path = output_dir / f'feature_importance_{model_name}.png'
        plt.savefig(plot_path, bbox_inches='tight')
        plt.close()
        
        logging.info(f"Feature importance plot saved to {plot_path}")
        
    except Exception as e:
        logging.error(f"Error plotting feature importance for {model_name}: {e}")
        raise

if __name__ == '__main__':
    logging.info("Running tree-based models example...")
    
    # Create dummy data
    np.random.seed(42)
    n_samples = 100
    dummy_df = pd.DataFrame({
        'LA_Intake': np.random.normal(10, 2, n_samples),
        'Plant_Fat_Ratio': np.random.normal(0.5, 0.1, n_samples),
        'Total_Calories': np.random.normal(2500, 200, n_samples),
        'BMI': 25 + 0.5 * np.random.normal(10, 2, n_samples) + 0.3 * np.random.normal(0.5, 0.1, n_samples)
    })
    
    # Configure model
    config = TreeModelConfig(
        target_variable='BMI',
        feature_columns=['LA_Intake', 'Plant_Fat_Ratio', 'Total_Calories'],
        test_size=0.2,
        n_estimators=100,
        max_depth=5
    )
    
    try:
        # Prepare data
        X_train, y_train, X_test, y_test = prepare_tree_data(dummy_df, config)
        
        # Fit and evaluate Random Forest
        rf_model = fit_random_forest(X_train, y_train, config)
        rf_metrics = evaluate_tree_model(rf_model, X_test, y_test, "Random Forest")
        
        # Fit and evaluate XGBoost
        xgb_model = fit_xgboost(X_train, y_train, config)
        xgb_metrics = evaluate_tree_model(xgb_model, X_test, y_test, "XGBoost")
        
        # Plot feature importance
        output_dir = Path("./figures/tree_based")
        plot_feature_importance(rf_model, config.feature_columns, output_dir, "Random Forest")
        plot_feature_importance(xgb_model, config.feature_columns, output_dir, "XGBoost")
        
        logging.info("Tree-based models example completed successfully")
        
    except Exception as e:
        logging.error(f"Error in tree-based models example: {e}") 