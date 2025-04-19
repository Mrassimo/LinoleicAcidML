# Portfolio Visualisation Plan for SeedoilsML Project

This document outlines a plan to create compelling visual assets from the SeedoilsML project, suitable for showcasing skills on a portfolio website.

## Goal

Leverage the project's ETL pipeline, analysis, and results to create visuals demonstrating expertise in data engineering, data analysis, statistical modelling, Python development, and modern development practices.

## Proposed Visual Assets

### 1. Showcase the Existing Interactive Dashboard

*   **Asset:** The primary interactive dashboard (`figures/dashboard.html`) generated using Plotly.
*   **Content:** Time series plots, correlation heatmaps, scatter plots, model comparison plots, GAM partial dependence plots.
*   **Portfolio Implementation:**
    *   **Embed Directly:** Use an `iframe` for live interaction on the portfolio page.
    *   **Prominent Link:** Provide a clear link/button to open the dashboard in a new tab.
    *   **Guided Tour (Video/GIF):** Create a short screen recording or GIF demonstrating key interactive features (zooming, panning, hovering, legend toggling) as outlined in `README.md`.
    *   **Highlight Key Plots:** Feature high-quality static screenshots (PNG exports) of the most impactful plots (e.g., key trend, correlation heatmap, GAM PDP) alongside the embed/link.

### 2. Visualise the ETL & Data Pipeline

*   **Asset:** A clear flowchart illustrating the data journey.
*   **Content:**
    *   **Inputs:** Raw data sources (FAOSTAT, NCD-RisC, IHME GBD*, ABS Causes of Death, ABS Population, Linoleic Acid Reference [USDA/Fire in a Bottle]). Highlight the manual download step for IHME.
    *   **Processing Steps:**
        *   Automated Downloading (`requests`, includes ABS data).
        *   Web Scraping (`beautifulsoup4`, `requests`) for LA reference data.
        *   Cleaning & Standardisation (Pandas).
        *   **Semantic Matching:** Linking FAOSTAT food items to Linoleic Acid content reference using `sentence-transformers`.
        *   LA Intake Calculation & Derived Metrics (Pandas).
        *   Data Validation (`pydantic`).
        *   Merging & Consolidation (Pandas).
        *   Lag Feature Engineering (Pandas).
    *   **Key Scripts:** Mention core scripts like `src/run_etl.py`, `src/download_data.py`, `src/data_processing/process_*.py`, `src/data_processing/merge_health_dietary.py`.
    *   **Outputs:** Staging files (`data/staging/`), Processed files (`data/processed/`), Final dataset (`analytical_data_australia_final.csv`).
*   **Portfolio Implementation:**
    *   **Flowchart Diagram:** Create using tools like:
        *   **Mermaid.js:** Embed directly into web page markup for a clean, code-based diagram.
        *   **Draw.io / Excalidraw:** Create visually richer diagrams, export as SVG for scalability.
    *   **Placement:** Dedicate a "Data Pipeline" section/slide on the portfolio page.

```mermaid
graph LR
    A[Raw Data Sources<br/>(FAOSTAT, NCD-RisC,<br/> IHME*, ABS CoD,<br/> ABS Pop, LA Ref)] --> B{Download/Scrape<br/>(requests, bs4)};
    B --> C{Clean/Standardise<br/>(pandas)};
    C --> D{Semantic Matching<br/>(sentence-transformers)};
    D --> E{Calculate Metrics<br/>(pandas)};
    E --> F{Validate<br/>(pydantic)};
    F --> G{Merge/Consolidate<br/>(pandas)};
    G --> H{Lag Features<br/>(pandas)};
    H --> I[Final Dataset<br/>(analytical_data_australia_final.csv)];

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style I fill:#ccf,stroke:#333,stroke-width:2px
    classDef default fill:#fff,stroke:#333,stroke-width:1px;

    %% *Indicates manual download required for IHME
```

*(Note: The Mermaid code above is an example structure, updated comment)*


### 3. Illustrate the Analysis Workflow & Modelling

*   **Asset:** A diagram showing the analytical process from data to insights.
*   **Content:**
    *   **Input:** `analytical_data_australia_final.csv`.
    *   **Steps:**
        *   Exploratory Data Analysis (EDA): Summary Stats (`pandas`), Visualisation (`matplotlib`, `seaborn`, `plotly`).
        *   Correlation & Lag Analysis (`pandas`, `numpy`, `statsmodels`).
        *   Modelling:
            *   Linear Regression (`scikit-learn` / `statsmodels`).
            *   GAMs (`pygam`).
            *   Time Series (ARIMA - `statsmodels`, Prophet - `prophet` if used, although not in reqs).
            *   Tree-Based (Random Forest, XGBoost - `scikit-learn`, `xgboost`).
        *   Model Evaluation (`scikit-learn`, `numpy`).
        *   Interpretation & Reporting.
    *   **Key Scripts:** Mention `src/run_analysis.py`, `src/analysis/*`, `src/models/*`.
    *   **Outputs:** Reports (`reports/`), Visualisations (`figures/`, Dashboard), Key Findings.
*   **Portfolio Implementation:**
    *   **Workflow Diagram:** Similar approach to the ETL flowchart (Mermaid/Draw.io/SVG).
    *   **Model Comparison Visual:** Simple bar chart or table comparing models used (e.g., R² values).
    *   **Feature Importance Snapshot:** Static image of a key feature importance plot (e.g., from XGBoost).
    *   **Placement:** Dedicate an "Analysis & Modelling" section/slide.

### 4. Create a Technology Stack Visual

*   **Asset:** A concise representation of the technologies employed.
*   **Content:** Categorise tools:
    *   **Core Language:** Python 3.
    *   **Data Manipulation & Analysis:** Pandas, NumPy, Statsmodels.
    *   **Machine Learning & Modelling:** Scikit-learn, PyGAM, XGBoost, Sentence-Transformers (for semantic matching).
    *   **Data Validation:** Pydantic.
    *   **Visualisation:** Plotly, Matplotlib, Seaborn, Kaleido (for static Plotly export).
    *   **Data Ingestion:** Requests, Beautifulsoup4, Openpyxl, lxml.
    *   **Testing:** Pytest, Pytest-Cov.
    *   **Code Quality & Formatting:** Black, Flake8, Mypy.
    *   **Development Environment:** Jupyter (optional for exploration), Git.
    *   **Interaction & Compute:** Torch (likely pulled in by `sentence-transformers`).
    *   **(Potential/Exploratory):** Dash (if used for alternative dashboards).
    *   **Meta-Tools & Development Process:**
        *   AI Pair Programming: Cursor AI / Large Language Models (LLMs).
        *   Version Control: Git / GitHub.
        *   Task Management: `tasks.md`.
        *   Project Planning: `planning.md`.
        *   *(Mention Retrieval-Augmented Generation (RAG) if specific RAG techniques were used beyond general LLM assistance)*.
        *   *(Mention "Vibe coding" if relevant to describe the development style)*.
*   **Portfolio Implementation:**
    *   **Icon Cloud/Grid:** Use logos for key technologies.
    *   **Categorised List:** A clean, well-formatted list under clear headings.
    *   **Placement:** Include in the project overview or a dedicated "Technical Skills Demonstrated" section linking back to this project.

## Implementation Notes

*   **Structure:** Organise the portfolio page into logical sections/slides corresponding to the assets above.
*   **Interactivity vs. Static:** Prioritise embedding the interactive dashboard. Flowcharts can be static (SVG/PNG) or interactive (Mermaid).
*   **Conciseness:** Keep explanatory text brief; let visuals dominate. Link to GitHub repo (`README.md`, reports) for details.
*   **Visual Consistency:** Maintain consistent styling (fonts, colours) across all visuals and the portfolio site.
