import os
import requests
import zipfile
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the target directory for raw data
RAW_DATA_DIR = Path("data/raw")
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Define the extraction directories for FAOSTAT data
FAOSTAT_EXTRACT_DIR = RAW_DATA_DIR / "faostat_oceania"
FAOSTAT_HISTORIC_EXTRACT_DIR = RAW_DATA_DIR / "faostat_historic_oceania"
FAOSTAT_EXTRACT_DIR.mkdir(parents=True, exist_ok=True)
FAOSTAT_HISTORIC_EXTRACT_DIR.mkdir(parents=True, exist_ok=True)

# Common headers for requests
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# List of files to download with their specific requirements
FILES_TO_DOWNLOAD = [
    {
        "url": "https://ncdrisc.org/downloads/dm-2024/individual-countries/NCD_RisC_Lancet_2024_Diabetes_Australia.csv",
        "filename": "NCD_RisC_Lancet_2024_Diabetes_Australia.csv",
        "type": "csv"
    },
    {
        "url": "https://ncdrisc.org/downloads/chol/individual-countries/Australia.csv",
        "filename": "NCD_RisC_Cholesterol_Australia.csv",
        "type": "csv"
    },
    {
        "url": "https://ncdrisc.org/downloads/bmi-2024/adult/by_country/NCD_RisC_Lancet_2024_BMI_age_standardised_Australia.csv",
        "filename": "NCD_RisC_Lancet_2024_BMI_age_standardised_Australia.csv",
        "type": "csv"
    },
    {
        "url": "https://www.aihw.gov.au/getmedia/25edf694-fd9b-4f74-bf16-22bbc969a194/AIHW-DEM-02-S2-Prevalence.xlsx",
        "filename": "AIHW-DEM-02-S2-Prevalence.xlsx",
        "type": "excel",
        "headers": {
            'Accept': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'Referer': 'https://www.aihw.gov.au/'
        }
    },
    {
        "url": "https://www.aihw.gov.au/getmedia/e1e90ec9-fc7b-4a7a-a74d-91d7bb4e3ba3/AIHW-DEM-02-S3-Mortality-202409.xlsx",
        "filename": "AIHW-DEM-02-S3-Mortality-202409.xlsx",
        "type": "excel",
        "headers": {
            'Accept': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'Referer': 'https://www.aihw.gov.au/'
        }
    },
    {
        "url": "https://www.aihw.gov.au/getmedia/76862f38-806d-489e-b85b-7974435bc3d7/AIHW-CVD-92-HSVD-facts-data-tables-12122024.xlsx",
        "filename": "AIHW-CVD-92-HSVD-facts-data-tables-12122024.xlsx",
        "type": "excel",
        "headers": {
            'Accept': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'Referer': 'https://www.aihw.gov.au/'
        }
    },
    {
        "url": "https://bulks-faostat.fao.org/production/FoodBalanceSheets_E_Oceania.zip",
        "filename": "FoodBalanceSheets_E_Oceania.zip",
        "type": "zip",
        "extract": True
    },
    {
        "url": "https://bulks-faostat.fao.org/production/FoodBalanceSheetsHistoric_E_Oceania.zip",
        "filename": "FoodBalanceSheetsHistoric_E_Oceania.zip",
        "type": "zip",
        "extract": True,
        "specific_files": ["FoodBalanceSheetsHistoric_E_Oceania.csv"]
    }
]

def validate_file(file_path: Path, file_type: str) -> bool:
    """Validates downloaded files based on their type."""
    try:
        if not file_path.exists():
            return False
        
        if file_path.stat().st_size == 0:
            logging.error(f"File {file_path} is empty")
            return False

        if file_type == "csv":
            df = pd.read_csv(file_path)
            return len(df) > 0
        elif file_type == "excel":
            df = pd.read_excel(file_path)
            return len(df) > 0
        elif file_type == "zip":
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                return len(zip_ref.namelist()) > 0
        return True
    except Exception as e:
        logging.error(f"Validation failed for {file_path}: {e}")
        return False

def download_file(url: str, destination: Path, headers: Optional[Dict] = None, max_retries: int = 3) -> bool:
    """Downloads a file from a URL to a destination path with retries."""
    all_headers = {**DEFAULT_HEADERS, **(headers or {})}
    
    for attempt in range(max_retries):
        try:
            logging.info(f"Attempting to download: {url} (Attempt {attempt + 1}/{max_retries})")
            response = requests.get(url, stream=True, timeout=60, headers=all_headers)
            response.raise_for_status()

            with open(destination, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            logging.info(f"Successfully downloaded: {destination.name}")
            return True
        except requests.exceptions.RequestException as e:
            logging.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
            if destination.exists():
                destination.unlink()
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            continue
        except Exception as e:
            logging.error(f"An unexpected error occurred while downloading {url}: {e}")
            if destination.exists():
                destination.unlink()
            return False
    return False

def extract_zip(zip_path: Path, extract_to: Path, specific_files: Optional[List[str]] = None):
    """
    Extracts a ZIP file to a specified directory.
    
    Args:
        zip_path: Path to the ZIP file
        extract_to: Directory to extract to
        specific_files: Optional list of specific files to extract. If None, extracts all files.
    """
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            if specific_files:
                # Only extract specified files
                for file in specific_files:
                    if file in zip_ref.namelist():
                        zip_ref.extract(file, extract_to)
                        logging.info(f"Successfully extracted {file} from {zip_path.name}")
                    else:
                        logging.warning(f"File {file} not found in {zip_path.name}")
            else:
                # Extract all files
                zip_ref.extractall(extract_to)
                logging.info(f"Successfully extracted all files from {zip_path.name}")
    except zipfile.BadZipFile:
        logging.error(f"Error: {zip_path.name} is not a valid ZIP file or is corrupted.")
    except Exception as e:
        logging.error(f"Failed to extract {zip_path.name}: {e}")

def main():
    """Main function to download and extract files."""
    successful_downloads = []
    failed_downloads = []

    # First handle regular file downloads
    for file_info in FILES_TO_DOWNLOAD:
        url = file_info["url"]
        filename = file_info["filename"]
        file_type = file_info["type"]
        destination_path = RAW_DATA_DIR / filename
        headers = file_info.get("headers")

        if download_file(url, destination_path, headers=headers):
            if validate_file(destination_path, file_type):
                successful_downloads.append(filename)
                # Handle extraction if needed
                if file_info.get("extract"):
                    # Determine extraction directory and specific files
                    extract_dir = FAOSTAT_HISTORIC_EXTRACT_DIR if "Historic" in filename else FAOSTAT_EXTRACT_DIR
                    specific_files = file_info.get("specific_files")
                    extract_zip(destination_path, extract_dir, specific_files)
            else:
                failed_downloads.append(url)
                logging.error(f"File validation failed for {filename}")
        else:
            failed_downloads.append(url)

    # Print summary
    logging.info("\n--- Download Summary ---")
    if successful_downloads:
        logging.info("Successfully downloaded:")
        for f in successful_downloads:
            logging.info(f"  - {f}")
        if any(f.endswith('.zip') for f in successful_downloads):
             logging.info(f"  (ZIP contents extracted to {FAOSTAT_EXTRACT_DIR})")
    else:
        logging.info("No files were downloaded successfully.")

    if failed_downloads:
        logging.warning("\nFailed to download:")
        for url in failed_downloads:
            logging.warning(f"  - {url}")
    else:
        logging.info("\nAll downloads attempted were successful.")

if __name__ == "__main__":
    main()