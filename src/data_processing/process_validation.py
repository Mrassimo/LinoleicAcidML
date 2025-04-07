"""
Process the validated FAOSTAT to LA content mapping table and create final mapping.
"""

import pandas as pd
from pathlib import Path
import logging
from difflib import get_close_matches

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

def create_validation_data():
    """
    Create validation DataFrame from the provided validation data
    """
    validation_data = {
        'fao_item': [
            'Alcohol, Non-Food', 'Alcoholic Beverages', 'Animal Products', 'Animal fats',
            'Apples and products', 'Aquatic Animals, Others', 'Aquatic Products, Other',
            'Bananas', 'Barley and products', 'Beans', 'Beer', 'Beverages, Alcoholic',
            'Beverages, Fermented', 'Bovine Meat', 'Butter, Ghee', 'Cassava and products',
            'Cereals - Excluding Beer', 'Cereals, Other', 'Citrus, Other', 'Cloves',
            'Cocoa Beans and products', 'Coconut Oil', 'Coconuts - Incl Copra',
            'Coffee and products', 'Cottonseed', 'Cottonseed Oil', 'Cream', 'Crustaceans',
            'Dates', 'Demersal Fish'
        ],
        'matched_la_item': [
            'Beverages, Wine, non-alcoholic', 'Alcoholic beverage, wine, cooking',
            'Animal fat, bacon grease', 'Animal fat, bacon grease',
            'Babyfood, fruit, applesauce, junior', 'Fish, shark, mixed species, raw',
            'Fish, ocean perch, Atlantic, raw', 'Bananas, raw', 'Barley, pearled, cooked',
            'Beans, liquid from stewed kidney beans', 'Alcoholic beverage, beer, light',
            'Beverages, Wine, non-alcoholic', 'Beverages, tea, Oolong, brewed',
            'Beef, variety meats and by-products, liver, cooked', 'Butter, without salt',
            'Cassava, raw', 'Cereals, MALT-O-MEAL, original, plain, dry',
            'Cereals, whole wheat hot natural cereal, dry', 'Lemons, raw, without peel',
            'Spices, cloves, ground', 'Candies, milk chocolate coated coffee beans',
            'Oil, coconut', 'Oil, coconut', 'Beverages, coffee, brewed, espresso',
            'Shortening, household, soybean-cottonseed', 'Oil, cottonseed, salad or cooking',
            'Cream, fluid, light whipping', 'Crustaceans, lobster, northern, raw',
            'Dates, deglet noor', 'Fish, tilapia, raw'
        ],
        'manual_validation_status': [
            'No Match', 'Approved', 'Rejected', 'Approved', 'Rejected', 'Rejected',
            'Rejected', 'Approved', 'Approved', 'Rejected', 'Approved', 'Rejected',
            'Rejected', 'Rejected', 'Approved', 'Approved', 'Rejected', 'Approved',
            'Rejected', 'Approved', 'Rejected', 'Approved', 'Rejected', 'Approved',
            'Rejected', 'Approved', 'Approved', 'Approved', 'Approved', 'Rejected'
        ],
        'corrected_la_item': [
            '', '', '', '', 'Apples, raw', '', '', '', '', 'Beans, kidney, raw',
            '', 'Alcoholic beverage, wine', '', 'Beef, ground, raw', '', '', 'Cereals, whole grain',
            '', 'Citrus fruit, raw', '', 'Cocoa powder, unsweetened', '', 'Coconut, raw',
            '', 'Cottonseed oil', '', '', '', '', 'Fish, cod, raw'
        ],
        'notes': [
            'Non-food item (industrial alcohol); LA content is for food items only.',
            'High similarity; wine is a representative alcoholic beverage.',
            'Low similarity; "Animal Products" is broad (meat, dairy, eggs); "bacon grease" is too specific. Suggest a broader match or "No Match."',
            'Moderate similarity; both are animal fats, reasonable match (LA ~10.18 g).',
            'Moderate similarity; "Babyfood" is processed; suggest "Apples, raw" (LA ~0.74 g).',
            'Low similarity; "Aquatic Animals" is broad; "shark" is specific. Suggest a general seafood match.',
            'Low similarity; broad category needs a general aquatic match.',
            'High similarity; direct match, likely low LA content.',
            'Moderate similarity; processed form fits "products," likely low LA.',
            'Moderate similarity; "liquid" isn\'t representative; suggest "Beans, kidney, raw."',
            'Moderate similarity; "beer, light" is a type of beer, reasonable match.',
            'High similarity, but "non-alcoholic" doesn\'t fit; suggest "Alcoholic beverage, wine."',
            'Moderate similarity; tea isn\'t typically fermented; suggest a fermented drink like kombucha.',
            'Low similarity; "Bovine Meat" is muscle meat, not organs; suggest "Beef, ground, raw."',
            'Moderate similarity; butter is a form of ghee, reasonable match.',
            'High similarity; "Cassava, raw" fits "products."',
            'Moderate similarity; "MALT-O-MEAL" is specific; suggest a general cereal.',
            'Moderate similarity; whole wheat cereal fits "Other."',
            'Low similarity; "Lemons" are specific; suggest a general citrus item.',
            'Moderate similarity; direct match for cloves.',
            'Moderate similarity; "Candies" are processed; suggest "Cocoa powder" or "Cocoa beans, raw."',
            'Very high similarity; direct match.',
            'Moderate similarity; "Oil" is processed; suggest "Coconut, raw."',
            'Moderate similarity; espresso is a type of coffee, reasonable match.',
            'Low similarity; "Shortening" is processed; suggest "Cottonseed oil."',
            'Moderate similarity; direct match for cottonseed oil.',
            'Moderate similarity; light whipping cream fits "Cream."',
            'Moderate similarity; lobster is a type of crustacean.',
            'Moderate similarity; direct match for dates.',
            'Low similarity; tilapia is freshwater, demersal fish are marine; suggest "Fish, cod, raw."'
        ]
    }
    return pd.DataFrame(validation_data)

def process_validation(validation_df: pd.DataFrame, la_df: pd.DataFrame) -> pd.DataFrame:
    """
    Process the validated mapping table to create final mapping
    """
    # Create final mapping DataFrame
    final_mapping = []
    
    # Get list of available food names and manual mapping
    available_names = la_df['food_name'].unique().tolist()
    manual_mapping = get_manual_mapping()
    
    for _, row in validation_df.iterrows():
        status = row['manual_validation_status'].lower()
        if status == 'approved':
            # Use the original match
            final_mapping.append({
                'fao_item': row['fao_item'],
                'matched_la_item': row['matched_la_item'],
                'validation_status': 'APPROVED',
                'notes': row['notes']
            })
        elif status == 'rejected' and pd.notna(row['corrected_la_item']) and row['corrected_la_item']:
            # Use the corrected match
            final_mapping.append({
                'fao_item': row['fao_item'],
                'matched_la_item': row['corrected_la_item'],
                'validation_status': 'CORRECTED',
                'notes': row['notes']
            })
        elif status == 'no match':
            # Mark as having no appropriate match
            final_mapping.append({
                'fao_item': row['fao_item'],
                'matched_la_item': None,
                'validation_status': 'NO_MATCH',
                'notes': row['notes']
            })
    
    final_df = pd.DataFrame(final_mapping)
    
    # Add LA content information
    la_content = (la_df.groupby('food_name')['la_cal'].first() / 
                 la_df.groupby('food_name')['cal'].first() * 100).round(2)
    
    # Try to find LA content for each item
    for idx, row in final_df.iterrows():
        if pd.isna(row['matched_la_item']) or row['validation_status'] == 'NO_MATCH':
            continue
            
        la_value = la_content.get(row['matched_la_item'])
        if pd.isna(la_value):
            # Try to find a close match
            closest_match, similarity = find_closest_match(row['matched_la_item'], available_names, manual_mapping)
            if closest_match:
                logger.info(f"Found match for '{row['matched_la_item']}': '{closest_match}' "
                          f"(LA content: {la_content.get(closest_match)}%)")
                final_df.at[idx, 'matched_la_item'] = closest_match
                final_df.at[idx, 'notes'] = f"{row['notes']} [Original item mapped to: {closest_match}]"
            else:
                logger.warning(f"No LA content found for '{row['matched_la_item']}' (FAO item: {row['fao_item']})")
                # Show some available similar items for manual review
                similar_items = get_close_matches(row['matched_la_item'], available_names, n=3, cutoff=0.3)
                if similar_items:
                    logger.warning(f"  Suggested alternatives:")
                    for item in similar_items:
                        logger.warning(f"  * {item} (LA content: {la_content.get(item)}%)")
    
    final_df['la_content_per_100g'] = final_df['matched_la_item'].map(la_content)
    
    # Log items with missing LA content
    missing_la = final_df[pd.isna(final_df['la_content_per_100g']) & 
                         (final_df['validation_status'] != 'NO_MATCH')]
    if not missing_la.empty:
        logger.warning("\nItems missing LA content:")
        for _, row in missing_la.iterrows():
            logger.warning(f"- FAO: {row['fao_item']}, LA item: {row['matched_la_item']}")
            # Show some available similar items
            similar_items = get_close_matches(row['matched_la_item'], available_names, n=3, cutoff=0.3)
            if similar_items:
                logger.warning(f"  Suggested alternatives:")
                for item in similar_items:
                    logger.warning(f"  * {item} (LA content: {la_content.get(item)}%)")
    
    return final_df

def main():
    # Set up paths
    data_dir = Path('data')
    processed_dir = data_dir / 'processed'
    
    # Create validation DataFrame from provided data
    validation_df = create_validation_data()
    
    # Load LA content data
    la_path = processed_dir / 'fire_in_a_bottle_la_content.csv'
    la_df = pd.read_csv(la_path)
    
    # Process validation and create final mapping
    final_mapping = process_validation(validation_df, la_df)
    
    # Save final mapping
    output_path = processed_dir / 'fao_la_mapping_final.csv'
    final_mapping.to_csv(output_path, index=False)
    logger.info(f"Saved final mapping to {output_path}")
    
    # Print summary
    total = len(final_mapping)
    approved = (final_mapping['validation_status'] == 'APPROVED').sum()
    corrected = (final_mapping['validation_status'] == 'CORRECTED').sum()
    no_match = (final_mapping['validation_status'] == 'NO_MATCH').sum()
    has_la = final_mapping['la_content_per_100g'].notna().sum()
    
    print("\nValidation Summary:")
    print(f"Total FAOSTAT items: {total}")
    print(f"Approved matches: {approved}")
    print(f"Corrected matches: {corrected}")
    print(f"No appropriate match: {no_match}")
    print(f"Items with LA content: {has_la}")
    print(f"\nFinal mapping saved to {output_path}")

if __name__ == "__main__":
    main() 