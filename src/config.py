"""
Centralised configuration module for the ETL pipeline.
All configurable parameters (paths, URLs, model names, etc.) are defined here.
Use Australian English for all comments and variable names.
"""

from pathlib import Path

# === Directory Paths ===
RAW_DATA_DIR = Path("data/raw")
PROCESSED_DATA_DIR = Path("data/processed")
STAGING_DATA_DIR = Path("data/staging")
DATA_DIR = Path("data")
FIGURES_DIR = Path("figures")
REPORTS_DIR = Path("reports")

# === Download URLs and Filenames ===
NCD_DIABETES_URL = "https://ncdrisc.org/downloads/dm-2024/individual-countries/NCD_RisC_Lancet_2024_Diabetes_Australia.csv"
NCD_DIABETES_FILENAME = "NCD_RisC_Lancet_2024_Diabetes_Australia.csv"

NCD_CHOLESTEROL_URL = "https://ncdrisc.org/downloads/chol/individual-countries/Australia.csv"
NCD_CHOLESTEROL_FILENAME = "NCD_RisC_Cholesterol_Australia.csv"

NCD_BMI_URL = "https://ncdrisc.org/downloads/bmi-2024/adult/by_country/NCD_RisC_Lancet_2024_BMI_age_standardised_Australia.csv"
NCD_BMI_FILENAME = "NCD_RisC_Lancet_2024_BMI_age_standardised_Australia.csv"

AIHW_PREVALENCE_URL = "https://www.aihw.gov.au/getmedia/25edf694-fd9b-4f74-bf16-22bbc969a194/AIHW-DEM-02-S2-Prevalence.xlsx"
AIHW_PREVALENCE_FILENAME = "AIHW-DEM-02-S2-Prevalence.xlsx"

AIHW_MORTALITY_URL = "https://www.aihw.gov.au/getmedia/e1e90ec9-fc7b-4a7a-a74d-91d7bb4e3ba3/AIHW-DEM-02-S3-Mortality-202409.xlsx"
AIHW_MORTALITY_FILENAME = "AIHW-DEM-02-S3-Mortality-202409.xlsx"

AIHW_CVD_URL = "https://www.aihw.gov.au/getmedia/76862f38-806d-489e-b85b-7974435bc3d7/AIHW-CVD-92-HSVD-facts-data-tables-12122024.xlsx"
AIHW_CVD_FILENAME = "AIHW-CVD-92-HSVD-facts-data-tables-12122024.xlsx"

FAOSTAT_FBS_URL = "https://bulks-faostat.fao.org/production/FoodBalanceSheets_E_Oceania.zip"
FAOSTAT_FBS_FILENAME = "FoodBalanceSheets_E_Oceania.zip"

FAOSTAT_HISTORIC_URL = "https://bulks-faostat.fao.org/production/FoodBalanceSheetsHistoric_E_Oceania.zip"
FAOSTAT_HISTORIC_FILENAME = "FoodBalanceSheetsHistoric_E_Oceania.zip"
FAOSTAT_HISTORIC_SPECIFIC_FILES = ["FoodBalanceSheetsHistoric_E_Oceania.csv"]

FIRE_IN_A_BOTTLE_URL = "https://fireinabottle.net/foods-highest-and-lowest-in-linoleic-acid-n6-pufa/"
FIRE_IN_A_BOTTLE_OUTPUT_FILE = RAW_DATA_DIR / "la_content_fireinabottle_processed.csv"

# === Processed Data Filenames ===
FAOSTAT_PROCESSED_FILE = PROCESSED_DATA_DIR / "faostat_fbs_australia_processed.csv"
FAOSTAT_LA_MAPPING_FILE = PROCESSED_DATA_DIR / "fao_la_mapping_validated.csv"
DIETARY_METRICS_FILE = PROCESSED_DATA_DIR / "dietary_metrics_australia_calculated.csv"
DIETARY_METRICS_METADATA_FILE = PROCESSED_DATA_DIR / "dietary_metrics_metadata.md"
HEALTH_METRICS_FILE = PROCESSED_DATA_DIR / "health_metrics_australia_combined.csv"
AIHW_PREVALENCE_PROCESSED_FILE = PROCESSED_DATA_DIR / "aihw_dementia_prevalence_australia_processed.csv"
AIHW_MORTALITY_PROCESSED_FILE = PROCESSED_DATA_DIR / "aihw_dementia_mortality_australia_processed.csv"
AIHW_CVD_PROCESSED_FILE = PROCESSED_DATA_DIR / "aihw_cvd_metrics_australia_processed.csv"
ANALYTICAL_DATA_FINAL_FILE = PROCESSED_DATA_DIR / "analytical_data_australia_final.csv"
ANALYTICAL_DATA_VALIDATION_ERRORS_FILE = PROCESSED_DATA_DIR / "analytical_data_validation_errors.csv"
FAO_LA_MAPPING_SEMANTIC_MATCHES_FILE = PROCESSED_DATA_DIR / "fao_la_mapping_semantic_matches.csv"
LA_CONTENT_FIREINABOTTLE_PROCESSED_FILE = PROCESSED_DATA_DIR / "la_content_fireinabottle_processed.csv"

# === Model Names ===
SENTENCE_TRANSFORMER_MODEL = "all-MiniLM-L6-v2"

# === Miscellaneous ===
# ABS Causes of Death (Australia) 2023 Excel file
ABS_CAUSES_OF_DEATH_URL = "https://www.abs.gov.au/statistics/health/causes-death/causes-death-australia/2023/2023_01%20Underlying%20causes%20of%20death%20%28Australia%29.xlsx"
ABS_CAUSES_OF_DEATH_FILENAME = "2023_01 Underlying causes of death (Australia).xlsx"
# Add any additional configuration parameters here as needed.