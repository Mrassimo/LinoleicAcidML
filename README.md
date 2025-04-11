# Australian Health & Dietary Trends Analysis

This project investigates the relationship between seed oil intake (focusing on linoleic acid) and metabolic health outcomes in Australia from 1980 to present. The analysis leverages dietary data from 1961 onward to provide historical context.

## Project Structure

```
.
├── data/
│   ├── raw/            # Raw data files
│   └── processed/      # Processed and cleaned datasets
├── src/
│   ├── run_etl.py                # Main ETL pipeline entry point (run as module)
│   ├── download_data.py          # Data download utilities
│   ├── data_processing/          # Core data processing modules
│   ├── models/                   # Pydantic models
│   └── visualization/            # Plotting and visualisation scripts
├── tests/                       # Pytest suite covering all modules
├── planning.md                  # Project planning and architecture
├── tasks.md                     # Task tracking
└── requirements.txt             # Python dependencies
```

The core data cleaning, transformation, and integration logic now resides in `src/data_processing/`. Previous standalone scripts have been modularised or removed.

## Setup

1. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Run the ETL pipeline from the project root:

   ```bash
   python -m src.run_etl --no-download --force
   ```

   The above command executes the full ETL pipeline. Optional flags:

   - `--no-download` to skip re-downloading data if already present
   - `--force` to overwrite existing processed outputs

   You can omit these flags or combine them as needed.

## Data Sources

The project uses data from:

- NCD Risk Factor Collaboration (Diabetes, Cholesterol, BMI)
- Australian Institute of Health and Welfare (Dementia, CVD)
- FAOSTAT Food Balance Sheets
- Fire in a Bottle (Linoleic acid content derived from - [U.S. Department of Agriculture](https://www.usda.gov/))

**Note:** The data extraction from Fire in a Bottle relies on the website providing data within <pre> tags in a specific pipe-delimited format. This approach is inherently fragile—if the website structure changes, the scraping script (`src/data_processing/scrape_fire_in_bottle.py`) may fail and require maintenance. Please check the script and update it if the data source is modified.

## Manual Data Acquisition (ABS & IHME)

Some health outcome datasets (notably ABS Causes of Death and IHME Global Burden of Disease) require manual download due to licensing or access restrictions. These files are not included in the repository and must be acquired and placed in the correct location before running the full ETL pipeline.

- **ABS Causes of Death:**
  - Download the main data cube from the [ABS Causes of Death Australia](https://www.abs.gov.au/statistics/health/causes-death/causes-death-australia) website (navigate to the latest release and download the relevant Excel file).
  - Place the downloaded file(s) in the `data/raw/` directory. The expected filename(s) are referenced in `src/config.py` and `src/data_processing/health_outcome_metrics.py`.

- **IHME GBD:**
  - Use the [IHME GBD Results Tool](https://vizhub.healthdata.org/gbd-results/) to select Australia, the relevant causes (e.g., Dementia, CVD), and the required measures (prevalence, incidence, deaths, etc.). Download the resulting CSV files.
  - Place these files in the `data/raw/` directory. The expected filenames are referenced in `src/config.py` and `src/data_processing/health_outcome_metrics.py`.

If these files are not present, the ETL pipeline will skip the corresponding processing steps or raise a warning. For more details, see comments in the relevant processing scripts.

For detailed information about data sources and project planning, see `planning.md`.

## FAO/LA Mapping Workflow

The mapping between FAOSTAT food items and linoleic acid (LA) content items is maintained manually for quality and transparency. The script `src/data_processing/semantic_matching.py` is provided as a manual helper tool: it generates candidate matches using semantic similarity to assist in curating the validated mapping. However, its output is not used directly in the automated ETL pipeline. The final mapping used in the pipeline is maintained in `src/data_processing/update_validation.py` and is updated manually based on expert review, optionally informed by the semantic matching results.

If you update the mapping, please ensure changes are reflected in `update_validation.py` and not just in the semantic matching output.

## Development Status

See `tasks.md` for current development status and upcoming tasks.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
