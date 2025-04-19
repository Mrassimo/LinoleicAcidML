"""Process ABS Causes of Death and IHME GBD data for analytics integration.

This module extracts, cleans, and standardises health outcome metrics from:
- ABS Causes of Death (Excel, manually downloaded)
- IHME GBD (CSV, extracted automatically from a manually downloaded zip)

All code and comments use Australian English spelling.
Follows project modularity, PEP8, and pydantic validation.

Outputs:
- data/processed/abs_cod_metrics.csv
- data/processed/gbd_dementia_metrics.csv
- data/processed/gbd_cvd_metrics.csv

"""

import pandas as pd
from pathlib import Path
from typing import Optional, List, Dict
from pydantic import BaseModel, ValidationError, Field
import logging
import zipfile
import shutil
import numpy as np

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
STAGING_DIR = Path("data/staging")
IHME_ZIP = RAW_DIR / "IHME-GBD_2021_DATA-31d73d81-1.zip"
IHME_EXTRACTED_DIR = STAGING_DIR / "ihme_gbd_extracted"

ABS_FILE = RAW_DIR / "ABS_Causes_of_Death_Australia.xlsx"

ABS_OUT = PROCESSED_DIR / "abs_cod_metrics.csv"
IHME_DEMENTIA_OUT = PROCESSED_DIR / "gbd_dementia_metrics.csv"
IHME_CVD_OUT = PROCESSED_DIR / "gbd_cvd_metrics.csv"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HealthMetricRecord(BaseModel):
    """Pydantic model for health metric records."""
    Year: int = Field(..., ge=1980, le=2025)
    Metric: str
    Value: float = Field(..., ge=0)
    Source: str
    Age_Group: Optional[str] = None
    Sex: Optional[str] = None
    Measure: Optional[str] = None
    Location: str = "Australia"

def clean_column_name(col: str) -> str:
    """Standardise column names to snake_case."""
    return col.lower().replace(" ", "_").replace("-", "_").replace("/", "_").replace("(", "").replace(")", "")

def process_abs_cod(abs_file: Path = ABS_FILE, output_file: Path = ABS_OUT) -> None:
    """Extract and clean ABS Causes of Death data for Dementia, IHD, Stroke.
    
    Processes the ABS Excel file to extract age-standardised mortality rates
    for key conditions. Handles ICD code changes across years.
    """
    if not abs_file.exists():
        logger.warning(f"ABS file not found: {abs_file}. Please download and place it in data/raw/.")
        return

    try:
        # Read the Excel file - adjust sheet name based on actual file
        df = pd.read_excel(abs_file, sheet_name="Mortality Rates")
        
        # Clean column names
        df.columns = [clean_column_name(col) for col in df.columns]
        
        # Filter for relevant conditions and standardise
        condition_mapping = {
            "dementia": ["Dementia", "Alzheimer", "Senile dementia"],
            "ihd": ["Ischaemic heart disease", "Coronary heart disease"],
            "stroke": ["Cerebrovascular disease", "Stroke"]
        }
        
        records = []
        for year in df["year"].unique():
            year_data = df[df["year"] == year]
            
            # Process each condition group
            for condition, terms in condition_mapping.items():
                # Filter rows containing any of the terms
                condition_data = year_data[
                    year_data["cause_of_death"].str.contains("|".join(terms), case=False, na=False)
                ]
                
                if not condition_data.empty:
                    # Get age-standardised rate
                    rate = condition_data["age_standardised_rate"].mean()
                    
                    # Create standardised metric name
                    metric_name = f"{condition.upper()}_Mortality_Rate_ABS"
                    
                    # Create record
                    record = HealthMetricRecord(
                        Year=year,
                        Metric=metric_name,
                        Value=rate,
                        Source="ABS_COD",
                        Measure="Mortality_Rate"
                    )
                    records.append(record)
        
        # Convert to DataFrame and save
        out_df = pd.DataFrame([r.dict() for r in records])
        output_file.parent.mkdir(parents=True, exist_ok=True)
        out_df.to_csv(output_file, index=False)
        logger.info(f"ABS metrics saved to {output_file}")
        
    except Exception as e:
        logger.error(f"Error processing ABS CoD file: {e}")
        raise

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

def process_ihme_csv(csv_path: Path, condition: str) -> List[HealthMetricRecord]:
    """Process a single IHME CSV file for a specific condition."""
    df = pd.read_csv(csv_path)
    
    # Clean column names
    df.columns = [clean_column_name(col) for col in df.columns]
    
    # Filter for Australia
    df = df[df["location"].str.contains("Australia", case=False, na=False)]
    
    # Define metrics to extract
    metrics = {
        "prevalence": "Prevalence_Rate",
        "incidence": "Incidence_Rate",
        "deaths": "Death_Rate"
    }
    
    records = []
    for year in df["year"].unique():
        year_data = df[df["year"] == year]
        
        for measure, metric_suffix in metrics.items():
            # Filter for the measure
            measure_data = year_data[year_data["measure"].str.contains(measure, case=False, na=False)]
            
            if not measure_data.empty:
                # Get age-standardised rate
                rate = measure_data["val"].mean()
                
                # Create standardised metric name
                metric_name = f"{condition}_{metric_suffix}_GBD"
                
                # Create record
                record = HealthMetricRecord(
                    Year=year,
                    Metric=metric_name,
                    Value=rate,
                    Source="IHME_GBD",
                    Measure=measure.capitalize()
                )
                records.append(record)
    
    return records

def process_ihme_gbd(
    zip_path: Path = IHME_ZIP,
    extract_dir: Path = IHME_EXTRACTED_DIR,
    dementia_out: Path = IHME_DEMENTIA_OUT,
    cvd_out: Path = IHME_CVD_OUT,
) -> None:
    """Extract and clean IHME GBD CSVs for Dementia and CVD."""
    extracted = extract_ihme_zip(zip_path, extract_dir)
    if extracted is None:
        return

    try:
        csvs = find_ihme_csvs(extract_dir)
        
        # Process Dementia data
        if csvs["dementia"] and csvs["dementia"].exists():
            dementia_records = process_ihme_csv(csvs["dementia"], "Dementia")
            dementia_df = pd.DataFrame([r.dict() for r in dementia_records])
            dementia_out.parent.mkdir(parents=True, exist_ok=True)
            dementia_df.to_csv(dementia_out, index=False)
            logger.info(f"IHME Dementia metrics saved to {dementia_out}")
        else:
            logger.warning("IHME Dementia CSV not found in extracted zip.")
        
        # Process CVD data
        if csvs["cvd"] and csvs["cvd"].exists():
            cvd_records = process_ihme_csv(csvs["cvd"], "CVD")
            cvd_df = pd.DataFrame([r.dict() for r in cvd_records])
            cvd_out.parent.mkdir(parents=True, exist_ok=True)
            cvd_df.to_csv(cvd_out, index=False)
            logger.info(f"IHME CVD metrics saved to {cvd_out}")
        else:
            logger.warning("IHME CVD CSV not found in extracted zip.")
            
    except Exception as e:
        logger.error(f"Error processing IHME GBD data: {e}")
        raise
    finally:
        # Clean up extracted files
        if extract_dir.exists():
            shutil.rmtree(extract_dir)
            logger.info("Cleaned up extracted IHME files")

if __name__ == "__main__":
    process_abs_cod()
    process_ihme_gbd()