"""
Process Linoleic Acid content data from Fire in a Bottle website data.
Creates a clean lookup table mapping food items to their LA content.
"""

import pandas as pd
from pathlib import Path
from pydantic import BaseModel, Field
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LAContentRecord(BaseModel):
    """Pydantic model for validating LA content records"""
    food_item: str = Field(..., min_length=1)
    linoleic_acid_g_per_100g: float = Field(..., ge=0, le=100)

def clean_la_content_data(file_path: Path) -> pd.DataFrame:
    """
    Clean and validate the LA content data
    """
    try:
        # Read the raw data
        df = pd.read_csv(file_path)
        
        # Basic cleaning
        df = df.copy()
        df.columns = df.columns.str.lower().str.replace(' ', '_')
        
        # Convert columns to required format
        df['food_item'] = df['food_name']
        df['linoleic_acid_g_per_100g'] = (df['la_cal'] / df['cal']) * 100
        
        # Create final DataFrame with required columns
        clean_df = pd.DataFrame({
            'food_item': df['food_item'],
            'linoleic_acid_g_per_100g': df['linoleic_acid_g_per_100g']
        })
        
        # Remove any rows with missing values
        clean_df = clean_df.dropna()
        
        # Validate each record
        validated_records = []
        for record in clean_df.to_dict('records'):
            try:
                validated_record = LAContentRecord(**record)
                validated_records.append(validated_record.dict())
            except Exception as e:
                logger.warning(f"Invalid record: {record}. Error: {e}")
        
        # Convert back to DataFrame
        clean_df = pd.DataFrame(validated_records)
        
        # Sort by LA content (descending) for easier inspection
        clean_df = clean_df.sort_values('linoleic_acid_g_per_100g', ascending=False)
        
        return clean_df
    
    except Exception as e:
        logger.error(f"Error processing LA content data from {file_path}: {e}")
        raise

def main():
    # Set up paths
    data_dir = Path('data')
    raw_dir = data_dir / 'raw'
    processed_dir = data_dir / 'processed'
    processed_dir.mkdir(exist_ok=True)
    
    # Process LA content data
    input_path = raw_dir / 'la_content_fireinabottle_processed.csv'
    clean_df = clean_la_content_data(input_path)
    
    # Save processed data
    # The intermediate cleaned LA content CSV is deprecated; skip saving
    output_path = None
    clean_df.to_csv(output_path, index=False)
    logger.info(f"Processed LA content data saved to {output_path}")
    
    # Log some basic statistics
    logger.info(f"Processed {len(clean_df)} food items")
    logger.info(f"LA content range: {clean_df['linoleic_acid_g_per_100g'].min():.2f} - {clean_df['linoleic_acid_g_per_100g'].max():.2f} g/100g")

if __name__ == "__main__":
    main() 