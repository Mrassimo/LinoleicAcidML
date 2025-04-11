"""Process ABS Causes of Death and IHME GBD data for analytics integration.

This module extracts, cleans, and standardises health outcome metrics from:
- ABS Causes of Death (Excel, manually downloaded)
- IHME GBD (CSV, extracted automatically from a manually downloaded zip)

All code and comments use Australian English.
Follows project modularity, PEP8, and pydantic validation.

Outputs:
- data/processed/abs_cod_metrics.csv
- data/processed/gbd_dementia_metrics.csv
- data/processed/gbd_cvd_metrics.csv

"""

import pandas as pd
from pathlib import Path
from typing import Optional, List
from pydantic import BaseModel, ValidationError
import logging
import zipfile
import shutil

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
STAGING_DIR = Path("data/staging")
IHME_ZIP = RAW_DIR / "IHME-GBD_2021_DATA-31d73d81-1.zip"
IHME_EXTRACTED_DIR = STAGING_DIR / "ihme_gbd_extracted"

ABS_FILE = RAW_DIR / "ABS_Causes_of_Death_Australia.xlsx"  # Update if filename differs

ABS_OUT = PROCESSED_DIR / "abs_cod_metrics.csv"
IHME_DEMENTIA_OUT = PROCESSED_DIR / "gbd_dementia_metrics.csv"
IHME_CVD_OUT = PROCESSED_DIR / "gbd_cvd_metrics.csv"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HealthMetricRecord(BaseModel):
    Year: int
    Metric: str
    Value: float
    Source: str

def process_abs_cod(abs_file: Path = ABS_FILE, output_file: Path = ABS_OUT) -> None:
    """Extract and clean ABS Causes of Death data for Dementia, IHD, Stroke.

    Manual step: Ensure the Excel file is present in data/raw/.
    """
    if not abs_file.exists():
        logger.warning(f"ABS file not found: {abs_file}. Please download and place it in data/raw/.")
        return

    # Example: Read Excel, filter for Australia, select relevant ICD codes, aggregate by year
    # This is a placeholder; update sheet names and columns as per actual file structure.
    df = pd.read_excel(abs_file, sheet_name=None)
    # TODO: Identify correct sheet(s) and columns for Dementia, IHD, Stroke
    # Example: sheet = df['Data']
    # Filter, clean, and standardise columns
    # For demonstration, create a dummy DataFrame
    records = [
        HealthMetricRecord(Year=2000, Metric="Dementia_Mortality_Rate_ABS", Value=25.0, Source="ABS"),
        HealthMetricRecord(Year=2001, Metric="IHD_Mortality_Rate_ABS", Value=120.0, Source="ABS"),
    ]
    out_df = pd.DataFrame([r.dict() for r in records])
    output_file.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(output_file, index=False)
    logger.info(f"ABS metrics saved to {output_file}")

def extract_ihme_zip(zip_path: Path = IHME_ZIP, extract_dir: Path = IHME_EXTRACTED_DIR) -> Optional[Path]:
    """Extract the IHME GBD zip file to the staging directory. Returns the extraction path or None if not found."""
    if not zip_path.exists():
        logger.warning(f"IHME GBD zip file not found: {zip_path}. Please download and place it in data/raw/.")
        return None
    # Clean up any previous extraction
    if extract_dir.exists():
        shutil.rmtree(extract_dir)
    extract_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_dir)
    logger.info(f"Extracted IHME GBD zip to {extract_dir}")
    return extract_dir

def find_ihme_csvs(extract_dir: Path) -> dict:
    """Find relevant IHME CSVs (Dementia, CVD) in the extracted directory."""
    dementia_csv = None
    cvd_csv = None
    for csv_file in extract_dir.glob("*.csv"):
        name = csv_file.name.lower()
        if "dementia" in name:
            dementia_csv = csv_file
        elif "cvd" in name or "ihd" in name or "stroke" in name:
            cvd_csv = csv_file
    return {"dementia": dementia_csv, "cvd": cvd_csv}

def process_ihme_gbd(
    zip_path: Path = IHME_ZIP,
    extract_dir: Path = IHME_EXTRACTED_DIR,
    dementia_out: Path = IHME_DEMENTIA_OUT,
    cvd_out: Path = IHME_CVD_OUT,
) -> None:
    """Extract and clean IHME GBD CSVs for Dementia and CVD.

    The IHME GBD zip file must be manually downloaded and placed in data/raw/.
    This function will automatically extract and process the relevant CSVs.
    """
    extracted = extract_ihme_zip(zip_path, extract_dir)
    if extracted is None:
        return

    csvs = find_ihme_csvs(extract_dir)
    # Dementia
    if not csvs["dementia"] or not csvs["dementia"].exists():
        logger.warning("IHME Dementia CSV not found in extracted zip.")
    else:
        try:
            df = pd.read_csv(csvs["dementia"])
            # TODO: Filter for Australia, select relevant metrics, standardise columns
            # For demonstration, create a dummy DataFrame
            records = [
                HealthMetricRecord(Year=2000, Metric="Dementia_Prevalence_Rate_GBD", Value=1.2, Source="IHME_GBD"),
                HealthMetricRecord(Year=2001, Metric="Dementia_Death_Rate_GBD", Value=2.3, Source="IHME_GBD"),
            ]
            out_df = pd.DataFrame([r.dict() for r in records])
            dementia_out.parent.mkdir(parents=True, exist_ok=True)
            out_df.to_csv(dementia_out, index=False)
            logger.info(f"IHME Dementia metrics saved to {dementia_out}")
        except Exception as e:
            logger.error(f"Error processing IHME Dementia CSV: {e}")

    # CVD
    if not csvs["cvd"] or not csvs["cvd"].exists():
        logger.warning("IHME CVD CSV not found in extracted zip.")
    else:
        try:
            df = pd.read_csv(csvs["cvd"])
            # TODO: Filter for Australia, select relevant metrics, standardise columns
            # For demonstration, create a dummy DataFrame
            records = [
                HealthMetricRecord(Year=2000, Metric="CVD_Prevalence_Rate_GBD", Value=3.4, Source="IHME_GBD"),
                HealthMetricRecord(Year=2001, Metric="CVD_Death_Rate_GBD", Value=4.5, Source="IHME_GBD"),
            ]
            out_df = pd.DataFrame([r.dict() for r in records])
            cvd_out.parent.mkdir(parents=True, exist_ok=True)
            out_df.to_csv(cvd_out, index=False)
            logger.info(f"IHME CVD metrics saved to {cvd_out}")
        except Exception as e:
            logger.error(f"Error processing IHME CVD CSV: {e}")

if __name__ == "__main__":
    process_abs_cod()
    process_ihme_gbd()