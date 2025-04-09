import pandas as pd
import numpy as np
from pydantic import BaseModel, validator, Field
from typing import Optional, Dict, List
from fuzzywuzzy import fuzz, process
import logging
import os
from datetime import datetime
import pyarrow.feather as feather
import gc

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MergedDatasetSchema(BaseModel):
    """Pydantic model for validating merged dataset"""
    area_code: int = Field(..., description="FAOSTAT area code")
    area: str = Field(..., description="Country/region name")
    item_code: int = Field(..., description="FAOSTAT item code")
    item: str = Field(..., description="Food item name")
    year: int = Field(..., description="Year of observation")
    value: float = Field(..., description="FAOSTAT metric value")
    la_perc: Optional[float] = Field(None, description="Linoleic acid percentage")
    health_metric: Optional[float] = Field(None, description="Health outcome metric")
    health_metric_type: Optional[str] = Field(None, description="Type of health metric")
    source: str = Field(..., description="Data source identifier")

    @validator('la_perc')
    def validate_la_perc(cls, v):
        if v is not None and (v < 0 or v > 100):
            raise ValueError('Linoleic acid percentage must be between 0-100')
        return v

def fuzzy_match_foods(
    faostat_items: List[str],
    fire_items: List[str],
    threshold: int = 80
) -> Dict[str, str]:
    """
    Perform fuzzy string matching between FAOSTAT and Fire in a Bottle food items.
    
    Args:
        faostat_items: List of food items from FAOSTAT
        fire_items: List of food items from Fire in a Bottle
        threshold: Minimum match score (0-100)
        
    Returns:
        Dictionary mapping FAOSTAT items to best Fire in a Bottle matches
    """
    matches = {}
    for faostat_item in faostat_items:
        best_match, score = process.extractOne(
            faostat_item,
            fire_items,
            scorer=fuzz.token_set_ratio
        )
        if score >= threshold:
            matches[faostat_item] = best_match
            logger.info(f"Matched '{faostat_item}' to '{best_match}' (score: {score})")
        else:
            logger.warning(f"No good match found for '{faostat_item}' (best score: {score})")
    
    return matches

def merge_faostat_fire(
    faostat_df: pd.DataFrame,
    fire_df: pd.DataFrame,
    merge_stats_path: str,
    chunk_size: int = 50000  # Process in chunks to reduce memory usage
) -> pd.DataFrame:
    """
    Merge FAOSTAT data with Fire in a Bottle linoleic acid content using fuzzy matching.
    
    Args:
        faostat_df: Cleaned FAOSTAT DataFrame
        fire_df: Processed Fire in a Bottle DataFrame
        merge_stats_path: Path to save merge statistics report
        chunk_size: Number of rows to process at once
        
    Returns:
        Merged DataFrame with linoleic acid content
    """
    logger.info("Starting merge of FAOSTAT with Fire in a Bottle")
    
    # Get unique food items for matching
    faostat_items = faostat_df['item'].unique().tolist()
    fire_items = fire_df['food_name'].unique().tolist()
    
    # Perform fuzzy matching
    logger.info(f"Performing fuzzy matching for {len(faostat_items)} FAOSTAT items")
    item_mapping = fuzzy_match_foods(faostat_items, fire_items)
    
    # Create merge statistics
    total_items = len(faostat_items)
    matched_items = len(item_mapping)
    merge_stats = {
        'total_faostat_items': total_items,
        'matched_items': matched_items,
        'unmatched_items': total_items - matched_items,
        'match_percentage': round((matched_items / total_items) * 100, 1),
        'match_threshold': 80,
        'timestamp': datetime.now().isoformat()
    }
    
    # Save merge statistics
    stats_df = pd.DataFrame([merge_stats])
    stats_df.to_csv(merge_stats_path, index=False)
    logger.info(f"Saved merge statistics to {merge_stats_path}")
    
    # Create mapping DataFrame
    mapping_df = pd.DataFrame({
        'faostat_item': list(item_mapping.keys()),
        'fire_item': list(item_mapping.values())
    })
    
    # Process data in chunks to reduce memory usage
    chunks = [faostat_df[i:i + chunk_size] for i in range(0, len(faostat_df), chunk_size)]
    merged_chunks = []
    
    for i, chunk in enumerate(chunks):
        logger.info(f"Processing chunk {i+1}/{len(chunks)} ({len(chunk)} rows)")
        
        # Merge linoleic acid data
        chunk_merged = chunk.merge(
            mapping_df,
            left_on='item',
            right_on='faostat_item',
            how='left'
        ).merge(
            fire_df,
            left_on='fire_item',
            right_on='food_name',
            how='left'
        )
        
        # Add source indicator
        chunk_merged['source'] = np.where(
            chunk_merged['fire_item'].notna(),
            'FAOSTAT + Fire in a Bottle',
            'FAOSTAT only'
        )
        
        # Keep only essential columns to reduce memory
        essential_cols = [
            'area_code', 'area', 'item_code', 'item', 'element', 'unit',
            'year', 'value', 'linoleic_acid_perc', 'source'
        ]
        
        # Rename columns for clarity
        column_mapping = {'linoleic_acid_perc': 'la_perc'}
        
        # Get only columns that exist
        available_cols = [col for col in essential_cols if col in chunk_merged.columns]
        chunk_merged = chunk_merged[available_cols].rename(columns=column_mapping)
        
        # Append to result list
        merged_chunks.append(chunk_merged)
        
        # Clear memory
        del chunk_merged
        gc.collect()
    
    # Combine all chunks
    merged_df = pd.concat(merged_chunks, ignore_index=True)
    logger.info(f"Completed merge, final shape: {merged_df.shape}")
    
    return merged_df

def merge_health_data(
    merged_df: pd.DataFrame,
    health_df: pd.DataFrame,
    health_metric: str,
    merge_stats_path: str
) -> pd.DataFrame:
    """
    Merge dietary data with health outcomes by year.
    
    Args:
        merged_df: Merged FAOSTAT + Fire in a Bottle DataFrame
        health_df: Health outcomes DataFrame
        health_metric: Name of health metric to merge
        merge_stats_path: Path to save merge statistics report
        
    Returns:
        DataFrame with health metrics merged by year
    """
    # Ensure year column exists in both datasets
    if 'year' not in health_df.columns:
        raise ValueError("Health DataFrame must contain 'year' column")
    
    # Select relevant health columns
    health_cols = ['year', health_metric]
    health_subset = health_df[health_cols].copy()
    health_subset.columns = ['year', 'health_metric_value']
    health_subset['health_metric_type'] = health_metric
    
    # Merge with dietary data
    health_merged = merged_df.merge(
        health_subset,
        on='year',
        how='left',
        indicator='health_merge'
    )
    
    # Calculate merge statistics
    total_records = len(health_merged)
    matched_records = sum(health_merged['health_merge'] == 'both')
    merge_stats = {
        'health_metric': health_metric,
        'total_records': total_records,
        'matched_records': matched_records,
        'unmatched_records': total_records - matched_records,
        'match_percentage': round((matched_records / total_records) * 100, 1),
        'merge_type': 'year',
        'timestamp': datetime.now().isoformat()
    }
    
    # Append to existing merge stats if file exists
    if os.path.exists(merge_stats_path):
        existing_stats = pd.read_csv(merge_stats_path)
        stats_df = pd.concat([existing_stats, pd.DataFrame([merge_stats])])
    else:
        stats_df = pd.DataFrame([merge_stats])
    
    stats_df.to_csv(merge_stats_path, index=False)
    logger.info(f"Updated merge statistics with health data at {merge_stats_path}")
    
    # Clean up columns
    health_merged = health_merged.rename(columns={
        'health_metric_value': 'health_metric',
        'health_merge': '_merge_indicator'
    }).drop(columns=['_merge_indicator'])
    
    return health_merged

def validate_merged_data(df: pd.DataFrame) -> Dict[int, List[str]]:
    """
    Validate merged dataset against schema.
    
    Args:
        df: Merged DataFrame to validate
        
    Returns:
        Dictionary of row numbers to error messages
    """
    errors = {}
    records = df.to_dict('records')
    
    for i, record in enumerate(records, start=1):
        try:
            MergedDatasetSchema(**record)
        except Exception as e:
            errors[i] = [str(err) for err in e.errors()]
            logger.error(f"Validation error in row {i}: {errors[i]}")
    
    return errors

def save_merged_dataset(
    df: pd.DataFrame,
    output_path: str,
    validation_report_path: str
) -> None:
    """
    Save merged dataset with validation report.
    
    Args:
        df: Merged DataFrame to save
        output_path: Path to save Feather file
        validation_report_path: Path to save validation report
    """
    # Validate data
    errors = validate_merged_data(df)
    
    # Generate validation report
    if errors:
        report_data = []
        for row_num, error_msgs in errors.items():
            for msg in error_msgs:
                report_data.append({
                    'row_number': row_num,
                    'error_message': msg
                })
        
        report_df = pd.DataFrame(report_data)
        report_df.to_csv(validation_report_path, index=False)
        logger.warning(f"Validation report saved to {validation_report_path}")
    else:
        logger.info("No validation errors found in merged data")
    
    # Save valid records only
    valid_indices = [i-1 for i in range(1, len(df)+1) if i not in errors]
    df_validated = df.iloc[valid_indices]
    
    # Save to Feather format
    feather.write_feather(df_validated, output_path)
    logger.info(f"Saved validated merged dataset to {output_path}")

def generate_merge_documentation(
    stats_paths: List[str],
    output_md_path: str
) -> None:
    """
    Generate markdown documentation of merge operations.
    
    Args:
        stats_paths: List of paths to merge statistics files
        output_md_path: Path to save markdown documentation
    """
    docs = ["# Dataset Merge Documentation", ""]
    docs.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    docs.append("")
    
    for path in stats_paths:
        if not os.path.exists(path):
            continue
            
        stats_df = pd.read_csv(path)
        docs.append(f"## Merge Statistics: {os.path.basename(path)}")
        docs.append("")
        docs.append(stats_df.to_markdown(index=False))
        docs.append("")
    
    # Write to file
    os.makedirs(os.path.dirname(output_md_path), exist_ok=True)
    with open(output_md_path, 'w') as f:
        f.write("\n".join(docs))
    
    logger.info(f"Merge documentation saved to {output_md_path}")

def main(force_processing=False):
    """Run the dataset merging process."""
    logger.info("=== Starting dataset merge process ===")
    
    # Define paths
    # Deprecated intermediate FAOSTAT file removed
    faostat_path = None
    fire_path = 'data/processed/la_content_fireinabottle_processed.csv'
    output_path = 'data/processed/merged_faostat_fire.csv'
    feather_path = 'data/processed/merged_faostat_fire.feather'
    stats_path = 'data/processed/merge_statistics.csv'
    
    # Check if output already exists, skip processing unless forced
    if os.path.exists(feather_path) and not force_processing:
        logger.info(f"Output file {feather_path} already exists. Skipping processing.")
        logger.info("Use --force flag to force reprocessing if needed.")
        return
    
    try:
        # Load the cleaned datasets
        logger.info(f"Loading FAOSTAT data from {faostat_path}")
        faostat_df = pd.read_csv(faostat_path)
        
        logger.info(f"Loading Fire in a Bottle data from {fire_path}")
        fire_df = pd.read_csv(fire_path)
        
        # Filter FAOSTAT data to only essential elements before merging
        # This reduces memory usage and processing time
        essential_elements = [
            'Food supply (kcal/capita/day)', 
            'Fat supply quantity (g/capita/day)'
        ]
        
        if 'element' in faostat_df.columns:
            logger.info(f"Filtering FAOSTAT data to essential elements")
            original_len = len(faostat_df)
            faostat_df = faostat_df[faostat_df['element'].isin(essential_elements)]
            logger.info(f"Filtered from {original_len} to {len(faostat_df)} rows")
        
        # Merge FAOSTAT with Fire in a Bottle
        merged_df = merge_faostat_fire(faostat_df, fire_df, stats_path)
        
        # Save the merged dataset
        save_merged_dataset(merged_df, output_path, stats_path.replace('.csv', '_validation.csv'))
        
        # Also save as feather for faster reading
        logger.info(f"Saving to feather format: {feather_path}")
        feather.write_feather(merged_df, feather_path)
        
        logger.info("=== Dataset merge completed successfully ===")
    
    except Exception as e:
        logger.error(f"Error in merge process: {e}")
        raise

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Merge FAOSTAT and Fire in a Bottle datasets.')
    parser.add_argument('--force', action='store_true', help='Force processing even if output files exist')
    args = parser.parse_args()
    
    main(force_processing=args.force)