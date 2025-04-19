# Project Tasks (Updated 1 June 2025 - Project Completion)

This file tracks project tasks, reflecting decisions made after the reviews on 12 April 2025 and 28 May 2025. All core tasks have been completed.

---

**Status Update (1 June 2025):**

- All core project tasks have been completed
- Project is ready for portfolio demonstration
- Interactive dashboard and documentation are complete
- Presentation materials have been prepared
- **Next:** Optional automation improvements can be considered

---

## Completed Phases

### Phase 1/2: ETL & Data Quality Fixes (Completed)

1. **[X] Fix AIHW Test Failures** (Completed 12 April 2025)
2. **[X] Create Dedicated Analysis Script** (Completed 12 April 2025)
3. **[X] Refine Key Visualisations** (Completed 12 April 2025)
4. **[X] Fix Pydantic ValidationErrors in run_analysis.py** (Completed 12 April 2025)
5. **[X] Fix NameError in scatter.py** (Completed 12 April 2025)
6. **[C] Investigate and Fix Missing `BMI_AgeStandardised` Data** (Closed 18 April 2025 - Data Not Available in Source)
7. **[X] Investigate and Add Missing `Population` Data** (Completed 18 April 2025)

### Phase 3: Integrate IHME GBD Data (Completed)

1. **[X] Integrate IHME Processing into ETL Runner** (Completed 28 May 2025)
   * **Files:** `src/run_etl.py`, `src/data_processing/process_abs_ihme_data.py`
   * **Action:** Modify `run_etl.py` to call the main function within `process_abs_ihme_data.py` at the appropriate stage (e.g., after downloads, before health metrics consolidation). Ensure it handles the case where the IHME zip file might be missing.
   * **Delegate To:** `code` mode.
2. **[X] Incorporate Processed IHME Data into Merge Logic** (Completed 28 May 2025)
   * **Files:** `src/data_processing/health_outcome_metrics.py`
   * **Action:** Added new `extract_ihme_metrics()` function to process GBD metrics. Updated main function to merge IHME data with NCD-RisC and AIHW metrics.
   * **Delegate To:** `code` mode.
3. **[X] Update Final Data Model (`AnalyticalRecord`)** (Completed 29 May 2025)
   * **Files:** `src/data_processing/merge_health_dietary.py`
   * **Action:** Added new optional fields to the `AnalyticalRecord` Pydantic model to accommodate IHME metrics (prevalence, incidence, death rates, and numbers for both dementia and CVD). Updated validation rules for non-negative fields.
   * **Delegate To:** `code` mode.

4. [X] **Update Documentation for IHME Integration** (Completed 30 May 2025)
    * **Files:** `README.md`, `planning.md`
    * **Action:** Update the documentation to accurately reflect that IHME data *is* used. Clarify the manual download step for the IHME zip file in `README.md`. Update the data source list and data integration notes in `planning.md`.
    * **Delegate To:** `code` mode.

### Phase 4: EDA & Modelling (Completed)

* **Objective**: Model and analyze relationships using the final data asset.
* **Status**:
  * [X] Initial EDA completed with comprehensive summary statistics and visualisations
  * [X] Detailed correlation and lag analyses completed
  * [X] MLR completed with comprehensive results
  * [X] GAMs implemented with cross-validation and model selection (Completed 30 May 2025)
    * Added GAMConfig for configuration management
    * Implemented cross-validation for hyperparameter selection
    * Added functions for analyzing specific health outcomes
    * Generated partial dependence plots for feature interpretation
    * Saved comprehensive results to `reports/gam_analysis_summary.csv`
  * [X] Time Series Models and Tree-Based Models (Completed 31 May 2025)
    * Implemented enhanced ARIMA with auto-parameter selection
    * Added Prophet model support for comparison
    * Implemented Random Forest and XGBoost models
    * Added feature importance analysis
    * Generated comprehensive evaluation metrics
    * Created visualisations for forecasts and feature importance
* **Tasks**:
  * [X] Complete remaining EDA tasks
  * [X] Implement MLR and GAMs
  * [X] Time Series Models, Tree-Based Models
  * [X] Interpret results, document findings and limitations (Completed 31 May 2025)
    * Created comprehensive findings document (`reports/findings_and_limitations.md`)
    * Documented ecological fallacy considerations
    * Analyzed confounding factors
    * Discussed data source differences and limitations
    * Provided recommendations for interpretation
    * Suggested future research directions

### Phase 5: Visualisation and Documentation (Completed)

* **Objective**: Present findings effectively through an interactive dashboard.
* **Status**: All tasks completed, project ready for portfolio demonstration
* **Completed Tasks**:
  * [X] Create interactive visualisations (Completed 31 May 2025)
    * Created new module `src/visualisation/interactive.py` for Plotly-based visualizations
    * Implemented interactive time series plots with zoom/pan
    * Added correlation heatmaps with hover details
    * Created scatter plots with trend lines
    * Added feature importance and model comparison plots
    * Implemented GAM partial dependence plots
    * Created comprehensive HTML dashboard (`figures/dashboard.html`)
    * Added unit tests in `tests/test_interactive_viz.py`
    * Updated requirements.txt with plotly and related packages
  * [X] Configure for Local Demonstration (Completed 1 June 2025)
    * Updated dashboard creation script for local viewing
    * Organized files in appropriate directory structure
    * Added local setup documentation
  * [X] Take Down Vercel Deployment (Completed 1 June 2025)
    * Removed project from Vercel dashboard
    * Updated documentation to remove deployment URLs
    * Archived deployment configuration files
    * Documented local setup for portfolio demonstration
  * [X] Write final documentation (Completed 1 June 2025)
    * Updated README with comprehensive project overview
    * Added detailed findings summary
    * Documented local development setup
    * Created interactive dashboard user guide
    * Added acknowledgments section
  * [X] Create presentation materials (Completed 1 June 2025)
    * Created comprehensive presentation in `reports/presentation.md`
    * Included key findings and methodology
    * Added local dashboard demo instructions
    * Documented conclusions and future directions
    * Prepared technical appendix

---

## Optional Future Improvements

### Phase 6: Automation Enhancements (Optional)

1. **[I] ABS Causes of Death Automation** (Investigated [Current Date])
    * **Priority**: Low
    * **Action**: Research if the ABS data cube can be downloaded programmatically.
    * **Findings**: Investigation complete. Direct programmatic download via API/stable URL seems unlikely. Data is released as versioned Excel files. Automation would likely require manual URL updates in `src/download_data.py` per release cycle and Excel parsing, or potentially complex access via ABS TableBuilder/Microdata services. No code changes made.
    * **Implementation**: If possible, add to `src/download_data.py`
    * **Status**: Investigated - Automation difficult
    * **Dependencies**: None
    * **Effort**: Medium (for partial automation), High (for full automation if possible via other services)

2. **Dependency Management**
    * **Priority**: Low
    * **Action**: Create `requirements.lock` for exact version pinning
    * **Implementation**: Use `pip freeze`
    * **Status**: Not started
    * **Dependencies**: None
    * **Effort**: Low

3. **CI/CD Pipeline**
    * **Priority**: Low
    * **Action**: Add GitHub Actions for automated testing
    * **Implementation**: Create workflow files
    * **Status**: Not started
    * **Dependencies**: None
    * **Effort**: Medium

4. **Data Update Automation**
    * **Priority**: Low
    * **Action**: Create scripts for automated data updates
    * **Implementation**: Add scheduling and validation
    * **Status**: Not started
    * **Dependencies**: ABS automation
    * **Effort**: High

Note: These improvements are optional and not critical for the project's core functionality or demonstration purposes.
