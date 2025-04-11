"""
Exploratory Data Analysis (EDA) module for the unified Australian dataset.

Provides functions for summary statistics, distribution plots, and initial data inspection.
All code and comments use Australian English.

Author: SeedoilsML Team
"""

from typing import Optional
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pydantic import BaseModel, Field

class EDAConfig(BaseModel):
    """Configuration for EDA visualisations."""
    output_dir: str = Field(..., description="Directory to save EDA plots")
    show_plots: bool = Field(default=True, description="Whether to display plots interactively")

def summary_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate summary statistics for the provided DataFrame.

    Args:
        df (pd.DataFrame): Input data.

    Returns:
        pd.DataFrame: Summary statistics.
    """
    return df.describe(include='all')

def plot_distributions(
    df: pd.DataFrame,
    columns: Optional[list[str]] = None,
    config: Optional[EDAConfig] = None
) -> None:
    """
    Plot distributions (histograms and KDEs) for selected columns.

    Args:
        df (pd.DataFrame): Input data.
        columns (list[str], optional): Columns to plot. If None, all numeric columns are used.
        config (EDAConfig, optional): Configuration for output and display.
    """
    if columns is None:
        columns = df.select_dtypes(include='number').columns.tolist()
    for col in columns:
        plt.figure(figsize=(8, 5))
        sns.histplot(df[col].dropna(), kde=True, bins=30)
        plt.title(f"Distribution of {col}")
        plt.xlabel(col)
        plt.ylabel("Frequency")
        if config and config.output_dir:
            plt.savefig(f"{config.output_dir}/distribution_{col}.png", dpi=150)
        if config is None or config.show_plots:
            plt.show()
        plt.close()

def eda_report(
    df: pd.DataFrame,
    config: Optional[EDAConfig] = None
) -> None:
    """
    Run a standard EDA report: summary stats and distributions.

    Args:
        df (pd.DataFrame): Input data.
        config (EDAConfig, optional): Configuration for output and display.
    """
    stats = summary_statistics(df)
    if config and config.output_dir:
        stats.to_csv(f"{config.output_dir}/summary_statistics.csv")
    print("Summary statistics:")
    print(stats)
    plot_distributions(df, config=config)