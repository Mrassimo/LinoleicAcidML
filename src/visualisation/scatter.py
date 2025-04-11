"""
Scatter Plot Visualisation module for the unified Australian dataset.

Provides functions for overlay and lagged scatter plots.
All code and comments use Australian English.

Author: SeedoilsML Team
"""

from typing import Optional, List
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pydantic import BaseModel, Field

class ScatterConfig(BaseModel):
    """Configuration for scatter plot visualisations."""
    output_dir: str = Field(..., description="Directory to save scatter plots")
    show_plots: bool = Field(default=True, description="Whether to display plots interactively")
    lag: int = Field(default=0, description="Lag to apply to the x variable (for lagged scatter plots)")

def plot_scatter(
    df: pd.DataFrame,
    x: str,
    y: str,
    config: Optional[ScatterConfig] = None
) -> None:
    """
    Plot a standard scatter plot between two variables.

    Args:
        df (pd.DataFrame): Input data.
        x (str): X-axis variable.
        y (str): Y-axis variable.
        config (ScatterConfig, optional): Configuration for output and display.
    """
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=df[x], y=df[y])
    plt.title(f"Scatter Plot: {x} vs {y}")
    plt.xlabel(x)
    plt.ylabel(y)
    if config and config.output_dir:
        plt.savefig(f"{config.output_dir}/scatter_{x}_vs_{y}.png", dpi=150)
    if config is None or config.show_plots:
        plt.show()
    plt.close()

def plot_lagged_scatter(
    df: pd.DataFrame,
    x: str,
    y: str,
    config: Optional[ScatterConfig] = None
) -> None:
    """
    Plot a lagged scatter plot (x variable lagged by config.lag periods).

    Args:
        df (pd.DataFrame): Input data.
        x (str): X-axis variable (to be lagged).
        y (str): Y-axis variable.
        config (ScatterConfig, optional): Configuration for output and display.
    """
    lag = config.lag if config else 1
    x_lagged = df[x].shift(lag)
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=x_lagged, y=df[y])
    plt.title(f"Lagged Scatter Plot: {x} (lag {lag}) vs {y}")
    plt.xlabel(f"{x} (lag {lag})")
    plt.ylabel(y)
    if config and config.output_dir:
        plt.savefig(f"{config.output_dir}/lagged_scatter_{x}_lag{lag}_vs_{y}.png", dpi=150)
    if config is None or config.show_plots:
        plt.show()
    plt.close()

def overlay_scatter(
    df: pd.DataFrame,
    x: str,
    y_list: List[str],
    config: Optional[ScatterConfig] = None
) -> None:
    """
    Overlay multiple scatter plots with a shared x variable.

    Args:
        df (pd.DataFrame): Input data.
        x (str): X-axis variable.
        y_list (List[str]): List of Y-axis variables to overlay.
        config (ScatterConfig, optional): Configuration for output and display.
    """
    plt.figure(figsize=(10, 7))
    for y in y_list:
        sns.scatterplot(x=df[x], y=df[y], label=y)
    plt.title(f"Overlayed Scatter Plots: {x} vs Multiple Variables")
    plt.xlabel(x)
    plt.ylabel("Value")
    plt.legend()
    if config and config.output_dir:
        plt.savefig(f"{config.output_dir}/overlay_scatter_{x}_vs_multiple.png", dpi=150)
    if config is None or config.show_plots:
        plt.show()
    plt.close()