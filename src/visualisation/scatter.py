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
import scipy.stats as stats

class ScatterConfig(BaseModel):
    """Configuration for scatter plot visualisations."""
    output_dir: str = Field(..., description="Directory to save scatter plots")
    show_plots: bool = Field(default=True, description="Whether to display plots interactively")
    lag: int = Field(default=0, description="Lag to apply to the x variable (for lagged scatter plots)")

def plot_scatter(
    df: pd.DataFrame,
    x: str,
    y: str,
    config: Optional[ScatterConfig] = None,
    caption: str = None
) -> None:
    """
    Plot a standard scatter plot between two variables with enhanced clarity.

    Args:
        df (pd.DataFrame): Input data.
        x (str): X-axis variable.
        y (str): Y-axis variable.
        config (ScatterConfig, optional): Configuration for output and display.
        caption (str, optional): Explanatory caption to add below the plot.
    """
    plt.figure(figsize=(10, 7))
    sns.set_palette("colorblind")  # Reason: Improve accessibility for colourblind viewers
    sns.scatterplot(x=df[x], y=df[y], s=80)
    plt.title(f"Scatter Plot: {x} vs {y}", fontsize=20, fontweight="bold")
    plt.xlabel(x, fontsize=16)
    plt.ylabel(y, fontsize=16)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    if caption:
        plt.figtext(0.5, -0.08, caption, ha='center', fontsize=13, wrap=True)
        plt.subplots_adjust(bottom=0.18)
    if config and config.output_dir:
        plt.savefig(f"{config.output_dir}/scatter_{x}_vs_{y}.png", dpi=300, bbox_inches='tight')
    if config is None or config.show_plots:
        plt.show()
    plt.close()

def plot_lagged_scatter(
    df: pd.DataFrame,
    x: str,
    y: str,
    config: Optional[ScatterConfig] = None,
    hue: Optional[str] = None,
    title: Optional[str] = None,
    caption: str = None
) -> plt.Figure:
    """
    Plot an enhanced lagged scatter plot with statistical annotations and improved clarity.

    Args:
        df (pd.DataFrame): Input data.
        x (str): X-axis variable (to be lagged).
        y (str): Y-axis variable.
        config (ScatterConfig, optional): Configuration for output and display.
        hue (str, optional): Variable for colour coding points.
        title (str, optional): Custom plot title.
        caption (str, optional): Explanatory caption to add below the plot.

    Returns:
        plt.Figure: The generated figure for further customization.
    """
    lag = config.lag if config else 1
    x_lagged = df[x].shift(lag)

    # Calculate correlation
    valid_mask = ~x_lagged.isna() & ~df[y].isna()
    r, p = stats.pearsonr(x_lagged[valid_mask], df[y][valid_mask])

    # Create plot
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.set_palette("colorblind")  # Reason: Improve accessibility for colourblind viewers
    sns.scatterplot(
        x=x_lagged,
        y=df[y],
        hue=df[hue] if hue else None,
        ax=ax,
        s=90,
        palette="colorblind" if hue else None
    )

    # Add regression line
    sns.regplot(
        x=x_lagged,
        y=df[y],
        scatter=False,
        ax=ax,
        color='red',
        line_kws={"linewidth": 2.5, "label": "Linear fit"}
    )

    # Set title and labels
    default_title = f"{y} vs. {lag}-Year Lagged {x}"
    ax.set_title(title or default_title, fontsize=20, fontweight="bold")
    ax.set_xlabel(f"{x} (lag {lag})", fontsize=16)
    ax.set_ylabel(y, fontsize=16)
    ax.tick_params(axis="x", labelsize=14)
    ax.tick_params(axis="y", labelsize=14)

    # Add correlation annotation with explanation
    ax.annotate(
        f"Pearson r = {r:.2f} (correlation)\np = {p:.3f} (significance)",
        xy=(0.05, 0.95),
        xycoords='axes fraction',
        fontsize=14,
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.85)
    )

    if hue:
        ax.legend(title=hue, fontsize=13)
    else:
        ax.legend(fontsize=13)

    if caption:
        fig.text(0.5, -0.08, caption, ha='center', fontsize=13, wrap=True)
        plt.subplots_adjust(bottom=0.18)
    if config and config.output_dir:
        fig.savefig(
            f"{config.output_dir}/lagged_scatter_{x}_lag{lag}_vs_{y}.png",
            dpi=300,
            bbox_inches='tight'
        )
    if config is None or config.show_plots:
        plt.show()

    return fig

def overlay_scatter(
    df: pd.DataFrame,
    x: str,
    y_list: List[str],
    config: Optional[ScatterConfig] = None,
    caption: str = None
) -> None:
    """
    Overlay multiple scatter plots with a shared x variable, with enhanced clarity.

    Args:
        df (pd.DataFrame): Input data.
        x (str): X-axis variable.
        y_list (List[str]): List of Y-axis variables to overlay.
        config (ScatterConfig, optional): Configuration for output and display.
        caption (str, optional): Explanatory caption to add below the plot.
    """
    plt.figure(figsize=(12, 8))
    sns.set_palette("colorblind")  # Reason: Improve accessibility for colourblind viewers
    for y in y_list:
        sns.scatterplot(x=df[x], y=df[y], label=y, s=80)
    plt.title(f"Overlayed Scatter Plots: {x} vs Multiple Variables", fontsize=20, fontweight="bold")
    plt.xlabel(x, fontsize=16)
    plt.ylabel("Value", fontsize=16)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.legend(fontsize=14)
    if caption:
        plt.figtext(0.5, -0.08, caption, ha='center', fontsize=13, wrap=True)
        plt.subplots_adjust(bottom=0.18)
    if config and config.output_dir:
        plt.savefig(f"{config.output_dir}/overlay_scatter_{x}_vs_multiple.png", dpi=300, bbox_inches='tight')
    if config is None or config.show_plots:
        plt.show()
    plt.close()