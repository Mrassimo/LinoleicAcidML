"""
Utility functions for FAO-LA content mapping validation.
"""

import pandas as pd
from difflib import get_close_matches
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_manual_mapping():
    """
    Define manual mappings for common food items
    """
    return {
        'Apples, raw': 'Apples, raw, with skin',
        'Beans, kidney, raw': 'Beans, kidney, red, mature seeds, raw',
        'Cereals, whole grain': 'Cereals, whole wheat hot natural cereal, dry',
        'Citrus fruit, raw': 'Oranges, raw, all commercial varieties',
        'Coconut, raw': 'Nuts, coconut meat, raw',
        'Cottonseed oil': 'Oil, cottonseed, salad or cooking',
        'Fish, cod, raw': 'Fish, cod, Atlantic, raw',
        'Beef, ground, raw': 'Beef, ground, 85% lean meat / 15% fat, raw',
        'Beverages, coffee, brewed, espresso': 'Beverages, coffee, brewed, espresso, restaurant-prepared',
        'Alcoholic beverage, wine': 'Alcoholic beverages, wine, table, all',
        'Beans, kidney, raw': 'Beans, kidney, red, mature seeds, raw'
    }

def find_closest_match(food_name: str, available_names: list, manual_mapping: dict) -> tuple[str, float]:
    """
    Find the closest matching food name in the LA content database
    Returns the closest match and its similarity score
    """
    # Check manual mapping first
    if food_name in manual_mapping:
        mapped_name = manual_mapping[food_name]
        if mapped_name in available_names:
            return mapped_name, 1.0
    
    # Try exact match first
    if food_name in available_names:
        return food_name, 1.0
    
    # Try removing common variations
    normalized_name = food_name.replace(', raw', '').replace(', dried', '').replace(', cooked', '')
    for available in available_names:
        normalized_available = available.replace(', raw', '').replace(', dried', '').replace(', cooked', '')
        if normalized_name == normalized_available:
            return available, 1.0
    
    # Try fuzzy matching with higher cutoff
    matches = get_close_matches(food_name, available_names, n=1, cutoff=0.8)
    if matches:
        return matches[0], 0.8
    
    return None, 0.0

def get_la_content_for_item(item_name: str, la_content_df: pd.DataFrame) -> float:
    """Get LA content percentage for a given food item.
    
    Args:
        item_name: Name of the food item
        la_content_df: DataFrame containing LA content data
        
    Returns:
        float: LA content percentage for the item, or 0 if not found
    """
    # Dictionary mapping FAO names to LA content names
    name_mapping = {
        "Oil, sunflower": "Oil, sunflower, linoleic",
        "Oil, soybean": "Oil, soybean, salad or cooking",
        "Oil, peanut": "Oil, peanut, salad or cooking",
        "Oil, corn germ": "Oil, corn, industrial and retail",
        "Oil, sesame": "Oil, sesame, salad or cooking",
        "Oil, olive": "Oil, olive, extra virgin",
        "Oil, palm": "Oil, palm kernel",
        "Oil, rapeseed": "Oil, canola",
        "Nuts, walnuts": "Nuts, walnuts, english",
        "Seeds, sunflower": "Seeds, sunflower seed kernels",
        "Seeds, sesame": "Seeds, sesame seed kernels",
        "Peanuts": "Peanuts, all types",
        "Soybeans": "Soybeans, mature seeds",
    }
    
    try:
        # Try exact match first
        mask = la_content_df['food_name'].str.lower().str.contains(item_name.lower())
        if mask.any():
            return float(la_content_df.loc[mask, 'percent'].iloc[0])
            
        # Try mapped name
        mapped_name = name_mapping.get(item_name)
        if mapped_name:
            mask = la_content_df['food_name'].str.lower().str.contains(mapped_name.lower())
            if mask.any():
                return float(la_content_df.loc[mask, 'percent'].iloc[0])
                
        # Try partial match
        words = item_name.lower().split()
        for word in words:
            if len(word) > 3:  # Only try matching words longer than 3 chars
                mask = la_content_df['food_name'].str.lower().str.contains(word)
                if mask.any():
                    return float(la_content_df.loc[mask, 'percent'].iloc[0])
        
        logging.warning(f"No LA content data found for item: {item_name}")
        return 0.0
        
    except Exception as e:
        logging.error(f"Error getting LA content for {item_name}: {str(e)}")
        return 0.0

def validate_mapping(fao_items: list, matched_la_items: list) -> list:
    """
    Create validation status list based on matched items
    """
    validation_status = []
    for la_item in matched_la_items:
        if la_item == '':
            validation_status.append('NO_MATCH')
        else:
            validation_status.append('APPROVED')
    return validation_status

def get_notes_for_item(fao_item: str, matched_la_item: str, validation_status: str) -> str:
    """
    Generate appropriate notes for each item based on its validation status
    """
    if validation_status == 'NO_MATCH':
        if fao_item in ['Grand Total', 'Population']:
            return 'Not a food item; no appropriate match.'
        elif fao_item in ['Animal Products', 'Vegetal Products']:
            return 'Broad category; no single representative item.'
        elif fao_item == 'Miscellaneous':
            return 'Too vague; no appropriate match.'
        elif fao_item == 'Aquatic Animals, Others':
            return 'Broad category for miscellaneous aquatic animals; no specific match.'
        elif fao_item == 'Aquatic Plants':
            return 'Aquatic plants are not typically consumed; no appropriate match.'
        elif fao_item == 'Aquatic Products, Other':
            return 'Broad category for miscellaneous aquatic products; no specific match.'
        elif fao_item == 'Oilcrops':
            return 'Broad category for oil-producing crops; no single match.'
    elif validation_status == 'APPROVED' and matched_la_item:
        return f"Direct match for {fao_item.lower()}."
    return '' 