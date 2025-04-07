"""
Perform semantic matching between FAOSTAT food items and LA content items using sentence embeddings.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from pydantic import BaseModel, Field
import logging
from typing import List, Dict, Tuple

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ItemMatch(BaseModel):
    """Pydantic model for validating item matches"""
    fao_item: str = Field(..., min_length=1)
    matched_la_item: str = Field(..., min_length=1)
    similarity_score: float = Field(..., ge=0, le=1)
    manual_validation_status: str = Field(default='PENDING')

def preprocess_item_name(item_name: str) -> str:
    """
    Preprocess item names for better matching
    """
    # Convert to lowercase
    item_name = item_name.lower()
    
    # Remove common prefixes/suffixes that might interfere with matching
    prefixes_to_remove = ['raw ', 'processed ', 'prepared ']
    for prefix in prefixes_to_remove:
        if item_name.startswith(prefix):
            item_name = item_name[len(prefix):]
    
    return item_name

def find_best_matches(
    fao_items: List[str],
    la_items: List[str],
    similarity_matrix: np.ndarray,
    similarity_threshold: float = 0.5
) -> List[Dict]:
    """
    Find best matches between FAOSTAT items and LA content items using semantic similarity
    """
    # Preprocess item names
    fao_items_clean = [preprocess_item_name(item) for item in fao_items]
    la_items_clean = [preprocess_item_name(item) for item in la_items]
    
    # Find best matches
    matches = []
    for i, fao_item in enumerate(fao_items):
        best_match_idx = np.argmax(similarity_matrix[i])
        similarity_score = similarity_matrix[i][best_match_idx]
        
        match = {
            'fao_item': fao_item,
            'matched_la_item': la_items[best_match_idx],
            'similarity_score': float(similarity_score),
            'manual_validation_status': 'PENDING'
        }
        
        # Only include matches above threshold
        if similarity_score >= similarity_threshold:
            try:
                validated_match = ItemMatch(**match)
                matches.append(validated_match.dict())
            except Exception as e:
                logger.warning(f"Invalid match: {match}. Error: {e}")
    
    return matches

def load_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load the processed FAOSTAT and LA content data
    """
    try:
        data_dir = Path('data')
        processed_dir = data_dir / 'processed'
        
        # Load FAOSTAT data
        fao_path = processed_dir / 'faostat_food_balance_sheets.csv'
        fao_df = pd.read_csv(fao_path)
        
        # Load LA content data
        la_path = processed_dir / 'fire_in_a_bottle_la_content.csv'
        la_df = pd.read_csv(la_path)
        
        return fao_df, la_df
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        return None, None

def get_unique_items(fao_df: pd.DataFrame, la_df: pd.DataFrame) -> Tuple[List[str], List[str]]:
    """
    Get unique food items from both datasets
    """
    fao_items = sorted(fao_df['item'].unique())
    la_items = sorted(la_df['food_name'].unique())
    
    logger.info(f"Found {len(fao_items)} unique FAOSTAT items and {len(la_items)} unique LA items")
    return fao_items, la_items

def generate_embeddings(items: List[str], model: SentenceTransformer) -> np.ndarray:
    """
    Generate embeddings for a list of items using a sentence transformer model
    """
    # Preprocess item names
    items_clean = [preprocess_item_name(item) for item in items]
    
    # Generate embeddings
    logger.info("Generating embeddings...")
    embeddings = model.encode(items_clean, show_progress_bar=True)
    
    return embeddings

def main():
    # Load data
    fao_df, la_df = load_data()
    
    # Get unique items
    fao_items, la_items = get_unique_items(fao_df, la_df)
    
    # Load model
    logger.info("Loading sentence transformer model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Generate embeddings
    logger.info("Generating embeddings for FAOSTAT items...")
    fao_embeddings = generate_embeddings(fao_items, model)
    logger.info("Generating embeddings for LA content items...")
    la_embeddings = generate_embeddings(la_items, model)
    
    # Calculate similarity
    logger.info("Calculating similarity matrix...")
    similarity_matrix = cosine_similarity(fao_embeddings, la_embeddings)
    
    # Find best matches
    logger.info("Finding best matches...")
    matches = find_best_matches(fao_items, la_items, similarity_matrix)
    
    # Create and save mapping table
    mapping_df = pd.DataFrame(matches)
    output_path = Path('data') / 'processed' / 'fao_la_mapping.csv'
    mapping_df.to_csv(output_path, index=False)
    logger.info(f"Saved mapping table to {output_path}")
    
    # Print summary
    needs_validation = mapping_df['manual_validation_status'] == 'PENDING'
    logger.info(f"Total matches: {len(mapping_df)}")
    logger.info(f"Matches needing validation: {needs_validation.sum()}")
    logger.info(f"Auto-approved matches: {(~needs_validation).sum()}")

if __name__ == "__main__":
    main() 