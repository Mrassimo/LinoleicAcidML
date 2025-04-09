import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from unittest.mock import patch
import tempfile
import shutil

from src.data_processing.merge_datasets import (
    fuzzy_match_foods,
    merge_faostat_fire,
    merge_health_data,
    validate_merged_data,
    save_merged_dataset,
    generate_merge_documentation,
    MergedDatasetSchema
)

@pytest.fixture
def sample_faostat_data():
    return pd.DataFrame({
        'area_code': [5000, 5000, 5000],
        'area': ['Australia', 'Australia', 'Australia'],
        'item_code': [1001, 1002, 1003],
        'item': ['Wheat flour products', 'Beef', 'Unmatched food'],
        'year': [2020, 2020, 2020],
        'value': [100.5, 50.2, 30.0],
        'flag': ['E', 'I', 'X']
    })

@pytest.fixture
def sample_fire_data():
    return pd.DataFrame({
        'food_name': ['Wheat flour', 'Beef meat'],
        'la_cal': [10.5, 2.3],
        'cal': [200, 180],
        'la_perc': [5.25, 1.28]
    })

@pytest.fixture
def sample_health_data():
    return pd.DataFrame({
        'year': [2020, 2021],
        'metric': [15.2, 16.1]
    })

def test_fuzzy_match_foods(sample_faostat_data, sample_fire_data):
    # Get unique food items
    faostat_items = sample_faostat_data['item'].unique().tolist()
    fire_items = sample_fire_data['food_name'].unique().tolist()
    
    # Test matching
    matches = fuzzy_match_foods(faostat_items, fire_items, threshold=70)
    
    # Check expected matches
    assert len(matches) == 2
    assert matches['Wheat flour products'] == 'Wheat flour'
    assert matches['Beef'] == 'Beef meat'
    
    # Test with higher threshold (should only match perfect matches)
    matches_strict = fuzzy_match_foods(faostat_items, fire_items, threshold=95)
    assert len(matches_strict) == 2  # Both items match well at high threshold

def test_merge_faostat_fire(sample_faostat_data, sample_fire_data, tmp_path):
    # Set up temp file for stats
    stats_path = tmp_path / "merge_stats.csv"
    
    # Perform merge
    merged_df = merge_faostat_fire(
        sample_faostat_data,
        sample_fire_data,
        str(stats_path)
    )
    
    # Check results
    assert len(merged_df) == 3
    assert 'la_perc' in merged_df.columns
    assert merged_df['source'].nunique() == 2
    
    # Check stats file was created
    assert Path(stats_path).exists()
    stats_df = pd.read_csv(stats_path)
    assert stats_df['matched_items'].values[0] == 2

def test_merge_health_data(sample_faostat_data, sample_fire_data, sample_health_data, tmp_path):
    # First merge FAOSTAT and Fire data
    stats_path = tmp_path / "merge_stats.csv"
    merged_df = merge_faostat_fire(
        sample_faostat_data,
        sample_fire_data,
        str(stats_path)
    )
    
    # Rename health metric column to match expected
    health_df = sample_health_data.rename(columns={'metric': 'health_metric'})
    
    # Merge with health data
    health_merged = merge_health_data(
        merged_df,
        health_df,
        'health_metric',
        str(stats_path)
    )
    
    # Check results
    assert 'health_metric' in health_merged.columns
    assert 'health_metric_type' in health_merged.columns
    assert health_merged['health_metric'].notna().sum() == 3
    
    # Check stats were appended
    stats_df = pd.read_csv(stats_path)
    assert len(stats_df) == 2

def test_validate_merged_data(sample_faostat_data, sample_fire_data):
    # Create merged test data
    merged_df = pd.DataFrame({
        'area_code': [5000],
        'area': ['Australia'],
        'item_code': [1001],
        'item': ['Wheat'],
        'year': [2020],
        'value': [100.5],
        'la_perc': [5.2],
        'health_metric': [15.2],
        'health_metric_type': ['diabetes'],
        'source': ['FAOSTAT + Fire in a Bottle']
    })
    
    # Test valid data
    errors = validate_merged_data(merged_df)
    assert not errors
    
    # Test invalid data
    invalid_df = merged_df.copy()
    invalid_df.at[0, 'la_perc'] = 150
    errors = validate_merged_data(invalid_df)
    assert len(errors) == 1
    assert "Linoleic acid percentage must be between 0-100" in errors[1][0]

def test_save_merged_dataset(sample_faostat_data, sample_fire_data, tmp_path):
    # Create merged test data
    merged_df = pd.DataFrame({
        'area_code': [5000],
        'area': ['Australia'],
        'item_code': [1001],
        'item': ['Wheat'],
        'year': [2020],
        'value': [100.5],
        'la_perc': [5.2],
        'source': ['FAOSTAT + Fire in a Bottle']
    })
    
    # Set up output paths
    output_path = tmp_path / "output.feather"
    report_path = tmp_path / "validation_errors.csv"
    
    # Test save with valid data
    save_merged_dataset(merged_df, str(output_path), str(report_path))
    assert output_path.exists()
    assert not report_path.exists()
    
    # Test save with invalid data
    invalid_df = merged_df.copy()
    invalid_df.at[0, 'la_perc'] = 150
    save_merged_dataset(invalid_df, str(output_path), str(report_path))
    assert report_path.exists()

def test_generate_merge_documentation(tmp_path):
    # Create test stats files
    stats_path1 = tmp_path / "stats1.csv"
    stats_path2 = tmp_path / "stats2.csv"
    
    pd.DataFrame({'metric': ['value1']}).to_csv(stats_path1, index=False)
    pd.DataFrame({'metric': ['value2']}).to_csv(stats_path2, index=False)
    
    # Set up output path
    docs_path = tmp_path / "merge_docs.md"
    
    # Generate documentation
    generate_merge_documentation(
        [str(stats_path1), str(stats_path2)],
        str(docs_path)
    )
    
    # Check results
    assert docs_path.exists()
    content = docs_path.read_text()
    assert "Merge Statistics" in content
    assert "value1" in content
    assert "value2" in content

def test_merged_dataset_schema():
    # Test valid data
    valid_data = {
        'area_code': 5000,
        'area': 'Australia',
        'item_code': 1001,
        'item': 'Wheat',
        'year': 2020,
        'value': 100.5,
        'source': 'FAOSTAT'
    }
    assert MergedDatasetSchema(**valid_data)
    
    # Test invalid data
    invalid_data = valid_data.copy()
    invalid_data['la_perc'] = 150
    
    with pytest.raises(ValueError) as excinfo:
        MergedDatasetSchema(**invalid_data)
    assert "Linoleic acid percentage must be between 0-100" in str(excinfo.value)