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
    config: TimeSeriesConfig,
    caption: str = None
) -> None:
    """
    Plot time series for selected variables with enhanced clarity and shareability.

    Args:
        df (pd.DataFrame): Input data.
        config (TimeSeriesConfig): Configuration for plotting.
        caption (str, optional): Explanatory caption to add below the plot.
    """
    variables = config.variables or df.select_dtypes(include='number').columns.tolist()
    for var in variables:
        plt.figure(figsize=(12, 7))
        sns.set_palette("colorblind")  # Reason: Improve accessibility for colourblind viewers
        sns.lineplot(x=df[config.date_col], y=df[var])
        plt.title(f"Time Series of {var}", fontsize=20, fontweight="bold")
        plt.xlabel(config.date_col, fontsize=16)
        plt.ylabel(var, fontsize=16)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        if caption:
            plt.figtext(0.5, -0.08, caption, ha='center', fontsize=13, wrap=True)
            plt.subplots_adjust(bottom=0.18)
        if config.output_dir:
            plt.savefig(f"{config.output_dir}/time_series_{var}.png", dpi=300, bbox_inches='tight')
        if config.show_plots:
            plt.show()
        plt.close()

def plot_la_trend(
    df: pd.DataFrame,
    config: TimeSeriesConfig,
    la_col: str = "LA_Intake_percent_calories",
    window: int = 5,
    caption: str = None
) -> plt.Figure:
    """
    Plot annotated LA intake trend with rolling average and enhanced clarity.

    Args:
        df (pd.DataFrame): Input data.
        config (TimeSeriesConfig): Configuration for plotting.
        la_col (str): Column name for LA intake data.
        window (int): Rolling window size for smoothing.
        caption (str, optional): Explanatory caption to add below the plot.

    Returns:
        plt.Figure: The generated figure for further annotation.
    """
    fig, ax = plt.subplots(figsize=(14, 8))
    sns.set_palette("colorblind")  # Reason: Improve accessibility for colourblind viewers

    # Plot raw data and rolling average
    sns.lineplot(x=df[config.date_col], y=df[la_col], ax=ax, label="Raw Data", linewidth=2.5)
    sns.lineplot(x=df[config.date_col], y=df[la_col].rolling(window).mean(),
                 ax=ax, label=f"{window}-Year Rolling Avg", linewidth=3.5, linestyle="--")

    # Set title and labels
    ax.set_title("Rise in Estimated Linoleic Acid Intake (% Calories) in Australia (1961-2022)",
                 fontsize=22, fontweight="bold")
    ax.set_xlabel(config.date_col, fontsize=16)
    ax.set_ylabel("LA Intake (% Calories)", fontsize=16)
    ax.legend(fontsize=14)
    ax.tick_params(axis="x", labelsize=14)
    ax.tick_params(axis="y", labelsize=14)

    # Add annotations for key periods
    # Reason: Highlight key inflection points in LA intake for interpretability
    ax.annotate("Rapid increase in LA intake during the 1970s",
                xy=(1975, df[la_col].loc[df[config.date_col] == 1975].values[0]),
                xytext=(1970, df[la_col].max() * 0.7),
                arrowprops=dict(facecolor='black', shrink=0.05),
                fontsize=13, backgroundcolor="white")
    ax.annotate("Plateau in LA intake post-2000",
                xy=(2005, df[la_col].loc[df[config.date_col] == 2005].values[0]),
                xytext=(1995, df[la_col].max() * 0.8),
                arrowprops=dict(facecolor='black', shrink=0.05),
                fontsize=13, backgroundcolor="white")

    if caption:
        fig.text(0.5, -0.08, caption, ha='center', fontsize=13, wrap=True)
        plt.subplots_adjust(bottom=0.18)
    if config.output_dir:
        fig.savefig(f"{config.output_dir}/time_series_LA_Intake_percent_calories_annotated.png",
                   dpi=300, bbox_inches='tight')
    if config.show_plots:
        plt.show()

    return fig

def plot_faceted_trends(
    df: pd.DataFrame,
    config: TimeSeriesConfig,
    variables: List[str],
    titles: List[str],
    caption: str = None
) -> None:
    """
    Plot multiple time series in a faceted grid with enhanced clarity.

    Args:
        df (pd.DataFrame): Input data.
        config (TimeSeriesConfig): Configuration for plotting.
        variables (List[str]): Variables to plot (one per panel).
        titles (List[str]): Titles for each panel.
        caption (str, optional): Explanatory caption to add below the plot.
    """
    fig, axes = plt.subplots(2, 2, figsize=(16, 11), sharex=True)
    axes = axes.ravel()
    sns.set_palette("colorblind")  # Reason: Improve accessibility for colourblind viewers

    for i, (var, title) in enumerate(zip(variables, titles)):
        sns.lineplot(
            x=df[config.date_col],
            y=df[var],
            ax=axes[i],
            linewidth=2.5
        )
        axes[i].set_title(title, fontsize=16, fontweight="bold")
        axes[i].set_xlabel(config.date_col, fontsize=14)
        axes[i].set_ylabel(var, fontsize=14)
        axes[i].tick_params(axis="x", labelsize=12)
        axes[i].tick_params(axis="y", labelsize=12)

    plt.tight_layout()
    if caption:
        fig.text(0.5, -0.08, caption, ha='center', fontsize=13, wrap=True)
        plt.subplots_adjust(bottom=0.18)
    if config.output_dir:
        plt.savefig(f"{config.output_dir}/faceted_trends.png", dpi=300, bbox_inches='tight')
    if config.show_plots:
        plt.show()
    plt.close()

def overlay_time_series(
    df: pd.DataFrame,
    variables: List[str],
    config: TimeSeriesConfig,
    caption: str = None
) -> None:
    """
    Overlay multiple time series on a single plot with enhanced clarity.

    Args:
        df (pd.DataFrame): Input data.
        variables (List[str]): Variables to overlay.
        config (TimeSeriesConfig): Configuration for plotting.
        caption (str, optional): Explanatory caption to add below the plot.
    """
    plt.figure(figsize=(14, 8))
    sns.set_palette("colorblind")  # Reason: Improve accessibility for colourblind viewers
    for var in variables:
        sns.lineplot(x=df[config.date_col], y=df[var], label=var, linewidth=2.5)
    plt.title("Overlayed Time Series", fontsize=20, fontweight="bold")
    plt.xlabel(config.date_col, fontsize=16)
    plt.ylabel("Value", fontsize=16)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.legend(fontsize=14)
    if caption:
        plt.figtext(0.5, -0.08, caption, ha='center', fontsize=13, wrap=True)
        plt.subplots_adjust(bottom=0.18)
    if config.output_dir:
        plt.savefig(f"{config.output_dir}/overlay_time_series.png", dpi=300, bbox_inches='tight')
    if config.show_plots:
        plt.show()

def plot_dual_axis_time_series(
    df: pd.DataFrame,
    config: TimeSeriesConfig,
    la_col: str = "LA_Intake_percent_calories",
    health_col: str = "Obesity_Prevalence_AgeStandardised",
    title: str = None,
    la_label: str = None,
    health_label: str = None,
    annotate: bool = True,
    caption: str = None,
    output_filename: str = None,
) -> plt.Figure:
    """
    Plot a dual-axis time series with LA intake and a health outcome on shared x-axis, with enhanced clarity.

    Args:
        df (pd.DataFrame): Input data.
        config (TimeSeriesConfig): Configuration for plotting.
        la_col (str): Column name for LA intake metric.
        health_col (str): Column name for health outcome metric.
        title (str, optional): Plot title.
        la_label (str, optional): Y-axis label for LA intake.
        health_label (str, optional): Y-axis label for health outcome.
        annotate (bool): Whether to add key annotations.
        caption (str, optional): Explanatory caption to add below the plot.
        output_filename (str, optional): Custom filename for saving the figure in the output directory.

    Returns:
        plt.Figure: The generated figure for further annotation or saving.
    """
    fig, ax1 = plt.subplots(figsize=(16, 9))
    color_la = "#0072B2"  # Reason: Colourblind-friendly blue for LA
    color_health = "#D55E00"  # Reason: Colourblind-friendly orange for health outcome
    x = df[config.date_col]
    y1 = df[la_col]
    y2 = df[health_col]

    ax1.plot(x, y1, color=color_la, linewidth=3, label=la_label or la_col)
    ax1.set_xlabel(config.date_col, fontsize=18)
    ax1.set_ylabel(la_label or la_col, color=color_la, fontsize=18)
    ax1.tick_params(axis="y", labelcolor=color_la, labelsize=16)
    ax1.tick_params(axis="x", labelsize=16)

    ax2 = ax1.twinx()
    ax2.plot(x, y2, color=color_health, linewidth=3, linestyle="--", label=health_label or health_col)
    ax2.set_ylabel(health_label or health_col, color=color_health, fontsize=18)
    ax2.tick_params(axis="y", labelcolor=color_health, labelsize=16)

    # Title and legend
    plot_title = title or f"{la_label or la_col} and {health_label or health_col} Over Time"
    plt.title(plot_title, fontsize=24, fontweight="bold")
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc="upper left", fontsize=16)

    # Annotations for impact
    if annotate:
        # Reason: Highlight peaks for both LA and health outcome for interpretability
        max_la_year = x.iloc[y1.idxmax()]
        max_health_year = x.iloc[y2.idxmax()]
        ax1.annotate(
            f"Peak LA: {y1.max():.2f} ({max_la_year})",
            xy=(max_la_year, y1.max()),
            xytext=(max_la_year, y1.max() * 0.9),
            arrowprops=dict(facecolor=color_la, arrowstyle="->"),
            fontsize=15,
            color=color_la,
            backgroundcolor="white",
        )
        ax2.annotate(
            f"Peak Health: {y2.max():.2f} ({max_health_year})",
            xy=(max_health_year, y2.max()),
            xytext=(max_health_year, y2.max() * 0.9),
            arrowprops=dict(facecolor=color_health, arrowstyle="->"),
            fontsize=15,
            color=color_health,
            backgroundcolor="white",
        )

    fig.tight_layout()
    if caption:
        fig.text(0.5, -0.08, caption, ha='center', fontsize=14, wrap=True)
        plt.subplots_adjust(bottom=0.18)
    if config.output_dir:
        if output_filename:
            fig.savefig(f"{config.output_dir}/{output_filename}", dpi=300, bbox_inches='tight')
        else:
            fname = f"dual_axis_{la_col}_vs_{health_col}.png"
            fig.savefig(f"{config.output_dir}/{fname}", dpi=300, bbox_inches='tight')
    if config.show_plots:
        plt.show()
    plt.close(fig)
    return fig