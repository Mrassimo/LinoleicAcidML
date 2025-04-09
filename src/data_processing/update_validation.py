"""
Update the FAO-LA mapping with validated matches.
"""

import pandas as pd
import logging
from pathlib import Path
from .validation_utils import (
    get_manual_mapping,
    find_closest_match,
    get_la_content_for_item,
    validate_mapping,
    get_notes_for_item
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_validation_data():
    """Create DataFrame from validated matches"""
    # Load the data from your validated table
    fao_items = [
        'Animal Products', 'Aquatic Animals, Others', 'Aquatic Plants', 'Aquatic Products, Other',
        'Beverages, Fermented', 'Cephalopods', 'Cereals, other', 'Eggs', 'Fats, Animals, Raw',
        'Fish, Body Oil', 'Fish, Liver Oil', 'Fish, Seafood', 'Freshwater Fish', 'Fruits - Excluding Wine',
        'Fruits, other', 'Grand Total', 'Grapefruit and products', 'Grapes and products (excl wine)',
        'Groundnut Oil', 'Groundnuts', 'Groundnuts (Shelled Eq)', 'Honey', 'Infant food',
        'Lemons, Limes and products', 'Maize Germ Oil', 'Maize and products', 'Marine Fish, Other',
        'Meat', 'Meat, Other', 'Milk - Excluding Butter', 'Millet and products', 'Miscellaneous',
        'Molluscs, Other', 'Mutton & Goat Meat', 'Nuts and products', 'Oats', 'Offals', 'Offals, Edible',
        'Oilcrops', 'Oilcrops Oil, Other', 'Oilcrops, Other', 'Olive Oil', 'Olives (including preserved)',
        'Onions', 'Oranges, Mandarines', 'Palm Oil', 'Palm kernels', 'Palmkernel Oil', 'Peas',
        'Pelagic Fish', 'Pepper', 'Pigmeat', 'Pimento', 'Pineapples and products', 'Plantains',
        'Population', 'Potatoes and products', 'Poultry Meat', 'Pulses', 'Pulses, Other and products',
        'Rape and Mustard Oil', 'Rape and Mustardseed', 'Rice (Milled Equivalent)', 'Rice and products',
        'Roots, Other', 'Rye and products', 'Sesame seed', 'Sesameseed Oil', 'Sorghum and products',
        'Soyabean Oil', 'Soyabeans', 'Spices', 'Spices, Other', 'Starchy Roots', 'Stimulants',
        'Sugar & Sweeteners', 'Sugar (Raw Equivalent)', 'Sugar Crops', 'Sugar beet', 'Sugar cane',
        'Sunflower seed', 'Sunflowerseed Oil', 'Sweet potatoes', 'Sweeteners, Other',
        'Tea (including mate)', 'Tomatoes and products', 'Treenuts', 'Vegetable Oils', 'Vegetables',
        'Vegetables, other', 'Vegetal Products', 'Wheat and products', 'Wine', 'Yams'
    ]
    
    matched_la_items = [
        '', '', '', '', 'Beverages, kombucha, fermented', 'Cephalopods, squid, raw',
        'Cereals, mixed grain, cooked', 'Egg, whole, raw', 'Animal fat, lard', 'Oil, fish, cod liver',
        'Oil, fish, cod liver', 'Fish, tuna, raw', 'Fish, trout, raw', 'Fruit, mixed, raw',
        'Fruit, tropical, raw', '', 'Grapefruit, raw', 'Grapes, raw', 'Oil, peanut', 'Peanuts, raw',
        'Peanuts, shelled, raw', 'Honey', 'Babyfood, infant formula, with iron', 'Lemons, raw',
        'Oil, corn germ', 'Corn, yellow, raw', 'Fish, mackerel, raw', 'Beef, ground, raw',
        'Game meat, venison, raw', 'Milk, whole, fluid', 'Millet, cooked', '', 'Mollusks, oyster, raw',
        'Lamb, ground, raw', 'Nuts, almonds, raw', 'Oats, rolled, uncooked', 'Beef, liver, raw',
        'Beef, liver, raw', '', 'Oil, sesame', 'Seeds, sunflower, raw', 'Oil, olive, extra virgin',
        'Olives, green, canned', 'Onions, raw', 'Oranges, raw', 'Oil, palm', 'Palm kernel, raw',
        'Oil, palm kernel', 'Peas, green, raw', 'Fish, sardine, canned', 'Spices, pepper, black',
        'Pork, ground, raw', 'Pimento, canned', 'Pineapple, raw', 'Plantains, raw', '',
        'Potatoes, raw', 'Chicken, breast, raw', 'Beans, kidney, raw', 'Lentils, raw',
        'Oil, rapeseed', 'Seeds, rapeseed', 'Rice, white, cooked', 'Rice, brown, raw',
        'Carrots, raw', 'Rye, grain, raw', 'Seeds, sesame, raw', 'Oil, sesame',
        'Sorghum, grain, raw', 'Oil, soybean', 'Soybeans, raw', 'Spices, mixed',
        'Spices, cumin, ground', 'Cassava, raw', 'Coffee, brewed', 'Sugar, granulated',
        'Sugar, raw', 'Sugarcane, raw', 'Beets, sugar, raw', 'Sugarcane, raw',
        'Seeds, sunflower, raw', 'Oil, sunflower', 'Sweet potatoes, raw', 'Honey',
        'Tea, black, brewed', 'Tomatoes, raw', 'Nuts, walnuts, raw', 'Oil, vegetable, blended',
        'Vegetables, mixed, frozen', 'Vegetables, leafy, raw', '', 'Wheat, whole grain, raw',
        'Wine, red', 'Yams, raw'
    ]
    
    # Create validation status array using utility function
    validation_status = validate_mapping(fao_items, matched_la_items)
    
    # Log array lengths
    logger.info(f"Length of fao_items: {len(fao_items)}")
    logger.info(f"Length of matched_la_items: {len(matched_la_items)}")
    logger.info(f"Length of validation_status: {len(validation_status)}")
    
    # Create DataFrame
    df = pd.DataFrame({
        'fao_item': fao_items,
        'matched_la_item': matched_la_items,
        'validation_status': validation_status
    })
    
    # Add notes column using utility function
    df['notes'] = df.apply(lambda row: get_notes_for_item(
        row['fao_item'], 
        row['matched_la_item'], 
        row['validation_status']
    ), axis=1)
    
    return df

def main():
    # Create validation DataFrame from validated data
    logger.info("Creating validation DataFrame from validated data")
    validation_df = create_validation_data()
    
    # Load LA content data to get LA values
    logger.info("Loading LA content data")
    la_content_df = pd.read_csv('data/processed/la_content_fireinabottle_processed.csv')
    
    # Add LA content values using utility function
    validation_df['la_content_per_100g'] = validation_df['matched_la_item'].apply(
        lambda x: get_la_content_for_item(x, la_content_df)
    )
    
    # Save the updated validation
    output_path = 'data/processed/fao_la_mapping_validated.csv'
    validation_df.to_csv(output_path, index=False)
    logger.info(f"Saved updated mapping to {output_path}")
    
    # Print statistics
    total_items = len(validation_df)
    approved_items = len(validation_df[validation_df['validation_status'] == 'APPROVED'])
    no_match_items = len(validation_df[validation_df['validation_status'] == 'NO_MATCH'])
    
    logger.info("\nValidation Statistics:")
    logger.info(f"Total FAOSTAT items: {total_items}")
    logger.info(f"Approved matches: {approved_items}")
    logger.info(f"No appropriate match: {no_match_items}")
    logger.info(f"Match rate: {approved_items/total_items*100:.1f}%")

if __name__ == "__main__":
    main() 