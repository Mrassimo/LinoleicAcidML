"""
Interactive visualisations for the SeedoilsML project using Plotly.

This module creates interactive visualisations for the project's key findings,
including time series, correlations, model results, and feature importance.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional, Tuple

def create_time_series_plot(
    df: pd.DataFrame,
    y_cols: List[str],
    title: str = "Time Series Analysis",
    y_axis_title: str = "Value"
) -> go.Figure:
    """Create an interactive time series plot with multiple metrics."""
    fig = go.Figure()
    
    for col in y_cols:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df[col],
                name=col.replace("_", " "),
                mode='lines+markers'
            )
        )
    
    fig.update_layout(
        title=title,
        xaxis_title="Year",
        yaxis_title=y_axis_title,
        hovermode='x unified',
        template='plotly_white'
    )
    
    return fig

def create_correlation_heatmap(
    corr_matrix: pd.DataFrame,
    title: str = "Correlation Analysis"
) -> go.Figure:
    """Create an interactive correlation heatmap."""
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        hoverongaps=False,
        hovertemplate='%{x}<br>%{y}<br>Correlation: %{z:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=title,
        template='plotly_white',
        width=800,
        height=800
    )
    
    return fig

def create_scatter_with_trend(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str = "Relationship Analysis"
) -> go.Figure:
    """Create an interactive scatter plot with trend line."""
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        trendline="ols",
        title=title
    )
    
    fig.update_layout(
        template='plotly_white',
        hovermode='closest'
    )
    
    return fig

def create_feature_importance_plot(
    importance_df: pd.DataFrame,
    title: str = "Feature Importance Analysis"
) -> go.Figure:
    """Create an interactive feature importance bar plot."""
    fig = px.bar(
        importance_df,
        x='importance',
        y='feature',
        orientation='h',
        title=title
    )
    
    fig.update_layout(
        template='plotly_white',
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return fig

def create_model_comparison_plot(
    metrics_df: pd.DataFrame,
    title: str = "Model Performance Comparison"
) -> go.Figure:
    """Create an interactive model comparison plot."""
    fig = go.Figure()
    
    for metric in metrics_df.columns:
        fig.add_trace(
            go.Bar(
                name=metric,
                x=metrics_df.index,
                y=metrics_df[metric],
                text=metrics_df[metric].round(3),
                textposition='auto',
            )
        )
    
    fig.update_layout(
        title=title,
        template='plotly_white',
        barmode='group',
        showlegend=True
    )
    
    return fig

def create_gam_partial_dependence_plot(
    x_values: np.ndarray,
    y_values: np.ndarray,
    confidence_intervals: Optional[Tuple[np.ndarray, np.ndarray]] = None,
    feature_name: str = "",
    title: str = "GAM Partial Dependence Plot"
) -> go.Figure:
    """Create an interactive GAM partial dependence plot."""
    fig = go.Figure()
    
    # Add main effect line
    fig.add_trace(
        go.Scatter(
            x=x_values,
            y=y_values,
            mode='lines',
            name='Partial Effect',
            line=dict(color='blue')
        )
    )
    
    # Add confidence intervals if provided
    if confidence_intervals is not None:
        lower, upper = confidence_intervals
        fig.add_trace(
            go.Scatter(
                x=np.concatenate([x_values, x_values[::-1]]),
                y=np.concatenate([upper, lower[::-1]]),
                fill='toself',
                fillcolor='rgba(0,100,255,0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                name='95% CI'
            )
        )
    
    fig.update_layout(
        title=title,
        xaxis_title=feature_name,
        yaxis_title="Partial Effect",
        template='plotly_white',
        hovermode='x unified'
    )
    
    return fig

def save_interactive_plots(
    df: pd.DataFrame,
    output_dir: Path,
    model_results: Optional[Dict] = None
) -> None:
    """
    Create and save all interactive plots for the project.
    
    Args:
        df: The main analytical dataset
        output_dir: Directory to save the plots
        model_results: Dictionary containing model results and metrics
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Time series plots
    health_metrics = [col for col in df.columns if any(x in col.lower() for x in ['mortality', 'prevalence', 'incidence'])]
    dietary_metrics = [col for col in df.columns if any(x in col.lower() for x in ['la', 'fat', 'calorie'])]
    
    ts_health = create_time_series_plot(df, health_metrics, "Health Metrics Over Time")
    ts_health.write_html(output_dir / "health_metrics_time_series.html")
    
    ts_dietary = create_time_series_plot(df, dietary_metrics, "Dietary Metrics Over Time")
    ts_dietary.write_html(output_dir / "dietary_metrics_time_series.html")
    
    # Correlation heatmap
    corr_matrix = df[health_metrics + dietary_metrics].corr()
    corr_plot = create_correlation_heatmap(corr_matrix)
    corr_plot.write_html(output_dir / "correlation_heatmap.html")
    
    # Scatter plots for key relationships
    la_cols = [col for col in df.columns if 'la' in col.lower()]
    for health_metric in health_metrics:
        for la_col in la_cols:
            scatter = create_scatter_with_trend(
                df, la_col, health_metric,
                f"Relationship: {la_col} vs {health_metric}"
            )
            safe_filename = f"scatter_{la_col}_{health_metric}.html".replace(" ", "_")
            scatter.write_html(output_dir / safe_filename)
    
    # Model comparison and feature importance plots if results provided
    if model_results:
        if 'feature_importance' in model_results:
            imp_plot = create_feature_importance_plot(
                model_results['feature_importance'],
                "Feature Importance Across Models"
            )
            imp_plot.write_html(output_dir / "feature_importance.html")
        
        if 'model_metrics' in model_results:
            metrics_plot = create_model_comparison_plot(
                model_results['model_metrics'],
                "Model Performance Comparison"
            )
            metrics_plot.write_html(output_dir / "model_comparison.html")
        
        if 'gam_results' in model_results:
            for feature, result in model_results['gam_results'].items():
                gam_plot = create_gam_partial_dependence_plot(
                    result['x_values'],
                    result['y_values'],
                    result.get('confidence_intervals'),
                    feature,
                    f"GAM Partial Dependence Plot: {feature}"
                )
                safe_filename = f"gam_pdp_{feature}.html".replace(" ", "_")
                gam_plot.write_html(output_dir / safe_filename) 