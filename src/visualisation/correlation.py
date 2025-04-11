"""
Correlation Visualisation module for the unified Australian dataset.

Provides functions for correlation heatmaps and rolling window correlations.
All code and comments use Australian English.

Author: SeedoilsML Team
"""

from typing import Optional, List
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pydantic import BaseModel, Field

class CorrelationConfig(BaseModel):
    """Configuration for correlation visualisations."""
    output_dir: str = Field(..., description="Directory to save correlation plots")
    show_plots: bool = Field(default=True, description="Whether to display plots interactively")
    method: str = Field(default="pearson", description="Correlation method: 'pearson', 'spearman', or 'kendall'")

def plot_correlation_heatmap(
    df: pd.DataFrame,
    variables: Optional[List[str]] = None,
    config: Optional[CorrelationConfig] = None
) -> None:
    """
    Plot a correlation matrix heatmap for selected variables.

    Args:
        df (pd.DataFrame): Input data.
        variables (List[str], optional): Variables to include. If None, all numeric columns are used.
        config (CorrelationConfig, optional): Configuration for output and display.
    """
    if variables is None:
        variables = df.select_dtypes(include='number').columns.tolist()
    corr = df[variables].corr(method=config.method if config else "pearson")
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Heatmap")
    if config and config.output_dir:
        plt.savefig(f"{config.output_dir}/correlation_heatmap.png", dpi=150)
    if config is None or config.show_plots:
        plt.show()
    plt.close()

def plot_rolling_correlation(
    df: pd.DataFrame,
    var1: str,
    var2: str,
    window: int,
    config: Optional[CorrelationConfig] = None
) -> None:
    """
    Plot rolling window correlation between two variables.

    Args:
        df (pd.DataFrame): Input data.
        var1 (str): First variable.
        var2 (str): Second variable.
        window (int): Rolling window size.
        config (CorrelationConfig, optional): Configuration for output and display.
    """
    rolling_corr = df[var1].rolling(window).corr(df[var2])
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, rolling_corr, label=f"Rolling Corr ({var1}, {var2})")
    plt.title(f"Rolling Correlation ({window}-period) between {var1} and {var2}")
    plt.xlabel("Index")
    plt.ylabel("Correlation")
    plt.legend()
    if config and config.output_dir:
        plt.savefig(f"{config.output_dir}/rolling_corr_{var1}_{var2}.png", dpi=150)
    if config is None or config.show_plots:
        plt.show()
    plt.close()