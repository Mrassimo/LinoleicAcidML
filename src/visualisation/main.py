"""
Main entry point for analytics and visualisation of the unified Australian dataset.

Demonstrates usage of modular visualisation functions for EDA, time series, correlation, scatter, and regression.
All code and comments use Australian English.

Author: SeedoilsML Team
"""

import os
from src.visualisation.utils import load_unified_dataset, set_plot_style, DatasetConfig
from src.visualisation.eda import eda_report, EDAConfig
from src.visualisation.time_series import plot_time_series, TimeSeriesConfig
from src.visualisation.correlation import plot_correlation_heatmap, CorrelationConfig
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

if __name__ == "__main__":
    main()