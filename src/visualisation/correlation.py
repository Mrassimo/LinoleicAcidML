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
    config: Optional[CorrelationConfig] = None,
    title: str = "Correlation Heatmap",
    caption: Optional[str] = None
) -> plt.Figure:
    """
    Plot an enhanced correlation matrix heatmap with improved clarity and accessibility.

    Args:
        df (pd.DataFrame): Input data.
        variables (List[str], optional): Variables to include. If None, all numeric columns are used.
        config (CorrelationConfig, optional): Configuration for output and display.
        title (str): Plot title.
        caption (str, optional): Caption text to add below the heatmap.

    Returns:
        plt.Figure: The generated figure for further customization.
    """
    if variables is None:
        # Default to key health and LA variables if none specified
        variables = [
            'LA_Intake_percent_calories',
            'LA_perc_kcal_lag5', 'LA_perc_kcal_lag10',
            'LA_perc_kcal_lag15', 'LA_perc_kcal_lag20',
            'Obesity_Prevalence_AgeStandardised',
            'Diabetes_Prevalence_Rate_AgeStandardised',
            'CVD_Mortality_Rate_ASMR'
        ]
        variables = [v for v in variables if v in df.columns]

    corr = df[variables].corr(method=config.method if config else "pearson")

    fig, ax = plt.subplots(figsize=(14, 12))
    # Reason: Use a colourblind-friendly palette for accessibility
    sns.heatmap(
        corr,
        annot=True,
        cmap="YlGnBu",
        fmt=".2f",
        ax=ax,
        annot_kws={"fontsize": 15},
        cbar_kws={"label": "Correlation coefficient", "shrink": 0.8}
    )
    ax.set_title(title, fontsize=24, fontweight="bold", pad=24)
    ax.tick_params(axis="x", labelsize=15, rotation=45)
    ax.tick_params(axis="y", labelsize=15, rotation=0)

    if caption:
        fig.text(
            0.5, -0.08,
            caption,
            ha='center',
            fontsize=15,
            wrap=True
        )
        plt.subplots_adjust(bottom=0.18)

    if config and config.output_dir:
        fig.savefig(
            f"{config.output_dir}/correlation_heatmap.png",
            dpi=300,
            bbox_inches='tight'
        )
    if config is None or config.show_plots:
        plt.show()

    return fig

def plot_rolling_correlation(
    df: pd.DataFrame,
    var1: str,
    var2: str,
    window: int,
    config: Optional[CorrelationConfig] = None,
    caption: str = None
) -> None:
    """
    Plot rolling window correlation between two variables with enhanced clarity.

    Args:
        df (pd.DataFrame): Input data.
        var1 (str): First variable.
        var2 (str): Second variable.
        window (int): Rolling window size.
        config (CorrelationConfig, optional): Configuration for output and display.
        caption (str, optional): Explanatory caption to add below the plot.
    """
    rolling_corr = df[var1].rolling(window).corr(df[var2])
    plt.figure(figsize=(12, 7))
    plt.plot(df.index, rolling_corr, label=f"Rolling Corr ({var1}, {var2})", linewidth=2.5, color="#0072B2")
    plt.title(f"Rolling Correlation ({window}-period) between {var1} and {var2}", fontsize=20, fontweight="bold")
    plt.xlabel("Index", fontsize=16)
    plt.ylabel("Correlation", fontsize=16)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.legend(fontsize=14)
    if caption:
        plt.figtext(0.5, -0.08, caption, ha='center', fontsize=13, wrap=True)
        plt.subplots_adjust(bottom=0.18)
    if config and config.output_dir:
        plt.savefig(f"{config.output_dir}/rolling_corr_{var1}_{var2}.png", dpi=300, bbox_inches='tight')
    if config is None or config.show_plots:
        plt.show()
    plt.close()