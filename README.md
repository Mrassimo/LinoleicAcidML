# Australian Health & Dietary Trends Analysis

This project investigates the relationship between seed oil intake (focusing on linoleic acid, LA) and metabolic health outcomes in Australia from 1980 to present. Through rigorous data engineering and statistical analysis, we explore associations between dietary patterns and health outcomes while acknowledging important limitations and confounding factors.

## Key Findings

Our analysis reveals several significant patterns:

### Correlation Analysis
- Strong positive correlations between LA intake and obesity/diabetes prevalence (r > 0.85)
- Strong negative correlation with CVD mortality (r ≈ -0.94)
- Moderate to strong positive correlations with CVD and dementia prevalence
- Lag analysis suggests potential delayed effects, particularly for obesity

### Advanced Modelling
- GAMs reveal complex non-linear relationships between LA intake and health outcomes
- Time series models effectively capture temporal patterns and seasonality
- Tree-based models highlight LA intake as a consistently important predictor
- Cross-validation across multiple modelling approaches increases result robustness

For detailed findings, limitations, and caveats, see `reports/findings_and_limitations.md`.

## Data Sources

The analysis combines data from multiple authoritative sources:
- FAOSTAT Food Balance Sheets (dietary data, 1961-present)
- NCD Risk Factor Collaboration (diabetes, cholesterol, BMI, 1980-2022)
- IHME Global Burden of Disease Study (dementia, CVD, 1990-present)
- Australian Bureau of Statistics (mortality data, ~1980-present)

## Features

### Analysis Pipeline
- Comprehensive data processing and validation
- Multiple statistical modelling approaches:
  - Generalized Additive Models (GAMs)
  - Time Series Models (ARIMA, Prophet)
  - Tree-Based Models (Random Forest, XGBoost)
- Extensive correlation and lag analyses
- Robust data validation using Pydantic

### Interactive Dashboard
- Time series visualisations with zoom/pan
- Correlation heatmaps with detailed hover information
- Scatter plots with trend lines and confidence intervals
- Feature importance visualisations
- Model comparison plots
- GAM partial dependence plots

## Local Development Setup

### Prerequisites
- Python 3.8+
- pip package manager
- Git

### Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd SeedoilsML
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Data Processing Pipeline

1. Download required data files:
   - Place IHME GBD data zip file in `data/raw/`
   - Download ABS Causes of Death data (if needed)
   - NCD-RisC and FAOSTAT data are downloaded automatically

2. Run the ETL pipeline:
```bash
python src/run_etl.py
```

3. Run the analysis:
```bash
python src/run_analysis.py
```

### Generating the Dashboard

1. Generate the interactive dashboard:
```bash
python src/visualisation/create_dashboard.py
```

2. Start the local server:
```bash
python -m http.server 8000
```

3. View the dashboard:
   Open `http://localhost:8000/figures/dashboard.html` in your browser

## Using the Interactive Dashboard

### Time Series Plots
- **Zoom**: Use the zoom tools in the toolbar to focus on specific time periods
- **Pan**: Click and drag to move through time periods
- **Reset**: Double-click to reset the view
- **Legend**: Click items to show/hide specific series
- **Hover**: Move mouse over points for detailed values

### Correlation Heatmaps
- **Hover Details**: Move mouse over cells for exact correlation values
- **Scale**: Colour intensity indicates correlation strength
- **Interpretation**: Red = positive correlation, Blue = negative correlation

### Scatter Plots
- **Trend Lines**: Show relationship direction and confidence intervals
- **Hover**: View exact values and additional metrics
- **Zoom**: Focus on specific regions of interest
- **Export**: Use camera icon to save plots as PNG files

### Model Comparison Plots
- **Performance Metrics**: Compare RMSE, MAPE, and R² across models
- **Feature Importance**: View relative importance of predictors
- **Hover**: See exact values and descriptions
- **Legend**: Toggle different models and metrics

### GAM Plots
- **Partial Dependence**: Visualise non-linear relationships
- **Confidence Bands**: Show uncertainty in relationships
- **Interpretation Guide**: Available in hover text
- **Export Options**: Save plots for presentations

## Project Structure

```
SeedoilsML/
├── data/                  # Data files
│   ├── processed/        # Processed datasets
│   ├── raw/             # Original data sources
│   └── staging/         # Intermediate processing
├── figures/              # Generated visualisations
│   ├── interactive/     # Interactive plot files
│   ├── gam_analysis/    # GAM visualisations
│   └── time_series/     # Time series plots
├── reports/              # Analysis reports
├── src/                  # Source code
│   ├── analysis/        # Analysis modules
│   ├── data_processing/ # Data processing scripts
│   ├── models/         # Statistical models
│   └── visualisation/  # Visualisation code
├── tests/               # Test files
└── requirements.txt     # Python dependencies
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Make your changes
4. Run tests: `pytest`
5. Submit a pull request

## License

This project is licensed under the terms of the LICENSE file included in the repository.

## Acknowledgments

- NCD Risk Factor Collaboration for health metrics data
- FAOSTAT for dietary data
- IHME for Global Burden of Disease data
- Australian Bureau of Statistics for mortality data
