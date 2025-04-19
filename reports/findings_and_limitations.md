# Findings and Limitations Report: Australian Health & Dietary Trends Analysis

## Executive Summary

This report presents the findings from our comprehensive analysis of the relationship between seed oil intake (particularly linoleic acid, LA) and metabolic health outcomes in Australia from 1980 to present. The analysis combines multiple modelling approaches and data sources to provide robust insights while acknowledging important limitations.

## Key Findings

### 1. Correlation Analysis (April 2025)

#### Primary Correlations
- Strong positive correlations between LA intake and:
  * Obesity prevalence (r > 0.85)
  * Diabetes prevalence (r > 0.85)
- Strong negative correlation with CVD mortality (r ≈ -0.94)
- Moderate to strong positive correlations with:
  * CVD prevalence (r ≈ 0.76, IHME data)
  * Dementia prevalence (r ≈ 0.72, IHME data)

#### Lag Analysis
- Obesity correlations strengthen with longer lags (5-20 years)
- Suggests potential delayed effects of dietary changes
- Consistent patterns across different lag periods

#### Cross-Source Validation
- Correlations remain robust across different data sources:
  * IHME GBD
  * ABS Causes of Death
  * NCD-RisC
- Similar patterns observed for Plant Fat Ratio and Total Fat Supply

### 2. GAM Analysis (May 2025)

#### Model Performance
- Non-linear relationships detected between LA intake and health outcomes
- Improved fit compared to linear regression for most outcomes
- Significant non-linear effects in lagged relationships

#### Key Insights
- Complex, non-linear relationships between LA intake and:
  * BMI trajectories
  * Diabetes prevalence
  * CVD mortality
- Threshold effects identified in several relationships
- Temporal dependencies captured through lag terms

### 3. Time Series Analysis (May 2025)

#### ARIMA Models
- Successfully captured temporal patterns in health metrics
- Auto-selected parameters provide optimal fit
- Reliable short-term forecasting capabilities

#### Prophet Models
- Effective at handling seasonality and trend changes
- Robust to missing data and outliers
- Provides uncertainty estimates for forecasts

### 4. Tree-Based Models (May 2025)

#### Feature Importance
- LA intake consistently ranks as a top predictor
- Plant Fat Ratio shows significant importance
- Temporal features (lags) contribute substantially

#### Model Performance
- High predictive accuracy for most health outcomes
- Robust to non-linear relationships
- Effective at capturing feature interactions

## Limitations and Caveats

### 1. Ecological Fallacy

#### Population-Level Data
- Analysis uses aggregated national-level data
- Cannot make individual-level causal claims
- Relationships may differ at individual level

#### Aggregation Effects
- Potential masking of subgroup variations
- Loss of individual-level variability
- Risk of ecological bias in interpretations

### 2. Confounding Factors

#### Unmeasured Variables
- Socioeconomic changes
- Healthcare system improvements
- Lifestyle and physical activity trends
- Environmental factors

#### Temporal Confounding
- General technological advancement
- Changes in medical treatments
- Evolving diagnostic criteria
- Population demographic shifts

### 3. Data Source Differences

#### Time Ranges
- NCD-RisC: 1980-2022
- IHME GBD: 1990-present
- ABS CoD: ~1980-present
- Varying coverage affects analysis completeness

#### Methodological Differences
- Different standardisation approaches
- Varying definitions of health outcomes
- Changes in ICD coding over time
- Different modelling assumptions between sources

### 4. Data Quality Considerations

#### FAOSTAT Data
- Food availability vs. actual consumption
- Assumptions in LA content calculations
- Changes in food classification over time
- Limited granularity in food categories

#### Health Outcome Data
- Changes in diagnostic criteria
- Improvements in detection/reporting
- Varying data collection methods
- Potential reporting biases

## Recommendations for Interpretation

1. **Causality**: Results should be interpreted as associations rather than causal relationships.
2. **Context**: Consider findings within broader public health and dietary pattern changes.
3. **Uncertainty**: Acknowledge the multiple sources of uncertainty in both data and analysis.
4. **Generalisability**: Exercise caution in extending findings beyond the Australian context.
5. **Time Sensitivity**: Consider the temporal nature of relationships and potential lag effects.

## Future Research Directions

1. Individual-level studies to validate population-level findings
2. Investigation of potential mechanisms linking LA intake to health outcomes
3. Subgroup analyses where data permits
4. Integration of additional confounding variables
5. Extended time series analysis with newer data as it becomes available

## Technical Notes

### Model Selection Rationale
- Multiple modelling approaches provide complementary insights
- Each method addresses different aspects of the relationships
- Cross-validation of findings across methods increases robustness

### Data Processing Decisions
- Standardisation choices
- Treatment of missing values
- Handling of outliers
- Temporal alignment of different sources

## Conclusion

While our analysis reveals strong associations between LA intake and various health outcomes in Australia, these findings must be interpreted within the context of the stated limitations. The use of multiple modelling approaches and data sources strengthens our confidence in the observed patterns, but causal interpretations require additional research at the individual level. 