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
    Finds <pre> blocks potentially containing the data and parses them.

    WARNING: This function is highly dependent on the current structure of the source website.
    It specifically looks for <pre> tags containing pipe-delimited tables. If the website
    changes its structure or removes these <pre> tags, this function will fail.

    Args:
        soup: A BeautifulSoup object representing the parsed HTML.

    Returns:
        A pandas DataFrame containing the combined parsed data, or None if parsing fails.
    """
    pre_tags = soup.find_all('pre')
    logging.info(f"Found {len(pre_tags)} <pre> tag(s).")

    if not pre_tags:
        logging.error("No <pre> tags found on the page. The website structure may have changed. "
                      "This script is fragile to such changes.")
        return None

    if len(pre_tags) > 1:
        logging.warning(f"More than one <pre> tag found ({len(pre_tags)}). "
                        "If the data is not in the first tag, this may indicate a site structure change.")

    all_data = []
    found_data = False

    for i, pre_tag in enumerate(pre_tags):
        logging.info(f"Processing <pre> tag {i}...")
        pre_text = pre_tag.get_text()

        # Heuristic: Check if the text looks like the data table format
        # Check for the header separator line ('+-'), pipe delimiters '|', and 'food' keyword
        if '+-' in pre_text and '|' in pre_text and 'food' in pre_text.lower():
            logging.info(f"<pre> tag {i} seems to contain formatted data. Attempting to parse.")

            try:
                # Clean the text block: remove separator lines starting with '+'
                lines = pre_text.strip().split('\n')
                # Keep only lines that start with '|' (potential header or data)
                potential_lines = [line for line in lines if line.strip().startswith('|')]

                if not potential_lines:
                     logging.warning(f"No lines starting with '|' found in <pre> tag {i}. Skipping.")
                     continue

                # Strategy: Read line by line, split by '|', strip whitespace
                parsed_rows = []
                temp_headers = []

                # Extract headers from the first valid line
                # Assumes the first line starting with '|' is the header
                header_line = potential_lines[0]
                temp_headers = [h.strip() for h in header_line.strip('|').split('|')]
                logging.info(f"Extracted headers from <pre> tag {i}: {temp_headers}")

                # Process data rows (starting from the second potential line)
                for line in potential_lines[1:]:
                    # Ensure it's a data row (starts with '|')
                    if line.strip().startswith('|'):
                        parts = [p.strip() for p in line.strip('|').split('|')]
                        # Check if the number of parts matches the number of headers
                        if len(parts) == len(temp_headers):
                            parsed_rows.append(parts)
                        else:
                            logging.warning(f"Skipping line in <pre> tag {i} due to mismatched parts count ({len(parts)} vs {len(temp_headers)} expected): {line}")

                if not parsed_rows:
                     logging.warning(f"No data rows successfully parsed from <pre> tag {i}.")
                     continue

                # Create DataFrame for this block using extracted headers
                df_block = pd.DataFrame(parsed_rows, columns=temp_headers)
                logging.info(f"Parsed {len(df_block)} rows from <pre> tag {i}.")

                # --- Column Renaming and Selection ---
                # Rename based on the actual headers found to match EXPECTED_COLUMNS standard names
                column_mapping_found = {}
                actual_cols_lower = [col.lower() for col in df_block.columns]

                # Map based on common variations found in the <pre> block headers
                if 'food' in actual_cols_lower:
                    column_mapping_found[df_block.columns[actual_cols_lower.index('food')]] = 'food_name'
                if 'la_cal' in actual_cols_lower:
                     column_mapping_found[df_block.columns[actual_cols_lower.index('la_cal')]] = 'la_cal'
                if 'cal' in actual_cols_lower:
                     column_mapping_found[df_block.columns[actual_cols_lower.index('cal')]] = 'cal'
                if 'percent' in actual_cols_lower: # Check for 'percent' based on definitions
                     column_mapping_found[df_block.columns[actual_cols_lower.index('percent')]] = 'percent'

                df_block = df_block.rename(columns=column_mapping_found)

                # Select only the columns matching our EXPECTED_COLUMNS list
                final_block_cols = [col for col in EXPECTED_COLUMNS if col in df_block.columns]

                if final_block_cols:
                     # Ensure the DataFrame only contains the successfully mapped expected columns
                     df_block_final = df_block[final_block_cols]
                     all_data.append(df_block_final)
                     found_data = True
                     logging.info(f"Added data from <pre> tag {i} with columns: {final_block_cols}")
                else:
                     logging.warning(f"Could not map required columns ({EXPECTED_COLUMNS}) in <pre> tag {i}. Skipping this block.")


            except Exception as e_parse:
                logging.error(f"Error parsing content of <pre> tag {i}: {e_parse}", exc_info=True)
                continue # Try next pre tag
        else:
            logging.info(f"<pre> tag {i} does not appear to contain the formatted data table based on heuristics. Skipping.")


    if not found_data:
        logging.error("Could not find or parse any <pre> block containing the expected data format.")
        return None

    # Combine data from all parsed blocks
    if not all_data:
         logging.error("No data was successfully extracted from any <pre> block.")
         return None

    combined_df = pd.concat(all_data, ignore_index=True)
    logging.info(f"Combined data from all parsed <pre> blocks. Total rows: {len(combined_df)}")

    # --- Final Data Cleaning and Type Conversion ---
    # Ensure columns exist before attempting conversion
    for col in ['la_cal', 'cal', 'percent']:
        if col in combined_df.columns:
            # Convert to numeric, replacing non-numeric values with NaN (Not a Number)
            original_dtype = combined_df[col].dtype
            combined_df[col] = pd.to_numeric(combined_df[col], errors='coerce')
            nan_count = combined_df[col].isna().sum()
            if nan_count > 0:
                logging.warning(f"{nan_count} values in column '{col}' (original dtype: {original_dtype}) could not be converted to numeric.")
        else:
             logging.warning(f"Expected numeric column '{col}' not found in combined data for type conversion.")

    # Ensure food_name is string and stripped (already done during parsing, but double-check)
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
