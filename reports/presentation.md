# Australian Health & Dietary Trends Analysis
## Investigating Seed Oil Intake and Health Outcomes (1980-Present)

---

## Project Overview

### Research Question
- How does seed oil intake (particularly linoleic acid) correlate with metabolic health outcomes in Australia?
- Focus on diabetes, obesity, cardiovascular disease, and dementia

### Time Period
- Primary analysis: 1980-present
- Historical context: FAOSTAT data from 1961
- Health outcomes data from multiple time ranges

### Key Health Metrics
- Diabetes and obesity prevalence
- Cardiovascular disease mortality and prevalence
- Dementia incidence and mortality
- Cholesterol levels

---

## Data Sources & Integration

### Dietary Data
- FAOSTAT Food Balance Sheets
  * Historical (1961-2013) and modern (2014-present)
  * Food availability as proxy for consumption
  * Detailed commodity breakdown

### Health Outcomes Data
- NCD Risk Factor Collaboration (1980-2022)
  * Diabetes prevalence
  * Cholesterol levels
  * BMI/obesity metrics
- IHME Global Burden of Disease (1990-present)
  * Dementia prevalence/incidence
  * CVD prevalence/mortality
- Australian Bureau of Statistics
  * Cause-specific mortality rates
  * Population demographics

---

## Methodology

### Data Processing
- Standardisation of food categories
- LA content calculation methodology
- Health metric harmonisation
- Temporal alignment of sources

### Analysis Approaches
1. Correlation Analysis
   - Direct correlations
   - Lag analysis (5-20 years)
   - Cross-source validation

2. Advanced Modelling
   - Generalized Additive Models (GAMs)
   - Time Series Models (ARIMA, Prophet)
   - Tree-Based Models (Random Forest, XGBoost)

---

## Key Findings

### Correlation Analysis
- Strong positive correlations:
  * LA intake → Obesity (r > 0.85)
  * LA intake → Diabetes (r > 0.85)
- Strong negative correlation:
  * LA intake → CVD mortality (r ≈ -0.94)
- Moderate to strong positive:
  * LA intake → CVD prevalence (r ≈ 0.76)
  * LA intake → Dementia prevalence (r ≈ 0.72)

### Lag Analysis Insights
- Obesity correlations strengthen with longer lags
- Suggests potential delayed effects
- Consistent patterns across lag periods

---

## Model-Specific Insights

### GAM Analysis
- Non-linear relationships detected
- Improved fit vs linear regression
- Significant lag effects
- Threshold effects identified

### Time Series Analysis
- Strong temporal patterns
- Reliable short-term forecasting
- Effective seasonality handling
- Robust uncertainty estimates

### Tree-Based Models
- LA intake: top predictor
- Plant Fat Ratio: significant importance
- Strong predictive accuracy
- Effective feature interaction capture

---

## Interactive Dashboard Demo

### Key Features
- Time series visualisations
- Correlation heatmaps
- Scatter plots with trend lines
- Model comparison plots
- GAM partial dependence plots

### Live Demo Instructions
1. Start local server:
   ```bash
   python -m http.server 8000
   ```
2. Navigate to dashboard
3. Demonstrate interactive features

---

## Limitations & Caveats

### Ecological Fallacy
- Population-level data
- Cannot make individual-level claims
- Potential masking of subgroup variations

### Confounding Factors
- Socioeconomic changes
- Healthcare improvements
- Lifestyle trends
- Environmental factors

### Data Considerations
- Different time ranges
- Varying methodologies
- Changes in definitions/coding
- Food availability vs consumption

---

## Conclusions

### Key Takeaways
1. Strong associations between LA intake and health outcomes
2. Complex, non-linear relationships identified
3. Temporal dependencies and lag effects observed
4. Robust findings across multiple models
5. Important limitations to consider

### Future Directions
1. Individual-level studies needed
2. Mechanism investigation
3. Subgroup analyses
4. Additional confounding variables
5. Extended time series analysis

---

## Questions & Discussion

### Contact Information
- Project Repository: [URL]
- Documentation: See README.md
- Interactive Dashboard: Local setup instructions in README

### Acknowledgments
- NCD Risk Factor Collaboration
- FAOSTAT
- IHME Global Burden of Disease Study
- Australian Bureau of Statistics

---

## Technical Appendix

### Repository Structure
```
SeedoilsML/
├── data/                  # Data files
├── figures/              # Visualisations
├── reports/              # Analysis reports
├── src/                  # Source code
└── tests/               # Test files
```

### Key Technologies
- Python data processing pipeline
- Pydantic for validation
- Plotly for visualisations
- Multiple statistical packages

### Documentation
- Comprehensive README
- Detailed methodology
- Interactive features guide
- Local setup instructions 