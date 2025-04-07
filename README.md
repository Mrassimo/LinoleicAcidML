# Australian Health & Dietary Trends Analysis

This project investigates the relationship between seed oil intake (focusing on linoleic acid) and metabolic health outcomes in Australia from 1980 to present. The analysis leverages dietary data from 1961 onward to provide historical context.

## Project Structure

```
.
├── data/
│   ├── raw/          # Raw data files
│   └── processed/    # Processed and cleaned datasets
├── src/
│   ├── download_data.py       # Data download script
│   ├── process_raw_data.py    # Raw data processing
│   ├── process_aihw_data.py   # AIHW Excel processing
│   ├── process_faostat_fbs.py # FAOSTAT processing
│   ├── scrape_fire_in_bottle.py # Web scraping
│   ├── initial_data_cleaning.py # Data cleaning
│   ├── merge_datasets.py      # Dataset merging
│   └── models/               # Pydantic models
├── tests/                    # Test suite
├── planning.md              # Project planning and architecture
├── tasks.md                # Task tracking
└── requirements.txt        # Python dependencies
```

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
3. Run the ETL pipeline:

   ```bash
   python src/run_etl.py
   ```

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
