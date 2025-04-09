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

For detailed information about data sources and project planning, see `planning.md`.

## Development Status

See `tasks.md` for current development status and upcoming tasks.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
