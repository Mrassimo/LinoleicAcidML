# Project Tasks (Derived from apply.md Review - 2025-04-11)

This file tracks the specific tasks identified in the `apply.md` review received on 2025-04-11, aimed at improving the ETL pipeline's robustness and maintainability before the analytics phase.

## Task List

### Phase 1: Core Improvements (High Priority)

1.  **[X] Update Out-of-Sync Tests**
    *   **Files:** `tests/test_process_faostat_fbs.py`, `tests/test_faostat_validation.py`, `tests/test_scrape_fire_in_a_bottle.py`, `tests/test_calculate_dietary_metrics.py`
    *   **Action:** Review these test files. Align test logic, function calls, model references, and file path expectations (e.g., Markdown vs. `<pre>` tag parsing for Fire-in-a-Bottle test) with the current refactored code in the corresponding `src/data_processing/` modules. Ensure tests accurately reflect current functionality.
    *   **Delegate To:** `code` mode.

2.  **[X] Add New Tests for Complex Logic**
    *   **Files:** `src/data_processing/process_aihw_data.py`, `src/data_processing/calculate_dietary_metrics.py`, `tests/test_process_aihw_data.py`, `tests/test_calculate_dietary_metrics.py`
    *   **Action:** Add new Pytest tests covering complex conditional logic (e.g., special sheet handling in `process_aihw_data.py`, imputation/adjustments in `calculate_dietary_metrics.py`) and edge cases identified as needing coverage.
    *   **Delegate To:** `code` mode.

3.  **[X] Clarify and Remove Deprecated Code**
    *   **Files:** `src/data_processing/process_la_content.py`, `src/data_processing/merge_datasets.py`, `tests/test_process_la_content.py`, `tests/test_merge_datasets.py`
    *   **Action:** Investigate source files (`process_la_content.py`, `merge_datasets.py`). Confirm if their functionality is fully superseded by `scrape_fire_in_bottle.py`, `update_validation.py`, `calculate_dietary_metrics.py`, and `merge_health_dietary.py`. If confirmed deprecated, remove both the source files and their corresponding test files.
    *   **Delegate To:** `code` mode.

### Phase 2: Verification

4.  **[X] Verify Final Output**
    *   **Action 1:** Run the full ETL pipeline locally using `python -m src.run_etl --force --no-download`.
    *   **Action 2:** Review logs for any new warnings or errors.
    *   **Action 3:** Perform spot-checks on the generated `analytical_data_australia_final.csv`, focusing on data integrity, expected columns, ranges, and completeness, especially for recently fixed metrics (Carbs, Dementia/CVD).
    *   **Delegate To:** `execute_command` for Action 1, then potentially `code` or `ask` mode for Actions 2 & 3 depending on outcome.

### Phase 3: Further Enhancements (Optional but Recommended)

5.  **[X] Refine FAO/LA Mapping Workflow**
    *   **Files:** `src/data_processing/semantic_matching.py`, `src/data_processing/update_validation.py`
    *   **Action:** Clarify the role of `semantic_matching.py`. Determine if its output informs the hardcoded lists in `update_validation.py` or if it's unused/exploratory. Adjust the pipeline logic or documentation (`README.md`/`PLANNING.md`) accordingly.
    *   **Delegate To:** `code` mode.

6.  **[X] Improve Configuration Management**
    *   **Files:** Various `src/` files.
    *   **Action:** Identify hardcoded values (URLs, file paths, model names, thresholds). Move these into a central configuration file (e.g., `config.yaml` or `src/config.py`). Update the code to read from this configuration.
    *   **Delegate To:** `code` mode.

7.  **[X] Address Web Scraping Fragility**
    *   **File:** `src/data_processing/scrape_fire_in_bottle.py`
    *   **Action:** Review the scraping logic. Consider adding more specific selectors or enhanced error checking if feasible. Document the inherent fragility in `README.md` or code comments.
    *   **Delegate To:** `code` mode.

8.  **[X] Document Manual Data Steps**
    *   **Files:** `README.md`, `PLANNING.md`
    *   **Action:** Update documentation with clear instructions on how to acquire and place manual data files (ABS, IHME) if they are needed for future analysis or reproducibility.
    *   **Delegate To:** `code` mode (or self if simple text update).

9.  **[ ] Verify Final Schema**
    *   **File:** `src/data_processing/merge_health_dietary.py` (specifically `AnalyticalRecord` model)
    *   **Action:** Review the `AnalyticalRecord` Pydantic model against anticipated requirements for the analytics phase. Ensure all necessary columns are present and correctly typed.
    *   **Delegate To:** `code` mode.
