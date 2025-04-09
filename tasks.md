# Project Tasks (Derived from apply.md - 2025-04-09)

This file tracks the specific tasks identified in `apply.md` to resolve issues after recent refactoring.

## Task List

1.  **[X] Fix Carbohydrate Calculation Sequence (apply.md Step 1)**
    *   **File:** `src/data_processing/calculate_dietary_metrics.py`
    *   **Action:** Ensure `calculate_nutrient_supply` is called correctly and `Total_Carb_Supply_g` is included in the final saved DataFrame.
    *   **Delegate To:** `code` mode.

2.  **[X] Fix AIHW Processing Logic (apply.md Step 2)**
    *   **File:** `src/data_processing/process_aihw_data.py`
    *   **Action:** Review `process_sheet` function, specifically handling of S2.4 and Table 11, ensuring correct 'sex' column assignment and adding logging.
    *   **Delegate To:** `code` mode (or `debug` if complex issues arise).

3.  **[X] Address FAOSTAT Duplicates (apply.md Step 3)**
    *   **File:** `src/data_processing/process_faostat_fbs.py`
    *   **Action:** Add `drop_duplicates` step in `clean_faostat_data` before pivoting, based on `year`, `item`, `element`, `data_type`.
    *   **Delegate To:** `code` mode.

4.  **[X] Refactor run_etl.py Imports (apply.md Step 4 & 5)**
    *   **File:** `src/run_etl.py`
    *   **Action:** Replace dynamic imports with standard top-level imports. Remove `process_faostat_directory` and staging logic (confirm removal).
    *   **Delegate To:** `code` mode.

5.  **[X] Review and Update File Renames (apply.md Step 6)**
    *   **Files:** `src/run_etl.py`, `src/data_processing/calculate_dietary_metrics.py`, `src/data_processing/health_outcome_metrics.py`, `src/data_processing/merge_health_dietary.py`, `src/data_processing/update_validation.py`
    *   **Action:** Ensure all internal file read/write operations use the standardized names listed in `apply.md`.
    *   **Delegate To:** `code` mode.

6.  **[X] Update Tests (apply.md Step 7)**
    *   **Directory:** `tests/`
    *   **Action:** Update imports, file paths, remove obsolete test files (`test_process_excel.py`, `test_process_faostat.py`), and review existing tests (`test_process_aihw_data.py`, `test_process_faostat_fbs.py`) for relevance to updated logic.
    *   **Delegate To:** `code` mode.

7.  **[ ] Re-run ETL and Verify (apply.md Step 8)**
    *   **Action 1:** Delete processed/staging data (`execute_command`).
    *   **Action 2:** Run ETL pipeline (`execute_command: python -m src.run_etl --force --no-download`).
    *   **Action 3:** Examine logs and final output (`analytical_data_australia_final.csv`) for correctness (Carb column, AIHW sex data, CVD/Dementia metrics, absence of warnings).
    *   **Delegate To:** `execute_command` for Actions 1 & 2, then potentially `ask` or `code` mode for Action 3 depending on outcome.
