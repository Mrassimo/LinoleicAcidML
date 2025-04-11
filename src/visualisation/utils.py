"""
Utility functions and shared configuration for analytics and visualisation modules.

Includes dataset loading, common plotting settings, and shared pydantic models.
All code and comments use Australian English.

Author: SeedoilsML Team
"""

from typing import Optional
import pandas as pd
import seaborn as sns
from pydantic import BaseModel, Field

class DatasetConfig(BaseModel):
    """Configuration for loading the unified dataset."""
    csv_path: str = Field(
        default="data/processed/analytical_data_australia_final.csv",
        description="Path to the unified analytical dataset CSV"
    )

def load_unified_dataset(config: Optional[DatasetConfig] = None) -> pd.DataFrame:
    """
    Load the unified analytical dataset from CSV.

    Args:
        config (DatasetConfig, optional): Configuration specifying the CSV path.

    Returns:
        pd.DataFrame: Loaded dataset.
    """
    path = config.csv_path if config else "data/processed/analytical_data_australia_final.csv"
    df = pd.read_csv(path)
    return df

def set_plot_style(style: str = "whitegrid") -> None:
    """
    Set the default seaborn/matplotlib plot style.

    Args:
        style (str): Seaborn style to use (default: 'whitegrid').
    """
    sns.set_theme(style=style)