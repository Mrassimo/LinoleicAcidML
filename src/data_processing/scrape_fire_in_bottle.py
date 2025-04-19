import logging
# DEBUG LOG: The parser should robustly skip header/separator rows and return None for unrecoverable malformed tables.
# Please confirm this is the intended behaviour before proceeding with code changes.
# ---------------------------------------------------------------------------------
# WARNING: This script relies on the current structure of the source website,
# specifically the presence of data within <pre> tags formatted as pipe-delimited tables.
# If the website changes its structure (e.g., removes or alters <pre> tags, or changes
# the table format), this script will likely break or fail to extract data correctly.
# This fragility is a known limitation. See README.md for further details.
# ---------------------------------------------------------------------------------

import pandas as pd
import requests
from bs4 import BeautifulSoup
import logging
import os
import re # Import regex for cleaning
from io import StringIO # Needed for parsing text blocks that look like tables
from src import config

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
# Constants centralised in config.py
# Use config.FIRE_IN_A_BOTTLE_URL, config.RAW_DATA_DIR, config.FIRE_IN_A_BOTTLE_OUTPUT_FILE
RAW_HTML_DEBUG_FILE = str(config.RAW_DATA_DIR / "debug_raw_html.html")
# Define the columns we absolutely expect in the final output CSV.
# These names will be used as the header row.
EXPECTED_COLUMNS = [
    'food_name', # Name of the food item
    'la_cal',    # Calories from linoleic acid per 100g
    'cal',       # Total calories per 100g
    'percent'    # Percentage of calories from linoleic acid (la_cal / cal * 100)
]

def find_and_parse_pre_blocks(soup: BeautifulSoup) -> pd.DataFrame | None:
    """
    Robustly finds and parses data blocks (preferably <pre>, but will try <code> and <div> as fallback)
    containing pipe-delimited tables. Handles missing, malformed, or changed website structure gracefully.

    This function is designed to be tolerant of minor format issues and will attempt to recover data
    from alternative tags if <pre> is missing. All error messages and comments use Australian English.

    Args:
        soup: A BeautifulSoup object representing the parsed HTML.

    Returns:
        A pandas DataFrame containing the combined parsed data, or None if parsing fails.
    """

    def parse_table_text_block(text: str, block_label: str = "<unknown>") -> pd.DataFrame | None:
        """
        Attempt to parse a text block as a pipe-delimited table.
        Returns a DataFrame or None if parsing fails.
        """
        # Remove separator lines (e.g., +----+---+)
        lines = [line for line in text.strip().split('\n') if not line.strip().startswith('+')]
        # Keep only lines that look like table rows (start with '|' or contain multiple pipes)
        potential_lines = [line for line in lines if line.strip().startswith('|') or line.count('|') >= 2]
        if not potential_lines:
            logging.info(f"No table-like lines found in {block_label}. Skipping.")
            return None

        # Try to extract headers from the first valid line
        header_line = potential_lines[0]
        headers = [h.strip() for h in header_line.strip('|').split('|')]
        if not headers or all(h == "" for h in headers):
            logging.warning(f"Could not extract headers from {block_label}. Skipping.")
            return None

        # Parse data rows, always exclude the header row (even if input is inconsistent)
        parsed_rows = []
        header_norm = [h.strip().lower() for h in headers]
        for line in potential_lines[1:]:
            line_stripped = line.strip()
            if not line_stripped:
                continue
            # Skip lines that are only dashes, only pipes, or look like a header row
            if re.fullmatch(r"[-\s|]+", line_stripped):
                continue
            # Defensive: Only call .strip() if not None
            raw_parts = line_stripped.strip('|').split('|')
            parts = [p.strip() if p is not None else None for p in raw_parts]
            # Pad or truncate to match header length
            if len(parts) < len(headers):
                logging.warning(f"Header/data row mismatch in {block_label}: row has {len(parts)} columns, expected {len(headers)}. Padding with None.")
                parts += [None] * (len(headers) - len(parts))
            elif len(parts) > len(headers):
                logging.warning(f"Header/data row mismatch in {block_label}: row has {len(parts)} columns, expected {len(headers)}. Truncating extra columns.")
                parts = parts[:len(headers)]
            # Skip row if it matches the header (case-insensitive, ignoring whitespace)
            # Defensive: Only call .strip().lower() if p is not None
            parts_norm = [p.strip().lower() if p is not None else "" for p in parts]
            if parts_norm == header_norm:
                continue
            parsed_rows.append(parts)

        if not parsed_rows:
            logging.warning(f"No data rows successfully parsed from {block_label}.")
            return None

        df_block = pd.DataFrame(parsed_rows, columns=headers)
        logging.info(f"Parsed {len(df_block)} rows from {block_label}.")

        # --- Column Renaming and Selection ---
        column_mapping_found = {}
        actual_cols_lower = [col.lower() for col in df_block.columns]
        if 'food' in actual_cols_lower:
            column_mapping_found[df_block.columns[actual_cols_lower.index('food')]] = 'food_name'
        if 'la_cal' in actual_cols_lower:
            column_mapping_found[df_block.columns[actual_cols_lower.index('la_cal')]] = 'la_cal'
        if 'cal' in actual_cols_lower:
            column_mapping_found[df_block.columns[actual_cols_lower.index('cal')]] = 'cal'
        if 'percent' in actual_cols_lower:
            column_mapping_found[df_block.columns[actual_cols_lower.index('percent')]] = 'percent'

        df_block = df_block.rename(columns=column_mapping_found)
        final_block_cols = [col for col in EXPECTED_COLUMNS if col in df_block.columns]
        if final_block_cols:
            df_block_final = df_block[final_block_cols]
            return df_block_final
        else:
            logging.warning(f"Could not map required columns ({EXPECTED_COLUMNS}) in {block_label}. Skipping this block.")
            return None

    # Try <pre> tags first
    pre_tags = soup.find_all('pre')
    logging.info(f"Found {len(pre_tags)} <pre> tag(s).")
    all_data = []
    found_data = False

    if pre_tags:
        for i, pre_tag in enumerate(pre_tags):
            logging.info(f"Processing <pre> tag {i}...")
            pre_text = pre_tag.get_text()
            # Heuristic: Only try to parse if it looks like a table
            if '|' in pre_text and 'food' in pre_text.lower():
                df_block = parse_table_text_block(pre_text, block_label=f"<pre> tag {i}")
                if df_block is not None:
                    all_data.append(df_block)
                    found_data = True
            else:
                logging.info(f"<pre> tag {i} does not appear to contain the formatted data table. Skipping.")
    else:
        logging.warning("No <pre> tags found. Attempting to find data in <code> or <div> tags as fallback.")

        # Try <code> tags
        code_tags = soup.find_all('code')
        for i, code_tag in enumerate(code_tags):
            code_text = code_tag.get_text()
            if '|' in code_text and 'food' in code_text.lower():
                logging.info(f"Processing <code> tag {i} as fallback...")
                df_block = parse_table_text_block(code_text, block_label=f"<code> tag {i}")
                if df_block is not None:
                    all_data.append(df_block)
                    found_data = True

        # Try <div> tags (only those with table-like content)
        if not found_data:
            div_tags = soup.find_all('div')
            for i, div_tag in enumerate(div_tags):
                div_text = div_tag.get_text()
                if '|' in div_text and 'food' in div_text.lower():
                    logging.info(f"Processing <div> tag {i} as fallback...")
                    df_block = parse_table_text_block(div_text, block_label=f"<div> tag {i}")
                    if df_block is not None:
                        all_data.append(df_block)
                        found_data = True

    if not found_data:
        logging.error("Could not find or parse any data block containing the expected data format in <pre>, <code>, or <div> tags.")
        return None

    if not all_data:
        logging.error("No data was successfully extracted from any data block.")
        return None

    combined_df = pd.concat(all_data, ignore_index=True)
    logging.info(f"Combined data from all parsed blocks. Total rows: {len(combined_df)}")

    # --- Final Data Cleaning and Type Conversion ---
    for col in ['la_cal', 'cal', 'percent']:
        if col in combined_df.columns:
            original_dtype = combined_df[col].dtype
            combined_df[col] = pd.to_numeric(combined_df[col], errors='coerce')
            nan_count = combined_df[col].isna().sum()
            if nan_count > 0:
                logging.warning(
                    f"{nan_count} values in column '{col}' (original dtype: {original_dtype}) could not be converted to numeric."
                )
        else:
            logging.warning(f"Expected numeric column '{col}' not found in combined data for type conversion.")

    if 'food_name' in combined_df.columns:
        combined_df['food_name'] = combined_df['food_name'].astype(str).str.strip()
    else:
        logging.warning("Expected column 'food_name' not found in combined data.")

    return combined_df


def scrape_la_content(url: str) -> pd.DataFrame | None:
    """
    Scrapes the linoleic acid content data from the given URL by parsing <pre> tags.

    WARNING: This scraping approach is fragile and depends on the source website
    continuing to provide data in <pre> tags with a specific pipe-delimited format.
    If the website changes, this function will likely break and require maintenance.

    Args:
        url: The URL of the webpage to scrape.

    Returns:
        A pandas DataFrame containing the scraped data, or None if an error occurs.
    """
    try:
        logging.info(f"Attempting to fetch content from {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, timeout=30, headers=headers)
        response.raise_for_status() # Check for HTTP errors (like 404, 500)
        logging.info("Successfully fetched content.")

        # --- Debugging Step: Save Raw HTML ---
        try:
            os.makedirs(config.RAW_DATA_DIR, exist_ok=True) # Ensure dir exists
            with open(RAW_HTML_DEBUG_FILE, 'w', encoding=response.encoding or 'utf-8') as f: # Use detected encoding
                f.write(response.text)
            logging.info(f"Saved raw HTML response for debugging to {RAW_HTML_DEBUG_FILE}")
        except Exception as e_save:
            logging.error(f"Could not save raw HTML debug file: {e_save}")
        # --- /Debugging Step ---

        logging.info("Parsing HTML with BeautifulSoup...")
        try:
            # Using lxml is generally recommended if available (pip install lxml)
            # soup = BeautifulSoup(response.text, 'lxml')
            soup = BeautifulSoup(response.text, 'html.parser')
            logging.info("Using 'html.parser'. If issues persist, consider installing 'lxml'.")
        except Exception as e_parse:
             logging.error(f"BeautifulSoup failed to parse the HTML: {e_parse}")
             return None

        # Find and parse data within <pre> blocks
        df = find_and_parse_pre_blocks(soup)

        if df is not None:
             # Data cleaning and type conversion happens within find_and_parse_pre_blocks
             logging.info(f"Successfully processed data.")
             return df
        else:
             # Errors logged within find_and_parse_pre_blocks
             logging.error("Failed to find or parse data from <pre> blocks.")
             return None

    except requests.exceptions.RequestException as e:
        logging.error(f"Network error fetching URL {url}: {e}")
        return None
    except ImportError:
        logging.error("Required libraries (pandas, requests, beautifulsoup4) not installed.")
        logging.error("Please install them: pip install pandas requests beautifulsoup4")
        # If using lxml: logging.error("Also consider: pip install lxml")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred during scraping: {e}", exc_info=True) # Log traceback
        return None

def save_to_csv(df: pd.DataFrame, path: str):
    """
    Saves the DataFrame to a CSV file with standard formatting.

    Args:
        df: The pandas DataFrame to save.
        path: The full path for the output CSV file.
    """
    try:
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        # Save to CSV, ensuring UTF-8 encoding and no pandas index column
        df.to_csv(path, index=False, encoding='utf-8')
        logging.info(f"Successfully saved data to {path}")
    except Exception as e:
        logging.error(f"Error saving DataFrame to CSV at {path}: {e}")

if __name__ == "__main__":
    logging.info("Starting scraping process...")
    # Ensure OUTPUT_DIR exists before scraping attempt
    os.makedirs(config.RAW_DATA_DIR, exist_ok=True)
    scraped_data = scrape_la_content(config.FIRE_IN_A_BOTTLE_URL)

    if scraped_data is not None and not scraped_data.empty:
        # Ensure final DataFrame has exactly the EXPECTED_COLUMNS in the correct order
        # Create a new DataFrame to guarantee column order and presence
        final_df = pd.DataFrame()
        for col in EXPECTED_COLUMNS:
            if col in scraped_data.columns:
                final_df[col] = scraped_data[col]
            else:
                # If an expected column is missing after parsing, add it with None/NaN
                final_df[col] = None
                logging.warning(f"Expected column '{col}' was not found/mapped in the scraped data. Added as empty column to the final CSV.")

        logging.info(f"Final DataFrame shape before saving: {final_df.shape}")
        logging.info(f"Final DataFrame columns for CSV: {final_df.columns.tolist()}")
        save_to_csv(final_df, str(config.FIRE_IN_A_BOTTLE_OUTPUT_FILE))

    elif scraped_data is not None and scraped_data.empty:
         logging.warning("Scraping process finished, but the resulting DataFrame is empty (no data rows found or parsed).")
    else:
        # Error should have been logged previously if scrape_la_content returned None
        logging.error("Scraping process failed to produce data.")

    logging.info("Scraping process finished.")
