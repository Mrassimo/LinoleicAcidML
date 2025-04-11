"""
Regression Visualisation module for the unified Australian dataset.

Provides functions for linear regression and Generalised Additive Models (GAMs).
All code and comments use Australian English.

Author: SeedoilsML Team
"""

from typing import Optional, List
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pydantic import BaseModel, Field

from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
try:
    from pygam import LinearGAM, s
except ImportError:
    LinearGAM = None  # type: ignore

class RegressionConfig(BaseModel):
    """Configuration for regression visualisations."""
    output_dir: str = Field(..., description="Directory to save regression plots")
    show_plots: bool = Field(default=True, description="Whether to display plots interactively")

def plot_linear_regression(
    df: pd.DataFrame,
    x: str,
    y: str,
    config: Optional[RegressionConfig] = None
) -> None:
    """
    Fit and plot a linear regression between two variables.

    Args:
        df (pd.DataFrame): Input data.
        x (str): Predictor variable.
        y (str): Response variable.
        config (RegressionConfig, optional): Configuration for output and display.
    """
    X = df[[x]].dropna()
    y_vals = df.loc[X.index, y]
    model = LinearRegression()
    model.fit(X, y_vals)
    y_pred = model.predict(X)
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=X[x], y=y_vals, label="Observed")
    plt.plot(X[x], y_pred, color="red", label="Linear Fit")
    plt.title(f"Linear Regression: {y} ~ {x}")
    plt.xlabel(x)
    plt.ylabel(y)
    plt.legend()
    if config and config.output_dir:
        plt.savefig(f"{config.output_dir}/linear_regression_{y}_on_{x}.png", dpi=150)
    if config is None or config.show_plots:
        plt.show()
    plt.close()

def plot_gam(
    df: pd.DataFrame,
    x: str,
    y: str,
    config: Optional[RegressionConfig] = None
) -> None:
    """
    Fit and plot a Generalised Additive Model (GAM) between two variables.

    Args:
        df (pd.DataFrame): Input data.
        x (str): Predictor variable.
        y (str): Response variable.
        config (RegressionConfig, optional): Configuration for output and display.
    """
    if LinearGAM is None:
        raise ImportError("pygam is not installed. Please install pygam to use GAM visualisation.")
    X = df[[x]].dropna()
    y_vals = df.loc[X.index, y]
    gam = LinearGAM(s(0)).fit(X, y_vals)
    XX = pd.DataFrame({x: np.linspace(X[x].min(), X[x].max(), 100)})
    y_gam = gam.predict(XX)
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=X[x], y=y_vals, label="Observed")
    plt.plot(XX[x], y_gam, color="green", label="GAM Fit")
    plt.title(f"GAM: {y} ~ s({x})")
    plt.xlabel(x)
    plt.ylabel(y)
    plt.legend()
    if config and config.output_dir:
        plt.savefig(f"{config.output_dir}/gam_{y}_on_{x}.png", dpi=150)
    if config is None or config.show_plots:
        plt.show()
    plt.close()