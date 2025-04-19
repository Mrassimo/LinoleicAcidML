# Australian Health & Dietary Trends Dashboard

This dashboard presents an interactive visualization of the relationship between dietary patterns (particularly seed oil consumption) and health outcomes in Australia from 1980 to present.

## Data Sources

- FAOSTAT Food Balance Sheets (dietary data)
- NCD Risk Factor Collaboration (diabetes, cholesterol, BMI)
- IHME Global Burden of Disease Study (dementia, CVD)
- Australian Bureau of Statistics (mortality data)

## Features

- Interactive time series plots
- Correlation analysis
- Key relationship scatter plots
- Model performance comparisons
- GAM partial dependence plots

## Technical Details

- Built with Plotly for interactive visualizations
- Deployed on Vercel
- Data processing pipeline in Python
- Statistical analysis using GAMs, Time Series Models, and Tree-Based Models

## Local Development

To run this dashboard locally:

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the dashboard creation script: `python src/visualisation/create_dashboard.py`
4. Open `public/index.html` in your browser

## Deployment

This dashboard is automatically deployed to Vercel. Each commit to the main branch triggers a new deployment. 