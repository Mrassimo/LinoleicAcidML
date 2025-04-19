# Project Tasks (Derived from apply.md Review – 12 April 2025)

This file tracks the specific tasks identified in the `apply.md` review received on 12 April 2025, focused on fixing minor test issues and refining visualisations for impact. It also includes subsequent fixes.

---

**Status Update (12 April 2025):**
All tasks derived from the `apply.md` review (received 12 April 2025) have been completed.

- AIHW test failures have been resolved.
- A dedicated analysis script (`src/run_analysis.py`) has been created.
- Key visualisations (LA Trend, Juxtaposing Trends, Lagged Scatter, Correlation Heatmap) have been refined as per the review recommendations.
- The project is ready for final review or further analysis steps.

---

## Task List (Based on apply.md Review - 12 April 2025)

1. **[X] Fix AIHW Test Failures**

   * **Files:** `tests/test_process_aihw_data.py`, `src/data_processing/process_aihw_data.py`
   * **Action:** Addressed `test_process_aihw_excel` by ensuring the output CSV is always created (with headers if empty). Updated `test_process_sheet_table11` assertion to expect 'persons'.
   * **Delegate To:** `debug` mode.
   * **Status:** Completed.
2. **[X] Create Dedicated Analysis Script**

   * **Files:** `src/run_analysis.py`
   * **Action:** Created the script framework to load data, call visualisation functions, and apply specific annotations/overlays, separating analysis logic from `src/visualisation/main.py`.
   * **Delegate To:** `code` mode.
   * **Status:** Completed.
3. **[X] Refine Key Visualisations**

   * **Files:** `src/run_analysis.py`, `src/visualisation/time_series.py`, `src/visualisation/scatter.py`, `src/visualisation/correlation.py`
   * **Action:** Implemented enhancements detailed in `apply.md` for the LA Trend (title, annotations, rolling average), Juxtaposing Trends (faceted plot), Lagged Scatter (titles, correlation stats annotation, selected lags), and Correlation Heatmap (subset variables, caption).
   * **Delegate To:** `code` mode.
   * **Status:** Completed.

---

## Ad-hoc Fixes (Post 12 April 2025 Review)

1. **[X] Fix Pydantic ValidationErrors in run_analysis.py**

   * **Date:** 12 April 2025
   * **Files:** `src/run_analysis.py`
   * **Action:** Corrected recurring type mismatches for the `output_dir` parameter passed to various Pydantic configuration classes (`TimeSeriesConfig`, `CorrelationConfig`, `ScatterConfig`). Ensured the `FIGURES_DIR` `Path` object is consistently converted to a string (`str(FIGURES_DIR)`) before instantiation in all relevant cases within the `main` function.
   * **Delegate To:** `debug` mode (initial fixes), `code` mode (comprehensive fix).
   * **Status:** Completed.
2. **[X] Fix NameError in scatter.py**

   * **Date:** 12 April 2025
   * **Files:** `src/visualisation/scatter.py`
   * **Action:** Resolved `NameError: name 'stats' is not defined` by adding the missing import statement `import scipy.stats as stats` to the file.
   * **Delegate To:** `debug` mode.
   * **Status:** Completed.

---

## Data Validation & Enhancement (Post-ETL Run - 18 April 2025)

1. **[C] Investigate and Fix Missing `BMI_AgeStandardised` Data**

   * **Date:** 18 April 2025
   * **Files:** `src/run_etl.py`, `src/data_processing/health_outcome_metrics.py`, `src/download_data.py`, `data/raw/NCD_RisC_Lancet_2024_BMI_age_standardised_Australia.csv` (verified existence)
   * **Action:** Verified the raw BMI data file exists. Checked processing logic in `health_outcome_metrics.py`. Confirmed the source file (`NCD_RisC_Lancet_2024_BMI_age_standardised_Australia.csv`) provides BMI *category prevalence* (e.g., obesity), not mean age-standardised BMI. Reverted code changes attempting to extract mean BMI.
   * **Delegate To:** `code` mode.
   * **Status:** Closed - Data Not Available in Source.
2. **[X] Investigate and Add Missing `Population` Data**

   * **Date:** 18 April 2025
   * **Files:** `planning.md`, `src/config.py`, `src/download_data.py`, `src/data_processing/process_abs_population.py`, `src/run_etl.py`, `tests/test_process_abs_population.py`
   * **Action:** Identified ABS historical time series as the source. Updated download script. Created processing script (`process_abs_population.py`) to extract annual (December quarter) data from the correct sheet, handling metadata rows and date parsing. Integrated processing and merging into `run_etl.py`. Added unit tests.
   * **Delegate To:** `code` mode.
   * **Status:** Completed.
   * **Note (18 April 2025):** Required follow-up fix to ensure `process_abs_population.py` saved output to `data/processed/` (using `config.ABS_POPULATION_PROCESSED_FILE`) and `merge_health_dietary.py` loaded it correctly.

---

## Phase 3: EDA & Modelling (added 27 May 2025)

1. [ ] **Develop EDA module/notebook**

    * **Files:** `src/analysis/eda.py` 
    * **Action:** Create framework for exploratory data analysis.
2. [ ] **Perform Summary Statistics & Distribution Checks**

    * **Files:** `src/analysis/eda.py` or `/notebooks/EDA.ipynb`
    * **Action:** Calculate and visualise basic statistics (mean, median, sd, distributions) for key variables.
3. [ ] **Conduct Correlation and Lag Analyses**

    * **Files:** `src/analysis/eda.py` or `/notebooks/EDA.ipynb`
    * **Action:** Generate correlation heatmaps (including lags) and pairwise scatter plots.
4. [ ] **Implement Linear Regression Models**

    * **Files:** `src/models/regression.py`, `tests/test_regression.py`
    * **Action:** Develop functions for fitting and evaluating multiple linear regression models. Add unit tests.
5. [ ] **Implement Generalised Additive Models (GAMs)**

    * **Files:** `src/models/gam.py`, `tests/test_gam.py`
    * **Action:** Develop functions for fitting and evaluating GAMs using `pygam` or `statsmodels`. Add unit tests.
6. [ ] **(Optional) Implement Time-Series Models**

    * **Files:** `src/models/time_series.py`, `tests/test_time_series.py`
    * **Action:** Develop functions for time-series analysis (e.g., ARIMA, Prophet). Add unit tests.
7. [ ] **Write Unit Tests for Analysis Helpers**

    * **Files:** `tests/test_eda_helpers.py` (if applicable)
    * **Action:** Add tests for any reusable helper functions created during EDA.
8. [ ] **Document EDA & Modelling**

    * **Files:** `/notebooks/Analysis_Narrative.ipynb` or `reports/Analysis_Summary.md`
    * **Action:** Write a narrative report detailing the analysis process, findings, and limitations.
9. [ ] **Update README.md**

    * **Files:** `README.md`
    * **Action:** Add instructions on how to run analysis/models and locate results/figures.

## Phase 1: Data Acquisition Automation Investigation (added 27 May 2025)

1. [ ] **Investigate ABS Causes of Death Automation**

    * **Action:** Research if the ABS data cube can be downloaded programmatically (e.g., via API or stable URL). If possible, implement in `src/download_data.py`.
2. [ ] **Investigate IHME GBD Data Automation**

    * **Action:** Research if specific GBD results can be downloaded programmatically (e.g., via API or direct CSV links) instead of manual VizHub export. If possible, implement in `src/download_data.py`.
