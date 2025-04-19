"""
Main entry point for analytics and visualisation of the unified Australian dataset.

Demonstrates usage of modular visualisation functions for EDA, time series, correlation, scatter, and regression.
All code and comments use Australian English.

Run from project root with:
    python -m src.visualisation.main

Author: SeedoilsML Team
"""

import os
from src.visualisation.utils import load_unified_dataset, set_plot_style, DatasetConfig
from src.visualisation.eda import eda_report, EDAConfig
from src.visualisation.time_series import plot_dual_axis_time_series
from src.visualisation.time_series import plot_time_series, TimeSeriesConfig
from src.visualisation.correlation import plot_correlation_heatmap, CorrelationConfig
from src.visualisation.scatter import plot_lagged_scatter
from src.visualisation.scatter import plot_scatter, ScatterConfig
from src.visualisation.regression import plot_linear_regression, RegressionConfig

def main():
    # Set up output directory
    output_dir = "figures"
    os.makedirs(output_dir, exist_ok=True)

    # Set plot style
    set_plot_style("whitegrid")

    # Load dataset
    df = load_unified_dataset()

    # EDA
    eda_cfg = EDAConfig(output_dir=output_dir, show_plots=False)
    eda_report(df, config=eda_cfg)

    # Time series plot (example: first numeric variable)
    ts_cfg = TimeSeriesConfig(
        output_dir=output_dir,
        show_plots=False,
        date_col="Year",  # Adjust as appropriate for your dataset
        variables=None
    )
    plot_time_series(df, config=ts_cfg)

    # Dual-axis time series: LA intake vs Obesity Prevalence
    plot_dual_axis_time_series(
        df,
        config=ts_cfg,
        la_col="LA_Intake_percent_calories",
        health_col="Obesity_Prevalence_AgeStandardised",
        title="LA Intake (% Calories) and Obesity Prevalence (Age-Standardised) Over Time",
        la_label="LA Intake (% Calories)",
        health_label="Obesity Prevalence (%)",
        annotate=True,
    )

    # Dedicated high-impact visual for website: LA vs Health (Obesity) with required filename
    plot_dual_axis_time_series(
        df,
        config=ts_cfg,
        la_col="LA_Intake_percent_calories",
        health_col="Obesity_Prevalence_AgeStandardised",
        title="Rising Linoleic Acid Intake and Obesity Prevalence in Australia",
        la_label="LA Intake (% Calories)",
        health_label="Obesity Prevalence (%)",
        annotate=True,
        output_filename="impact_LA_vs_Health_timeseries.png",
    )

    # Lagged scatter plot: LA_perc_kcal_lag10 vs Diabetes Prevalence
    scatter_cfg = ScatterConfig(output_dir=output_dir, show_plots=False, lag=0)
    plot_lagged_scatter(
        df,
        x="LA_perc_kcal_lag10",
        y="Diabetes_Prevalence_Rate_AgeStandardised",
        config=scatter_cfg,
        title="Diabetes Prevalence vs. 10-Year Lagged LA Intake (% Calories)",
    )


    # Correlation heatmap
    corr_cfg = CorrelationConfig(output_dir=output_dir, show_plots=False)
    plot_correlation_heatmap(df, config=corr_cfg)

    # Scatter plot (example: first two numeric variables)
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    if len(numeric_cols) >= 2:
        scatter_cfg = ScatterConfig(output_dir=output_dir, show_plots=False)
        plot_scatter(df, x=numeric_cols[0], y=numeric_cols[1], config=scatter_cfg)

        # Linear regression
        reg_cfg = RegressionConfig(output_dir=output_dir, show_plots=False)
        plot_linear_regression(df, x=numeric_cols[0], y=numeric_cols[1], config=reg_cfg)

    # Generate Markdown Overview of Figures
    import glob
    import pandas as pd

    md_path = os.path.join(output_dir, "figures_overview.md")
    with open(md_path, "w") as md:
        md.write("# Visualisation Figures Overview\n\n")
        md.write("This file provides a summary of each figure, a snippet of the input data, and a link to the PNG.\n\n")
        
        # Map figure filenames to descriptions and data columns
        figure_map = {
            "correlation_heatmap.png": {
                "desc": "Correlation heatmap of all numeric variables.",
                "cols": df.select_dtypes(include='number').columns.tolist()
            },
            "la_intake_trends.png": {
                "desc": "Trends in Linoleic Acid (LA) intake over time.",
                "cols": ["Year", "Total_LA_Intake_g_per_capita_day", "LA_Intake_percent_calories"]
            },
            "time_series_LA_Intake_percent_calories.png": {
                "desc": "Time series of LA intake as percent of calories.",
                "cols": ["Year", "LA_Intake_percent_calories"]
            },
            "time_series_LA_Intake_percent_calories_annotated.png": {
                "desc": "Annotated time series of LA intake as percent of calories.",
                "cols": ["Year", "LA_Intake_percent_calories"]
            },
            "time_series_Plant_Fat_Ratio.png": {
                "desc": "Time series of plant fat ratio.",
                "cols": ["Year", "Plant_Fat_Ratio"]
            },
            "time_series_Total_Calorie_Supply.png": {
                "desc": "Time series of total calorie supply.",
                "cols": ["Year", "Total_Calorie_Supply"]
            },
            "time_series_Total_Fat_Supply_g.png": {
                "desc": "Time series of total fat supply (g).",
                "cols": ["Year", "Total_Fat_Supply_g"]
            },
            "overlay_time_series.png": {
                "desc": "Overlay of multiple time series variables.",
                "cols": ["Year"] + [c for c in df.select_dtypes(include='number').columns if c != "Year"]
            },
            "lagged_scatter_Obesity_Prevalence_AgeStandardised_vs_LA_perc_kcal_lag10_by_decade.png": {
                "desc": "Lagged scatter: Obesity Prevalence (Age-Standardised) vs LA % kcal (lag 10, by decade).",
                "cols": ["Obesity_Prevalence_AgeStandardised", "LA_Intake_percent_calories", "Year"]
            },
        }
        
        for fig_path in sorted(glob.glob(os.path.join(output_dir, "*.png"))):
            fname = os.path.basename(fig_path)
            info = figure_map.get(fname, None)
            md.write(f"## {fname}\n\n")
            if info:
                md.write(f"**Description:** {info['desc']}\n\n")
                # Data snippet
                cols = [c for c in info["cols"] if c in df.columns]
                snippet = df[cols].head(5)
                md.write("**Data snippet:**\n\n")
                md.write(snippet.to_markdown(index=False))
                md.write("\n\n")
            else:
                md.write("No mapping found for this figure.\n\n")
            md.write(f"![{fname}]({fname})\n\n")

if __name__ == "__main__":
    main()