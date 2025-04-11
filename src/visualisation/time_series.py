"""
Time Series Visualisation module for the unified Australian dataset.

Provides functions for plotting time series trends, including overlays for multiple variables.
All code and comments use Australian English.

Author: SeedoilsML Team
"""

from typing import Optional, List
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pydantic import BaseModel, Field

class TimeSeriesConfig(BaseModel):
    """Configuration for time series plots."""
    output_dir: str = Field(..., description="Directory to save time series plots")
    show_plots: bool = Field(default=True, description="Whether to display plots interactively")
    date_col: str = Field(..., description="Name of the date or year column")
    variables: Optional[List[str]] = Field(default=None, description="Variables to plot")

def plot_time_series(
    df: pd.DataFrame,
    config: TimeSeriesConfig
) -> None:
    """
    Plot time series for selected variables.

    Args:
        df (pd.DataFrame): Input data.
        config (TimeSeriesConfig): Configuration for plotting.
    """
    variables = config.variables or df.select_dtypes(include='number').columns.tolist()
    for var in variables:
        plt.figure(figsize=(10, 6))
        sns.lineplot(x=df[config.date_col], y=df[var])
        plt.title(f"Time Series of {var}")
        plt.xlabel(config.date_col)
        plt.ylabel(var)
        if config.output_dir:
            plt.savefig(f"{config.output_dir}/time_series_{var}.png", dpi=150)
        if config.show_plots:
            plt.show()
        plt.close()

def overlay_time_series(
    df: pd.DataFrame,
    variables: List[str],
    config: TimeSeriesConfig
) -> None:
    """
    Overlay multiple time series on a single plot.

    Args:
        df (pd.DataFrame): Input data.
        variables (List[str]): Variables to overlay.
        config (TimeSeriesConfig): Configuration for plotting.
    """
    plt.figure(figsize=(12, 7))
    for var in variables:
        sns.lineplot(x=df[config.date_col], y=df[var], label=var)
    plt.title("Overlayed Time Series")
    plt.xlabel(config.date_col)
    plt.ylabel("Value")
    plt.legend()
    if config.output_dir:
        plt.savefig(f"{config.output_dir}/overlay_time_series.png", dpi=150)
    if config.show_plots:
        plt.show()
    plt.close()