"""
Tests for semantic matching functions
"""

import pytest
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from src.data_processing.semantic_matching import (
    ItemMatch,
    preprocess_item_name,
    find_best_matches
)

@pytest.fixture
def sample_items():
    """Create sample items for testing"""
    fao_items = [
        'Soybean Oil',
        'Raw Olive Oil',
        'Processed Butter',
        'Sunflower Oil'
    ]
    
    la_items = [
        'Soybean Oil',
        'Olive Oil',
        'Butter',
        'Canola Oil'
    ]
    
    return fao_items, la_items

@pytest.fixture
def model():
    """Load sentence transformer model for testing"""
    return SentenceTransformer('all-MiniLM-L6-v2')

def test_item_match_validation():
    """Test item match validation with Pydantic"""
    # Valid match
    valid_match = {
        'fao_item': 'Soybean Oil',
        'matched_la_item': 'Soybean Oil',
        'similarity_score': 0.95,
        'manual_validation_status': 'PENDING'
    }
    match = ItemMatch(**valid_match)
    assert match.fao_item == 'Soybean Oil'
    assert match.similarity_score == 0.95
    
    # Invalid fao_item (empty)
    with pytest.raises(Exception):
        ItemMatch(**{**valid_match, 'fao_item': ''})
    
    # Invalid similarity score (> 1)
    with pytest.raises(Exception):
        ItemMatch(**{**valid_match, 'similarity_score': 1.1})
    
    # Invalid similarity score (< 0)
    with pytest.raises(Exception):
        ItemMatch(**{**valid_match, 'similarity_score': -0.1})

def test_preprocess_item_name():
    """Test item name preprocessing"""
    # Test lowercase conversion
    assert preprocess_item_name('Soybean Oil') == 'soybean oil'
    
    # Test prefix removal
    assert preprocess_item_name('Raw Olive Oil') == 'olive oil'
    assert preprocess_item_name('Processed Butter') == 'butter'
    assert preprocess_item_name('Prepared Sunflower Oil') == 'sunflower oil'
    
    # Test multiple prefixes
    assert preprocess_item_name('Raw Processed Butter') == 'processed butter'

def test_find_best_matches(sample_items, model):
    """Test finding best matches between items"""
    fao_items, la_items = sample_items
    
    # Find matches with default threshold
    matches = find_best_matches(fao_items, la_items, model)
    
    # Check that we got matches
    assert len(matches) > 0
    
    # Check match structure
    first_match = matches[0]
    assert 'fao_item' in first_match
    assert 'matched_la_item' in first_match
    assert 'similarity_score' in first_match
    assert 'manual_validation_status' in first_match
    
    # Check exact match has high similarity
    soybean_matches = [m for m in matches if m['fao_item'] == 'Soybean Oil']
    if soybean_matches:
        assert soybean_matches[0]['matched_la_item'] == 'Soybean Oil'
        assert soybean_matches[0]['similarity_score'] > 0.9
    
    # Test with high threshold
    high_threshold_matches = find_best_matches(fao_items, la_items, model, similarity_threshold=0.9)
    assert len(high_threshold_matches) <= len(matches)

def test_find_best_matches_empty_input(model):
    """Test handling of empty input lists"""
    # Empty FAO items
    matches = find_best_matches([], ['Soybean Oil'], model)
    assert len(matches) == 0
    
    # Empty LA items
    matches = find_best_matches(['Soybean Oil'], [], model)
    assert len(matches) == 0
    
    # Both empty
    matches = find_best_matches([], [], model)
    assert len(matches) == 0 