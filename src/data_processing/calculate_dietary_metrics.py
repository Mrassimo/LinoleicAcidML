"""
Calculate derived dietary metrics from FAOSTAT and LA content data.
Includes Total LA Intake, % Calories from LA, and Plant Fat Ratio.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from pydantic import BaseModel, Field
import logging
from typing import Dict, List

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DietaryMetrics(BaseModel):
    """Pydantic model for validating dietary metrics"""
    Year: int = Field(..., ge=1961, le=2024)
    Total_LA_Intake_g_per_capita_day: float = Field(..., ge=0)
    LA_Intake_percent_calories: float = Field(..., ge=0, le=100)
    Plant_Fat_Ratio: float = Field(..., ge=0, le=1)
    Total_Calorie_Supply: float = Field(..., ge=0)
    Total_Fat_Supply_g: float = Field(..., ge=0)
    Total_Carb_Supply_g: float = Field(..., ge=0)
    Total_Protein_Supply_g: float = Field(..., ge=0)

def classify_fat_source(item: str) -> str:
    """
    Classify FAOSTAT items as plant or animal fat sources
    """
    # Common animal products
    animal_keywords = [
        'meat', 'fish', 'poultry', 'milk', 'dairy', 'cheese', 'butter',
        'cream', 'egg', 'lard', 'tallow', 'animal', 'beef', 'pork',
        'mutton', 'lamb', 'offal'
    ]
    
    item_lower = item.lower()
    for keyword in animal_keywords:
        if keyword in item_lower:
            return 'Animal'
    
    return 'Plant'

def calculate_la_intake(
    faostat_df: pd.DataFrame,
    la_content_df: pd.DataFrame,
    mapping_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculate LA intake from food supply and LA content data.
    LA content values are typically given as g LA per 100g of fat portion.
    For oils/fats, we use the fat supply directly.
    For other foods, we first get their fat content, then calculate LA based on that.
    """
    # Clean up validation status by stripping quotes and whitespace
    mapping_df['validation_status'] = mapping_df['validation_status'].str.strip().str.strip('"')
    
    # Filter for validated matches only
    validated_mapping = mapping_df[mapping_df['validation_status'] == 'APPROVED']
    
    # Create a lookup dictionary for LA content directly from the mapping file
    la_content_lookup = validated_mapping.set_index('fao_item')['la_content_per_100g'].to_dict()
    
    # Filter FAOSTAT for food supply quantity
    supply_df = faostat_df[
        (faostat_df['data_type'] == 'historical')
    ].copy()
    
    # Calculate LA intake for each item
    la_intake_records = []
    for _, row in supply_df.iterrows():
        fao_item = row['item']
        
        if fao_item in la_content_lookup:
            la_content = la_content_lookup[fao_item]
            
            # For oils and fats, use Fat supply quantity (g/day) directly
            # For other foods, calculate based on their fat content
            if 'oil' in fao_item.lower() or 'fat' in fao_item.lower():
                # Fat supply is already in g/day, multiply by LA percentage
                fat_supply_g = row['Fat supply quantity (g/capita/day)']
                la_intake = fat_supply_g * (la_content / 100)
            else:
                # Get the fat supply for this food item
                fat_supply_g = row['Fat supply quantity (g/capita/day)']
                if pd.isna(fat_supply_g) or fat_supply_g == 0:
                    # Skip items with no fat content
                    continue
                
                # Calculate LA based on the fat content
                la_intake = fat_supply_g * (la_content / 100)
            
            la_intake_records.append({
                'Year': row['year'],
                'Item': fao_item,
                'LA_Intake_g': la_intake
            })
            
            # Log high LA contributors
            if la_intake > 1:  # Log items contributing more than 1g LA per day
                logger.info(f"High LA contributor - Year: {row['year']}, Item: {fao_item}, LA intake: {la_intake:.2f} g/day")
    
    # Convert to DataFrame and aggregate by year
    la_intake_df = pd.DataFrame(la_intake_records)
    if la_intake_df.empty:
        raise ValueError("No LA intake could be calculated. Check mappings and data.")
    
    # Only return the LA intake totals by year, % calories will be calculated later
    yearly_la_intake = la_intake_df.groupby('Year')['LA_Intake_g'].sum().reset_index()
    yearly_la_intake = yearly_la_intake.rename(columns={'LA_Intake_g': 'Total_LA_Intake_g_per_capita_day'})
    
    return yearly_la_intake

def calculate_plant_fat_ratio(faostat_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the ratio of plant-based fats to total fats
    """
    # Filter for historical data
    fat_df = faostat_df[
        (faostat_df['data_type'] == 'historical')
    ].copy()
    
    # Classify fat sources
    fat_df['Fat_Source'] = fat_df['item'].apply(classify_fat_source)
    
    # Calculate yearly totals by source
    yearly_fat = fat_df.groupby(['year', 'Fat_Source'])['Fat supply quantity (g/capita/day)'].sum().unstack(fill_value=0)
    
    # Calculate ratio
    yearly_fat['Total_Fat'] = yearly_fat['Plant'] + yearly_fat['Animal']
    yearly_fat['Plant_Fat_Ratio'] = yearly_fat['Plant'] / yearly_fat['Total_Fat']
    
    # Rename year column to match other functions
    return yearly_fat.reset_index().rename(columns={'year': 'Year'})[['Year', 'Plant_Fat_Ratio']]

def calculate_nutrient_supply(faostat_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate total supply of calories, fat, protein, and carbs using the Grand Total item from FAOSTAT
    """
    # Filter for historical data and Grand Total only
    nutrient_df = faostat_df[
        (faostat_df['data_type'] == 'historical') &
        (faostat_df['item'] == 'Grand Total')
    ].copy()
    
    # Extract the nutrients directly from Grand Total rows (no need to sum)
    yearly_nutrients = nutrient_df[['year', 'Food supply (kcal/capita/day)', 
                                    'Fat supply quantity (g/capita/day)', 
                                    'Protein supply quantity (g/capita/day)']].copy()
    
    # Rename columns
    yearly_nutrients = yearly_nutrients.rename(columns={
        'year': 'Year',
        'Food supply (kcal/capita/day)': 'Total_Calorie_Supply',
        'Fat supply quantity (g/capita/day)': 'Total_Fat_Supply_g',
        'Protein supply quantity (g/capita/day)': 'Total_Protein_Supply_g'
    })
    
    # Calculate carbs (assuming 4 kcal/g for protein and carbs, 9 kcal/g for fat)
    yearly_nutrients['Total_Carb_Supply_g'] = (
        (yearly_nutrients['Total_Calorie_Supply'] - 
         (yearly_nutrients['Total_Fat_Supply_g'] * 9) - 
         (yearly_nutrients['Total_Protein_Supply_g'] * 4)
        ) / 4
    )
    
    # Add log for verification
    logger.info(f"Total calorie range: {yearly_nutrients['Total_Calorie_Supply'].min():.2f} to {yearly_nutrients['Total_Calorie_Supply'].max():.2f} kcal/day")
    logger.info(f"Total fat range: {yearly_nutrients['Total_Fat_Supply_g'].min():.2f} to {yearly_nutrients['Total_Fat_Supply_g'].max():.2f} g/day")
    
    return yearly_nutrients

def main():
    # Set up paths
    data_dir = Path('data')
    processed_dir = data_dir / 'processed'
    
    # Load required datasets
    logger.info("Loading dietary metrics...")
    faostat_df = pd.read_csv(processed_dir / 'faostat_food_balance_sheets.csv')
    la_content_df = pd.read_csv(processed_dir / 'fire_in_a_bottle_la_content.csv')
    mapping_df = pd.read_csv(processed_dir / 'fao_la_mapping_final.csv')
    
    # Calculate LA intake (now only returns LA intake without calorie percentage)
    logger.info("Calculating LA intake...")
    la_intake_df = calculate_la_intake(faostat_df, la_content_df, mapping_df)
    
    # Calculate plant fat ratio
    logger.info("Calculating plant fat ratio...")
    plant_fat_df = calculate_plant_fat_ratio(faostat_df)
    
    # Calculate nutrient supply (includes total calories from ALL foods)
    logger.info("Calculating nutrient supply...")
    nutrient_df = calculate_nutrient_supply(faostat_df)
    
    # Merge all metrics
    metrics_df = pd.merge(la_intake_df, plant_fat_df, on='Year')
    metrics_df = pd.merge(metrics_df, nutrient_df, on='Year')
    
    # Calculate % calories from LA using total calories from ALL foods
    # LA has 9 kcal/g energy density
    metrics_df['LA_Intake_percent_calories'] = (
        (metrics_df['Total_LA_Intake_g_per_capita_day'] * 9) / 
        metrics_df['Total_Calorie_Supply'] * 100
    )
    
    # Validate metrics
    validated_records = []
    for record in metrics_df.to_dict('records'):
        try:
            validated_record = DietaryMetrics(**record)
            validated_records.append(validated_record.dict())
        except Exception as e:
            logger.warning(f"Invalid metrics for year {record['Year']}: {e}")
    
    # Convert back to DataFrame and save
    final_df = pd.DataFrame(validated_records)
    output_path = processed_dir / 'australia_dietary_metrics.csv'
    final_df.to_csv(output_path, index=False)
    logger.info(f"Dietary metrics saved to {output_path}")
    
    # Log some statistics
    logger.info(f"Processed metrics for {len(final_df)} years")
    logger.info(f"Average LA intake: {final_df['Total_LA_Intake_g_per_capita_day'].mean():.2f} g/day")
    logger.info(f"Average % calories from LA: {final_df['LA_Intake_percent_calories'].mean():.2f}%")
    logger.info(f"Average plant fat ratio: {final_df['Plant_Fat_Ratio'].mean():.2f}")

if __name__ == "__main__":
    main() 