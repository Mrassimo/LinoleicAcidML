# Australian Health Data Collection & Analysis Tasks

## Environment Setup

* [X] Install required tools
* [X] Create project directory structure
* [X] Set up virtual environment
* [X] Install dependencies

## Data Collection

* [X] Web scraping setup for LA content
* [X] Download NCD-RisC datasets (Diabetes, Cholesterol, BMI)
* [X] Download FAOSTAT datasets (Historical, Modern)
* [X] Automated download script implemented for NCD-RisC/FAOSTAT.

## Data Processing, Validation & Feature Engineering

* [X] Initial cleaning & standardization of NCD-RisC datasets.
* [X] Process FAOSTAT data (Combine historical/modern, filter AUS, calculate daily units). Save `faostat_food_balance_sheets.csv`.
* [X] Prepare clean Linoleic Acid content lookup table (`fire_in_a_bottle_la_content.csv`).
* [X] Implement and Manually Validate FAOSTAT -> LA Content Semantic Matches. Save `fao_la_mapping_final.csv`.
* [X] Calculate Derived Dietary Metrics (LA Intake, % Cals, Plant Ratio, Totals). Apply adjustments. Save `australia_dietary_metrics.csv`.

## Exploratory Data Analysis (on final dataset)

* [X] Analyse final dataset structure (`analytical_merged_data_with_lags.csv`).
* [ ] Generate time series plots (note different start years).
* [ ] Calculate and visualize correlation matrix.
* [ ] Analyze distributions.

## Predictive & Explanatory Modeling

* [ ] Split data (time-series aware).
* [ ] Fit MLR models (adjust timeframe based on outcome availability).
* [ ] Fit GAMs (adjust timeframe based on outcome availability).
* [ ] (Optional) Fit ARIMAX models.
* [ ] (Optional) Fit Tree-based models.
* [ ] Interpret and synthesize results across models and timeframes.

## Documentation

* [X] Document data sources (NCD-RisC, FAOSTAT, LA).

* **[ ] Document ABS CoD source (incl. data cube version, ICD codes used).**
* **[ ] Document IHME GBD source (incl. GBD round, selections made).**

* [X] Document FAOSTAT/LA processing & adjustments.

* **[ ] Document ABS/GBD processing steps.**

* [ ] Document semantic matching methodology and validation results.
* [ ] Document derived dietary metric calculations.
* [ ] Write final analysis methodology and results summary (acknowledging data limitations).
* [ ] Update `README.md`.

## Testing

* [ ] Add test suite for ABS CoD processing.
* [ ] Add test suite for GBD processing.
* [X] Add tests for dietary metric calculations.

* [-] Add tests for semantic matching logic.

## Discovered During Work

* (Keep existing relevant items)
* **[X] Identified AIHW data sources lack historical depth for 1980+ analysis.**
* **[X] Switched Dementia/CVD outcomes to ABS CoD (Mortality) and IHME GBD (Prevalence/Incidence).**
* **[X] Fixed AIHW time series data processing for sheets S3.3 and S3.5 to properly extract historical dementia mortality data.**
* **[X] Implemented strict year validation (2009-2022 only) for AIHW data to prevent invalid years from appearing in processed datasets.**
* **[X] Refined AIHW data extraction to focus on the most relevant sheets: S2.4 for dementia prevalence (2010-2025), S3.5 for dementia mortality (2009-2022), and Table 11 for CVD mortality with complete data from 1980-2022.**
* **[X] Fixed critical issue with Total Supply Calculation to properly use the Grand Total values from FAOSTAT instead of summing across all individual food items.**
* (Previous items related to methodology adjustments, LA imputation etc. remain relevant)
