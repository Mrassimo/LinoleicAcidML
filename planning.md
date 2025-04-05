# Australian Health & Dietary Trends: Project Plan

## Project Overview

This project investigates the relationship between seed oil intake (focusing on linoleic acid) and metabolic health outcomes (diabetes, cardiovascular disease, dementia, and mortality) in Australia. The analysis will span from 1980 to the present, leveraging dietary data from 1961 onward where available to provide context. The primary focus is on constructing a robust data asset through extensive data engineering, followed by predictive modeling to explore diet-health relationships.

## Project Phases

### Phase 1: Data Collection & Preparation

- **Objective**: Gather and prepare datasets to enable analysis of linoleic acid intake and health outcomes.
- **Tasks**:
  - Scrape linoleic acid content data from the Fire in a Bottle website using FireCrawl.
  - Download metabolic health and dietary datasets from specified URLs using FireDuck.
  - Validate data structures with Pydantic to ensure consistency and quality.
  - Clean and standardize datasets (e.g., convert formats, handle missing values).
  - Develop a comprehensive data dictionary documenting columns, data types, and key variables.
  - Plan data merges with Mermaid diagrams to visualize relationships.
  - Generate detailed data summary reports for all processed datasets.

### Phase 2: Exploratory Data Analysis (Data Engineering Focus)

- **Objective**: Construct a unified data asset linking dietary patterns to health outcomes, emphasizing engineering over visualization.
- **Tasks**:
  - Analyze each dataset's structure (CSVs and Excel files) to identify mergeable columns (e.g., year, region).
  - Map FAO food consumption data to linoleic acid content using Fire in a Bottle and Australian Food Composition Database (AFCD) data, potentially with AI-assisted fuzzy matching.
  - Merge health datasets (NCD-RisC, AIHW) by year (and region where available), focusing on 1980-present.
  - Create Mermaid diagrams to document join logic and data flow.
  - Execute merges with FireDuck to build the data asset.
  - Perform basic validation (e.g., summary stats, missing data checks) to confirm asset quality.

### Phase 3: Predictive Modeling

- **Objective**: Use the data asset to model relationships between linoleic acid intake and metabolic health outcomes from 1980 onward.
- **Tasks**:
  - Apply time series models (e.g., ARIMA) to forecast health trends based on dietary data.
  - Use regression models (e.g., multiple regression) to quantify the impact of linoleic acid and other factors (e.g., BMI) on health outcomes.
  - Split data into training (e.g., 1980-2000) and testing (2001-2024) sets for validation.
  - Generate results highlighting key predictors and model performance.

### Phase 4: React visualisation and github pages intergration

* **Objective**:  begin process of merging with git repo.. to publish all phases.. as a portfolio project
* generate beautiful graphics and react charts

## Data Sources

### Metabolic Health Data

- **Diabetes**: NCD Risk Factor Collaboration (1980-2024)
  - URL: [https://ncdrisc.org/downloads/dm-2024/individual-countries/NCD_RisC_Lancet_2024_Diabetes_Australia.csv](https://ncdrisc.org/downloads/dm-2024/individual-countries/NCD_RisC_Lancet_2024_Diabetes_Australia.csv)
- **Cholesterol**: NCD Risk Factor Collaboration
  - URL: [https://ncdrisc.org/downloads/chol/individual-countries/Australia.csv](https://ncdrisc.org/downloads/chol/individual-countries/Australia.csv)
- **Adult BMI**: NCD Risk Factor Collaboration
  - URL: [https://ncdrisc.org/downloads/bmi-2024/adult/by_country/NCD_RisC_Lancet_2024_BMI_age_standardised_Australia.csv](https://ncdrisc.org/downloads/bmi-2024/adult/by_country/NCD_RisC_Lancet_2024_BMI_age_standardised_Australia.csv)
- **Dementia Prevalence**: AIHW
  - URL: [https://www.aihw.gov.au/getmedia/25edf694-fd9b-4f74-bf16-22bbc969a194/AIHW-DEM-02-S2-Prevalence.xlsx](https://www.aihw.gov.au/getmedia/25edf694-fd9b-4f74-bf16-22bbc969a194/AIHW-DEM-02-S2-Prevalence.xlsx)
- **Dementia Mortality**: AIHW
  - URL: [https://www.aihw.gov.au/getmedia/e1e90ec9-fc7b-4a7a-a74d-91d7bb4e3ba3/AIHW-DEM-02-S3-Mortality-202409.xlsx](https://www.aihw.gov.au/getmedia/e1e90ec9-fc7b-4a7a-a74d-91d7bb4e3ba3/AIHW-DEM-02-S3-Mortality-202409.xlsx)
- **Cardiovascular Disease**: AIHW
  - URL: [https://www.aihw.gov.au/getmedia/76862f38-806d-489e-b85b-7974435bc3d7/AIHW-CVD-92-HSVD-facts-data-tables-12122024.xlsx](https://www.aihw.gov.au/getmedia/76862f38-806d-489e-b85b-7974435bc3d7/AIHW-CVD-92-HSVD-facts-data-tables-12122024.xlsx)

### Dietary Data

- **FAOSTAT Food Balance Sheets**: Food supply data (1961-present)
  - URL: https://bulks-faostat.fao.org/production/FoodBalanceSheets_E_Oceania.zip (Extract filter for Australia)
- Linoleic Acid Reference
- **Fire in a Bottle**: Foods highest/lowest in linoleic acid (firecraw web scrape this table)
  - URL: [https://fireinabottle.net/foods-highest-and-lowest-in-linoleic-acid-n6-pufa/](https://fireinabottle.net/foods-highest-and-lowest-in-linoleic-acid-n6-pufa/)

## Data Integration Notes

- Use ISO3 code (AUS) for consistency across datasets where applicable.
- Focus joins on the year (1980-present for analysis, 1961-present for dietary context).
- Leverage state/territory breakdowns where available (e.g., AIHW data).
- Plan for AI-assisted matching of FAO food categories to linoleic acid content due to broad categorizations (e.g., "vegetable oils").

### Data Cleaning and Standardisation

- AIHW datasets have been cleaned to remove empty columns ('region', 'indigenous_status', 'notes') that provided no analytical value.
- A comprehensive data summary report (`reports/processed_data_summary.md`) has been generated containing:
  - Dataset overviews (rows, columns, memory usage)
  - Detailed column information and statistics
  - Value distributions and sample data
  - Missing value analysis
  - Data quality metrics
- Standard column names have been implemented across datasets to facilitate merging:
  - year: Temporal reference
  - value: Numeric measurements
  - metric_type: Type of measurement
  - sex: Gender categories
  - age_group: Age brackets
  - condition: Health condition or measurement type
  - source_sheet: Original data source

## Expected Outcomes

- A unified data asset linking Australian dietary patterns (1961-present) to metabolic health outcomes (1980-present).
- Predictive models identifying key dietary drivers of health trends.
- Comprehensive documentation including:
  - Data dictionary
  - Mermaid diagrams
  - Detailed data quality reports
  - Processing methodology documentation
