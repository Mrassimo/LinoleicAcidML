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

* **[ ] Manual: Download ABS Causes of Death Data Cube (Latest release with historical data)**
* **[ ] Manual: Use IHME GBD tool to download Dementia metrics (Prevalence/Incidence/Deaths, Rate/Number, Age-Std, 1990+)**
* **[ ] Manual: Use IHME GBD tool to download CVD metrics (IHD/Stroke Prevalence/Incidence/Deaths, Rate/Number, Age-Std, 1990+)**
* [-] ~~Download AIHW Dementia/CVD Excel files~~ (Superseded by ABS/GBD for long-term analysis)

## Data Processing, Validation & Feature Engineering

* [X] Initial cleaning & standardization of NCD-RisC datasets.
* [X] Process FAOSTAT data (Combine historical/modern, filter AUS, calculate daily units). Save `faostat_food_balance_sheets.csv`.
* [X] Prepare clean Linoleic Acid content lookup table (`fire_in_a_bottle_la_content.csv`).
* [X] Implement and Manually Validate FAOSTAT -> LA Content Semantic Matches. Save `fao_la_mapping_final.csv`.
* [X] Calculate Derived Dietary Metrics (LA Intake, % Cals, Plant Ratio, Totals). Apply adjustments. Save `australia_dietary_metrics.csv`.

* **[ ] Process ABS Causes of Death Data:**
  * [ ] Load data cube.
  * [ ] Filter Australia.
  * [ ] Identify/Map ICD codes for Dementia/Alz, IHD, Stroke across versions.
  * [ ] Aggregate deaths by Year (and Sex if needed).
  * [ ] Extract/Calculate Age-Standardized Mortality Rates (ASMR).
  * [ ] Standardize columns. Save `abs_cod_metrics.csv`.
* **[ ] Process IHME GBD Dementia Data:**
  * [ ] Load downloaded CSV(s).
  * [ ] Select relevant columns (Year, measure, metric, val).
  * [ ] Reshape/Pivot if necessary.
  * [ ] Standardize columns. Save `gbd_dementia_metrics.csv`.
* **[ ] Process IHME GBD CVD Data:**
  * [ ] Load downloaded CSV(s).
  * [ ] Select relevant columns (Year, cause, measure, metric, val).
  * [ ] Reshape/Pivot if necessary.
  * [ ] Standardize columns. Save `gbd_cvd_metrics.csv`.
* **[ ] Consolidate Health Metrics:**
  * [ ] Load processed NCD-RisC, ABS CoD, GBD metric files.
  * [ ] Merge into single health metrics file by Year (`health_outcome_metrics.csv`).
* **[ ] Merge Datasets:**
  * [ ] Merge `australia_dietary_metrics.csv` with `health_outcome_metrics.csv` by Year.
  * [ ] Handle missing values/years. Save `analytical_merged_data.csv`.
* **[ ] Feature Engineering (Lags):**
  * [ ] Create lagged LA intake columns (5, 10, 15, 20 years).
  * [ ] Save final dataset with lags (`analytical_merged_data_with_lags.csv`).
* [-] ~~Implement AIHW Excel processing logic~~ (Superseded)

## Exploratory Data Analysis (on final dataset)

* [ ] Analyse final dataset structure (`analytical_merged_data_with_lags.csv`).
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
* (Previous items related to methodology adjustments, LA imputation etc. remain relevant)
