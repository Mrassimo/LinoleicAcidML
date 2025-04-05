import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import os
from src.combine_processed_data import read_csv_to_markdown, get_column_stats, format_value

@pytest.fixture
def sample_csv():
    """Create a temporary CSV file for testing."""
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False, mode='w') as f:
        f.write("name,age,height,city\n")
        f.write("John,30,180.5,Sydney\n")
        f.write("Jane,25,165.0,Melbourne\n")
        f.write("Bob,40,175.5,Brisbane\n")
        f.write("Alice,,170.0,Perth\n")  # Missing age
    yield Path(f.name)
    os.unlink(f.name)

def test_format_value():
    """Test the format_value function."""
    assert format_value(np.nan) == 'NA'
    assert format_value(1.23456789) == '1.235'
    assert format_value('test') == 'test'
    assert format_value(1000000) == '1000000'

def test_get_column_stats(sample_csv):
    """Test the get_column_stats function."""
    df = pd.read_csv(sample_csv)
    
    # Test numeric column
    age_stats = get_column_stats(df, 'age')
    assert age_stats['count'] == 4
    assert age_stats['missing'] == 1
    assert age_stats['unique'] == 3
    assert 'mean' in age_stats
    assert 'std' in age_stats
    
    # Test string column
    city_stats = get_column_stats(df, 'city')
    assert city_stats['count'] == 4
    assert city_stats['missing'] == 0
    assert city_stats['unique'] == 4
    assert 'min_length' in city_stats
    assert 'max_length' in city_stats

def test_read_csv_to_markdown(sample_csv):
    """Test the read_csv_to_markdown function with a sample CSV file."""
    markdown_content = read_csv_to_markdown(sample_csv)
    
    # Check if the markdown content contains expected sections
    assert "## " + sample_csv.name in markdown_content
    assert "### Dataset Overview" in markdown_content
    assert "### Column Information" in markdown_content
    assert "### Column Value Distributions" in markdown_content
    assert "### Sample Data" in markdown_content
    
    # Check if all columns are present
    assert "name" in markdown_content
    assert "age" in markdown_content
    assert "city" in markdown_content
    
    # Check if sample data is present
    assert "John" in markdown_content
    assert "Sydney" in markdown_content
    
    # Check if statistics are present
    assert "Mean:" in markdown_content
    assert "Std:" in markdown_content
    assert "Min Length:" in markdown_content
    
    # Check if value distributions are present (for small datasets, we show all unique values)
    assert "All Unique Values:" in markdown_content
    assert "Value | Count | Percentage" in markdown_content

def test_read_csv_to_markdown_empty_file():
    """Test handling of an empty CSV file."""
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False, mode='w') as f:
        f.write("name,age,city\n")  # Only headers, no data
    
    try:
        markdown_content = read_csv_to_markdown(Path(f.name))
        assert "Total Rows: 0" in markdown_content
        assert "Missing Values: 0" in markdown_content
    finally:
        os.unlink(f.name)

def test_read_csv_to_markdown_aihw_file():
    """Test handling of an AIHW file."""
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False, mode='w') as f:
        f.write("category,value,year\n")
        f.write("A,10,2020\n")
        f.write("B,20,2020\n")
        f.write("C,30,2020\n")
        f.name_with_aihw = f.name[:-4] + "_aihw.csv"
        os.rename(f.name, f.name_with_aihw)
    
    try:
        markdown_content = read_csv_to_markdown(Path(f.name_with_aihw))
        assert "All Unique Values:" in markdown_content
        assert "category" in markdown_content
        assert "A" in markdown_content
    finally:
        os.unlink(f.name_with_aihw)

def test_read_csv_to_markdown_file_not_found():
    """Test handling of a non-existent file."""
    with pytest.raises(FileNotFoundError):
        read_csv_to_markdown(Path("non_existent_file.csv")) 