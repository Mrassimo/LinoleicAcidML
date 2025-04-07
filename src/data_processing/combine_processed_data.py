import pandas as pd
import numpy as np
import os
from pathlib import Path
from typing import Dict, Any

def get_column_stats(df: pd.DataFrame, col: str) -> Dict[str, Any]:
    """Get detailed statistics for a column."""
    stats = {}
    series = df[col]
    non_null_series = series.dropna()
    
    # Basic stats
    stats['count'] = len(series)
    stats['missing'] = series.isna().sum()
    stats['unique'] = series.nunique()
    stats['memory_usage'] = series.memory_usage(deep=True) / 1024 / 1024  # MB
    
    # Type-specific statistics
    if pd.api.types.is_numeric_dtype(series):
        if len(non_null_series) > 0:  # Only calculate stats if we have non-null values
            stats.update({
                'mean': non_null_series.mean(),
                'std': non_null_series.std() if len(non_null_series) > 1 else None,
                'min': non_null_series.min(),
                'max': non_null_series.max(),
                'median': non_null_series.median(),
                'skewness': non_null_series.skew() if len(non_null_series) > 2 else None,
                'kurtosis': non_null_series.kurtosis() if len(non_null_series) > 3 else None,
                'zeros': (non_null_series == 0).sum()
            })
        else:
            stats.update({
                'mean': None,
                'std': None,
                'min': None,
                'max': None,
                'median': None,
                'skewness': None,
                'kurtosis': None,
                'zeros': 0
            })
    elif pd.api.types.is_string_dtype(series):
        if len(non_null_series) > 0:
            str_lengths = non_null_series.str.len()
            stats.update({
                'min_length': str_lengths.min(),
                'max_length': str_lengths.max(),
                'avg_length': str_lengths.mean(),
                'empty_strings': (non_null_series == '').sum()
            })
        else:
            stats.update({
                'min_length': None,
                'max_length': None,
                'avg_length': None,
                'empty_strings': 0
            })
    
    return stats

def format_value(value: Any) -> str:
    """Format a value for markdown display."""
    if pd.isna(value):
        return 'NA'
    elif isinstance(value, (float, np.floating)):
        return f"{value:.4g}"
    return str(value)

def read_csv_to_markdown(file_path: Path) -> str:
    """Read a CSV file and convert it to a markdown table with detailed metadata."""
    # Read the CSV file
    df = pd.read_csv(file_path)
    is_aihw = 'aihw' in file_path.name.lower()
    
    content = []
    
    # Add header with file name and basic stats
    filename = file_path.name
    content.append(f"## {filename}")
    content.append(f"\n### Dataset Overview")
    content.append(f"- Total Rows: {len(df):,}")
    content.append(f"- Total Columns: {len(df.columns):,}")
    content.append(f"- Memory Usage: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
    content.append(f"- Missing Values: {df.isna().sum().sum():,}")
    content.append(f"- Duplicate Rows: {df.duplicated().sum():,}")
    
    # Detailed column information
    content.append("\n### Column Information")
    content.append("| Column | Type | Non-Null | Unique | Memory (MB) | Additional Statistics |")
    content.append("|--------|------|-----------|---------|-------------|---------------------|")
    
    for col in df.columns:
        stats = get_column_stats(df, col)
        
        # Format additional statistics based on data type
        if pd.api.types.is_numeric_dtype(df[col]):
            if stats.get('mean') is not None:
                additional_stats = (
                    f"Mean: {format_value(stats.get('mean'))}, "
                    f"Std: {format_value(stats.get('std'))}, "
                    f"Min: {format_value(stats.get('min'))}, "
                    f"Max: {format_value(stats.get('max'))}, "
                    f"Median: {format_value(stats.get('median'))}"
                )
            else:
                additional_stats = "No numeric data available"
        elif pd.api.types.is_string_dtype(df[col]):
            if stats.get('min_length') is not None:
                additional_stats = (
                    f"Min Length: {format_value(stats.get('min_length'))}, "
                    f"Max Length: {format_value(stats.get('max_length'))}, "
                    f"Avg Length: {format_value(stats.get('avg_length'))}"
                )
            else:
                additional_stats = "No string data available"
        else:
            additional_stats = "N/A"
        
        content.append(
            f"| {col} | {df[col].dtype} | "
            f"{len(df) - stats['missing']:,} | {stats['unique']:,} | "
            f"{stats['memory_usage']:.2f} | {additional_stats} |"
        )
    
    # Column value distributions
    content.append("\n### Column Value Distributions")
    
    for col in df.columns:
        content.append(f"\n#### {col}")
        
        # For AIHW files or if column is string type and has few unique values, show all unique values
        if (is_aihw and pd.api.types.is_string_dtype(df[col])) or df[col].nunique() < 20:
            value_counts = df[col].value_counts()
            content.append("\nAll Unique Values:")
            content.append("| Value | Count | Percentage |")
            content.append("|-------|--------|------------|")
            for val, count in value_counts.items():
                percentage = (count / len(df)) * 100
                content.append(f"| {format_value(val)} | {count:,} | {percentage:.2f}% |")
        else:
            # Show top and bottom 10 values
            content.append("\nTop 10 Most Frequent Values:")
            content.append("| Value | Count | Percentage |")
            content.append("|-------|--------|------------|")
            for val, count in df[col].value_counts().head(10).items():
                percentage = (count / len(df)) * 100
                content.append(f"| {format_value(val)} | {count:,} | {percentage:.2f}% |")
            
            content.append("\nBottom 10 Least Frequent Values:")
            content.append("| Value | Count | Percentage |")
            content.append("|-------|--------|------------|")
            for val, count in df[col].value_counts().tail(10).items():
                percentage = (count / len(df)) * 100
                content.append(f"| {format_value(val)} | {count:,} | {percentage:.2f}% |")
    
    # Sample data
    content.append("\n### Sample Data")
    content.append("\nFirst 10 Rows:")
    content.append(df.head(10).to_markdown())
    
    content.append("\nLast 10 Rows:")
    content.append(df.tail(10).to_markdown())
    
    return "\n".join(content)

def main():
    # Define paths
    processed_dir = Path("data/processed")
    output_file = Path("reports/processed_data_summary.md")
    
    # Create reports directory if it doesn't exist
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Initialize the markdown content
    markdown_content = ["# Processed Data Summary\n"]
    
    # Process each CSV file
    csv_files = sorted(processed_dir.glob("*.csv"))
    total_files = len(csv_files)
    
    for i, file_path in enumerate(csv_files, 1):
        print(f"Processing {file_path.name}... ({i}/{total_files})")
        try:
            markdown_content.append(read_csv_to_markdown(file_path))
            markdown_content.append("\n---\n")  # Add separator between files
        except Exception as e:
            print(f"Error processing {file_path.name}: {str(e)}")
    
    # Write the combined markdown file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(markdown_content))
    
    print(f"\nMarkdown summary has been created at: {output_file}")

if __name__ == "__main__":
    main() 