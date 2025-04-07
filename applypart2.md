
## Consolidated Project Implementation Guide (Post Initial Cleaning)

**Phase 2 Continued: Data Processing & Feature Engineering**

1. **Verify/Finalize FAOSTAT Processing:**
   * Load your processed FAOSTAT data for Australia (expected in `data/processed/`).
   * **Confirm:** It includes necessary `Element` values like 'Food supply quantity (kg/capita/yr)', 'Fat supply quantity (g/capita/yr)', 'Protein supply quantity (g/capita/yr)', 'Food supply (kcal/capita/day)'.
   * **Confirm:** It's filtered for `Area == 'Australia'`.
   * **Confirm/Calculate:** You have `Food supply quantity (g/capita/day)` and `Fat supply quantity (g/capita/day)` correctly calculated (original values divided by 365.25, kg supply also multiplied by 1000).
   * *Action:* If any of these are missing, perform the necessary calculations/filtering now. Ensure data is tidy (e.g., rows for each Year-Item-Element). Save the verified/finalized version.
2. **Prepare Linoleic Acid (LA) Content Data:**
   * Ensure your scraped/sourced LA data (from Fire in a Bottle/USDA) is processed into a clean lookup table format: `la_food_item | linoleic_acid_g_per_100g`.
   * *Action:* Save this lookup to `data/processed/linoleic_acid_content.csv` if not already done.
3. **Semantic Matching (FAOSTAT Items -> LA Food Items):**
   * **Prepare Lists:** Extract unique `Item` names from your verified processed FAOSTAT data (`fao_items_list`). Use the `la_food_item` names from the LA lookup (`la_items_list`).
   * **Load Model:** `model = SentenceTransformer('all-MiniLM-L6-v2')` (Ensure `sentence-transformers`, `torch`/`tensorflow`, `scikit-learn` are installed: `pip install sentence-transformers torch scikit-learn`).
   * **Generate Embeddings:** `fao_embeddings = model.encode(...)`, `la_embeddings = model.encode(...)`
   * **Calculate Similarity:** `similarity_matrix = cosine_similarity(fao_embeddings, la_embeddings)`
   * **Find Best Matches:** Loop through FAO items, find the `la_item` with the highest `argmax` similarity score.
   * **Create Mapping Table:** Build a DataFrame: `fao_item | matched_la_item | similarity_score | manual_validation_status`
   * **>> CRITICAL STEP: Manual Validation <<:** Review every match. Pay close attention to scores < ~0.7 (or adjust threshold). Correct mistakes by updating the `matched_la_item` or adding a `corrected_la_item` column and changing `manual_validation_status` (e.g., to 'CONFIRMED', 'OVERRIDDEN').
   * **Save:** Save the **validated** mapping table (e.g., `data/processed/validated_fao_la_mapping.csv`).
4. **Calculate Derived Dietary Metrics:**
   * Load the finalized processed FAOSTAT data (step 1), the validated mapping table (step 3), and the LA content lookup (step 2).
   * **Join LA Content:** Join the LA content (g/100g) onto the FAOSTAT data using the validated mapping.
   * **Calculate LA Intake per Item (g/day):** `LA_g_day = Supply_g_day * (LA_g_per_100g / 100)`
   * **Aggregate Total LA Intake:** Group by `Year` and sum `LA_g_day` across all items to get `Total_LA_Intake_g_per_capita_day`.
   * **Calculate % Calories from LA:** Get `Total_Calories_Supply` (kcal/day) from FAOSTAT. `LA_Intake_percent_calories = (Total_LA_Intake_g_per_capita_day * 9 / Total_Calories_Supply) * 100`.
   * **Calculate Plant Fat Ratio:**
     * Classify each FAOSTAT item providing fat as 'Plant' or 'Animal'.
     * Get `Fat_Supply_g_day` for each item from FAOSTAT.
     * Sum `Fat_Supply_g_day` for all 'Plant' items = `Total_Plant_Fat_g_day`.
     * Get `Total_Fat_Supply_g_day` from FAOSTAT.
     * `Plant_Fat_Ratio = Total_Plant_Fat_g_day / Total_Fat_Supply_g_day`.
   * **Save:** Create a DataFrame containing `Year`, `Total_LA_Intake_g_per_capita_day`, `LA_Intake_percent_calories`, `Plant_Fat_Ratio`, `Total_Calorie_Supply`, `Total_Fat_Supply`, `Total_Carb_Supply`, `Total_Protein_Supply`. Save this (e.g., `data/processed/australia_dietary_metrics.csv`).
5. **Merge Health Outcomes & Dietary Metrics:**
   * Load your previously cleaned/processed health datasets (AIHW, NCD-RisC) from `data/processed/`.
   * Load the `australia_dietary_metrics.csv` (step 4).
   * Select the specific, aggregated health outcome metrics needed for modeling (e.g., `Diabetes_Prevalence_Rate_AgeStandardised`, `Dementia_Mortality_Rate_65plus`, `Mean_BMI_AgeStandardised`). Ensure these represent a single value per year (or per year/sex if stratifying later). Use the standardized names you created earlier.
   * Merge these health outcomes with the dietary metrics DataFrame, joining on `Year`.
   * Handle any potential missing years or data points resulting from the merge appropriately (review carefully before deciding on imputation or dropping specific years/series).
   * **Save:** Save the merged analytical dataset (e.g., `data/processed/analytical_merged_data.csv`).
6. **Feature Engineering (Lags):**
   * Load the merged analytical dataset (`analytical_merged_data.csv`).
   * Create lagged versions of your primary predictor (`LA_Intake_percent_calories`):
     * `df['LA_perc_kcal_lag5'] = df['LA_Intake_percent_calories'].shift(5)`
     * `df['LA_perc_kcal_lag10'] = df['LA_Intake_percent_calories'].shift(10)`
     * `df['LA_perc_kcal_lag15'] = df['LA_Intake_percent_calories'].shift(15)`
     * `df['LA_perc_kcal_lag20'] = df['LA_Intake_percent_calories'].shift(20)`
   * Note: The first N rows for an N-year lag will become `NaN`. You will need to handle these (e.g., by dropping them in the modeling stage) before model fitting. This effectively shortens your time series for models using those lags (e.g., a model using `_lag20` can only start 20 years after your data begins).
   * **Save:** Save the final dataset with lags, ready for modeling (e.g., `data/processed/analytical_merged_data_with_lags.csv`).

**Phase 3: Modeling and Analysis**

7. **Exploratory Data Analysis (EDA) on Final Dataset:**
   * Load `analytical_merged_data_with_lags.csv`.
   * Drop rows with NaNs introduced by the longest lag you intend to use in a given model.
   * Plot time series for key predictors (LA%, Plant Fat Ratio, Calories, BMI) and outcomes over the analysis period. Look for trends, seasonality, potential outliers, or structural breaks.
   * Calculate correlations between variables (especially predictors like lagged LA%, BMI, Calories) to check for multicollinearity. Visualize with a heatmap.
   * Examine distributions of variables (histograms, density plots).
8. **Data Splitting (for Predictive Models):**
   * If using models like Random Forest/XGBoost for  *predictive performance assessment* , split data based on time. **Crucially, do not shuffle time series data randomly.**
   * Example using the data *after* dropping NaN rows from lags: `split_year = 2005 # Or other appropriate year`
     `train_df = df[df['Year'] <= split_year]`
     `test_df = df[df['Year'] > split_year]`
   * For models focused on *explanation* (like MLR, GAMs fitted to the whole available period after handling lags), a formal train/test split might not be necessary, but holdout validation can still be useful.
9. **Model Fitting & Evaluation:** (Install libraries like `statsmodels`, `scikit-learn`, `pygam`, `xgboost` if not already done: `pip install statsmodels scikit-learn pygam xgboost`)
   * **(Start Simple) Multiple Linear Regression (MLR):**
     * Use `statsmodels.api.OLS`.
     * Define models using the dataset *after* handling NaNs from lags: `Outcome ~ LA_perc_kcal_lagX + Plant_Fat_Ratio + Mean_BMI + Total_Calorie_Supply + Year` (include relevant lags one by one or together; `Year` can help detrend).
     * Analyze coefficients, standard errors, p-values, R-squared. Check model assumptions (linearity, independence via Durbin-Watson test, homoscedasticity via residual plots or Breusch-Pagan test, normality of residuals via Q-Q plot).
   * **(Check Non-Linearity) Generalized Additive Models (GAMs):**
     * Use `pygam.LinearGAM` or `statsmodels.gam.GLMGam`.
     * Define models: `Outcome ~ s(LA_perc_kcal_lagX) + s(Mean_BMI) + s(Year) + Plant_Fat_Ratio + ...` (Use `s()` for variables expected to have non-linear effects).
     * Analyze partial dependence plots for smoothed terms (`s()`) to understand the shape of relationships. Compare model fit (e.g., AIC, pseudo-R-squared) to MLR. Check convergence and diagnostics.
   * **(Time Dynamics) ARIMAX / Regression with ARIMA errors:**
     * Use `statsmodels.tsa.arima.ARIMA`.
     * Check outcome variable (and potentially predictors) for stationarity using `statsmodels.tsa.stattools.adfuller`. If non-stationary, apply differencing (`.diff()`) as needed before modeling.
     * Fit model: `ARIMA(endog=outcome_diff, order=(p,d,q), exog=regressors_diff).fit()`. Analyze coefficients of exogenous regressors (`exog`). Interpreting coefficients on differenced data requires care.
   * **(Predictive Power) Tree-Based Models (Random Forest / XGBoost):**
     * Use `sklearn.ensemble.RandomForestRegressor` or `xgboost.XGBRegressor`.
     * Train on the `train_df`, make predictions on `test_df`.
     * Evaluate using time-series appropriate metrics (e.g., Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), Mean Absolute Percentage Error (MAPE) on the `test_df`).
     * Analyze feature importances (`model.feature_importances_`). Be aware importance can be biased by correlated predictors.
10. **Interpret Results & Document Findings:**
    * Synthesize findings across different models. Where do they agree or disagree on the role of lagged LA intake?
    * Clearly state the estimated association (size, direction, significance, linearity) between lagged LA intake (% calories) and each health outcome,  *after accounting for confounders* .
    * Emphasize limitations: **Ecological study design** (cannot infer individual risk), potential **unmeasured confounders** (smoking, physical activity, medication changes), accuracy/assumptions in **FAOSTAT data** and the **LA mapping/content** data.
    * Document the methodology precisely (lags used, model specifications, validation approach), parameters, evaluation metrics, and key results.

**Phase 4: Reporting and Visualization**

11. **Create Visualizations:** Generate publication-quality plots:
    * Time series plots of key variables.
    * Scatter plots showing relationships (e.g., Outcome vs Lagged LA) perhaps with regression lines or smooths overlaid.
    * Partial dependence plots from GAMs.
    * Feature importance plots from tree models.
    * Residual diagnostic plots for regression models.
12. **Write Report/Summary:** Structure your findings logically, starting with the objective, methods, results (per outcome), discussion (including limitations), and conclusion.
13. **Publish (e.g., GitHub Pages):** Organize your final code, data summaries (`reports/processed_data_summary.md`), the validated mapping file, the final analytical dataset (optional, depending on size/privacy), results tables/plots, and documentation into your project repository for showcasing. Ensure the `README.md` is updated to reflect the final project status and how to run/interpret the analysis.
