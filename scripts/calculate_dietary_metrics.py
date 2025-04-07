import pandas as pd
import numpy as np
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_data():
    """Load and prepare the required datasets."""
    # Load FAOSTAT data
    fao_df = pd.read_csv('data/processed/faostat_food_balance_sheets.csv')
    
    # Load LA content mapping
    la_mapping = pd.read_csv('data/processed/fao_la_mapping_final.csv')
    
    # Log data shapes
    logging.info(f"Loaded FAOSTAT data: {fao_df.shape} rows")
    logging.info(f"Loaded LA mapping: {la_mapping.shape} rows")
    
    return fao_df, la_mapping

def validate_fao_data(fao_df):
    """Validate FAOSTAT data for potential issues."""
    issues = []
    
    # Check for missing values in key columns
    key_columns = [
        'Food supply quantity (kg/capita/yr)',
        'Fat supply quantity (g/capita/day)',
        'Food supply (kcal/capita/day)',
        'Protein supply quantity (g/capita/day)'
    ]
    
    for col in key_columns:
        missing = fao_df[col].isna().sum()
        if missing > 0:
            issues.append(f"Found {missing} missing values in {col}")
    
    # Check for unreasonable values
    if (fao_df['Food supply quantity (kg/capita/yr)'] > 1000).any():
        issues.append("Found food supply quantities over 1000 kg/capita/yr")
    
    if (fao_df['Fat supply quantity (g/capita/day)'] > 500).any():
        issues.append("Found fat supply quantities over 500 g/day")
    
    if (fao_df['Food supply (kcal/capita/day)'] > 5000).any():
        issues.append("Found calorie supply over 5000 kcal/day")
    
    # Log all issues
    for issue in issues:
        logging.warning(issue)
    
    return len(issues) == 0

def adjust_la_content(la_mapping):
    """Adjust LA content values based on scientific literature."""
    # Create a copy to avoid modifying the original
    adjusted_mapping = la_mapping.copy()
    
    # Adjust specific items based on literature values with clear scientific basis
    adjustments = {
        'Milk - Excluding Butter': 0.08,  # Whole milk typically has ~0.08g LA per 100g
        'Sweeteners, Other': 0.0,  # Sweeteners typically have negligible LA content
        'Sugar & Sweeteners': 0.0,
        'Sugar (Raw Equivalent)': 0.0,
        'Animal Products': 0.0,  # Broad category, should not have direct LA content
        'Aquatic Animals, Others': 0.0,
        'Aquatic Plants': 0.0,
        'Aquatic Products, Other': 0.0,
        'Grand Total': 0.0,  # Not a food item
        'Miscellaneous': 0.0,  # Too vague
        'Oilcrops': 0.0,  # Broad category
        'Population': 0.0,  # Not a food item
        'Vegetal Products': 0.0,  # Broad category
        'Honey': 0.0,  # Honey has negligible LA content
        'Olive Oil': 10.0,  # Olive oil typically has 3-14% LA
        'Sunflowerseed Oil': 65.0,  # Sunflower oil typically has 60-70% LA
        'Vegetable Oils': 52.0,  # Median value for common vegetable oils
        'Fish, Body Oil': 2.0,  # Fish oil typically has low LA content
        'Fish, Liver Oil': 2.0,
        'Fish, Seafood': 0.2,  # Fish typically has low LA content
        'Freshwater Fish': 0.2,
        'Marine Fish, Other': 0.2,
        'Pelagic Fish': 0.2
    }
    
    for item, la_content in adjustments.items():
        if item in adjusted_mapping['fao_item'].values:
            adjusted_mapping.loc[adjusted_mapping['fao_item'] == item, 'la_content_per_100g'] = la_content
            logging.info(f"Adjusted LA content for {item} to {la_content}g/100g")
    
    return adjusted_mapping

def create_food_group_mapping(fao_df):
    """Create a mapping of food items to food groups for imputation purposes."""
    # Define food groups and their member items
    food_groups = {
        'Oils and Fats': [
            'Vegetable Oils', 'Olive Oil', 'Soyabean Oil', 'Sunflowerseed Oil',
            'Groundnut Oil', 'Rape and Mustard Oil', 'Cottonseed Oil', 'Palm Oil',
            'Palmkernel Oil', 'Maize Germ Oil', 'Sesameseed Oil', 'Oilcrops Oil, Other',
            'Butter, Ghee', 'Cream', 'Fats, Animals, Raw', 'Fish, Body Oil', 'Fish, Liver Oil'
        ],
        'Meats': [
            'Bovine Meat', 'Mutton & Goat Meat', 'Pigmeat', 'Poultry Meat', 
            'Meat, Other', 'Offals, Edible'
        ],
        'Grains': [
            'Wheat and products', 'Rice (Milled Equivalent)', 'Barley and products',
            'Maize and products', 'Rye and products', 'Oats', 'Millet and products',
            'Sorghum and products', 'Cereals, Other'
        ],
        'Fruits': [
            'Oranges, Mandarines', 'Lemons, Limes', 'Grapefruit', 'Citrus, Other',
            'Bananas', 'Apples and products', 'Pineapples and products', 'Dates',
            'Grapes and products', 'Fruits, Other'
        ],
        'Vegetables': [
            'Tomatoes and products', 'Onions', 'Vegetables, Other'
        ],
        'Nuts and Seeds': [
            'Groundnuts (Shelled Eq)', 'Coconuts - Incl Copra', 'Sesame seed',
            'Sunflower seed', 'Rape and Mustardseed', 'Cottonseed', 'Coconut Oil',
            'Nuts and products'
        ],
        'Dairy': [
            'Milk - Excluding Butter', 'Cheese', 'Whey'
        ],
        'Fish': [
            'Freshwater Fish', 'Demersal Fish', 'Pelagic Fish', 'Marine Fish, Other',
            'Crustaceans', 'Cephalopods', 'Molluscs, Other', 'Aquatic Animals, Others',
            'Aquatic Products, Other'
        ]
    }
    
    # Create reverse mapping (item to group)
    item_to_group = {}
    for group, items in food_groups.items():
        for item in items:
            item_to_group[item] = group
    
    return item_to_group

def impute_missing_la_values(fao_df, la_mapping):
    """Impute missing LA values based on food group averages instead of using zeros."""
    # Create food group mapping
    item_to_group = create_food_group_mapping(fao_df)
    
    # Add food group to both dataframes
    fao_df['food_group'] = fao_df['item'].map(item_to_group)
    
    # Merge LA content with FAOSTAT data
    fao_with_la = pd.merge(
        fao_df,
        la_mapping[['fao_item', 'la_content_per_100g']],
        left_on='item',
        right_on='fao_item',
        how='left'
    )
    
    # Log items with missing LA content
    missing_la_items = fao_with_la[fao_with_la['la_content_per_100g'].isna()]['item'].unique()
    logging.warning(f"Found {len(missing_la_items)} items without LA content mapping")
    
    # Calculate average LA content by food group for imputation
    group_la_avg = {}
    for group in fao_with_la['food_group'].dropna().unique():
        group_items = fao_with_la[(fao_with_la['food_group'] == group) & 
                                 fao_with_la['la_content_per_100g'].notna()]
        if not group_items.empty:
            group_la_avg[group] = group_items['la_content_per_100g'].mean()
            logging.info(f"Food group '{group}' average LA content: {group_la_avg[group]:.2f}g/100g")
    
    # Impute missing LA values using food group averages
    for idx, row in fao_with_la.iterrows():
        if pd.isna(row['la_content_per_100g']) and not pd.isna(row['food_group']):
            if row['food_group'] in group_la_avg:
                fao_with_la.loc[idx, 'la_content_per_100g'] = group_la_avg[row['food_group']]
                logging.info(f"Imputed LA content for {row['item']} using {row['food_group']} average: {group_la_avg[row['food_group']]:.2f}g/100g")
    
    # For items still missing LA content (no food group or no group average), use 0
    # But log these separately as a limitation
    still_missing = fao_with_la['la_content_per_100g'].isna().sum()
    if still_missing > 0:
        missing_items = fao_with_la[fao_with_la['la_content_per_100g'].isna()]['item'].unique()
        logging.warning(f"Still missing LA content for {still_missing} items after imputation")
        logging.warning("Using 0 for these items, which may lead to underestimation of total LA intake")
        logging.warning(f"Items still missing LA content: {missing_items}")
        fao_with_la['la_content_per_100g'] = fao_with_la['la_content_per_100g'].fillna(0)
    
    return fao_with_la

def calculate_la_intake(fao_df, la_mapping):
    """Calculate total LA intake and % calories from LA."""
    # Adjust LA content values
    adjusted_la_mapping = adjust_la_content(la_mapping)
    
    # Define broad categories to exclude (these sum up other items)
    broad_categories = [
        'Grand Total',
        'Vegetal Products',
        'Animal Products',
        'Cereals - Excluding Beer',
        'Starchy Roots',
        'Sugar & Sweeteners',
        'Pulses',
        'Tree Nuts',
        'Oilcrops',
        'Vegetables',
        'Fruits - Excluding Wine',
        'Stimulants',
        'Spices',
        'Alcoholic Beverages',
        'Miscellaneous',
        'Fish, Seafood',
        'Meat',
        'Offals',
        'Animal fats',
        'Eggs',
        'Milk - Excluding Butter',
        'Aquatic Products, Other'
    ]
    
    # Filter out broad categories
    fao_detailed = fao_df[~fao_df['item'].isin(broad_categories)].copy()
    
    # Impute missing LA values using food group averages
    fao_with_la = impute_missing_la_values(fao_detailed, adjusted_la_mapping)
    
    # Handle duplicate entries by taking the maximum value for each item per year
    # Log duplicates for transparency
    duplicate_items = fao_with_la[fao_with_la.duplicated(['year', 'item'], keep=False)]
    if not duplicate_items.empty:
        logging.warning(f"Found {len(duplicate_items)} duplicate entries")
        for (year, item), group in duplicate_items.groupby(['year', 'item']):
            logging.info(f"Duplicate for {item} in {year}: {len(group)} entries, values: {group['Fat supply quantity (g/capita/day)'].tolist()}")
    
    # Fill NaN values in Fat supply for groupby operations only after logging duplicates
    fao_with_la['Fat supply quantity (g/capita/day)'] = fao_with_la['Fat supply quantity (g/capita/day)'].fillna(0)
    
    # Group by year and item, taking the maximum fat supply value
    fao_with_la = fao_with_la.loc[
        fao_with_la.groupby(['year', 'item'])['Fat supply quantity (g/capita/day)'].idxmax()
    ]
    
    # Calculate LA intake per item (g/day)
    fao_with_la['la_intake_g_day'] = (
        fao_with_la['Food supply quantity (kg/capita/yr)'] * 10 *  # Convert kg/year to g/day
        (fao_with_la['la_content_per_100g'] / 100)  # Apply LA content percentage
    )
    
    # Ensure LA intake doesn't exceed fat supply
    fao_with_la['la_intake_g_day'] = fao_with_la.apply(
        lambda row: min(row['la_intake_g_day'], row['Fat supply quantity (g/capita/day)'])
        if pd.notna(row['Fat supply quantity (g/capita/day)']) and row['Fat supply quantity (g/capita/day)'] > 0
        else row['la_intake_g_day'],
        axis=1
    )
    
    # Log high LA intake items
    high_la_items = fao_with_la[fao_with_la['la_intake_g_day'] > 5].groupby('item')['la_intake_g_day'].mean()
    if not high_la_items.empty:
        logging.info(f"Items with high LA intake (>5g/day):")
        for item, intake in high_la_items.items():
            logging.info(f"  {item}: {intake:.2f} g/day")
    
    # Group by year to get total LA intake and calories
    la_intake = fao_with_la.groupby('year').agg({
        'la_intake_g_day': 'sum',  # Sum LA intake across all items
        'Food supply (kcal/capita/day)': lambda x: x[x.notna()].sum()  # Sum calories across all items
    }).reset_index()
    
    # Calculate % calories from LA (LA has 9 kcal/g)
    la_intake['la_intake_percent_calories'] = (
        (la_intake['la_intake_g_day'] * 9) /  # Convert LA grams to kcal
        la_intake['Food supply (kcal/capita/day)'] * 100  # Convert to percentage
    )
    
    # Rename the calorie column
    la_intake.rename(columns={
        'Food supply (kcal/capita/day)': 'total_calorie_supply'
    }, inplace=True)
    
    # Log summary statistics
    logging.info(f"LA intake summary statistics (per capita):")
    logging.info(f"  Mean: {la_intake['la_intake_g_day'].mean():.2f} g/day")
    logging.info(f"  Median: {la_intake['la_intake_g_day'].median():.2f} g/day")
    logging.info(f"  Min: {la_intake['la_intake_g_day'].min():.2f} g/day")
    logging.info(f"  Max: {la_intake['la_intake_g_day'].max():.2f} g/day")
    
    # Log calorie statistics
    logging.info(f"Calorie intake summary statistics (per capita):")
    logging.info(f"  Mean: {la_intake['total_calorie_supply'].mean():.0f} kcal/day")
    logging.info(f"  Median: {la_intake['total_calorie_supply'].median():.0f} kcal/day")
    logging.info(f"  Min: {la_intake['total_calorie_supply'].min():.0f} kcal/day")
    logging.info(f"  Max: {la_intake['total_calorie_supply'].max():.0f} kcal/day")
    
    return la_intake

def calculate_plant_fat_ratio(fao_df):
    """Calculate the ratio of plant-based fats to total fats."""
    # Define plant-based fat sources (excluding animal products)
    plant_based_items = [
        'Vegetable Oils', 'Olive Oil', 'Soyabean Oil', 'Sunflowerseed Oil',
        'Groundnut Oil', 'Rape and Mustard Oil', 'Cottonseed Oil', 'Palm Oil',
        'Palmkernel Oil', 'Maize Germ Oil', 'Sesameseed Oil', 'Oilcrops Oil, Other'
    ]
    
    # Calculate fat supply by source
    fat_supply = fao_df[fao_df['Fat supply quantity (g/capita/day)'].notna()].copy()
    fat_supply['is_plant'] = fat_supply['item'].isin(plant_based_items)
    
    # Group by year and calculate ratios
    plant_fat_ratio = fat_supply.groupby('year').agg({
        'Fat supply quantity (g/capita/day)': lambda x: (
            x[fat_supply['is_plant']].sum() / x.sum()  # Plant fat / Total fat
        ) if x.sum() > 0 else np.nan  # Handle zero total fat
    }).reset_index()
    
    plant_fat_ratio.rename(
        columns={'Fat supply quantity (g/capita/day)': 'plant_fat_ratio'},
        inplace=True
    )
    
    # Log plant fat ratio statistics
    logging.info(f"Plant fat ratio summary statistics:")
    logging.info(f"  Mean: {plant_fat_ratio['plant_fat_ratio'].mean():.2%}")
    logging.info(f"  Median: {plant_fat_ratio['plant_fat_ratio'].median():.2%}")
    logging.info(f"  Min: {plant_fat_ratio['plant_fat_ratio'].min():.2%}")
    logging.info(f"  Max: {plant_fat_ratio['plant_fat_ratio'].max():.2%}")
    
    return plant_fat_ratio

def handle_methodology_change(df):
    """Handle the methodology change in FAOSTAT data after 2010."""
    # Split data into pre-2010 and post-2010 periods
    pre_2010 = df[df['year'] < 2010].copy()
    post_2010 = df[df['year'] >= 2010].copy()
    
    if len(pre_2010) == 0 or len(post_2010) == 0:
        return df, {}
    
    # Debug: print column names
    logging.info(f"Available columns: {df.columns.tolist()}")
    
    # Calculate adjustment factors based on 2005-2009 vs 2010-2014 averages
    pre_period = pre_2010[pre_2010['year'].between(2005, 2009)]
    post_period = post_2010[post_2010['year'].between(2010, 2014)]
    
    metrics = {
        'la_intake_g_day': 'LA intake',
        'total_calorie_supply': 'calorie',
        'total_fat_supply': 'fat',
        'total_protein_supply': 'protein'
    }
    
    adjustment_factors = {}
    for col, name in metrics.items():
        pre_avg = pre_period[col].mean()
        post_avg = post_period[col].mean()
        factor = pre_avg / post_avg if post_avg != 0 else 1
        adjustment_factors[col] = factor
        logging.info(f"Methodology change adjustment factor for {name}: {factor:.2f}")
    
    # Apply adjustment factors to post-2010 data
    for col in metrics.keys():
        post_2010[col] = post_2010[col] * adjustment_factors[col]
    
    # Combine pre and post periods
    return pd.concat([pre_2010, post_2010]).sort_values('year'), adjustment_factors

def calculate_dietary_metrics():
    """Main function to calculate all dietary metrics."""
    # Load data
    fao_df, la_mapping = load_data()
    
    # Define broad categories to exclude
    broad_categories = [
        'Grand Total',
        'Vegetal Products',
        'Animal Products',
        'Cereals - Excluding Beer',
        'Starchy Roots',
        'Sugar & Sweeteners',
        'Pulses',
        'Tree Nuts',
        'Oilcrops',
        'Vegetables',
        'Fruits - Excluding Wine',
        'Stimulants',
        'Spices',
        'Alcoholic Beverages',
        'Miscellaneous',
        'Fish, Seafood',
        'Meat',
        'Offals',
        'Animal fats',
        'Eggs',
        'Milk - Excluding Butter',
        'Aquatic Products, Other'
    ]
    
    # Filter out broad categories for total supply calculations
    fao_detailed = fao_df[~fao_df['item'].isin(broad_categories)].copy()
    
    # Validate FAOSTAT data
    if not validate_fao_data(fao_detailed):
        logging.warning("Proceeding with calculations despite validation issues")
    
    # Calculate LA intake metrics
    la_intake = calculate_la_intake(fao_df, la_mapping)
    
    # Calculate plant fat ratio
    plant_fat_ratio = calculate_plant_fat_ratio(fao_detailed)
    
    # Handle duplicate entries by taking the maximum value for each nutrient
    fat_supply = fao_detailed.groupby(['year', 'item'])['Fat supply quantity (g/capita/day)'].max().reset_index()
    protein_supply = fao_detailed.groupby(['year', 'item'])['Protein supply quantity (g/capita/day)'].max().reset_index()
    calorie_supply = fao_detailed.groupby(['year', 'item'])['Food supply (kcal/capita/day)'].max().reset_index()
    
    # Sum up the total supply by year
    total_fat = fat_supply.groupby('year')['Fat supply quantity (g/capita/day)'].sum().reset_index()
    total_protein = protein_supply.groupby('year')['Protein supply quantity (g/capita/day)'].sum().reset_index()
    total_calories = calorie_supply.groupby('year')['Food supply (kcal/capita/day)'].sum().reset_index()
    
    # Rename supply columns
    total_fat.rename(columns={'Fat supply quantity (g/capita/day)': 'total_fat_supply'}, inplace=True)
    total_protein.rename(columns={'Protein supply quantity (g/capita/day)': 'total_protein_supply'}, inplace=True)
    total_calories.rename(columns={'Food supply (kcal/capita/day)': 'total_calorie_supply'}, inplace=True)
    
    # Log nutrient supply statistics
    logging.info(f"Nutrient supply summary statistics (per capita):")
    logging.info(f"  Fat - Mean: {total_fat['total_fat_supply'].mean():.1f} g/day")
    logging.info(f"  Fat - Median: {total_fat['total_fat_supply'].median():.1f} g/day")
    logging.info(f"  Protein - Mean: {total_protein['total_protein_supply'].mean():.1f} g/day")
    logging.info(f"  Protein - Median: {total_protein['total_protein_supply'].median():.1f} g/day")
    logging.info(f"  Calories - Mean: {total_calories['total_calorie_supply'].mean():.0f} kcal/day")
    logging.info(f"  Calories - Median: {total_calories['total_calorie_supply'].median():.0f} kcal/day")
    
    # Drop any existing calorie supply columns from la_intake
    if 'total_calorie_supply' in la_intake.columns:
        la_intake = la_intake.drop(columns=['total_calorie_supply'])
    
    # Merge all metrics
    dietary_metrics = pd.merge(la_intake, plant_fat_ratio, on='year')
    dietary_metrics = pd.merge(dietary_metrics, total_fat, on='year')
    dietary_metrics = pd.merge(dietary_metrics, total_protein, on='year')
    dietary_metrics = pd.merge(dietary_metrics, total_calories, on='year')
    
    # Define metrics dictionary for adjustment factors
    metrics = {
        'la_intake_g_day': 'LA intake',
        'total_calorie_supply': 'calorie',
        'total_fat_supply': 'fat',
        'total_protein_supply': 'protein'
    }
    
    # Handle methodology change
    dietary_metrics, adjustment_factors = handle_methodology_change(dietary_metrics)
    
    # Save the results
    dietary_metrics.to_csv('data/processed/australia_dietary_metrics.csv', index=False)
    logging.info("Dietary metrics have been calculated and saved to 'data/processed/australia_dietary_metrics.csv'")
    
    # Save a metadata file with assumptions and limitations
    with open('data/processed/dietary_metrics_metadata.md', 'w') as f:
        f.write("# Dietary Metrics Calculation Metadata\n\n")
        f.write("## Data Processing Assumptions and Limitations\n\n")
        f.write("### FAOSTAT Data Processing\n\n")
        f.write("* **Broad Category Filtering**: Excluded categories that aggregate individual items to avoid double-counting.\n")
        f.write("* **Duplicate Entry Handling**: For items with multiple entries per year, used maximum value after logging duplicates.\n")
        f.write("* **Missing Values**: Used food group imputation for missing LA content. Where food group averages weren't available, filled with 0 (limitation).\n\n")
        f.write("### LA Content Adjustments\n\n")
        f.write("* **Specific Item Adjustments**: Several food items had LA content manually set based on scientific literature:\n")
        f.write("  - Milk: 0.08g/100g\n")
        f.write("  - Olive Oil: 10.0g/100g\n")
        f.write("  - Fish products: 0.2-2.0g/100g\n")
        f.write("  - Vegetable Oils: 52.0g/100g (median of common oils)\n")
        f.write("  - Sunflowerseed Oil: 65.0g/100g\n\n")
        f.write("### Methodology Change Handling (2010 Transition)\n\n")
        f.write("* **Adjustment Factors** applied to post-2010 data to maintain consistency with historical trends:\n")
        for col, name in metrics.items():
            if col in adjustment_factors:
                f.write(f"  - {name}: {adjustment_factors.get(col, 1.0):.2f}\n")
        f.write("\n### Plant Fat Classification\n\n")
        f.write("* **Plant-based Sources**: Explicitly defined list including vegetable oils, olive oil, seed oils\n")
        f.write("* **Ratio Calculation**: Calculated as (Plant Fat Supply / Total Fat Supply) per year\n\n")
    
    logging.info("Dietary metrics metadata has been saved to 'data/processed/dietary_metrics_metadata.md'")
    
    return dietary_metrics

if __name__ == "__main__":
    calculate_dietary_metrics() 