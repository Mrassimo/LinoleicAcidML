# Processed Data Summary

## aihw_cvd_all_facts.csv

### Dataset Overview
- Total Rows: 8,307
- Total Columns: 8
- Memory Usage: 3.95 MB
- Missing Values: 14,305
- Duplicate Rows: 777

### Column Information
| Column | Type | Non-Null | Unique | Memory (MB) | Additional Statistics |
|--------|------|-----------|---------|-------------|---------------------|
| year | int64 | 8,307 | 5 | 0.06 | Mean: 2022, Std: 3.63, Min: 2011, Max: 2025, Median: 2022 |
| value | float64 | 8,307 | 5,871 | 0.06 | Mean: 1.409e+07, Std: 2.887e+08, Min: 0.1, Max: 1.427e+10, Median: 752.3 |
| metric_type | object | 8,307 | 1 | 0.50 | Min Length: 6, Max Length: 6, Avg Length: 6 |
| source_sheet | object | 8,307 | 12 | 0.51 | Min Length: 2, Max Length: 22, Avg Length: 7.443 |
| sex | object | 33 | 3 | 0.25 | N/A |
| age_group | object | 2,276 | 60 | 0.32 | N/A |
| condition | object | 8,307 | 12 | 1.23 | Min Length: 5, Max Length: 110, Avg Length: 65.91 |
| table_name | object | 8,307 | 12 | 1.23 | Min Length: 5, Max Length: 110, Avg Length: 65.91 |

### Column Value Distributions

#### year

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 2025 | 3,942 | 47.45% |
| 2022 | 3,068 | 36.93% |
| 2011 | 479 | 5.77% |
| 2017 | 435 | 5.24% |
| 2018 | 383 | 4.61% |

#### value

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 1.2 | 27 | 0.33% |
| 0.8 | 26 | 0.31% |
| 1.1 | 25 | 0.30% |
| 0.9 | 24 | 0.29% |
| 0.6 | 22 | 0.26% |
| 1 | 22 | 0.26% |
| 1.7 | 22 | 0.26% |
| 0.7 | 21 | 0.25% |
| 1.4 | 20 | 0.24% |
| 1.9 | 19 | 0.23% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 79.3 | 1 | 0.01% |
| 64.3 | 1 | 0.01% |
| 1.011e+04 | 1 | 0.01% |
| 4040 | 1 | 0.01% |
| 6075 | 1 | 0.01% |
| 77.2 | 1 | 0.01% |
| 1.255e+04 | 1 | 0.01% |
| 4939 | 1 | 0.01% |
| 7610 | 1 | 0.01% |
| 1.828e+09 | 1 | 0.01% |

#### metric_type

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| number | 8,307 | 100.00% |

#### source_sheet

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| CHD | 1,331 | 16.02% |
| All CVD | 1,152 | 13.87% |
| Heart failure | 841 | 10.12% |
| PAD | 841 | 10.12% |
| AF | 824 | 9.92% |
| Treatment & management | 585 | 7.04% |
| Impact | 515 | 6.20% |
| Comorbidity | 479 | 5.77% |
| RHD | 470 | 5.66% |
| Congenital | 451 | 5.43% |
| Risk factors | 435 | 5.24% |
| Stroke | 383 | 4.61% |

#### sex

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| male | 11 | 0.13% |
| female | 11 | 0.13% |
| persons | 11 | 0.13% |

#### age_group

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 65-74 | 120 | 1.44% |
| 55-64 | 119 | 1.43% |
| allages | 110 | 1.32% |
| 45-54 | 109 | 1.31% |
| 75-84 | 108 | 1.30% |
| 35-44 | 98 | 1.18% |
| 25-34 | 64 | 0.77% |
| 2021-22 | 61 | 0.73% |
| 2016-17 | 61 | 0.73% |
| 2012-13 | 61 | 0.73% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 30-34 | 6 | 0.07% |
| 25-29 | 6 | 0.07% |
| 20-24 | 6 | 0.07% |
| 15-19 | 6 | 0.07% |
| 10-14 | 6 | 0.07% |
| 5-9 | 6 | 0.07% |
| total25andover | 6 | 0.07% |
| 0-4 | 4 | 0.05% |
| totalcardiovascularmedicines | 3 | 0.04% |
| allages(age-standardised) | 3 | 0.04% |

#### condition

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| Prevalence of self-reported coronary heart disease, persons 18 and over, by age and sex, 2022 | 1,331 | 16.02% |
| Prevalence of self-reported heart, stroke and vascular disease among persons 18 and over, by age and sex, 2022 | 1,152 | 13.87% |
| Heart failure and cardiomyopathy hospitalisations | 841 | 10.12% |
| Peripheral arterial disease hospitalisations | 841 | 10.12% |
| Atrial fibrillation hospitalisations | 824 | 9.92% |
| Supply of cardiovascular medicines, 2022–23 | 585 | 7.04% |
| Fatal | 515 | 6.20% |
| Prevalence of CVD, diabetes and CKD and their comorbidity, persons and 18 and over, by sex, 2011–12 | 479 | 5.77% |
| Acute rheumatic fever and rheumatic heart disease hospitalisations | 470 | 5.66% |
| Congenital heart disease hospitalisations | 451 | 5.43% |
| Prevalence distribution of systolic and diastolic blood pressure measurements among adults, 2017–18 | 435 | 5.24% |
| Prevalence of self-reported stroke, by age and sex, 2018 | 383 | 4.61% |

#### table_name

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| Prevalence of self-reported coronary heart disease, persons 18 and over, by age and sex, 2022 | 1,331 | 16.02% |
| Prevalence of self-reported heart, stroke and vascular disease among persons 18 and over, by age and sex, 2022 | 1,152 | 13.87% |
| Heart failure and cardiomyopathy hospitalisations | 841 | 10.12% |
| Peripheral arterial disease hospitalisations | 841 | 10.12% |
| Atrial fibrillation hospitalisations | 824 | 9.92% |
| Supply of cardiovascular medicines, 2022–23 | 585 | 7.04% |
| Fatal | 515 | 6.20% |
| Prevalence of CVD, diabetes and CKD and their comorbidity, persons and 18 and over, by sex, 2011–12 | 479 | 5.77% |
| Acute rheumatic fever and rheumatic heart disease hospitalisations | 470 | 5.66% |
| Congenital heart disease hospitalisations | 451 | 5.43% |
| Prevalence distribution of systolic and diastolic blood pressure measurements among adults, 2017–18 | 435 | 5.24% |
| Prevalence of self-reported stroke, by age and sex, 2018 | 383 | 4.61% |

### Sample Data

First 10 Rows:
|    |   year |   value | metric_type   | source_sheet   |   sex |   age_group | condition                                                                                           | table_name                                                                                          |
|---:|-------:|--------:|:--------------|:---------------|------:|------------:|:----------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------|
|  0 |   2017 |   0.196 | number        | Risk factors   |   nan |         nan | Prevalence distribution of systolic and diastolic blood pressure measurements among adults, 2017–18 | Prevalence distribution of systolic and diastolic blood pressure measurements among adults, 2017–18 |
|  1 |   2017 |   0.769 | number        | Risk factors   |   nan |         nan | Prevalence distribution of systolic and diastolic blood pressure measurements among adults, 2017–18 | Prevalence distribution of systolic and diastolic blood pressure measurements among adults, 2017–18 |
|  2 |   2017 |   0.478 | number        | Risk factors   |   nan |         nan | Prevalence distribution of systolic and diastolic blood pressure measurements among adults, 2017–18 | Prevalence distribution of systolic and diastolic blood pressure measurements among adults, 2017–18 |
|  3 |   2017 |   1.628 | number        | Risk factors   |   nan |         nan | Prevalence distribution of systolic and diastolic blood pressure measurements among adults, 2017–18 | Prevalence distribution of systolic and diastolic blood pressure measurements among adults, 2017–18 |
|  4 |   2017 |   0.632 | number        | Risk factors   |   nan |         nan | Prevalence distribution of systolic and diastolic blood pressure measurements among adults, 2017–18 | Prevalence distribution of systolic and diastolic blood pressure measurements among adults, 2017–18 |
|  5 |   2017 |   3.601 | number        | Risk factors   |   nan |         nan | Prevalence distribution of systolic and diastolic blood pressure measurements among adults, 2017–18 | Prevalence distribution of systolic and diastolic blood pressure measurements among adults, 2017–18 |
|  6 |   2017 |   1.827 | number        | Risk factors   |   nan |         nan | Prevalence distribution of systolic and diastolic blood pressure measurements among adults, 2017–18 | Prevalence distribution of systolic and diastolic blood pressure measurements among adults, 2017–18 |
|  7 |   2017 |   6.097 | number        | Risk factors   |   nan |         nan | Prevalence distribution of systolic and diastolic blood pressure measurements among adults, 2017–18 | Prevalence distribution of systolic and diastolic blood pressure measurements among adults, 2017–18 |
|  8 |   2017 |   4.472 | number        | Risk factors   |   nan |         nan | Prevalence distribution of systolic and diastolic blood pressure measurements among adults, 2017–18 | Prevalence distribution of systolic and diastolic blood pressure measurements among adults, 2017–18 |
|  9 |   2017 |  10.952 | number        | Risk factors   |   nan |         nan | Prevalence distribution of systolic and diastolic blood pressure measurements among adults, 2017–18 | Prevalence distribution of systolic and diastolic blood pressure measurements among adults, 2017–18 |

Last 10 Rows:
|      |   year |       value | metric_type   | source_sheet   | sex     |   age_group | condition   | table_name   |
|-----:|-------:|------------:|:--------------|:---------------|:--------|------------:|:------------|:-------------|
| 8297 |   2025 | 8.1842e+07  | number        | Impact         | persons |         nan | Fatal       | Fatal        |
| 8298 |   2025 | 1.75734e+08 | number        | Impact         | persons |         nan | Fatal       | Fatal        |
| 8299 |   2025 | 3.08971e+08 | number        | Impact         | persons |         nan | Fatal       | Fatal        |
| 8300 |   2025 | 5.87288e+08 | number        | Impact         | persons |         nan | Fatal       | Fatal        |
| 8301 |   2025 | 1.27414e+09 | number        | Impact         | persons |         nan | Fatal       | Fatal        |
| 8302 |   2025 | 2.42758e+09 | number        | Impact         | persons |         nan | Fatal       | Fatal        |
| 8303 |   2025 | 3.78581e+09 | number        | Impact         | persons |         nan | Fatal       | Fatal        |
| 8304 |   2025 | 3.61297e+09 | number        | Impact         | persons |         nan | Fatal       | Fatal        |
| 8305 |   2025 | 1.82822e+09 | number        | Impact         | persons |         nan | Fatal       | Fatal        |
| 8306 |   2025 | 1.42726e+10 | number        | Impact         | persons |         nan | Fatal       | Fatal        |

---

## aihw_dementia_mortality.csv

### Dataset Overview
- Total Rows: 546
- Total Columns: 8
- Memory Usage: 0.26 MB
- Missing Values: 858
- Duplicate Rows: 73

### Column Information
| Column | Type | Non-Null | Unique | Memory (MB) | Additional Statistics |
|--------|------|-----------|---------|-------------|---------------------|
| year | int64 | 546 | 4 | 0.00 | Mean: 2019, Std: 5.208, Min: 2009, Max: 2025, Median: 2022 |
| value | float64 | 546 | 388 | 0.00 | Mean: 1072, Std: 2771, Min: 0.1978, Max: 3.478e+04, Median: 75 |
| metric_type | object | 546 | 2 | 0.03 | Min Length: 4, Max Length: 6, Avg Length: 5.722 |
| source_sheet | object | 546 | 9 | 0.03 | Min Length: 4, Max Length: 4, Avg Length: 4 |
| sex | float64 | 0 | 0 | 0.00 | No numeric data available |
| age_group | object | 234 | 16 | 0.02 | N/A |
| condition | object | 546 | 9 | 0.08 | Min Length: 22, Max Length: 113, Avg Length: 94.32 |
| table_name | object | 546 | 9 | 0.08 | Min Length: 22, Max Length: 113, Avg Length: 94.32 |

### Column Value Distributions

#### year

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 2022 | 412 | 75.46% |
| 2009 | 98 | 17.95% |
| 2013 | 30 | 5.49% |
| 2025 | 6 | 1.10% |

#### value

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 43 | 8 | 1.47% |
| 45 | 7 | 1.28% |
| 46 | 7 | 1.28% |
| 48 | 7 | 1.28% |
| 40 | 6 | 1.10% |
| 49 | 6 | 1.10% |
| 41 | 5 | 0.92% |
| 64 | 5 | 0.92% |
| 39 | 5 | 0.92% |
| 4 | 5 | 0.92% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 16 | 1 | 0.18% |
| 17 | 1 | 0.18% |
| 8 | 1 | 0.18% |
| 41.09 | 1 | 0.18% |
| 47.67 | 1 | 0.18% |
| 39.52 | 1 | 0.18% |
| 6078 | 1 | 0.18% |
| 44.46 | 1 | 0.18% |
| 38.34 | 1 | 0.18% |
| 44.61 | 1 | 0.18% |

#### metric_type

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| number | 470 | 86.08% |
| rate | 76 | 13.92% |

#### source_sheet

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| S3.4 | 135 | 24.73% |
| S3.6 | 117 | 21.43% |
| S3.8 | 76 | 13.92% |
| S3.3 | 56 | 10.26% |
| S3.2 | 54 | 9.89% |
| S3.5 | 42 | 7.69% |
| S3.1 | 30 | 5.49% |
| S3.9 | 30 | 5.49% |
| S3.7 | 6 | 1.10% |

#### sex

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|

#### age_group

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 95+ | 42 | 7.69% |
| 85-94 | 39 | 7.14% |
| 75-84 | 36 | 6.59% |
| 65-74 | 27 | 4.95% |
| 30-64 | 17 | 3.11% |
| 65+ | 17 | 3.11% |
| 0-59 | 6 | 1.10% |
| 60-64 | 6 | 1.10% |
| 65-69 | 6 | 1.10% |
| 70-74 | 6 | 1.10% |
| 75-79 | 6 | 1.10% |
| 80-84 | 6 | 1.10% |
| 85-89 | 6 | 1.10% |
| 90-94 | 6 | 1.10% |
| all_ages | 5 | 0.92% |
| allages | 3 | 0.55% |

#### condition

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| a: Deaths due to dementia in 2022: number and crude rate by sex, age group and dementia type | 135 | 24.73% |
| Deaths due to dementia in 2022: age-standardised and crude rates by sex and geographic and socioeconomic areas | 117 | 21.43% |
| Leading underlying causes of death in 2022, when dementia was an associated cause of death | 76 | 13.92% |
| Deaths due to dementia in Australia over the period 2009 to 2022: number, age-standardised and crude rates by sex | 56 | 10.26% |
| Deaths due to dementia in 2022: number and crude rate by age and sex | 54 | 9.89% |
| Deaths due to dementia over the period 2009 to 2022: age-standardised and crude rates by dementia type | 42 | 7.69% |
| Leading causes of death in Australia in 2022, by sex: number and crude rate | 30 | 5.49% |
| Dementia deaths over the period 2013 to 2022: number, age-standardised rate and crude rate | 30 | 5.49% |
| Deaths due to dementia | 6 | 1.10% |

#### table_name

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| a: Deaths due to dementia in 2022: number and crude rate by sex, age group and dementia type | 135 | 24.73% |
| Deaths due to dementia in 2022: age-standardised and crude rates by sex and geographic and socioeconomic areas | 117 | 21.43% |
| Leading underlying causes of death in 2022, when dementia was an associated cause of death | 76 | 13.92% |
| Deaths due to dementia in Australia over the period 2009 to 2022: number, age-standardised and crude rates by sex | 56 | 10.26% |
| Deaths due to dementia in 2022: number and crude rate by age and sex | 54 | 9.89% |
| Deaths due to dementia over the period 2009 to 2022: age-standardised and crude rates by dementia type | 42 | 7.69% |
| Leading causes of death in Australia in 2022, by sex: number and crude rate | 30 | 5.49% |
| Dementia deaths over the period 2013 to 2022: number, age-standardised rate and crude rate | 30 | 5.49% |
| Deaths due to dementia | 6 | 1.10% |

### Sample Data

First 10 Rows:
|    |   year |      value | metric_type   | source_sheet   |   sex |   age_group | condition                                                                   | table_name                                                                  |
|---:|-------:|-----------:|:--------------|:---------------|------:|------------:|:----------------------------------------------------------------------------|:----------------------------------------------------------------------------|
|  0 |   2022 |    87.5513 | number        | S3.1           |   nan |         nan | Leading causes of death in Australia in 2022, by sex: number and crude rate | Leading causes of death in Australia in 2022, by sex: number and crude rate |
|  1 |   2022 | 11303      | number        | S3.1           |   nan |         nan | Leading causes of death in Australia in 2022, by sex: number and crude rate | Leading causes of death in Australia in 2022, by sex: number and crude rate |
|  2 |   2022 |    85.9797 | number        | S3.1           |   nan |         nan | Leading causes of death in Australia in 2022, by sex: number and crude rate | Leading causes of death in Australia in 2022, by sex: number and crude rate |
|  3 |   2022 | 11267      | number        | S3.1           |   nan |         nan | Leading causes of death in Australia in 2022, by sex: number and crude rate | Leading causes of death in Australia in 2022, by sex: number and crude rate |
|  4 |   2022 |    71.6642 | number        | S3.1           |   nan |         nan | Leading causes of death in Australia in 2022, by sex: number and crude rate | Leading causes of death in Australia in 2022, by sex: number and crude rate |
|  5 |   2022 | 18643      | number        | S3.1           |   nan |         nan | Leading causes of death in Australia in 2022, by sex: number and crude rate | Leading causes of death in Australia in 2022, by sex: number and crude rate |
|  6 |   2022 |    50.7663 | number        | S3.1           |   nan |         nan | Leading causes of death in Australia in 2022, by sex: number and crude rate | Leading causes of death in Australia in 2022, by sex: number and crude rate |
|  7 |   2022 |  6554      | number        | S3.1           |   nan |         nan | Leading causes of death in Australia in 2022, by sex: number and crude rate | Leading causes of death in Australia in 2022, by sex: number and crude rate |
|  8 |   2022 |    56.0124 | number        | S3.1           |   nan |         nan | Leading causes of death in Australia in 2022, by sex: number and crude rate | Leading causes of death in Australia in 2022, by sex: number and crude rate |
|  9 |   2022 |  7340      | number        | S3.1           |   nan |         nan | Leading causes of death in Australia in 2022, by sex: number and crude rate | Leading causes of death in Australia in 2022, by sex: number and crude rate |

Last 10 Rows:
|     |   year |     value | metric_type   | source_sheet   |   sex |   age_group | condition                                                                                  | table_name                                                                                 |
|----:|-------:|----------:|:--------------|:---------------|------:|------------:|:-------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------|
| 536 |   2013 |   37.8516 | rate          | S3.9           |   nan |         nan | Dementia deaths over the period 2013 to 2022: number, age-standardised rate and crude rate | Dementia deaths over the period 2013 to 2022: number, age-standardised rate and crude rate |
| 537 |   2013 | 2020      | number        | S3.9           |   nan |         nan | Dementia deaths over the period 2013 to 2022: number, age-standardised rate and crude rate | Dementia deaths over the period 2013 to 2022: number, age-standardised rate and crude rate |
| 538 |   2013 |   41.1215 | rate          | S3.9           |   nan |         nan | Dementia deaths over the period 2013 to 2022: number, age-standardised rate and crude rate | Dementia deaths over the period 2013 to 2022: number, age-standardised rate and crude rate |
| 539 |   2013 |   35.9169 | rate          | S3.9           |   nan |         nan | Dementia deaths over the period 2013 to 2022: number, age-standardised rate and crude rate | Dementia deaths over the period 2013 to 2022: number, age-standardised rate and crude rate |
| 540 |   2013 | 2021      | number        | S3.9           |   nan |         nan | Dementia deaths over the period 2013 to 2022: number, age-standardised rate and crude rate | Dementia deaths over the period 2013 to 2022: number, age-standardised rate and crude rate |
| 541 |   2013 |   43.0893 | rate          | S3.9           |   nan |         nan | Dementia deaths over the period 2013 to 2022: number, age-standardised rate and crude rate | Dementia deaths over the period 2013 to 2022: number, age-standardised rate and crude rate |
| 542 |   2013 |   38.2258 | rate          | S3.9           |   nan |         nan | Dementia deaths over the period 2013 to 2022: number, age-standardised rate and crude rate | Dementia deaths over the period 2013 to 2022: number, age-standardised rate and crude rate |
| 543 |   2013 | 2022      | number        | S3.9           |   nan |         nan | Dementia deaths over the period 2013 to 2022: number, age-standardised rate and crude rate | Dementia deaths over the period 2013 to 2022: number, age-standardised rate and crude rate |
| 544 |   2013 |   44.8377 | rate          | S3.9           |   nan |         nan | Dementia deaths over the period 2013 to 2022: number, age-standardised rate and crude rate | Dementia deaths over the period 2013 to 2022: number, age-standardised rate and crude rate |
| 545 |   2013 |   44.607  | rate          | S3.9           |   nan |         nan | Dementia deaths over the period 2013 to 2022: number, age-standardised rate and crude rate | Dementia deaths over the period 2013 to 2022: number, age-standardised rate and crude rate |

---

## aihw_dementia_prevalence.csv

### Dataset Overview
- Total Rows: 7,624
- Total Columns: 8
- Memory Usage: 3.36 MB
- Missing Values: 15,125
- Duplicate Rows: 6,452

### Column Information
| Column | Type | Non-Null | Unique | Memory (MB) | Additional Statistics |
|--------|------|-----------|---------|-------------|---------------------|
| year | int64 | 7,624 | 5 | 0.06 | Mean: 2021, Std: 2.67, Min: 2010, Max: 2025, Median: 2022 |
| value | float64 | 7,624 | 1,115 | 0.06 | Mean: 1.18e+04, Std: 6.662e+04, Min: 0.4802, Max: 8.493e+05, Median: 95 |
| metric_type | object | 7,624 | 2 | 0.46 | Min Length: 6, Max Length: 10, Avg Length: 6.016 |
| source_sheet | object | 7,624 | 9 | 0.44 | Min Length: 4, Max Length: 4, Avg Length: 4 |
| sex | object | 21 | 3 | 0.23 | N/A |
| age_group | object | 102 | 10 | 0.24 | N/A |
| condition | object | 7,624 | 9 | 0.93 | Min Length: 68, Max Length: 103, Avg Length: 71.49 |
| table_name | object | 7,624 | 9 | 0.93 | Min Length: 68, Max Length: 103, Avg Length: 71.49 |

### Column Value Distributions

#### year

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 2022 | 7,121 | 93.40% |
| 2010 | 392 | 5.14% |
| 2023 | 54 | 0.71% |
| 2025 | 39 | 0.51% |
| 2018 | 18 | 0.24% |

#### value

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 35 | 60 | 0.79% |
| 40 | 59 | 0.77% |
| 38 | 58 | 0.76% |
| 52 | 57 | 0.75% |
| 58 | 55 | 0.72% |
| 37 | 55 | 0.72% |
| 68 | 54 | 0.71% |
| 34 | 54 | 0.71% |
| 33 | 54 | 0.71% |
| 24 | 54 | 0.71% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 3.036e+05 | 1 | 0.01% |
| 3.152e+04 | 1 | 0.01% |
| 3.126e+05 | 1 | 0.01% |
| 3.127e+05 | 1 | 0.01% |
| 3.22e+04 | 1 | 0.01% |
| 3.16e+05 | 1 | 0.01% |
| 3.22e+05 | 1 | 0.01% |
| 3.305e+04 | 1 | 0.01% |
| 3.189e+05 | 1 | 0.01% |
| 648 | 1 | 0.01% |

#### metric_type

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| number | 7,594 | 99.61% |
| percentage | 30 | 0.39% |

#### source_sheet

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| S2.9 | 6,923 | 90.81% |
| S2.4 | 196 | 2.57% |
| S2.5 | 196 | 2.57% |
| S2.8 | 93 | 1.22% |
| S2.6 | 57 | 0.75% |
| S2.1 | 54 | 0.71% |
| S2.2 | 48 | 0.63% |
| S2.7 | 39 | 0.51% |
| S2.3 | 18 | 0.24% |

#### sex

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| male | 7 | 0.09% |
| female | 7 | 0.09% |
| persons | 7 | 0.09% |

#### age_group

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 65-69 | 12 | 0.16% |
| 70-74 | 12 | 0.16% |
| 75-79 | 12 | 0.16% |
| 80-84 | 12 | 0.16% |
| 85-89 | 12 | 0.16% |
| 90+ | 12 | 0.16% |
| all_ages | 12 | 0.16% |
| 30-59 | 6 | 0.08% |
| 60-64 | 6 | 0.08% |
| 30-64 | 6 | 0.08% |

#### condition

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| Australians living with dementia in 2022: number by statistical area 2 | 6,923 | 90.81% |
| Australians living with dementia between 2010 and 2058: estimated number by sex and year | 196 | 2.57% |
| Australians living with dementia between 2010 and 2058: estimated number by age and year | 196 | 2.57% |
| Australians living with dementia in 2022: number by PHN, age and sex | 93 | 1.22% |
| Australians living with dementia in 2022: estimated number by sex, and geographic or socioeconomic area | 57 | 0.75% |
| Prevalence of dementia in 2023: estimated number and rate, by age and sex | 54 | 0.71% |
| Australians living with dementia in 2022: number and percentage by age, sex and place of residence | 48 | 0.63% |
| People living with dementia in Organisation for Economic Co-operation and Development | 39 | 0.51% |
| Australians living with dementia in the community in 2018: percentage by sex and living arrangements | 18 | 0.24% |

#### table_name

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| Australians living with dementia in 2022: number by statistical area 2 | 6,923 | 90.81% |
| Australians living with dementia between 2010 and 2058: estimated number by sex and year | 196 | 2.57% |
| Australians living with dementia between 2010 and 2058: estimated number by age and year | 196 | 2.57% |
| Australians living with dementia in 2022: number by PHN, age and sex | 93 | 1.22% |
| Australians living with dementia in 2022: estimated number by sex, and geographic or socioeconomic area | 57 | 0.75% |
| Prevalence of dementia in 2023: estimated number and rate, by age and sex | 54 | 0.71% |
| Australians living with dementia in 2022: number and percentage by age, sex and place of residence | 48 | 0.63% |
| People living with dementia in Organisation for Economic Co-operation and Development | 39 | 0.51% |
| Australians living with dementia in the community in 2018: percentage by sex and living arrangements | 18 | 0.24% |

### Sample Data

First 10 Rows:
|    |   year |        value | metric_type   | source_sheet   | sex   | age_group   | condition                                                                 | table_name                                                                |
|---:|-------:|-------------:|:--------------|:---------------|:------|:------------|:--------------------------------------------------------------------------|:--------------------------------------------------------------------------|
|  0 |   2023 |  2966.37     | number        | S2.1           | male  | 30-59       | Prevalence of dementia in 2023: estimated number and rate, by age and sex | Prevalence of dementia in 2023: estimated number and rate, by age and sex |
|  1 |   2023 |     0.570647 | number        | S2.1           | male  | 30-59       | Prevalence of dementia in 2023: estimated number and rate, by age and sex | Prevalence of dementia in 2023: estimated number and rate, by age and sex |
|  2 |   2023 | 10306.2      | number        | S2.1           | nan   | 60-64       | Prevalence of dementia in 2023: estimated number and rate, by age and sex | Prevalence of dementia in 2023: estimated number and rate, by age and sex |
|  3 |   2023 |    13.9625   | number        | S2.1           | nan   | 60-64       | Prevalence of dementia in 2023: estimated number and rate, by age and sex | Prevalence of dementia in 2023: estimated number and rate, by age and sex |
|  4 |   2023 | 14023.7      | number        | S2.1           | nan   | 65-69       | Prevalence of dementia in 2023: estimated number and rate, by age and sex | Prevalence of dementia in 2023: estimated number and rate, by age and sex |
|  5 |   2023 |    21.9955   | number        | S2.1           | nan   | 65-69       | Prevalence of dementia in 2023: estimated number and rate, by age and sex | Prevalence of dementia in 2023: estimated number and rate, by age and sex |
|  6 |   2023 | 19803.3      | number        | S2.1           | nan   | 70-74       | Prevalence of dementia in 2023: estimated number and rate, by age and sex | Prevalence of dementia in 2023: estimated number and rate, by age and sex |
|  7 |   2023 |    35.8004   | number        | S2.1           | nan   | 70-74       | Prevalence of dementia in 2023: estimated number and rate, by age and sex | Prevalence of dementia in 2023: estimated number and rate, by age and sex |
|  8 |   2023 | 27335        | number        | S2.1           | nan   | 75-79       | Prevalence of dementia in 2023: estimated number and rate, by age and sex | Prevalence of dementia in 2023: estimated number and rate, by age and sex |
|  9 |   2023 |    61.2936   | number        | S2.1           | nan   | 75-79       | Prevalence of dementia in 2023: estimated number and rate, by age and sex | Prevalence of dementia in 2023: estimated number and rate, by age and sex |

Last 10 Rows:
|      |   year |   value | metric_type   | source_sheet   |   sex |   age_group | condition                                                              | table_name                                                             |
|-----:|-------:|--------:|:--------------|:---------------|------:|------------:|:-----------------------------------------------------------------------|:-----------------------------------------------------------------------|
| 7614 |   2022 |      10 | number        | S2.9           |   nan |         nan | Australians living with dementia in 2022: number by statistical area 2 | Australians living with dementia in 2022: number by statistical area 2 |
| 7615 |   2022 |      18 | number        | S2.9           |   nan |         nan | Australians living with dementia in 2022: number by statistical area 2 | Australians living with dementia in 2022: number by statistical area 2 |
| 7616 |   2022 |       9 | number        | S2.9           |   nan |         nan | Australians living with dementia in 2022: number by statistical area 2 | Australians living with dementia in 2022: number by statistical area 2 |
| 7617 |   2022 |       6 | number        | S2.9           |   nan |         nan | Australians living with dementia in 2022: number by statistical area 2 | Australians living with dementia in 2022: number by statistical area 2 |
| 7618 |   2022 |      15 | number        | S2.9           |   nan |         nan | Australians living with dementia in 2022: number by statistical area 2 | Australians living with dementia in 2022: number by statistical area 2 |
| 7619 |   2022 |       7 | number        | S2.9           |   nan |         nan | Australians living with dementia in 2022: number by statistical area 2 | Australians living with dementia in 2022: number by statistical area 2 |
| 7620 |   2022 |       9 | number        | S2.9           |   nan |         nan | Australians living with dementia in 2022: number by statistical area 2 | Australians living with dementia in 2022: number by statistical area 2 |
| 7621 |   2022 |      16 | number        | S2.9           |   nan |         nan | Australians living with dementia in 2022: number by statistical area 2 | Australians living with dementia in 2022: number by statistical area 2 |
| 7622 |   2022 |       5 | number        | S2.9           |   nan |         nan | Australians living with dementia in 2022: number by statistical area 2 | Australians living with dementia in 2022: number by statistical area 2 |
| 7623 |   2022 |       9 | number        | S2.9           |   nan |         nan | Australians living with dementia in 2022: number by statistical area 2 | Australians living with dementia in 2022: number by statistical area 2 |

---

## faostat_fbs_australia.csv

### Dataset Overview
- Total Rows: 1,333
- Total Columns: 48
- Memory Usage: 1.53 MB
- Missing Values: 38,509
- Duplicate Rows: 225

### Column Information
| Column | Type | Non-Null | Unique | Memory (MB) | Additional Statistics |
|--------|------|-----------|---------|-------------|---------------------|
| area_code | object | 1,333 | 249 | 0.08 | Min Length: 1, Max Length: 4, Avg Length: 2.297 |
| Area Code (M49) | object | 1,333 | 250 | 0.08 | Min Length: 4, Max Length: 39, Avg Length: 4.278 |
| area | object | 1,308 | 225 | 0.08 | N/A |
| item_code | float64 | 858 | 108 | 0.01 | Mean: 2693, Std: 143.9, Min: 2511, Max: 2960, Median: 2640 |
| Item Code (FBS) | object | 858 | 108 | 0.07 | N/A |
| item | object | 858 | 105 | 0.07 | N/A |
| element_code | float64 | 858 | 4 | 0.01 | Mean: 666.9, Std: 14.35, Min: 645, Max: 684, Median: 674 |
| element | object | 858 | 4 | 0.09 | N/A |
| Unit | object | 858 | 3 | 0.07 | N/A |
| Y2010 | float64 | 826 | 260 | 0.01 | Mean: 42.19, Std: 228.2, Min: 0, Max: 3534, Median: 1.4 |
| Y2010F | object | 826 | 265 | 0.06 | N/A |
| Y2010N | float64 | 417 | 266 | 0.01 | Mean: 42.06, Std: 229.6, Min: 0, Max: 3564, Median: 1.34 |
| Y2011 | float64 | 830 | 469 | 0.01 | Mean: 41.91, Std: 227.9, Min: 0, Max: 3546, Median: 1.435 |
| Y2011F | object | 834 | 270 | 0.06 | N/A |
| Y2011N | float64 | 420 | 268 | 0.01 | Mean: 41.27, Std: 225.1, Min: 0, Max: 3519, Median: 1.43 |
| Y2012 | float64 | 837 | 465 | 0.01 | Mean: 41.77, Std: 227.9, Min: 0, Max: 3564, Median: 1.47 |
| Y2012F | object | 837 | 263 | 0.06 | N/A |
| Y2012N | float64 | 420 | 267 | 0.01 | Mean: 40.63, Std: 222.1, Min: 0, Max: 3470, Median: 1.35 |
| Y2013 | float64 | 838 | 474 | 0.01 | Mean: 41.37, Std: 226.2, Min: 0, Max: 3546, Median: 1.555 |
| Y2013F | object | 838 | 274 | 0.06 | N/A |
| Y2013N | float64 | 420 | 268 | 0.01 | Mean: 40.73, Std: 223.2, Min: 0, Max: 3479, Median: 1.4 |
| Y2014 | float64 | 849 | 466 | 0.01 | Mean: 40.68, Std: 223.7, Min: 0, Max: 3533, Median: 1.42 |
| Y2014F | object | 421 | 1 | 0.05 | N/A |
| Y2014N | float64 | 0 | 0 | 0.01 | No numeric data available |
| Y2015 | float64 | 420 | 268 | 0.01 | Mean: 41.27, Std: 225.1, Min: 0, Max: 3519, Median: 1.43 |
| Y2015F | object | 420 | 1 | 0.05 | N/A |
| Y2015N | float64 | 0 | 0 | 0.01 | No numeric data available |
| Y2016 | float64 | 420 | 262 | 0.01 | Mean: 41.48, Std: 226.4, Min: 0, Max: 3537, Median: 1.57 |
| Y2016F | object | 420 | 1 | 0.05 | N/A |
| Y2016N | float64 | 0 | 0 | 0.01 | No numeric data available |
| Y2017 | float64 | 420 | 262 | 0.01 | Mean: 40.88, Std: 223.8, Min: 0, Max: 3493, Median: 1.45 |
| Y2017F | object | 420 | 1 | 0.05 | N/A |
| Y2017N | float64 | 0 | 0 | 0.01 | No numeric data available |
| Y2018 | float64 | 420 | 267 | 0.01 | Mean: 40.63, Std: 222.1, Min: 0, Max: 3470, Median: 1.35 |
| Y2018F | object | 420 | 1 | 0.05 | N/A |
| Y2018N | float64 | 0 | 0 | 0.01 | No numeric data available |
| Y2019 | float64 | 421 | 270 | 0.01 | Mean: 40.86, Std: 224, Min: 0, Max: 3503, Median: 1.57 |
| Y2019F | object | 421 | 1 | 0.05 | N/A |
| Y2019N | float64 | 0 | 0 | 0.01 | No numeric data available |
| Y2020 | float64 | 421 | 273 | 0.01 | Mean: 40.68, Std: 222.2, Min: 0, Max: 3478, Median: 1.55 |
| Y2020F | object | 421 | 1 | 0.05 | N/A |
| Y2020N | float64 | 0 | 0 | 0.01 | No numeric data available |
| Y2021 | float64 | 420 | 268 | 0.01 | Mean: 40.73, Std: 223.2, Min: 0, Max: 3479, Median: 1.4 |
| Y2021F | object | 420 | 1 | 0.05 | N/A |
| Y2021N | float64 | 0 | 0 | 0.01 | No numeric data available |
| Y2022 | float64 | 428 | 261 | 0.01 | Mean: 40.14, Std: 221.4, Min: 0, Max: 3471, Median: 1.37 |
| Y2022F | object | 428 | 1 | 0.05 | N/A |
| Y2022N | float64 | 0 | 0 | 0.01 | No numeric data available |

### Column Value Distributions

#### area_code

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 10 | 860 | 64.52% |
| 5301 | 3 | 0.23% |
| 181 | 2 | 0.15% |
| 117 | 2 | 0.15% |
| 147 | 2 | 0.15% |
| 148 | 2 | 0.15% |
| 149 | 2 | 0.15% |
| 5817 | 2 | 0.15% |
| 150 | 2 | 0.15% |
| 151 | 2 | 0.15% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 5154 | 1 | 0.08% |
| 5131 | 1 | 0.08% |
| 5511 | 1 | 0.08% |
| 674 | 1 | 0.08% |
| 671 | 1 | 0.08% |
| 5170 | 1 | 0.08% |
| 5527 | 1 | 0.08% |
| 5072 | 1 | 0.08% |
| 511 | 1 | 0.08% |
| X | 1 | 0.08% |

#### Area Code (M49)

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| '036 | 860 | 64.52% |
| '104 | 2 | 0.15% |
| '520 | 2 | 0.15% |
| '524 | 2 | 0.15% |
| '902 | 2 | 0.15% |
| '528 | 2 | 0.15% |
| '530 | 2 | 0.15% |
| '540 | 2 | 0.15% |
| '554 | 2 | 0.15% |
| '558 | 2 | 0.15% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| Processing | 1 | 0.08% |
| Production | 1 | 0.08% |
| Protein supply quantity (g/capita/day) | 1 | 0.08% |
| Protein supply quantity (t) | 1 | 0.08% |
| Residuals | 1 | 0.08% |
| Seed | 1 | 0.08% |
| Stock Variation | 1 | 0.08% |
| Total Population - Both sexes | 1 | 0.08% |
| Domestic supply quantity | 1 | 0.08% |
| Figure from international organizations | 1 | 0.08% |

#### area

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| Australia | 860 | 64.52% |
| Lithuania | 2 | 0.15% |
| Nicaragua | 2 | 0.15% |
| Niger | 2 | 0.15% |
| Nigeria | 2 | 0.15% |
| North Macedonia | 2 | 0.15% |
| Northern Africa | 2 | 0.15% |
| Northern America | 2 | 0.15% |
| Northern Europe | 2 | 0.15% |
| Norway | 2 | 0.15% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| French Polynesia | 2 | 0.15% |
| Gabon | 2 | 0.15% |
| Gambia | 2 | 0.15% |
| Georgia | 2 | 0.15% |
| Germany | 2 | 0.15% |
| Ghana | 2 | 0.15% |
| Greece | 2 | 0.15% |
| Grenada | 2 | 0.15% |
| Guatemala | 2 | 0.15% |
| Zimbabwe | 2 | 0.15% |

#### item_code

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 2611 | 8 | 0.60% |
| 2732 | 8 | 0.60% |
| 2943 | 8 | 0.60% |
| 2658 | 8 | 0.60% |
| 2657 | 8 | 0.60% |
| 2656 | 8 | 0.60% |
| 2655 | 8 | 0.60% |
| 2924 | 8 | 0.60% |
| 2645 | 8 | 0.60% |
| 2642 | 8 | 0.60% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 2570 | 8 | 0.60% |
| 2563 | 8 | 0.60% |
| 2560 | 8 | 0.60% |
| 2558 | 8 | 0.60% |
| 2552 | 8 | 0.60% |
| 2555 | 8 | 0.60% |
| 2913 | 8 | 0.60% |
| 2941 | 6 | 0.45% |
| 2903 | 6 | 0.45% |
| 2901 | 6 | 0.45% |

#### Item Code (FBS)

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 'S2611 | 8 | 0.60% |
| 'S2732 | 8 | 0.60% |
| 'S2943 | 8 | 0.60% |
| 'S2658 | 8 | 0.60% |
| 'S2657 | 8 | 0.60% |
| 'S2656 | 8 | 0.60% |
| 'S2655 | 8 | 0.60% |
| 'S2924 | 8 | 0.60% |
| 'S2645 | 8 | 0.60% |
| 'S2642 | 8 | 0.60% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 'S2570 | 8 | 0.60% |
| 'S2563 | 8 | 0.60% |
| 'S2560 | 8 | 0.60% |
| 'S2558 | 8 | 0.60% |
| 'S2552 | 8 | 0.60% |
| 'S2555 | 8 | 0.60% |
| 'S2913 | 8 | 0.60% |
| 'S2941 | 6 | 0.45% |
| 'S2903 | 6 | 0.45% |
| 'S2901 | 6 | 0.45% |

#### item

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| Eggs | 16 | 1.20% |
| Miscellaneous | 16 | 1.20% |
| Milk - Excluding Butter | 16 | 1.20% |
| Stimulants | 8 | 0.60% |
| Wine | 8 | 0.60% |
| Alcoholic Beverages | 8 | 0.60% |
| Spices, Other | 8 | 0.60% |
| Cloves | 8 | 0.60% |
| Pimento | 8 | 0.60% |
| Pepper | 8 | 0.60% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| Olives (including preserved) | 8 | 0.60% |
| Coconuts - Incl Copra | 8 | 0.60% |
| Rape and Mustardseed | 8 | 0.60% |
| Groundnuts | 8 | 0.60% |
| Soyabeans | 8 | 0.60% |
| Oilcrops | 8 | 0.60% |
| Nuts and products | 8 | 0.60% |
| Animal Products | 6 | 0.45% |
| Vegetal Products | 6 | 0.45% |
| Grand Total | 6 | 0.45% |

#### element_code

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 664 | 216 | 16.20% |
| 674 | 216 | 16.20% |
| 684 | 216 | 16.20% |
| 645 | 210 | 15.75% |

#### element

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| Food supply (kcal/capita/day) | 216 | 16.20% |
| Protein supply quantity (g/capita/day) | 216 | 16.20% |
| Fat supply quantity (g/capita/day) | 216 | 16.20% |
| Food supply quantity (kg/capita/yr) | 210 | 15.75% |

#### Unit

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| g/cap/d | 432 | 32.41% |
| kcal/cap/d | 216 | 16.20% |
| kg/cap | 210 | 15.75% |

#### Y2010

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0 | 94 | 7.05% |
| 0.01 | 34 | 2.55% |
| 0.03 | 20 | 1.50% |
| 0.02 | 16 | 1.20% |
| 0.04 | 12 | 0.90% |
| 0.08 | 12 | 0.90% |
| 0.06 | 10 | 0.75% |
| 0.28 | 8 | 0.60% |
| 0.29 | 8 | 0.60% |
| 0.14 | 8 | 0.60% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 7.94 | 2 | 0.15% |
| 195.5 | 2 | 0.15% |
| 1.63 | 2 | 0.15% |
| 40.27 | 2 | 0.15% |
| 4.47 | 2 | 0.15% |
| 4.48 | 2 | 0.15% |
| 110.2 | 2 | 0.15% |
| 12.24 | 2 | 0.15% |
| 3.79 | 2 | 0.15% |
| 2.11 | 2 | 0.15% |

#### Y2010F

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| E | 413 | 30.98% |
| 0.0 | 45 | 3.38% |
| 0.01 | 14 | 1.05% |
| 0.02 | 9 | 0.68% |
| 0.03 | 9 | 0.68% |
| 0.07 | 6 | 0.45% |
| 0.04 | 5 | 0.38% |
| 0.12 | 5 | 0.38% |
| 0.08 | 5 | 0.38% |
| 0.27 | 4 | 0.30% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 62.85 | 1 | 0.08% |
| 6.98 | 1 | 0.08% |
| 4.24 | 1 | 0.08% |
| 104.31 | 1 | 0.08% |
| 11.59 | 1 | 0.08% |
| 3.85 | 1 | 0.08% |
| 1.71 | 1 | 0.08% |
| 42.2 | 1 | 0.08% |
| 4.68 | 1 | 0.08% |
| 0.35 | 1 | 0.08% |

#### Y2010N

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0 | 45 | 3.38% |
| 0.01 | 15 | 1.13% |
| 0.02 | 10 | 0.75% |
| 0.03 | 8 | 0.60% |
| 0.15 | 7 | 0.53% |
| 0.04 | 7 | 0.53% |
| 0.05 | 5 | 0.38% |
| 0.09 | 5 | 0.38% |
| 0.29 | 4 | 0.30% |
| 0.11 | 4 | 0.30% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 3.58 | 1 | 0.08% |
| 1.71 | 1 | 0.08% |
| 42.22 | 1 | 0.08% |
| 4.69 | 1 | 0.08% |
| 5.09 | 1 | 0.08% |
| 7.39 | 1 | 0.08% |
| 162.5 | 1 | 0.08% |
| 18.02 | 1 | 0.08% |
| 131 | 1 | 0.08% |
| 0.35 | 1 | 0.08% |

#### Y2011

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0 | 87 | 6.53% |
| 0.01 | 30 | 2.25% |
| 0.02 | 18 | 1.35% |
| 0.03 | 17 | 1.28% |
| 0.07 | 10 | 0.75% |
| 0.11 | 9 | 0.68% |
| 0.29 | 8 | 0.60% |
| 0.14 | 8 | 0.60% |
| 0.08 | 8 | 0.60% |
| 0.04 | 7 | 0.53% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 7.42 | 1 | 0.08% |
| 7.47 | 1 | 0.08% |
| 97.04 | 1 | 0.08% |
| 23.62 | 1 | 0.08% |
| 4.41 | 1 | 0.08% |
| 4.09 | 1 | 0.08% |
| 55.99 | 1 | 0.08% |
| 9.22 | 1 | 0.08% |
| 9.69 | 1 | 0.08% |
| 34.66 | 1 | 0.08% |

#### Y2011F

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| E | 413 | 30.98% |
| 0.0 | 43 | 3.23% |
| 0.01 | 15 | 1.13% |
| 0.02 | 10 | 0.75% |
| 0.03 | 10 | 0.75% |
| 0.21 | 6 | 0.45% |
| 0.14 | 6 | 0.45% |
| 0.06 | 5 | 0.38% |
| 0.07 | 5 | 0.38% |
| 0.08 | 5 | 0.38% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 2.71 | 1 | 0.08% |
| 66.82 | 1 | 0.08% |
| 7.42 | 1 | 0.08% |
| 3.42 | 1 | 0.08% |
| 84.13 | 1 | 0.08% |
| 9.35 | 1 | 0.08% |
| 5.94 | 1 | 0.08% |
| 2.24 | 1 | 0.08% |
| 55.26 | 1 | 0.08% |
| 0.35 | 1 | 0.08% |

#### Y2011N

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0 | 45 | 3.38% |
| 0.01 | 16 | 1.20% |
| 0.02 | 9 | 0.68% |
| 0.03 | 7 | 0.53% |
| 0.06 | 5 | 0.38% |
| 0.05 | 5 | 0.38% |
| 0.1 | 5 | 0.38% |
| 0.13 | 5 | 0.38% |
| 0.09 | 5 | 0.38% |
| 0.15 | 4 | 0.30% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 23.62 | 1 | 0.08% |
| 2.66 | 1 | 0.08% |
| 65.63 | 1 | 0.08% |
| 7.29 | 1 | 0.08% |
| 3.47 | 1 | 0.08% |
| 85.47 | 1 | 0.08% |
| 9.5 | 1 | 0.08% |
| 2.01 | 1 | 0.08% |
| 5.16 | 1 | 0.08% |
| 0.35 | 1 | 0.08% |

#### Y2012

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0 | 91 | 6.83% |
| 0.01 | 26 | 1.95% |
| 0.02 | 22 | 1.65% |
| 0.03 | 16 | 1.20% |
| 0.09 | 12 | 0.90% |
| 0.05 | 10 | 0.75% |
| 0.04 | 10 | 0.75% |
| 0.15 | 9 | 0.68% |
| 0.06 | 7 | 0.53% |
| 0.14 | 7 | 0.53% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 15.24 | 1 | 0.08% |
| 137.9 | 1 | 0.08% |
| 37.05 | 1 | 0.08% |
| 31.67 | 1 | 0.08% |
| 50.09 | 1 | 0.08% |
| 486 | 1 | 0.08% |
| 121.5 | 1 | 0.08% |
| 18.29 | 1 | 0.08% |
| 1.75 | 1 | 0.08% |
| 2.1 | 1 | 0.08% |

#### Y2012F

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| E | 417 | 31.28% |
| 0.0 | 44 | 3.30% |
| 0.01 | 16 | 1.20% |
| 0.02 | 11 | 0.83% |
| 0.06 | 6 | 0.45% |
| 0.03 | 6 | 0.45% |
| 0.1 | 5 | 0.38% |
| 0.14 | 5 | 0.38% |
| 0.04 | 5 | 0.38% |
| 0.05 | 5 | 0.38% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 22.9 | 1 | 0.08% |
| 2.61 | 1 | 0.08% |
| 64.48 | 1 | 0.08% |
| 7.16 | 1 | 0.08% |
| 3.57 | 1 | 0.08% |
| 87.93 | 1 | 0.08% |
| 9.77 | 1 | 0.08% |
| 1.66 | 1 | 0.08% |
| 4.35 | 1 | 0.08% |
| 34.44 | 1 | 0.08% |

#### Y2012N

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0 | 46 | 3.45% |
| 0.01 | 15 | 1.13% |
| 0.02 | 12 | 0.90% |
| 0.03 | 8 | 0.60% |
| 0.12 | 7 | 0.53% |
| 0.17 | 6 | 0.45% |
| 0.05 | 5 | 0.38% |
| 0.07 | 5 | 0.38% |
| 0.04 | 4 | 0.30% |
| 0.1 | 4 | 0.30% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 63.18 | 1 | 0.08% |
| 7.02 | 1 | 0.08% |
| 3.67 | 1 | 0.08% |
| 90.38 | 1 | 0.08% |
| 10.04 | 1 | 0.08% |
| 1.86 | 1 | 0.08% |
| 4.43 | 1 | 0.08% |
| 0.49 | 1 | 0.08% |
| 47.82 | 1 | 0.08% |
| 1.92 | 1 | 0.08% |

#### Y2013

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0 | 88 | 6.60% |
| 0.01 | 30 | 2.25% |
| 0.02 | 18 | 1.35% |
| 0.03 | 16 | 1.20% |
| 0.07 | 11 | 0.83% |
| 0.05 | 9 | 0.68% |
| 0.11 | 9 | 0.68% |
| 0.14 | 9 | 0.68% |
| 0.29 | 8 | 0.60% |
| 0.06 | 8 | 0.60% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 9.97 | 1 | 0.08% |
| 14.79 | 1 | 0.08% |
| 133.8 | 1 | 0.08% |
| 35.97 | 1 | 0.08% |
| 31.41 | 1 | 0.08% |
| 49.73 | 1 | 0.08% |
| 482 | 1 | 0.08% |
| 120.5 | 1 | 0.08% |
| 18.41 | 1 | 0.08% |
| 2.95 | 1 | 0.08% |

#### Y2013F

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| E | 417 | 31.28% |
| 0.0 | 45 | 3.38% |
| 0.01 | 17 | 1.28% |
| 0.02 | 10 | 0.75% |
| 0.05 | 7 | 0.53% |
| 0.09 | 5 | 0.38% |
| 0.07 | 5 | 0.38% |
| 0.03 | 5 | 0.38% |
| 0.13 | 4 | 0.30% |
| 0.12 | 4 | 0.30% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 1.29 | 1 | 0.08% |
| 14.05 | 1 | 0.08% |
| 1.56 | 1 | 0.08% |
| 7.32 | 1 | 0.08% |
| 180.36 | 1 | 0.08% |
| 20.04 | 1 | 0.08% |
| 48.03 | 1 | 0.08% |
| 5.34 | 1 | 0.08% |
| 2.3 | 1 | 0.08% |
| 2.96 | 1 | 0.08% |

#### Y2013N

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0 | 50 | 3.75% |
| 0.01 | 13 | 0.98% |
| 0.02 | 12 | 0.90% |
| 0.08 | 6 | 0.45% |
| 0.17 | 5 | 0.38% |
| 0.49 | 4 | 0.30% |
| 0.07 | 4 | 0.30% |
| 0.05 | 4 | 0.30% |
| 0.13 | 4 | 0.30% |
| 0.09 | 4 | 0.30% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 9.56 | 1 | 0.08% |
| 1.56 | 1 | 0.08% |
| 12.16 | 1 | 0.08% |
| 1.35 | 1 | 0.08% |
| 10.38 | 1 | 0.08% |
| 255.6 | 1 | 0.08% |
| 28.41 | 1 | 0.08% |
| 1.54 | 1 | 0.08% |
| 38.05 | 1 | 0.08% |
| 46.51 | 1 | 0.08% |

#### Y2014

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0 | 103 | 7.73% |
| 0.01 | 31 | 2.33% |
| 0.02 | 20 | 1.50% |
| 0.03 | 16 | 1.20% |
| 0.08 | 13 | 0.98% |
| 0.13 | 10 | 0.75% |
| 0.07 | 9 | 0.68% |
| 0.05 | 8 | 0.60% |
| 0.21 | 8 | 0.60% |
| 0.14 | 7 | 0.53% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 35.18 | 1 | 0.08% |
| 31.74 | 1 | 0.08% |
| 49.29 | 1 | 0.08% |
| 484 | 1 | 0.08% |
| 119.8 | 1 | 0.08% |
| 27.26 | 1 | 0.08% |
| 3.52 | 1 | 0.08% |
| 1.98 | 1 | 0.08% |
| 103 | 1 | 0.08% |
| 40.55 | 1 | 0.08% |

#### Y2014F

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| E | 421 | 31.58% |

#### Y2014N

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|

#### Y2015

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0 | 45 | 3.38% |
| 0.01 | 16 | 1.20% |
| 0.02 | 9 | 0.68% |
| 0.03 | 7 | 0.53% |
| 0.06 | 5 | 0.38% |
| 0.05 | 5 | 0.38% |
| 0.1 | 5 | 0.38% |
| 0.13 | 5 | 0.38% |
| 0.09 | 5 | 0.38% |
| 0.15 | 4 | 0.30% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 23.62 | 1 | 0.08% |
| 2.66 | 1 | 0.08% |
| 65.63 | 1 | 0.08% |
| 7.29 | 1 | 0.08% |
| 3.47 | 1 | 0.08% |
| 85.47 | 1 | 0.08% |
| 9.5 | 1 | 0.08% |
| 2.01 | 1 | 0.08% |
| 5.16 | 1 | 0.08% |
| 0.35 | 1 | 0.08% |

#### Y2015F

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| E | 420 | 31.51% |

#### Y2015N

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|

#### Y2016

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0 | 46 | 3.45% |
| 0.02 | 12 | 0.90% |
| 0.01 | 11 | 0.83% |
| 0.03 | 8 | 0.60% |
| 0.09 | 7 | 0.53% |
| 0.05 | 5 | 0.38% |
| 0.07 | 4 | 0.30% |
| 0.19 | 4 | 0.30% |
| 1.93 | 4 | 0.30% |
| 0.16 | 4 | 0.30% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 2.6 | 1 | 0.08% |
| 64.2 | 1 | 0.08% |
| 7.13 | 1 | 0.08% |
| 3.36 | 1 | 0.08% |
| 82.77 | 1 | 0.08% |
| 2.06 | 1 | 0.08% |
| 0.18 | 1 | 0.08% |
| 2.07 | 1 | 0.08% |
| 51.12 | 1 | 0.08% |
| 2.1 | 1 | 0.08% |

#### Y2016F

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| E | 420 | 31.51% |

#### Y2016N

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|

#### Y2017

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0 | 44 | 3.30% |
| 0.01 | 16 | 1.20% |
| 0.02 | 11 | 0.83% |
| 0.06 | 6 | 0.45% |
| 0.03 | 6 | 0.45% |
| 0.05 | 5 | 0.38% |
| 0.04 | 5 | 0.38% |
| 0.14 | 5 | 0.38% |
| 0.1 | 5 | 0.38% |
| 0.17 | 4 | 0.30% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 22.9 | 1 | 0.08% |
| 2.61 | 1 | 0.08% |
| 64.48 | 1 | 0.08% |
| 7.16 | 1 | 0.08% |
| 3.57 | 1 | 0.08% |
| 87.93 | 1 | 0.08% |
| 9.77 | 1 | 0.08% |
| 1.66 | 1 | 0.08% |
| 4.35 | 1 | 0.08% |
| 34.44 | 1 | 0.08% |

#### Y2017F

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| E | 420 | 31.51% |

#### Y2017N

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|

#### Y2018

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0 | 46 | 3.45% |
| 0.01 | 15 | 1.13% |
| 0.02 | 12 | 0.90% |
| 0.03 | 8 | 0.60% |
| 0.12 | 7 | 0.53% |
| 0.17 | 6 | 0.45% |
| 0.05 | 5 | 0.38% |
| 0.07 | 5 | 0.38% |
| 0.04 | 4 | 0.30% |
| 0.1 | 4 | 0.30% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 63.18 | 1 | 0.08% |
| 7.02 | 1 | 0.08% |
| 3.67 | 1 | 0.08% |
| 90.38 | 1 | 0.08% |
| 10.04 | 1 | 0.08% |
| 1.86 | 1 | 0.08% |
| 4.43 | 1 | 0.08% |
| 0.49 | 1 | 0.08% |
| 47.82 | 1 | 0.08% |
| 1.92 | 1 | 0.08% |

#### Y2018F

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| E | 420 | 31.51% |

#### Y2018N

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|

#### Y2019

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0 | 46 | 3.45% |
| 0.01 | 14 | 1.05% |
| 0.02 | 9 | 0.68% |
| 0.03 | 8 | 0.60% |
| 0.07 | 7 | 0.53% |
| 0.26 | 5 | 0.38% |
| 0.24 | 5 | 0.38% |
| 0.06 | 5 | 0.38% |
| 0.21 | 5 | 0.38% |
| 0.12 | 4 | 0.30% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 197.3 | 1 | 0.08% |
| 21.92 | 1 | 0.08% |
| 2.05 | 1 | 0.08% |
| 50.57 | 1 | 0.08% |
| 5.62 | 1 | 0.08% |
| 3.21 | 1 | 0.08% |
| 78.95 | 1 | 0.08% |
| 2.15 | 1 | 0.08% |
| 4.83 | 1 | 0.08% |
| 2.95 | 1 | 0.08% |

#### Y2019F

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| E | 421 | 31.58% |

#### Y2019N

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|

#### Y2020

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0 | 45 | 3.38% |
| 0.01 | 17 | 1.28% |
| 0.02 | 10 | 0.75% |
| 0.05 | 7 | 0.53% |
| 0.09 | 5 | 0.38% |
| 0.03 | 5 | 0.38% |
| 0.07 | 5 | 0.38% |
| 0.12 | 4 | 0.30% |
| 0.13 | 4 | 0.30% |
| 0.14 | 4 | 0.30% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 14.05 | 1 | 0.08% |
| 1.56 | 1 | 0.08% |
| 7.32 | 1 | 0.08% |
| 180.4 | 1 | 0.08% |
| 20.04 | 1 | 0.08% |
| 48.03 | 1 | 0.08% |
| 5.34 | 1 | 0.08% |
| 2.3 | 1 | 0.08% |
| 56.62 | 1 | 0.08% |
| 2.96 | 1 | 0.08% |

#### Y2020F

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| E | 421 | 31.58% |

#### Y2020N

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|

#### Y2021

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0 | 50 | 3.75% |
| 0.01 | 13 | 0.98% |
| 0.02 | 12 | 0.90% |
| 0.08 | 6 | 0.45% |
| 0.17 | 5 | 0.38% |
| 0.49 | 4 | 0.30% |
| 0.07 | 4 | 0.30% |
| 0.05 | 4 | 0.30% |
| 0.13 | 4 | 0.30% |
| 0.09 | 4 | 0.30% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 9.56 | 1 | 0.08% |
| 1.56 | 1 | 0.08% |
| 12.16 | 1 | 0.08% |
| 1.35 | 1 | 0.08% |
| 10.38 | 1 | 0.08% |
| 255.6 | 1 | 0.08% |
| 28.41 | 1 | 0.08% |
| 1.54 | 1 | 0.08% |
| 38.05 | 1 | 0.08% |
| 46.51 | 1 | 0.08% |

#### Y2021F

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| E | 420 | 31.51% |

#### Y2021N

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|

#### Y2022

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0 | 60 | 4.50% |
| 0.01 | 16 | 1.20% |
| 0.02 | 10 | 0.75% |
| 0.08 | 8 | 0.60% |
| 0.13 | 7 | 0.53% |
| 0.03 | 6 | 0.45% |
| 0.05 | 5 | 0.38% |
| 2.47 | 5 | 0.38% |
| 0.24 | 4 | 0.30% |
| 0.22 | 4 | 0.30% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 1.23 | 1 | 0.08% |
| 0.57 | 1 | 0.08% |
| 14.1 | 1 | 0.08% |
| 11.35 | 1 | 0.08% |
| 279.4 | 1 | 0.08% |
| 31.05 | 1 | 0.08% |
| 1.93 | 1 | 0.08% |
| 47.51 | 1 | 0.08% |
| 5.28 | 1 | 0.08% |
| 40.55 | 1 | 0.08% |

#### Y2022F

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| E | 428 | 32.11% |

#### Y2022N

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|

### Sample Data

First 10 Rows:
|    |   area_code | Area Code (M49)   | area      |   item_code | Item Code (FBS)   | item                     |   element_code | element                                | Unit       |   Y2010 | Y2010F   |   Y2010N |   Y2011 | Y2011F   |   Y2011N |   Y2012 | Y2012F   |   Y2012N |   Y2013 | Y2013F   |   Y2013N |   Y2014 | Y2014F   |   Y2014N |   Y2015 | Y2015F   |   Y2015N |   Y2016 | Y2016F   |   Y2016N |   Y2017 | Y2017F   |   Y2017N |   Y2018 | Y2018F   |   Y2018N |   Y2019 | Y2019F   |   Y2019N |   Y2020 | Y2020F   |   Y2020N |   Y2021 | Y2021F   |   Y2021N |   Y2022 | Y2022F   |   Y2022N |
|---:|------------:|:------------------|:----------|------------:|:------------------|:-------------------------|---------------:|:---------------------------------------|:-----------|--------:|:---------|---------:|--------:|:---------|---------:|--------:|:---------|---------:|--------:|:---------|---------:|--------:|:---------|---------:|--------:|:---------|---------:|--------:|:---------|---------:|--------:|:---------|---------:|--------:|:---------|---------:|--------:|:---------|---------:|--------:|:---------|---------:|--------:|:---------|---------:|--------:|:---------|---------:|
|  0 |          10 | '036              | Australia |        2901 | 'S2901            | Grand Total              |            664 | Food supply (kcal/capita/day)          | kcal/cap/d | 3534    | E        |      nan | 3516    | E        |      nan | 3564    | E        |      nan | 3546    | E        |      nan | 3533    | E        |      nan | 3519    | E        |      nan | 3537    | E        |      nan | 3493    | E        |      nan | 3470    | E        |      nan | 3503    | E        |      nan | 3478    | E        |      nan | 3479    | E        |      nan | 3471    | E        |      nan |
|  1 |          10 | '036              | Australia |        2901 | 'S2901            | Grand Total              |            674 | Protein supply quantity (g/capita/day) | g/cap/d    |  123.51 | E        |      nan |  122.43 | E        |      nan |  121.93 | E        |      nan |  121.39 | E        |      nan |  119.79 | E        |      nan |  120.24 | E        |      nan |  121.17 | E        |      nan |  118.1  | E        |      nan |  118.92 | E        |      nan |  122.23 | E        |      nan |  124.23 | E        |      nan |  118    | E        |      nan |  116.5  | E        |      nan |
|  2 |          10 | '036              | Australia |        2901 | 'S2901            | Grand Total              |            684 | Fat supply quantity (g/capita/day)     | g/cap/d    |  153.9  | E        |      nan |  158.31 | E        |      nan |  159.65 | E        |      nan |  155.66 | E        |      nan |  161.06 | E        |      nan |  162.06 | E        |      nan |  162.83 | E        |      nan |  159.66 | E        |      nan |  160.4  | E        |      nan |  160.7  | E        |      nan |  155.85 | E        |      nan |  157.39 | E        |      nan |  159.57 | E        |      nan |
|  3 |          10 | '036              | Australia |        2903 | 'S2903            | Vegetal Products         |            664 | Food supply (kcal/capita/day)          | kcal/cap/d | 2443    | E        |      nan | 2411    | E        |      nan | 2453    | E        |      nan | 2451    | E        |      nan | 2427    | E        |      nan | 2380    | E        |      nan | 2395    | E        |      nan | 2381    | E        |      nan | 2342    | E        |      nan | 2385    | E        |      nan | 2355    | E        |      nan | 2420    | E        |      nan | 2469    | E        |      nan |
|  4 |          10 | '036              | Australia |        2903 | 'S2903            | Vegetal Products         |            674 | Protein supply quantity (g/capita/day) | g/cap/d    |   39.4  | E        |      nan |   36.37 | E        |      nan |   36.89 | E        |      nan |   37.59 | E        |      nan |   36.33 | E        |      nan |   36.03 | E        |      nan |   36.11 | E        |      nan |   36.32 | E        |      nan |   36.36 | E        |      nan |   40.23 | E        |      nan |   40.38 | E        |      nan |   40.4  | E        |      nan |   39.96 | E        |      nan |
|  5 |          10 | '036              | Australia |        2903 | 'S2903            | Vegetal Products         |            684 | Fat supply quantity (g/capita/day)     | g/cap/d    |   80.04 | E        |      nan |   83.77 | E        |      nan |   84.52 | E        |      nan |   81.24 | E        |      nan |   85    | E        |      nan |   83.11 | E        |      nan |   83.67 | E        |      nan |   82.49 | E        |      nan |   82.17 | E        |      nan |   83.43 | E        |      nan |   78.26 | E        |      nan |   83.96 | E        |      nan |   89.29 | E        |      nan |
|  6 |          10 | '036              | Australia |        2941 | 'S2941            | Animal Products          |            664 | Food supply (kcal/capita/day)          | kcal/cap/d | 1091    | E        |      nan | 1105    | E        |      nan | 1111    | E        |      nan | 1094    | E        |      nan | 1107    | E        |      nan | 1139    | E        |      nan | 1142    | E        |      nan | 1112    | E        |      nan | 1127    | E        |      nan | 1118    | E        |      nan | 1124    | E        |      nan | 1058    | E        |      nan | 1001    | E        |      nan |
|  7 |          10 | '036              | Australia |        2941 | 'S2941            | Animal Products          |            674 | Protein supply quantity (g/capita/day) | g/cap/d    |   84.11 | E        |      nan |   86.06 | E        |      nan |   85.03 | E        |      nan |   83.8  | E        |      nan |   83.45 | E        |      nan |   84.21 | E        |      nan |   85.07 | E        |      nan |   81.78 | E        |      nan |   82.57 | E        |      nan |   82    | E        |      nan |   83.85 | E        |      nan |   77.61 | E        |      nan |   76.54 | E        |      nan |
|  8 |          10 | '036              | Australia |        2941 | 'S2941            | Animal Products          |            684 | Fat supply quantity (g/capita/day)     | g/cap/d    |   73.86 | E        |      nan |   74.54 | E        |      nan |   75.13 | E        |      nan |   74.43 | E        |      nan |   76.06 | E        |      nan |   78.95 | E        |      nan |   79.16 | E        |      nan |   77.17 | E        |      nan |   78.24 | E        |      nan |   77.28 | E        |      nan |   77.59 | E        |      nan |   73.42 | E        |      nan |   70.28 | E        |      nan |
|  9 |          10 | '036              | Australia |        2905 | 'S2905            | Cereals - Excluding Beer |            645 | Food supply quantity (kg/capita/yr)    | kg/cap     |  100.86 | E        |      nan |  105.3  | E        |      nan |  102.97 | E        |      nan |  110.66 | E        |      nan |  109.24 | E        |      nan |  108.96 | E        |      nan |  110.35 | E        |      nan |  109.38 | E        |      nan |  108.24 | E        |      nan |  110.42 | E        |      nan |  110.81 | E        |      nan |  108.15 | E        |      nan |  105.93 | E        |      nan |

Last 10 Rows:
|      | area_code   | Area Code (M49)                         | area     |   item_code |   Item Code (FBS) |   item |   element_code |   element |   Unit |   Y2010 |   Y2010F |   Y2010N |   Y2011 |   Y2011F |   Y2011N |   Y2012 |   Y2012F |   Y2012N |   Y2013 |   Y2013F |   Y2013N |   Y2014 |   Y2014F |   Y2014N |   Y2015 |   Y2015F |   Y2015N |   Y2016 |   Y2016F |   Y2016N |   Y2017 |   Y2017F |   Y2017N |   Y2018 |   Y2018F |   Y2018N |   Y2019 |   Y2019F |   Y2019N |   Y2020 |   Y2020F |   Y2020N |   Y2021 |   Y2021F |   Y2021N |   Y2022 |   Y2022F |   Y2022N |
|-----:|:------------|:----------------------------------------|:---------|------------:|------------------:|-------:|---------------:|----------:|-------:|--------:|---------:|---------:|--------:|---------:|---------:|--------:|---------:|---------:|--------:|---------:|---------:|--------:|---------:|---------:|--------:|---------:|---------:|--------:|---------:|---------:|--------:|---------:|---------:|--------:|---------:|---------:|--------:|---------:|---------:|--------:|---------:|---------:|--------:|---------:|---------:|--------:|---------:|---------:|
| 1323 | 249         | '887                                    | Yemen    |         nan |               nan |    nan |            nan |       nan |    nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |
| 1324 | 249         | '887                                    | Yemen    |         nan |               nan |    nan |            nan |       nan |    nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |
| 1325 | 251         | '894                                    | Zambia   |         nan |               nan |    nan |            nan |       nan |    nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |
| 1326 | 251         | '894                                    | Zambia   |         nan |               nan |    nan |            nan |       nan |    nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |
| 1327 | 181         | '716                                    | Zimbabwe |         nan |               nan |    nan |            nan |       nan |    nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |
| 1328 | 181         | '716                                    | Zimbabwe |         nan |               nan |    nan |            nan |       nan |    nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |
| 1329 | A           | Official figure                         | nan      |         nan |               nan |    nan |            nan |       nan |    nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |
| 1330 | E           | Estimated value                         | nan      |         nan |               nan |    nan |            nan |       nan |    nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |
| 1331 | I           | Imputed value                           | nan      |         nan |               nan |    nan |            nan |       nan |    nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |
| 1332 | X           | Figure from international organizations | nan      |         nan |               nan |    nan |            nan |       nan |    nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |     nan |      nan |      nan |

---

## faostat_fbs_australia_clean.csv

### Dataset Overview
- Total Rows: 16,353
- Total Columns: 10
- Memory Usage: 6.68 MB
- Missing Values: 9,231
- Duplicate Rows: 390

### Column Information
| Column | Type | Non-Null | Unique | Memory (MB) | Additional Statistics |
|--------|------|-----------|---------|-------------|---------------------|
| area_code | int64 | 16,353 | 1 | 0.12 | Mean: 10, Std: 0, Min: 10, Max: 10, Median: 10 |
| area | object | 16,353 | 1 | 1.03 | Min Length: 9, Max Length: 9, Avg Length: 9 |
| item_code | float64 | 16,353 | 108 | 0.12 | Mean: 2693, Std: 143, Min: 2511, Max: 2960, Median: 2640 |
| item | object | 16,353 | 105 | 1.11 | Min Length: 4, Max Length: 31, Avg Length: 14.05 |
| element_code | float64 | 16,353 | 4 | 0.12 | Mean: 666.9, Std: 14.33, Min: 645, Max: 684, Median: 674 |
| element | object | 16,353 | 4 | 1.42 | Min Length: 29, Max Length: 38, Avg Length: 33.99 |
| unit | object | 16,353 | 3 | 1.01 | Min Length: 6, Max Length: 10, Avg Length: 7.512 |
| year | object | 16,353 | 1,929 | 0.94 | Min Length: 1, Max Length: 6, Avg Length: 3.074 |
| value | int64 | 16,353 | 13 | 0.12 | Mean: 2015, Std: 3.744, Min: 2010, Max: 2022, Median: 2013 |
| flag | object | 7,122 | 820 | 0.68 | N/A |

### Column Value Distributions

#### area_code

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 10 | 16,353 | 100.00% |

#### area

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| Australia | 16,353 | 100.00% |

#### item_code

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 2611 | 156 | 0.95% |
| 2732 | 156 | 0.95% |
| 2943 | 156 | 0.95% |
| 2658 | 156 | 0.95% |
| 2657 | 156 | 0.95% |
| 2656 | 156 | 0.95% |
| 2655 | 156 | 0.95% |
| 2924 | 156 | 0.95% |
| 2645 | 156 | 0.95% |
| 2642 | 156 | 0.95% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 2560 | 156 | 0.95% |
| 2513 | 156 | 0.95% |
| 2558 | 138 | 0.84% |
| 2535 | 132 | 0.81% |
| 2941 | 117 | 0.72% |
| 2903 | 117 | 0.72% |
| 2901 | 117 | 0.72% |
| 2570 | 108 | 0.66% |
| 2908 | 12 | 0.07% |
| 2537 | 12 | 0.07% |

#### item

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| Eggs | 312 | 1.91% |
| Miscellaneous | 312 | 1.91% |
| Milk - Excluding Butter | 312 | 1.91% |
| Stimulants | 156 | 0.95% |
| Wine | 156 | 0.95% |
| Alcoholic Beverages | 156 | 0.95% |
| Spices, Other | 156 | 0.95% |
| Cloves | 156 | 0.95% |
| Pimento | 156 | 0.95% |
| Pepper | 156 | 0.95% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| Groundnuts | 156 | 0.95% |
| Barley and products | 156 | 0.95% |
| Rape and Mustardseed | 138 | 0.84% |
| Yams | 132 | 0.81% |
| Animal Products | 117 | 0.72% |
| Vegetal Products | 117 | 0.72% |
| Grand Total | 117 | 0.72% |
| Oilcrops, Other | 108 | 0.66% |
| Sugar Crops | 12 | 0.07% |
| Sugar beet | 12 | 0.07% |

#### element_code

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 664 | 4,122 | 25.21% |
| 674 | 4,122 | 25.21% |
| 684 | 4,122 | 25.21% |
| 645 | 3,987 | 24.38% |

#### element

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| Food supply (kcal/capita/day) | 4,122 | 25.21% |
| Protein supply quantity (g/capita/day) | 4,122 | 25.21% |
| Fat supply quantity (g/capita/day) | 4,122 | 25.21% |
| Food supply quantity (kg/capita/yr) | 3,987 | 24.38% |

#### unit

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| g/cap/d | 8,244 | 50.41% |
| kcal/cap/d | 4,122 | 25.21% |
| kg/cap | 3,987 | 24.38% |

#### year

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| E | 5,451 | 33.33% |
| 0.0 | 1,208 | 7.39% |
| 0.01 | 390 | 2.38% |
| 0.02 | 262 | 1.60% |
| 0.03 | 194 | 1.19% |
| 0.05 | 108 | 0.66% |
| 0.08 | 104 | 0.64% |
| 0.13 | 100 | 0.61% |
| 0.04 | 100 | 0.61% |
| 0.07 | 100 | 0.61% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 14.29 | 2 | 0.01% |
| 10.38 | 2 | 0.01% |
| 8.01 | 2 | 0.01% |
| 8.37 | 2 | 0.01% |
| 8.63 | 2 | 0.01% |
| 8.92 | 2 | 0.01% |
| 1.5 | 2 | 0.01% |
| 14.1 | 2 | 0.01% |
| 12.16 | 2 | 0.01% |
| 40.55 | 2 | 0.01% |

#### value

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 2013 | 2,096 | 12.82% |
| 2012 | 2,094 | 12.80% |
| 2011 | 2,084 | 12.74% |
| 2010 | 2,069 | 12.65% |
| 2014 | 1,270 | 7.77% |
| 2022 | 856 | 5.23% |
| 2019 | 842 | 5.15% |
| 2020 | 842 | 5.15% |
| 2015 | 840 | 5.14% |
| 2016 | 840 | 5.14% |
| 2017 | 840 | 5.14% |
| 2018 | 840 | 5.14% |
| 2021 | 840 | 5.14% |

#### flag

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| E | 5,451 | 33.33% |
| 0.0 | 174 | 1.06% |
| 0.01 | 61 | 0.37% |
| 0.02 | 40 | 0.24% |
| 0.03 | 30 | 0.18% |
| 0.07 | 19 | 0.12% |
| 0.06 | 17 | 0.10% |
| 0.14 | 17 | 0.10% |
| 0.1 | 15 | 0.09% |
| 0.13 | 15 | 0.09% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 22.9 | 1 | 0.01% |
| 6.98 | 1 | 0.01% |
| 20.04 | 1 | 0.01% |
| 2.71 | 1 | 0.01% |
| 2.61 | 1 | 0.01% |
| 62.85 | 1 | 0.01% |
| 66.82 | 1 | 0.01% |
| 64.48 | 1 | 0.01% |
| 48.03 | 1 | 0.01% |
| 2.96 | 1 | 0.01% |

### Sample Data

First 10 Rows:
|    |   area_code | area      |   item_code | item        |   element_code | element                       | unit       | year   |   value | flag   |
|---:|------------:|:----------|------------:|:------------|---------------:|:------------------------------|:-----------|:-------|--------:|:-------|
|  0 |          10 | Australia |        2901 | Grand Total |            664 | Food supply (kcal/capita/day) | kcal/cap/d | 3534.0 |    2010 | E      |
|  1 |          10 | Australia |        2901 | Grand Total |            664 | Food supply (kcal/capita/day) | kcal/cap/d | E      |    2010 | nan    |
|  2 |          10 | Australia |        2901 | Grand Total |            664 | Food supply (kcal/capita/day) | kcal/cap/d | 3516.0 |    2011 | E      |
|  3 |          10 | Australia |        2901 | Grand Total |            664 | Food supply (kcal/capita/day) | kcal/cap/d | E      |    2011 | nan    |
|  4 |          10 | Australia |        2901 | Grand Total |            664 | Food supply (kcal/capita/day) | kcal/cap/d | 3564.0 |    2012 | E      |
|  5 |          10 | Australia |        2901 | Grand Total |            664 | Food supply (kcal/capita/day) | kcal/cap/d | E      |    2012 | nan    |
|  6 |          10 | Australia |        2901 | Grand Total |            664 | Food supply (kcal/capita/day) | kcal/cap/d | 3546.0 |    2013 | E      |
|  7 |          10 | Australia |        2901 | Grand Total |            664 | Food supply (kcal/capita/day) | kcal/cap/d | E      |    2013 | nan    |
|  8 |          10 | Australia |        2901 | Grand Total |            664 | Food supply (kcal/capita/day) | kcal/cap/d | 3533.0 |    2014 | E      |
|  9 |          10 | Australia |        2901 | Grand Total |            664 | Food supply (kcal/capita/day) | kcal/cap/d | E      |    2014 | nan    |

Last 10 Rows:
|       |   area_code | area      |   item_code | item          |   element_code | element                            | unit    |   year |   value |   flag |
|------:|------------:|:----------|------------:|:--------------|---------------:|:-----------------------------------|:--------|-------:|--------:|-------:|
| 16343 |          10 | Australia |        2899 | Miscellaneous |            684 | Fat supply quantity (g/capita/day) | g/cap/d |   0.35 |    2011 |   0.35 |
| 16344 |          10 | Australia |        2899 | Miscellaneous |            684 | Fat supply quantity (g/capita/day) | g/cap/d |   0.35 |    2011 | nan    |
| 16345 |          10 | Australia |        2899 | Miscellaneous |            684 | Fat supply quantity (g/capita/day) | g/cap/d |   0.35 |    2011 | nan    |
| 16346 |          10 | Australia |        2899 | Miscellaneous |            684 | Fat supply quantity (g/capita/day) | g/cap/d |   0.35 |    2012 |   0.34 |
| 16347 |          10 | Australia |        2899 | Miscellaneous |            684 | Fat supply quantity (g/capita/day) | g/cap/d |   0.34 |    2012 | nan    |
| 16348 |          10 | Australia |        2899 | Miscellaneous |            684 | Fat supply quantity (g/capita/day) | g/cap/d |   0.32 |    2012 | nan    |
| 16349 |          10 | Australia |        2899 | Miscellaneous |            684 | Fat supply quantity (g/capita/day) | g/cap/d |   0.48 |    2013 |   0.49 |
| 16350 |          10 | Australia |        2899 | Miscellaneous |            684 | Fat supply quantity (g/capita/day) | g/cap/d |   0.49 |    2013 | nan    |
| 16351 |          10 | Australia |        2899 | Miscellaneous |            684 | Fat supply quantity (g/capita/day) | g/cap/d |   0.47 |    2013 | nan    |
| 16352 |          10 | Australia |        2899 | Miscellaneous |            684 | Fat supply quantity (g/capita/day) | g/cap/d |   0.41 |    2014 | nan    |

---

## fire_in_a_bottle_la_content.csv

### Dataset Overview
- Total Rows: 2,500
- Total Columns: 4
- Memory Usage: 0.30 MB
- Missing Values: 11
- Duplicate Rows: 0

### Column Information
| Column | Type | Non-Null | Unique | Memory (MB) | Additional Statistics |
|--------|------|-----------|---------|-------------|---------------------|
| food_name | object | 2,500 | 2,492 | 0.24 | Min Length: 3, Max Length: 80, Avg Length: 45.17 |
| la_cal | float64 | 2,500 | 1,322 | 0.02 | Mean: 19.46, Std: 46.61, Min: 0, Max: 591.3, Median: 3.447 |
| cal | float64 | 2,500 | 581 | 0.02 | Mean: 226.9, Std: 178.6, Min: 0, Max: 902, Median: 194 |
| percent | float64 | 2,489 | 276 | 0.02 | Mean: 5.585, Std: 8.207, Min: 0, Max: 66.9, Median: 1.9 |

### Column Value Distributions

#### food_name

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| Bagels, plain, enriched, with calcium propionate (includes onion, poppy, sesame) | 2 | 0.08% |
| Beef, round, top round roast, boneless, separable lean only, trimmed to 0" fat, | 2 | 0.08% |
| Beef, round, top round steak, boneless, separable lean and fat, trimmed to 0" fa | 2 | 0.08% |
| Beef, round, eye of round steak, boneless, separable lean and fat, trimmed to 0" | 2 | 0.08% |
| Beef, top sirloin, steak, separable lean only, trimmed to 1/8" fat, all grades, | 2 | 0.08% |
| Pork, cured, ham with natural juices, spiral slice, boneless, separable lean and | 2 | 0.08% |
| Beef, round, top round roast, boneless, separable lean and fat, trimmed to 0" fa | 2 | 0.08% |
| Beef, round, top round steak, boneless, separable lean only, trimmed to 0" fat, | 2 | 0.08% |
| Cheese, romano | 1 | 0.04% |
| Beef, cured, pastrami | 1 | 0.04% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| Tortillas, ready-to-bake or -fry, flour, refrigerated | 1 | 0.04% |
| Bread, oat bran, toasted | 1 | 0.04% |
| Snacks, KRAFT, CORNNUTS, plain | 1 | 0.04% |
| Bread, oat bran | 1 | 0.04% |
| Bread, rice bran, toasted | 1 | 0.04% |
| Pork, fresh, shoulder, (Boston butt), blade (steaks), separable lean and fat, co | 1 | 0.04% |
| Bread, rice bran | 1 | 0.04% |
| Peppers, serrano, raw | 1 | 0.04% |
| Chicken, broiler, rotisserie, BBQ, drumstick meat and skin | 1 | 0.04% |
| English muffins, plain, toasted, enriched, with calcium propionate (includes sou | 1 | 0.04% |

#### la_cal

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0 | 175 | 7.00% |
| 0.171 | 20 | 0.80% |
| 0.18 | 17 | 0.68% |
| 0.135 | 17 | 0.68% |
| 0.45 | 16 | 0.64% |
| 0.153 | 15 | 0.60% |
| 0.207 | 15 | 0.60% |
| 0.288 | 13 | 0.52% |
| 0.414 | 13 | 0.52% |
| 0.216 | 12 | 0.48% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 27.19 | 1 | 0.04% |
| 36.21 | 1 | 0.04% |
| 17.59 | 1 | 0.04% |
| 5.85 | 1 | 0.04% |
| 33.65 | 1 | 0.04% |
| 38.92 | 1 | 0.04% |
| 32.94 | 1 | 0.04% |
| 51.57 | 1 | 0.04% |
| 19.91 | 1 | 0.04% |
| 7.488 | 1 | 0.04% |

#### cal

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 66 | 27 | 1.08% |
| 884 | 24 | 0.96% |
| 65 | 18 | 0.72% |
| 63 | 17 | 0.68% |
| 68 | 16 | 0.64% |
| 51 | 16 | 0.64% |
| 28 | 15 | 0.60% |
| 46 | 14 | 0.56% |
| 53 | 13 | 0.52% |
| 60 | 13 | 0.52% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 483 | 1 | 0.04% |
| 145 | 1 | 0.04% |
| 441 | 1 | 0.04% |
| 407 | 1 | 0.04% |
| 10 | 1 | 0.04% |
| 567 | 1 | 0.04% |
| 400 | 1 | 0.04% |
| 537 | 1 | 0.04% |
| 516 | 1 | 0.04% |
| 168 | 1 | 0.04% |

#### percent

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0 | 184 | 7.36% |
| 0.3 | 80 | 3.20% |
| 0.5 | 79 | 3.16% |
| 0.4 | 75 | 3.00% |
| 0.2 | 73 | 2.92% |
| 0.6 | 68 | 2.72% |
| 0.1 | 66 | 2.64% |
| 1 | 61 | 2.44% |
| 1.1 | 61 | 2.44% |
| 1.3 | 60 | 2.40% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 22.8 | 1 | 0.04% |
| 22.4 | 1 | 0.04% |
| 22.3 | 1 | 0.04% |
| 22.1 | 1 | 0.04% |
| 22 | 1 | 0.04% |
| 21.9 | 1 | 0.04% |
| 21.7 | 1 | 0.04% |
| 21.5 | 1 | 0.04% |
| 21.4 | 1 | 0.04% |
| 16.2 | 1 | 0.04% |

### Sample Data

First 10 Rows:
|    | food_name                                                      |   la_cal |   cal |   percent |
|---:|:---------------------------------------------------------------|---------:|------:|----------:|
|  0 | Oil, sunflower, linoleic, (approx. 65%)                        |  591.3   |   884 |      66.9 |
|  1 | Oil, wheat germ                                                |  493.2   |   884 |      55.8 |
|  2 | Oil, walnut                                                    |  476.1   |   884 |      53.9 |
|  3 | Oil, corn, industrial and retail, all purpose salad or cooking |  481.635 |   900 |      53.5 |
|  4 | Oil, cottonseed, salad or cooking                              |  463.5   |   884 |      52.4 |
|  5 | Nuts, walnuts, english                                         |  342.837 |   654 |      52.4 |
|  6 | Seeds, sunflower seed kernels, oil roasted, without salt       |  307.872 |   592 |      52   |
|  7 | Oil, soybean, salad or cooking                                 |  458.568 |   884 |      51.9 |
|  8 | Salad dressing, mayonnaise, regular                            |  352.314 |   680 |      51.8 |
|  9 | Seeds, sunflower seed kernels, dry roasted, without salt       |  295.038 |   582 |      50.7 |

Last 10 Rows:
|      | food_name                                                                        |   la_cal |   cal |   percent |
|-----:|:---------------------------------------------------------------------------------|---------:|------:|----------:|
| 2490 | Pork, cured, ham, extra lean (approximately 4% fat), canned, unheated            |    3.24  |   120 |       2.7 |
| 2491 | Protein supplement, milk based, Muscle Milk Light, powder                        |   10.764 |   396 |       2.7 |
| 2492 | Turnover, chicken- or turkey-, and vegetable-filled, reduced fat, frozen         |    4.608 |   168 |       2.7 |
| 2493 | Turkey, drumstick, from whole bird, meat only, roasted                           |    3.879 |   139 |       2.8 |
| 2494 | Pork, fresh, loin, center rib (chops), boneless, separable lean only, cooked, br |    5.94  |   211 |       2.8 |
| 2495 | Game meat, boar, wild, cooked, roasted                                           |    4.5   |   160 |       2.8 |
| 2496 | Snacks, granola bar, KASHI GOLEAN, crunchy, mixed flavors                        |   10.998 |   393 |       2.8 |
| 2497 | Tortillas, ready-to-bake or -fry, whole wheat                                    |    8.631 |   310 |       2.8 |
| 2498 | Lemon juice, frozen, unsweetened, single strength                                |    0.612 |    22 |       2.8 |
| 2499 | English muffins, plain, toasted, enriched, with calcium propionate (includes sou |    7.488 |   270 |       2.8 |

---

## ncd_risc_bmi_adult.csv

### Dataset Overview
- Total Rows: 66
- Total Columns: 35
- Memory Usage: 0.03 MB
- Missing Values: 0
- Duplicate Rows: 0

### Column Information
| Column | Type | Non-Null | Unique | Memory (MB) | Additional Statistics |
|--------|------|-----------|---------|-------------|---------------------|
| year | int64 | 66 | 33 | 0.00 | Mean: 2006, Std: 9.595, Min: 1990, Max: 2022, Median: 2006 |
| sex | object | 66 | 2 | 0.00 | Min Length: 3, Max Length: 5, Avg Length: 4 |
| country_region_world | object | 66 | 1 | 0.00 | Min Length: 9, Max Length: 9, Avg Length: 9 |
| iso | object | 66 | 1 | 0.00 | Min Length: 3, Max Length: 3, Avg Length: 3 |
| prevalence_of_bmi<18.5_kg_m²_underweight_ | float64 | 66 | 66 | 0.00 | Mean: 0.01568, Std: 0.00722, Min: 0.008296, Max: 0.03287, Median: 0.01555 |
| prevalence_of_bmi<18.5_kg_m²_underweight_lower_95%_uncertainty_interval | float64 | 66 | 66 | 0.00 | Mean: 0.01202, Std: 0.006119, Min: 0.006144, Max: 0.02657, Median: 0.00987 |
| prevalence_of_bmi<18.5_kg_m²_underweight_upper_95%_uncertainty_interval | float64 | 66 | 66 | 0.00 | Mean: 0.01999, Std: 0.008419, Min: 0.01081, Max: 0.03982, Median: 0.02121 |
| prevalence_of_bmi>=30_kg_m²_obesity_ | float64 | 66 | 66 | 0.00 | Mean: 0.2293, Std: 0.05331, Min: 0.129, Max: 0.3205, Median: 0.2372 |
| prevalence_of_bmi>=30_kg_m²_obesity_lower_95%_uncertainty_interval | float64 | 66 | 66 | 0.00 | Mean: 0.2113, Std: 0.04896, Min: 0.1162, Max: 0.2777, Median: 0.2214 |
| prevalence_of_bmi>=30_kg_m²_obesity_upper_95%_uncertainty_interval | float64 | 66 | 66 | 0.00 | Mean: 0.2483, Std: 0.05853, Min: 0.1423, Max: 0.3667, Median: 0.2535 |
| combined_prevalence_of_bmi<18.5_kg_m²_and_bmi>=30_kg_m²_double_burden_of_underweight_and_obesity_ | float64 | 66 | 66 | 0.00 | Mean: 0.245, Std: 0.05225, Min: 0.1386, Max: 0.3319, Median: 0.2521 |
| combined_prevalence_of_bmi<18.5_kg_m²_and_bmi>=30_kg_m²_double_burden_of_underweight_and_obesity_lower_95%_uncertainty_interval | float64 | 66 | 66 | 0.00 | Mean: 0.2267, Std: 0.04805, Min: 0.1253, Max: 0.2888, Median: 0.2362 |
| combined_prevalence_of_bmi<18.5_kg_m²_and_bmi>=30_kg_m²_double_burden_of_underweight_and_obesity_upper_95%_uncertainty_interval | float64 | 66 | 66 | 0.00 | Mean: 0.2642, Std: 0.05727, Min: 0.1522, Max: 0.3775, Median: 0.2685 |
| proportion_of_double_burden_from_obesity | float64 | 66 | 66 | 0.00 | Mean: 0.919, Std: 0.04362, Min: 0.7759, Max: 0.9605, Median: 0.9251 |
| proportion_of_double_burden_from_obesity_lower_95%_uncertainty_interval | float64 | 66 | 66 | 0.00 | Mean: 0.8993, Std: 0.04888, Min: 0.7391, Max: 0.9492, Median: 0.9041 |
| proportion_of_double_burden_from_obesity_upper_95%_uncertainty_interval | float64 | 66 | 66 | 0.00 | Mean: 0.9365, Std: 0.03814, Min: 0.8111, Max: 0.9758, Median: 0.9452 |
| prevalence_of_bmi_18.5_kg_m²_to_<20_kg_m² | float64 | 66 | 66 | 0.00 | Mean: 0.04253, Std: 0.02146, Min: 0.01718, Max: 0.085, Median: 0.04193 |
| prevalence_of_bmi_18.5_kg_m²_to_<20_kg_m²_lower_95%_uncertainty_interval | float64 | 66 | 66 | 0.00 | Mean: 0.03684, Std: 0.01945, Min: 0.01204, Max: 0.07552, Median: 0.03323 |
| prevalence_of_bmi_18.5_kg_m²_to_<20_kg_m²_upper_95%_uncertainty_interval | float64 | 66 | 66 | 0.00 | Mean: 0.04878, Std: 0.0236, Min: 0.02148, Max: 0.09466, Median: 0.04985 |
| prevalence_of_bmi_20_kg_m²_to_<25_kg_m² | float64 | 66 | 66 | 0.00 | Mean: 0.3544, Std: 0.06457, Min: 0.2525, Max: 0.4935, Median: 0.3571 |
| prevalence_of_bmi_20_kg_m²_to_<25_kg_m²_lower_95%_uncertainty_interval | float64 | 66 | 66 | 0.00 | Mean: 0.3348, Std: 0.06579, Min: 0.2148, Max: 0.4751, Median: 0.3371 |
| prevalence_of_bmi_20_kg_m²_to_<25_kg_m²_upper_95%_uncertainty_interval | float64 | 66 | 66 | 0.00 | Mean: 0.3741, Std: 0.06343, Min: 0.2871, Max: 0.5116, Median: 0.3781 |
| prevalence_of_bmi_25_kg_m²_to_<30_kg_m² | float64 | 66 | 66 | 0.00 | Mean: 0.3581, Std: 0.07372, Min: 0.2547, Max: 0.4454, Median: 0.346 |
| prevalence_of_bmi_25_kg_m²_to_<30_kg_m²_lower_95%_uncertainty_interval | float64 | 66 | 66 | 0.00 | Mean: 0.3382, Std: 0.07298, Min: 0.2383, Max: 0.4259, Median: 0.3164 |
| prevalence_of_bmi_25_kg_m²_to_<30_kg_m²_upper_95%_uncertainty_interval | float64 | 66 | 66 | 0.00 | Mean: 0.3783, Std: 0.07465, Min: 0.2716, Max: 0.4649, Median: 0.3819 |
| prevalence_of_bmi_30_kg_m²_to_<35_kg_m² | float64 | 66 | 66 | 0.00 | Mean: 0.1539, Std: 0.03208, Min: 0.09122, Max: 0.2168, Median: 0.1537 |
| prevalence_of_bmi_30_kg_m²_to_<35_kg_m²_lower_95%_uncertainty_interval | float64 | 66 | 66 | 0.00 | Mean: 0.1378, Std: 0.02854, Min: 0.0804, Max: 0.1828, Median: 0.1406 |
| prevalence_of_bmi_30_kg_m²_to_<35_kg_m²_upper_95%_uncertainty_interval | float64 | 66 | 66 | 0.00 | Mean: 0.1706, Std: 0.03648, Min: 0.1029, Max: 0.2579, Median: 0.1679 |
| prevalence_of_bmi_35_kg_m²_to_<40_kg_m² | float64 | 66 | 66 | 0.00 | Mean: 0.05157, Std: 0.01616, Min: 0.01723, Max: 0.07435, Median: 0.05483 |
| prevalence_of_bmi_35_kg_m²_to_<40_kg_m²_lower_95%_uncertainty_interval | float64 | 66 | 66 | 0.00 | Mean: 0.04277, Std: 0.01324, Min: 0.01351, Max: 0.05844, Median: 0.04692 |
| prevalence_of_bmi_35_kg_m²_to_<40_kg_m²_upper_95%_uncertainty_interval | float64 | 66 | 66 | 0.00 | Mean: 0.06137, Std: 0.02002, Min: 0.02144, Max: 0.103, Median: 0.06369 |
| prevalence_of_bmi_>=40_kg_m²_morbid_obesity_ | float64 | 66 | 66 | 0.00 | Mean: 0.02387, Std: 0.0134, Min: 0.003277, Max: 0.05087, Median: 0.02248 |
| prevalence_of_bmi_>=40_kg_m²_morbid_obesity_lower_95%_uncertainty_interval | float64 | 66 | 66 | 0.00 | Mean: 0.01793, Std: 0.0104, Min: 0.002115, Max: 0.03483, Median: 0.01648 |
| prevalence_of_bmi_>=40_kg_m²_morbid_obesity_upper_95%_uncertainty_interval | float64 | 66 | 66 | 0.00 | Mean: 0.03097, Std: 0.01728, Min: 0.00483, Max: 0.07405, Median: 0.02843 |
| source_file | object | 66 | 1 | 0.01 | Min Length: 55, Max Length: 55, Avg Length: 55 |

### Column Value Distributions

#### year

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 1990 | 2 | 3.03% |
| 2007 | 2 | 3.03% |
| 2021 | 2 | 3.03% |
| 2020 | 2 | 3.03% |
| 2019 | 2 | 3.03% |
| 2018 | 2 | 3.03% |
| 2017 | 2 | 3.03% |
| 2016 | 2 | 3.03% |
| 2015 | 2 | 3.03% |
| 2014 | 2 | 3.03% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 2000 | 2 | 3.03% |
| 1999 | 2 | 3.03% |
| 1998 | 2 | 3.03% |
| 1997 | 2 | 3.03% |
| 1996 | 2 | 3.03% |
| 1995 | 2 | 3.03% |
| 1994 | 2 | 3.03% |
| 1993 | 2 | 3.03% |
| 1992 | 2 | 3.03% |
| 2022 | 2 | 3.03% |

#### sex

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| Women | 33 | 50.00% |
| Men | 33 | 50.00% |

#### country_region_world

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| Australia | 66 | 100.00% |

#### iso

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| AUS | 66 | 100.00% |

#### prevalence_of_bmi<18.5_kg_m²_underweight_

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.03287 | 1 | 1.52% |
| 0.008311 | 1 | 1.52% |
| 0.009324 | 1 | 1.52% |
| 0.009188 | 1 | 1.52% |
| 0.009067 | 1 | 1.52% |
| 0.008953 | 1 | 1.52% |
| 0.008849 | 1 | 1.52% |
| 0.008757 | 1 | 1.52% |
| 0.008676 | 1 | 1.52% |
| 0.008607 | 1 | 1.52% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.01977 | 1 | 1.52% |
| 0.01977 | 1 | 1.52% |
| 0.01979 | 1 | 1.52% |
| 0.01982 | 1 | 1.52% |
| 0.01986 | 1 | 1.52% |
| 0.01991 | 1 | 1.52% |
| 0.01996 | 1 | 1.52% |
| 0.02002 | 1 | 1.52% |
| 0.02009 | 1 | 1.52% |
| 0.01133 | 1 | 1.52% |

#### prevalence_of_bmi<18.5_kg_m²_underweight_lower_95%_uncertainty_interval

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.02657 | 1 | 1.52% |
| 0.006152 | 1 | 1.52% |
| 0.006664 | 1 | 1.52% |
| 0.006587 | 1 | 1.52% |
| 0.006499 | 1 | 1.52% |
| 0.006428 | 1 | 1.52% |
| 0.006317 | 1 | 1.52% |
| 0.00624 | 1 | 1.52% |
| 0.00621 | 1 | 1.52% |
| 0.006199 | 1 | 1.52% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.01617 | 1 | 1.52% |
| 0.01609 | 1 | 1.52% |
| 0.01599 | 1 | 1.52% |
| 0.01581 | 1 | 1.52% |
| 0.01562 | 1 | 1.52% |
| 0.01538 | 1 | 1.52% |
| 0.01504 | 1 | 1.52% |
| 0.01454 | 1 | 1.52% |
| 0.01401 | 1 | 1.52% |
| 0.006191 | 1 | 1.52% |

#### prevalence_of_bmi<18.5_kg_m²_underweight_upper_95%_uncertainty_interval

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.03982 | 1 | 1.52% |
| 0.01095 | 1 | 1.52% |
| 0.01256 | 1 | 1.52% |
| 0.01233 | 1 | 1.52% |
| 0.01223 | 1 | 1.52% |
| 0.01211 | 1 | 1.52% |
| 0.012 | 1 | 1.52% |
| 0.01182 | 1 | 1.52% |
| 0.0117 | 1 | 1.52% |
| 0.01158 | 1 | 1.52% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.02363 | 1 | 1.52% |
| 0.02375 | 1 | 1.52% |
| 0.024 | 1 | 1.52% |
| 0.0243 | 1 | 1.52% |
| 0.02476 | 1 | 1.52% |
| 0.02515 | 1 | 1.52% |
| 0.02579 | 1 | 1.52% |
| 0.02654 | 1 | 1.52% |
| 0.02738 | 1 | 1.52% |
| 0.01879 | 1 | 1.52% |

#### prevalence_of_bmi>=30_kg_m²_obesity_

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.1339 | 1 | 1.52% |
| 0.2384 | 1 | 1.52% |
| 0.1417 | 1 | 1.52% |
| 0.1483 | 1 | 1.52% |
| 0.1551 | 1 | 1.52% |
| 0.1621 | 1 | 1.52% |
| 0.1691 | 1 | 1.52% |
| 0.1763 | 1 | 1.52% |
| 0.1834 | 1 | 1.52% |
| 0.1905 | 1 | 1.52% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.2606 | 1 | 1.52% |
| 0.2643 | 1 | 1.52% |
| 0.2681 | 1 | 1.52% |
| 0.272 | 1 | 1.52% |
| 0.276 | 1 | 1.52% |
| 0.28 | 1 | 1.52% |
| 0.2839 | 1 | 1.52% |
| 0.2879 | 1 | 1.52% |
| 0.2918 | 1 | 1.52% |
| 0.3205 | 1 | 1.52% |

#### prevalence_of_bmi>=30_kg_m²_obesity_lower_95%_uncertainty_interval

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.1217 | 1 | 1.52% |
| 0.2221 | 1 | 1.52% |
| 0.1281 | 1 | 1.52% |
| 0.1344 | 1 | 1.52% |
| 0.1413 | 1 | 1.52% |
| 0.1476 | 1 | 1.52% |
| 0.1543 | 1 | 1.52% |
| 0.161 | 1 | 1.52% |
| 0.1677 | 1 | 1.52% |
| 0.1747 | 1 | 1.52% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.2454 | 1 | 1.52% |
| 0.2485 | 1 | 1.52% |
| 0.2515 | 1 | 1.52% |
| 0.2543 | 1 | 1.52% |
| 0.2568 | 1 | 1.52% |
| 0.2591 | 1 | 1.52% |
| 0.2608 | 1 | 1.52% |
| 0.2616 | 1 | 1.52% |
| 0.2622 | 1 | 1.52% |
| 0.2777 | 1 | 1.52% |

#### prevalence_of_bmi>=30_kg_m²_obesity_upper_95%_uncertainty_interval

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.1469 | 1 | 1.52% |
| 0.2552 | 1 | 1.52% |
| 0.1556 | 1 | 1.52% |
| 0.1628 | 1 | 1.52% |
| 0.17 | 1 | 1.52% |
| 0.1774 | 1 | 1.52% |
| 0.1848 | 1 | 1.52% |
| 0.1921 | 1 | 1.52% |
| 0.1992 | 1 | 1.52% |
| 0.2067 | 1 | 1.52% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.2764 | 1 | 1.52% |
| 0.2808 | 1 | 1.52% |
| 0.2854 | 1 | 1.52% |
| 0.2906 | 1 | 1.52% |
| 0.296 | 1 | 1.52% |
| 0.3018 | 1 | 1.52% |
| 0.3084 | 1 | 1.52% |
| 0.3161 | 1 | 1.52% |
| 0.3236 | 1 | 1.52% |
| 0.3667 | 1 | 1.52% |

#### combined_prevalence_of_bmi<18.5_kg_m²_and_bmi>=30_kg_m²_double_burden_of_underweight_and_obesity_

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.1668 | 1 | 1.52% |
| 0.2467 | 1 | 1.52% |
| 0.151 | 1 | 1.52% |
| 0.1575 | 1 | 1.52% |
| 0.1642 | 1 | 1.52% |
| 0.171 | 1 | 1.52% |
| 0.178 | 1 | 1.52% |
| 0.185 | 1 | 1.52% |
| 0.192 | 1 | 1.52% |
| 0.1991 | 1 | 1.52% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.2804 | 1 | 1.52% |
| 0.2841 | 1 | 1.52% |
| 0.2879 | 1 | 1.52% |
| 0.2919 | 1 | 1.52% |
| 0.2959 | 1 | 1.52% |
| 0.2999 | 1 | 1.52% |
| 0.3039 | 1 | 1.52% |
| 0.3079 | 1 | 1.52% |
| 0.3119 | 1 | 1.52% |
| 0.3319 | 1 | 1.52% |

#### combined_prevalence_of_bmi<18.5_kg_m²_and_bmi>=30_kg_m²_double_burden_of_underweight_and_obesity_lower_95%_uncertainty_interval

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.1533 | 1 | 1.52% |
| 0.2304 | 1 | 1.52% |
| 0.1372 | 1 | 1.52% |
| 0.1435 | 1 | 1.52% |
| 0.1502 | 1 | 1.52% |
| 0.1566 | 1 | 1.52% |
| 0.1631 | 1 | 1.52% |
| 0.1698 | 1 | 1.52% |
| 0.1766 | 1 | 1.52% |
| 0.183 | 1 | 1.52% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.2649 | 1 | 1.52% |
| 0.2682 | 1 | 1.52% |
| 0.271 | 1 | 1.52% |
| 0.2738 | 1 | 1.52% |
| 0.2764 | 1 | 1.52% |
| 0.2784 | 1 | 1.52% |
| 0.2797 | 1 | 1.52% |
| 0.2806 | 1 | 1.52% |
| 0.2816 | 1 | 1.52% |
| 0.2888 | 1 | 1.52% |

#### combined_prevalence_of_bmi<18.5_kg_m²_and_bmi>=30_kg_m²_double_burden_of_underweight_and_obesity_upper_95%_uncertainty_interval

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.1809 | 1 | 1.52% |
| 0.2637 | 1 | 1.52% |
| 0.1651 | 1 | 1.52% |
| 0.1722 | 1 | 1.52% |
| 0.1791 | 1 | 1.52% |
| 0.1863 | 1 | 1.52% |
| 0.1936 | 1 | 1.52% |
| 0.201 | 1 | 1.52% |
| 0.2082 | 1 | 1.52% |
| 0.2155 | 1 | 1.52% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.2965 | 1 | 1.52% |
| 0.3006 | 1 | 1.52% |
| 0.3052 | 1 | 1.52% |
| 0.3103 | 1 | 1.52% |
| 0.3158 | 1 | 1.52% |
| 0.3218 | 1 | 1.52% |
| 0.3287 | 1 | 1.52% |
| 0.3358 | 1 | 1.52% |
| 0.3435 | 1 | 1.52% |
| 0.3775 | 1 | 1.52% |

#### proportion_of_double_burden_from_obesity

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.7759 | 1 | 1.52% |
| 0.9569 | 1 | 1.52% |
| 0.9204 | 1 | 1.52% |
| 0.9247 | 1 | 1.52% |
| 0.9287 | 1 | 1.52% |
| 0.9324 | 1 | 1.52% |
| 0.9358 | 1 | 1.52% |
| 0.9389 | 1 | 1.52% |
| 0.9417 | 1 | 1.52% |
| 0.9443 | 1 | 1.52% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.9182 | 1 | 1.52% |
| 0.9194 | 1 | 1.52% |
| 0.9205 | 1 | 1.52% |
| 0.9216 | 1 | 1.52% |
| 0.9226 | 1 | 1.52% |
| 0.9236 | 1 | 1.52% |
| 0.9246 | 1 | 1.52% |
| 0.9254 | 1 | 1.52% |
| 0.9263 | 1 | 1.52% |
| 0.9572 | 1 | 1.52% |

#### proportion_of_double_burden_from_obesity_lower_95%_uncertainty_interval

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.7391 | 1 | 1.52% |
| 0.944 | 1 | 1.52% |
| 0.8961 | 1 | 1.52% |
| 0.9016 | 1 | 1.52% |
| 0.9067 | 1 | 1.52% |
| 0.9113 | 1 | 1.52% |
| 0.9155 | 1 | 1.52% |
| 0.9195 | 1 | 1.52% |
| 0.9232 | 1 | 1.52% |
| 0.9262 | 1 | 1.52% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.9029 | 1 | 1.52% |
| 0.9035 | 1 | 1.52% |
| 0.9043 | 1 | 1.52% |
| 0.9046 | 1 | 1.52% |
| 0.9047 | 1 | 1.52% |
| 0.9047 | 1 | 1.52% |
| 0.904 | 1 | 1.52% |
| 0.9027 | 1 | 1.52% |
| 0.9005 | 1 | 1.52% |
| 0.9318 | 1 | 1.52% |

#### proportion_of_double_burden_from_obesity_upper_95%_uncertainty_interval

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.8111 | 1 | 1.52% |
| 0.9676 | 1 | 1.52% |
| 0.9418 | 1 | 1.52% |
| 0.9453 | 1 | 1.52% |
| 0.9484 | 1 | 1.52% |
| 0.9509 | 1 | 1.52% |
| 0.9533 | 1 | 1.52% |
| 0.9555 | 1 | 1.52% |
| 0.9574 | 1 | 1.52% |
| 0.9593 | 1 | 1.52% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.9326 | 1 | 1.52% |
| 0.9337 | 1 | 1.52% |
| 0.9352 | 1 | 1.52% |
| 0.9368 | 1 | 1.52% |
| 0.9384 | 1 | 1.52% |
| 0.9402 | 1 | 1.52% |
| 0.9426 | 1 | 1.52% |
| 0.945 | 1 | 1.52% |
| 0.9476 | 1 | 1.52% |
| 0.9758 | 1 | 1.52% |

#### prevalence_of_bmi_18.5_kg_m²_to_<20_kg_m²

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.085 | 1 | 1.52% |
| 0.02117 | 1 | 1.52% |
| 0.0303 | 1 | 1.52% |
| 0.02937 | 1 | 1.52% |
| 0.02852 | 1 | 1.52% |
| 0.02774 | 1 | 1.52% |
| 0.02701 | 1 | 1.52% |
| 0.02634 | 1 | 1.52% |
| 0.02572 | 1 | 1.52% |
| 0.02512 | 1 | 1.52% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.05684 | 1 | 1.52% |
| 0.0564 | 1 | 1.52% |
| 0.0559 | 1 | 1.52% |
| 0.05536 | 1 | 1.52% |
| 0.05479 | 1 | 1.52% |
| 0.0542 | 1 | 1.52% |
| 0.05362 | 1 | 1.52% |
| 0.05307 | 1 | 1.52% |
| 0.05252 | 1 | 1.52% |
| 0.01718 | 1 | 1.52% |

#### prevalence_of_bmi_18.5_kg_m²_to_<20_kg_m²_lower_95%_uncertainty_interval

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.07552 | 1 | 1.52% |
| 0.01804 | 1 | 1.52% |
| 0.02564 | 1 | 1.52% |
| 0.02487 | 1 | 1.52% |
| 0.02415 | 1 | 1.52% |
| 0.02349 | 1 | 1.52% |
| 0.02286 | 1 | 1.52% |
| 0.02232 | 1 | 1.52% |
| 0.02175 | 1 | 1.52% |
| 0.02125 | 1 | 1.52% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.05084 | 1 | 1.52% |
| 0.05046 | 1 | 1.52% |
| 0.04981 | 1 | 1.52% |
| 0.04907 | 1 | 1.52% |
| 0.04808 | 1 | 1.52% |
| 0.047 | 1 | 1.52% |
| 0.04568 | 1 | 1.52% |
| 0.04424 | 1 | 1.52% |
| 0.04259 | 1 | 1.52% |
| 0.01204 | 1 | 1.52% |

#### prevalence_of_bmi_18.5_kg_m²_to_<20_kg_m²_upper_95%_uncertainty_interval

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.09466 | 1 | 1.52% |
| 0.02464 | 1 | 1.52% |
| 0.03526 | 1 | 1.52% |
| 0.03423 | 1 | 1.52% |
| 0.03325 | 1 | 1.52% |
| 0.03242 | 1 | 1.52% |
| 0.03159 | 1 | 1.52% |
| 0.03084 | 1 | 1.52% |
| 0.0301 | 1 | 1.52% |
| 0.02936 | 1 | 1.52% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.06329 | 1 | 1.52% |
| 0.06279 | 1 | 1.52% |
| 0.06247 | 1 | 1.52% |
| 0.06214 | 1 | 1.52% |
| 0.06203 | 1 | 1.52% |
| 0.06222 | 1 | 1.52% |
| 0.06256 | 1 | 1.52% |
| 0.06324 | 1 | 1.52% |
| 0.06403 | 1 | 1.52% |
| 0.02393 | 1 | 1.52% |

#### prevalence_of_bmi_20_kg_m²_to_<25_kg_m²

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.4935 | 1 | 1.52% |
| 0.294 | 1 | 1.52% |
| 0.3838 | 1 | 1.52% |
| 0.3751 | 1 | 1.52% |
| 0.3667 | 1 | 1.52% |
| 0.3586 | 1 | 1.52% |
| 0.351 | 1 | 1.52% |
| 0.3437 | 1 | 1.52% |
| 0.3368 | 1 | 1.52% |
| 0.3303 | 1 | 1.52% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.3711 | 1 | 1.52% |
| 0.3681 | 1 | 1.52% |
| 0.3651 | 1 | 1.52% |
| 0.362 | 1 | 1.52% |
| 0.3588 | 1 | 1.52% |
| 0.3556 | 1 | 1.52% |
| 0.3525 | 1 | 1.52% |
| 0.3493 | 1 | 1.52% |
| 0.3462 | 1 | 1.52% |
| 0.2525 | 1 | 1.52% |

#### prevalence_of_bmi_20_kg_m²_to_<25_kg_m²_lower_95%_uncertainty_interval

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.4751 | 1 | 1.52% |
| 0.2774 | 1 | 1.52% |
| 0.365 | 1 | 1.52% |
| 0.3563 | 1 | 1.52% |
| 0.348 | 1 | 1.52% |
| 0.3397 | 1 | 1.52% |
| 0.3323 | 1 | 1.52% |
| 0.3253 | 1 | 1.52% |
| 0.3188 | 1 | 1.52% |
| 0.3126 | 1 | 1.52% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.3552 | 1 | 1.52% |
| 0.3518 | 1 | 1.52% |
| 0.3482 | 1 | 1.52% |
| 0.3441 | 1 | 1.52% |
| 0.3396 | 1 | 1.52% |
| 0.3346 | 1 | 1.52% |
| 0.3293 | 1 | 1.52% |
| 0.3233 | 1 | 1.52% |
| 0.3164 | 1 | 1.52% |
| 0.2148 | 1 | 1.52% |

#### prevalence_of_bmi_20_kg_m²_to_<25_kg_m²_upper_95%_uncertainty_interval

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.5116 | 1 | 1.52% |
| 0.3107 | 1 | 1.52% |
| 0.4028 | 1 | 1.52% |
| 0.394 | 1 | 1.52% |
| 0.3856 | 1 | 1.52% |
| 0.3776 | 1 | 1.52% |
| 0.3696 | 1 | 1.52% |
| 0.3623 | 1 | 1.52% |
| 0.3553 | 1 | 1.52% |
| 0.3489 | 1 | 1.52% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.3872 | 1 | 1.52% |
| 0.3845 | 1 | 1.52% |
| 0.382 | 1 | 1.52% |
| 0.3801 | 1 | 1.52% |
| 0.3784 | 1 | 1.52% |
| 0.3772 | 1 | 1.52% |
| 0.3764 | 1 | 1.52% |
| 0.3762 | 1 | 1.52% |
| 0.3766 | 1 | 1.52% |
| 0.2917 | 1 | 1.52% |

#### prevalence_of_bmi_25_kg_m²_to_<30_kg_m²

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.2547 | 1 | 1.52% |
| 0.4381 | 1 | 1.52% |
| 0.4349 | 1 | 1.52% |
| 0.438 | 1 | 1.52% |
| 0.4406 | 1 | 1.52% |
| 0.4426 | 1 | 1.52% |
| 0.444 | 1 | 1.52% |
| 0.4449 | 1 | 1.52% |
| 0.4454 | 1 | 1.52% |
| 0.4454 | 1 | 1.52% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.2917 | 1 | 1.52% |
| 0.2914 | 1 | 1.52% |
| 0.291 | 1 | 1.52% |
| 0.2908 | 1 | 1.52% |
| 0.2905 | 1 | 1.52% |
| 0.2903 | 1 | 1.52% |
| 0.29 | 1 | 1.52% |
| 0.2897 | 1 | 1.52% |
| 0.2894 | 1 | 1.52% |
| 0.3984 | 1 | 1.52% |

#### prevalence_of_bmi_25_kg_m²_to_<30_kg_m²_lower_95%_uncertainty_interval

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.2383 | 1 | 1.52% |
| 0.4196 | 1 | 1.52% |
| 0.4156 | 1 | 1.52% |
| 0.4188 | 1 | 1.52% |
| 0.4215 | 1 | 1.52% |
| 0.4238 | 1 | 1.52% |
| 0.4251 | 1 | 1.52% |
| 0.4258 | 1 | 1.52% |
| 0.4257 | 1 | 1.52% |
| 0.4259 | 1 | 1.52% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.2762 | 1 | 1.52% |
| 0.2756 | 1 | 1.52% |
| 0.2746 | 1 | 1.52% |
| 0.2736 | 1 | 1.52% |
| 0.2715 | 1 | 1.52% |
| 0.2697 | 1 | 1.52% |
| 0.2669 | 1 | 1.52% |
| 0.2639 | 1 | 1.52% |
| 0.2608 | 1 | 1.52% |
| 0.355 | 1 | 1.52% |

#### prevalence_of_bmi_25_kg_m²_to_<30_kg_m²_upper_95%_uncertainty_interval

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.2716 | 1 | 1.52% |
| 0.4561 | 1 | 1.52% |
| 0.4544 | 1 | 1.52% |
| 0.4578 | 1 | 1.52% |
| 0.4602 | 1 | 1.52% |
| 0.4624 | 1 | 1.52% |
| 0.4635 | 1 | 1.52% |
| 0.4645 | 1 | 1.52% |
| 0.4649 | 1 | 1.52% |
| 0.4646 | 1 | 1.52% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.3072 | 1 | 1.52% |
| 0.3074 | 1 | 1.52% |
| 0.3079 | 1 | 1.52% |
| 0.3087 | 1 | 1.52% |
| 0.3095 | 1 | 1.52% |
| 0.3113 | 1 | 1.52% |
| 0.3132 | 1 | 1.52% |
| 0.3159 | 1 | 1.52% |
| 0.3191 | 1 | 1.52% |
| 0.4414 | 1 | 1.52% |

#### prevalence_of_bmi_30_kg_m²_to_<35_kg_m²

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.09122 | 1 | 1.52% |
| 0.1741 | 1 | 1.52% |
| 0.1175 | 1 | 1.52% |
| 0.1221 | 1 | 1.52% |
| 0.1268 | 1 | 1.52% |
| 0.1314 | 1 | 1.52% |
| 0.1359 | 1 | 1.52% |
| 0.1402 | 1 | 1.52% |
| 0.1445 | 1 | 1.52% |
| 0.1486 | 1 | 1.52% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.1547 | 1 | 1.52% |
| 0.1568 | 1 | 1.52% |
| 0.1588 | 1 | 1.52% |
| 0.1609 | 1 | 1.52% |
| 0.163 | 1 | 1.52% |
| 0.165 | 1 | 1.52% |
| 0.167 | 1 | 1.52% |
| 0.1689 | 1 | 1.52% |
| 0.1708 | 1 | 1.52% |
| 0.2168 | 1 | 1.52% |

#### prevalence_of_bmi_30_kg_m²_to_<35_kg_m²_lower_95%_uncertainty_interval

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.0804 | 1 | 1.52% |
| 0.1584 | 1 | 1.52% |
| 0.1044 | 1 | 1.52% |
| 0.109 | 1 | 1.52% |
| 0.1133 | 1 | 1.52% |
| 0.1175 | 1 | 1.52% |
| 0.1216 | 1 | 1.52% |
| 0.1258 | 1 | 1.52% |
| 0.1297 | 1 | 1.52% |
| 0.1335 | 1 | 1.52% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.142 | 1 | 1.52% |
| 0.1437 | 1 | 1.52% |
| 0.1452 | 1 | 1.52% |
| 0.1462 | 1 | 1.52% |
| 0.1473 | 1 | 1.52% |
| 0.1473 | 1 | 1.52% |
| 0.1476 | 1 | 1.52% |
| 0.1466 | 1 | 1.52% |
| 0.1455 | 1 | 1.52% |
| 0.1796 | 1 | 1.52% |

#### prevalence_of_bmi_30_kg_m²_to_<35_kg_m²_upper_95%_uncertainty_interval

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.1029 | 1 | 1.52% |
| 0.1894 | 1 | 1.52% |
| 0.1312 | 1 | 1.52% |
| 0.1359 | 1 | 1.52% |
| 0.141 | 1 | 1.52% |
| 0.1457 | 1 | 1.52% |
| 0.1506 | 1 | 1.52% |
| 0.1551 | 1 | 1.52% |
| 0.1595 | 1 | 1.52% |
| 0.1636 | 1 | 1.52% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.168 | 1 | 1.52% |
| 0.1704 | 1 | 1.52% |
| 0.1733 | 1 | 1.52% |
| 0.176 | 1 | 1.52% |
| 0.1792 | 1 | 1.52% |
| 0.1826 | 1 | 1.52% |
| 0.1869 | 1 | 1.52% |
| 0.1916 | 1 | 1.52% |
| 0.1968 | 1 | 1.52% |
| 0.2579 | 1 | 1.52% |

#### prevalence_of_bmi_35_kg_m²_to_<40_kg_m²

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.03006 | 1 | 1.52% |
| 0.04933 | 1 | 1.52% |
| 0.02019 | 1 | 1.52% |
| 0.02181 | 1 | 1.52% |
| 0.02354 | 1 | 1.52% |
| 0.02538 | 1 | 1.52% |
| 0.02736 | 1 | 1.52% |
| 0.02943 | 1 | 1.52% |
| 0.03159 | 1 | 1.52% |
| 0.03382 | 1 | 1.52% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.06547 | 1 | 1.52% |
| 0.06624 | 1 | 1.52% |
| 0.06704 | 1 | 1.52% |
| 0.0679 | 1 | 1.52% |
| 0.06881 | 1 | 1.52% |
| 0.06973 | 1 | 1.52% |
| 0.07066 | 1 | 1.52% |
| 0.07158 | 1 | 1.52% |
| 0.0725 | 1 | 1.52% |
| 0.07433 | 1 | 1.52% |

#### prevalence_of_bmi_35_kg_m²_to_<40_kg_m²_lower_95%_uncertainty_interval

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.02497 | 1 | 1.52% |
| 0.04155 | 1 | 1.52% |
| 0.01601 | 1 | 1.52% |
| 0.01739 | 1 | 1.52% |
| 0.01887 | 1 | 1.52% |
| 0.02039 | 1 | 1.52% |
| 0.02209 | 1 | 1.52% |
| 0.02384 | 1 | 1.52% |
| 0.02577 | 1 | 1.52% |
| 0.02767 | 1 | 1.52% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.05724 | 1 | 1.52% |
| 0.05779 | 1 | 1.52% |
| 0.05818 | 1 | 1.52% |
| 0.05834 | 1 | 1.52% |
| 0.05844 | 1 | 1.52% |
| 0.05835 | 1 | 1.52% |
| 0.05801 | 1 | 1.52% |
| 0.05743 | 1 | 1.52% |
| 0.05671 | 1 | 1.52% |
| 0.05032 | 1 | 1.52% |

#### prevalence_of_bmi_35_kg_m²_to_<40_kg_m²_upper_95%_uncertainty_interval

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.03563 | 1 | 1.52% |
| 0.0579 | 1 | 1.52% |
| 0.02497 | 1 | 1.52% |
| 0.02691 | 1 | 1.52% |
| 0.02889 | 1 | 1.52% |
| 0.03106 | 1 | 1.52% |
| 0.0333 | 1 | 1.52% |
| 0.03559 | 1 | 1.52% |
| 0.03805 | 1 | 1.52% |
| 0.04055 | 1 | 1.52% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.07451 | 1 | 1.52% |
| 0.07544 | 1 | 1.52% |
| 0.07674 | 1 | 1.52% |
| 0.07809 | 1 | 1.52% |
| 0.07984 | 1 | 1.52% |
| 0.08198 | 1 | 1.52% |
| 0.08454 | 1 | 1.52% |
| 0.08702 | 1 | 1.52% |
| 0.09023 | 1 | 1.52% |
| 0.103 | 1 | 1.52% |

#### prevalence_of_bmi_>=40_kg_m²_morbid_obesity_

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.01261 | 1 | 1.52% |
| 0.01505 | 1 | 1.52% |
| 0.003955 | 1 | 1.52% |
| 0.004359 | 1 | 1.52% |
| 0.004816 | 1 | 1.52% |
| 0.005337 | 1 | 1.52% |
| 0.005928 | 1 | 1.52% |
| 0.006589 | 1 | 1.52% |
| 0.007312 | 1 | 1.52% |
| 0.008106 | 1 | 1.52% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.04039 | 1 | 1.52% |
| 0.04134 | 1 | 1.52% |
| 0.04228 | 1 | 1.52% |
| 0.04324 | 1 | 1.52% |
| 0.04423 | 1 | 1.52% |
| 0.04525 | 1 | 1.52% |
| 0.0463 | 1 | 1.52% |
| 0.04738 | 1 | 1.52% |
| 0.04849 | 1 | 1.52% |
| 0.02939 | 1 | 1.52% |

#### prevalence_of_bmi_>=40_kg_m²_morbid_obesity_lower_95%_uncertainty_interval

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.009579 | 1 | 1.52% |
| 0.01109 | 1 | 1.52% |
| 0.002594 | 1 | 1.52% |
| 0.002913 | 1 | 1.52% |
| 0.003246 | 1 | 1.52% |
| 0.003622 | 1 | 1.52% |
| 0.004035 | 1 | 1.52% |
| 0.004516 | 1 | 1.52% |
| 0.005038 | 1 | 1.52% |
| 0.005658 | 1 | 1.52% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.03324 | 1 | 1.52% |
| 0.03396 | 1 | 1.52% |
| 0.03421 | 1 | 1.52% |
| 0.03441 | 1 | 1.52% |
| 0.03478 | 1 | 1.52% |
| 0.03483 | 1 | 1.52% |
| 0.03465 | 1 | 1.52% |
| 0.03453 | 1 | 1.52% |
| 0.03404 | 1 | 1.52% |
| 0.01501 | 1 | 1.52% |

#### prevalence_of_bmi_>=40_kg_m²_morbid_obesity_upper_95%_uncertainty_interval

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.01621 | 1 | 1.52% |
| 0.01997 | 1 | 1.52% |
| 0.005727 | 1 | 1.52% |
| 0.006299 | 1 | 1.52% |
| 0.006897 | 1 | 1.52% |
| 0.007603 | 1 | 1.52% |
| 0.00841 | 1 | 1.52% |
| 0.009294 | 1 | 1.52% |
| 0.01024 | 1 | 1.52% |
| 0.01126 | 1 | 1.52% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.04841 | 1 | 1.52% |
| 0.0498 | 1 | 1.52% |
| 0.05137 | 1 | 1.52% |
| 0.05314 | 1 | 1.52% |
| 0.055 | 1 | 1.52% |
| 0.05732 | 1 | 1.52% |
| 0.05979 | 1 | 1.52% |
| 0.06266 | 1 | 1.52% |
| 0.06573 | 1 | 1.52% |
| 0.04901 | 1 | 1.52% |

#### source_file

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| NCD_RisC_Lancet_2024_BMI_age_standardised_Australia.csv | 66 | 100.00% |

### Sample Data

First 10 Rows:
|    |   year | sex   | country_region_world   | iso   |   prevalence_of_bmi<18.5_kg_m²_underweight_ |   prevalence_of_bmi<18.5_kg_m²_underweight_lower_95%_uncertainty_interval |   prevalence_of_bmi<18.5_kg_m²_underweight_upper_95%_uncertainty_interval |   prevalence_of_bmi>=30_kg_m²_obesity_ |   prevalence_of_bmi>=30_kg_m²_obesity_lower_95%_uncertainty_interval |   prevalence_of_bmi>=30_kg_m²_obesity_upper_95%_uncertainty_interval |   combined_prevalence_of_bmi<18.5_kg_m²_and_bmi>=30_kg_m²_double_burden_of_underweight_and_obesity_ |   combined_prevalence_of_bmi<18.5_kg_m²_and_bmi>=30_kg_m²_double_burden_of_underweight_and_obesity_lower_95%_uncertainty_interval |   combined_prevalence_of_bmi<18.5_kg_m²_and_bmi>=30_kg_m²_double_burden_of_underweight_and_obesity_upper_95%_uncertainty_interval |   proportion_of_double_burden_from_obesity |   proportion_of_double_burden_from_obesity_lower_95%_uncertainty_interval |   proportion_of_double_burden_from_obesity_upper_95%_uncertainty_interval |   prevalence_of_bmi_18.5_kg_m²_to_<20_kg_m² |   prevalence_of_bmi_18.5_kg_m²_to_<20_kg_m²_lower_95%_uncertainty_interval |   prevalence_of_bmi_18.5_kg_m²_to_<20_kg_m²_upper_95%_uncertainty_interval |   prevalence_of_bmi_20_kg_m²_to_<25_kg_m² |   prevalence_of_bmi_20_kg_m²_to_<25_kg_m²_lower_95%_uncertainty_interval |   prevalence_of_bmi_20_kg_m²_to_<25_kg_m²_upper_95%_uncertainty_interval |   prevalence_of_bmi_25_kg_m²_to_<30_kg_m² |   prevalence_of_bmi_25_kg_m²_to_<30_kg_m²_lower_95%_uncertainty_interval |   prevalence_of_bmi_25_kg_m²_to_<30_kg_m²_upper_95%_uncertainty_interval |   prevalence_of_bmi_30_kg_m²_to_<35_kg_m² |   prevalence_of_bmi_30_kg_m²_to_<35_kg_m²_lower_95%_uncertainty_interval |   prevalence_of_bmi_30_kg_m²_to_<35_kg_m²_upper_95%_uncertainty_interval |   prevalence_of_bmi_35_kg_m²_to_<40_kg_m² |   prevalence_of_bmi_35_kg_m²_to_<40_kg_m²_lower_95%_uncertainty_interval |   prevalence_of_bmi_35_kg_m²_to_<40_kg_m²_upper_95%_uncertainty_interval |   prevalence_of_bmi_>=40_kg_m²_morbid_obesity_ |   prevalence_of_bmi_>=40_kg_m²_morbid_obesity_lower_95%_uncertainty_interval |   prevalence_of_bmi_>=40_kg_m²_morbid_obesity_upper_95%_uncertainty_interval | source_file                                             |
|---:|-------:|:------|:-----------------------|:------|--------------------------------------------:|--------------------------------------------------------------------------:|--------------------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------------------------:|---------------------------------------------------------------------:|----------------------------------------------------------------------------------------------------:|----------------------------------------------------------------------------------------------------------------------------------:|----------------------------------------------------------------------------------------------------------------------------------:|-------------------------------------------:|--------------------------------------------------------------------------:|--------------------------------------------------------------------------:|--------------------------------------------:|---------------------------------------------------------------------------:|---------------------------------------------------------------------------:|------------------------------------------:|-------------------------------------------------------------------------:|-------------------------------------------------------------------------:|------------------------------------------:|-------------------------------------------------------------------------:|-------------------------------------------------------------------------:|------------------------------------------:|-------------------------------------------------------------------------:|-------------------------------------------------------------------------:|------------------------------------------:|-------------------------------------------------------------------------:|-------------------------------------------------------------------------:|-----------------------------------------------:|-----------------------------------------------------------------------------:|-----------------------------------------------------------------------------:|:--------------------------------------------------------|
|  0 |   1990 | Women | Australia              | AUS   |                                   0.032874  |                                                                 0.0265722 |                                                                 0.0398173 |                               0.133887 |                                                             0.121689 |                                                             0.146858 |                                                                                            0.166761 |                                                                                                                          0.153322 |                                                                                                                          0.180861 |                                   0.775896 |                                                                  0.739057 |                                                                  0.811071 |                                   0.0849955 |                                                                  0.075525  |                                                                  0.0946623 |                                  0.493515 |                                                                 0.475108 |                                                                 0.511585 |                                  0.254728 |                                                                 0.238254 |                                                                 0.271581 |                                 0.0912223 |                                                                0.0804047 |                                                                 0.102887 |                                 0.0300557 |                                                                0.0249708 |                                                                0.035627  |                                      0.0126086 |                                                                   0.00957938 |                                                                    0.0162125 | NCD_RisC_Lancet_2024_BMI_age_standardised_Australia.csv |
|  1 |   1991 | Women | Australia              | AUS   |                                   0.0312882 |                                                                 0.0252344 |                                                                 0.0379737 |                               0.140742 |                                                             0.128292 |                                                             0.154159 |                                                                                            0.172031 |                                                                                                                          0.158389 |                                                                                                                          0.186105 |                                   0.791864 |                                                                  0.75707  |                                                                  0.825344 |                                   0.0821296 |                                                                  0.072925  |                                                                  0.0915679 |                                  0.486112 |                                                                 0.467245 |                                                                 0.504321 |                                  0.259728 |                                                                 0.24331  |                                                                 0.277136 |                                 0.0950186 |                                                                0.0839342 |                                                                 0.106973 |                                 0.0320373 |                                                                0.0266516 |                                                                0.0379679 |                                      0.0136864 |                                                                   0.0104869  |                                                                    0.0175691 | NCD_RisC_Lancet_2024_BMI_age_standardised_Australia.csv |
|  2 |   1992 | Women | Australia              | AUS   |                                   0.0298014 |                                                                 0.024018  |                                                                 0.0362579 |                               0.147705 |                                                             0.134844 |                                                             0.161319 |                                                                                            0.177506 |                                                                                                                          0.163495 |                                                                                                                          0.191942 |                                   0.806721 |                                                                  0.773696 |                                                                  0.838347 |                                   0.0794314 |                                                                  0.0704534 |                                                                  0.088604  |                                  0.478589 |                                                                 0.459412 |                                                                 0.497049 |                                  0.264473 |                                                                 0.247752 |                                                                 0.281887 |                                 0.098825  |                                                                0.087543  |                                                                 0.111182 |                                 0.0340584 |                                                                0.0284148 |                                                                0.0402737 |                                      0.0148216 |                                                                   0.0114438  |                                                                    0.0189433 | NCD_RisC_Lancet_2024_BMI_age_standardised_Australia.csv |
|  3 |   1993 | Women | Australia              | AUS   |                                   0.0284273 |                                                                 0.0228625 |                                                                 0.0345754 |                               0.15474  |                                                             0.141576 |                                                             0.168933 |                                                                                            0.183167 |                                                                                                                          0.168862 |                                                                                                                          0.197901 |                                   0.820399 |                                                                  0.788819 |                                                                  0.850157 |                                   0.0769342 |                                                                  0.0682087 |                                                                  0.0861244 |                                  0.470996 |                                                                 0.451649 |                                                                 0.489609 |                                  0.268902 |                                                                 0.252271 |                                                                 0.286674 |                                 0.102623  |                                                                0.0909706 |                                                                 0.115091 |                                 0.0361051 |                                                                0.0303106 |                                                                0.0424578 |                                      0.0160122 |                                                                   0.0123862  |                                                                    0.0203649 | NCD_RisC_Lancet_2024_BMI_age_standardised_Australia.csv |
|  4 |   1994 | Women | Australia              | AUS   |                                   0.0271738 |                                                                 0.0218219 |                                                                 0.0331321 |                               0.161821 |                                                             0.148277 |                                                             0.176353 |                                                                                            0.188995 |                                                                                                                          0.174348 |                                                                                                                          0.203971 |                                   0.832875 |                                                                  0.802713 |                                                                  0.861637 |                                   0.0746445 |                                                                  0.0660927 |                                                                  0.0836725 |                                  0.463376 |                                                                 0.444422 |                                                                 0.482017 |                                  0.272985 |                                                                 0.25629  |                                                                 0.290638 |                                 0.106381  |                                                                0.0946441 |                                                                 0.119022 |                                 0.0381829 |                                                                0.0321012 |                                                                0.0448805 |                                      0.0172572 |                                                                   0.0133057  |                                                                    0.0218797 | NCD_RisC_Lancet_2024_BMI_age_standardised_Australia.csv |
|  5 |   1995 | Women | Australia              | AUS   |                                   0.0260443 |                                                                 0.0208556 |                                                                 0.0318039 |                               0.1689   |                                                             0.155076 |                                                             0.183857 |                                                                                            0.194944 |                                                                                                                          0.179963 |                                                                                                                          0.210385 |                                   0.844146 |                                                                  0.815694 |                                                                  0.871669 |                                   0.0725638 |                                                                  0.0642527 |                                                                  0.0814359 |                                  0.455792 |                                                                 0.436653 |                                                                 0.474512 |                                  0.276699 |                                                                 0.26006  |                                                                 0.294352 |                                 0.110067  |                                                                0.0981563 |                                                                 0.122904 |                                 0.0402763 |                                                                0.0339267 |                                                                0.0472723 |                                      0.0185564 |                                                                   0.0143594  |                                                                    0.023487  | NCD_RisC_Lancet_2024_BMI_age_standardised_Australia.csv |
|  6 |   1996 | Women | Australia              | AUS   |                                   0.0250354 |                                                                 0.0199588 |                                                                 0.0306214 |                               0.175967 |                                                             0.161779 |                                                             0.191175 |                                                                                            0.201002 |                                                                                                                          0.186034 |                                                                                                                          0.216679 |                                   0.854282 |                                                                  0.826717 |                                                                  0.880613 |                                   0.0706922 |                                                                  0.0626017 |                                                                  0.0794098 |                                  0.448296 |                                                                 0.429352 |                                                                 0.467017 |                                  0.28001  |                                                                 0.26322  |                                                                 0.297688 |                                 0.113668  |                                                                0.101326  |                                                                 0.126625 |                                 0.042385  |                                                                0.0358468 |                                                                0.0498327 |                                      0.0199138 |                                                                   0.0154621  |                                                                    0.025196  | NCD_RisC_Lancet_2024_BMI_age_standardised_Australia.csv |
|  7 |   1997 | Women | Australia              | AUS   |                                   0.0241495 |                                                                 0.0192072 |                                                                 0.0295445 |                               0.182983 |                                                             0.16842  |                                                             0.198296 |                                                                                            0.207133 |                                                                                                                          0.191801 |                                                                                                                          0.223021 |                                   0.86331  |                                                                  0.837291 |                                                                  0.888357 |                                   0.0689998 |                                                                  0.0609221 |                                                                  0.0775459 |                                  0.44093  |                                                                 0.421855 |                                                                 0.459359 |                                  0.282938 |                                                                 0.26604  |                                                                 0.300691 |                                 0.117173  |                                                                0.104425  |                                                                 0.130395 |                                 0.0444934 |                                                                0.0376114 |                                                                0.0521432 |                                      0.0213165 |                                                                   0.0165746  |                                                                    0.0269193 | NCD_RisC_Lancet_2024_BMI_age_standardised_Australia.csv |
|  8 |   1998 | Women | Australia              | AUS   |                                   0.0233788 |                                                                 0.0186643 |                                                                 0.0285974 |                               0.189888 |                                                             0.175105 |                                                             0.205272 |                                                                                            0.213267 |                                                                                                                          0.197795 |                                                                                                                          0.229266 |                                   0.871292 |                                                                  0.846432 |                                                                  0.894979 |                                   0.0674686 |                                                                  0.0596624 |                                                                  0.0758863 |                                  0.433819 |                                                                 0.415103 |                                                                 0.45216  |                                  0.285446 |                                                                 0.268559 |                                                                 0.303353 |                                 0.120559  |                                                                0.107773  |                                                                 0.134095 |                                 0.0465751 |                                                                0.0395494 |                                                                0.0543953 |                                      0.0227538 |                                                                   0.0177286  |                                                                    0.0285168 | NCD_RisC_Lancet_2024_BMI_age_standardised_Australia.csv |
|  9 |   1999 | Women | Australia              | AUS   |                                   0.0227202 |                                                                 0.0180824 |                                                                 0.027821  |                               0.196611 |                                                             0.181609 |                                                             0.212432 |                                                                                            0.219332 |                                                                                                                          0.203551 |                                                                                                                          0.235584 |                                   0.878276 |                                                                  0.854318 |                                                                  0.900464 |                                   0.0660938 |                                                                  0.0583968 |                                                                  0.074445  |                                  0.427005 |                                                                 0.408718 |                                                                 0.445229 |                                  0.287569 |                                                                 0.270829 |                                                                 0.30533  |                                 0.123804  |                                                                0.110878  |                                                                 0.13759  |                                 0.0485975 |                                                                0.0414053 |                                                                0.0566619 |                                      0.0242101 |                                                                   0.0189717  |                                                                    0.0302912 | NCD_RisC_Lancet_2024_BMI_age_standardised_Australia.csv |

Last 10 Rows:
|    |   year | sex   | country_region_world   | iso   |   prevalence_of_bmi<18.5_kg_m²_underweight_ |   prevalence_of_bmi<18.5_kg_m²_underweight_lower_95%_uncertainty_interval |   prevalence_of_bmi<18.5_kg_m²_underweight_upper_95%_uncertainty_interval |   prevalence_of_bmi>=30_kg_m²_obesity_ |   prevalence_of_bmi>=30_kg_m²_obesity_lower_95%_uncertainty_interval |   prevalence_of_bmi>=30_kg_m²_obesity_upper_95%_uncertainty_interval |   combined_prevalence_of_bmi<18.5_kg_m²_and_bmi>=30_kg_m²_double_burden_of_underweight_and_obesity_ |   combined_prevalence_of_bmi<18.5_kg_m²_and_bmi>=30_kg_m²_double_burden_of_underweight_and_obesity_lower_95%_uncertainty_interval |   combined_prevalence_of_bmi<18.5_kg_m²_and_bmi>=30_kg_m²_double_burden_of_underweight_and_obesity_upper_95%_uncertainty_interval |   proportion_of_double_burden_from_obesity |   proportion_of_double_burden_from_obesity_lower_95%_uncertainty_interval |   proportion_of_double_burden_from_obesity_upper_95%_uncertainty_interval |   prevalence_of_bmi_18.5_kg_m²_to_<20_kg_m² |   prevalence_of_bmi_18.5_kg_m²_to_<20_kg_m²_lower_95%_uncertainty_interval |   prevalence_of_bmi_18.5_kg_m²_to_<20_kg_m²_upper_95%_uncertainty_interval |   prevalence_of_bmi_20_kg_m²_to_<25_kg_m² |   prevalence_of_bmi_20_kg_m²_to_<25_kg_m²_lower_95%_uncertainty_interval |   prevalence_of_bmi_20_kg_m²_to_<25_kg_m²_upper_95%_uncertainty_interval |   prevalence_of_bmi_25_kg_m²_to_<30_kg_m² |   prevalence_of_bmi_25_kg_m²_to_<30_kg_m²_lower_95%_uncertainty_interval |   prevalence_of_bmi_25_kg_m²_to_<30_kg_m²_upper_95%_uncertainty_interval |   prevalence_of_bmi_30_kg_m²_to_<35_kg_m² |   prevalence_of_bmi_30_kg_m²_to_<35_kg_m²_lower_95%_uncertainty_interval |   prevalence_of_bmi_30_kg_m²_to_<35_kg_m²_upper_95%_uncertainty_interval |   prevalence_of_bmi_35_kg_m²_to_<40_kg_m² |   prevalence_of_bmi_35_kg_m²_to_<40_kg_m²_lower_95%_uncertainty_interval |   prevalence_of_bmi_35_kg_m²_to_<40_kg_m²_upper_95%_uncertainty_interval |   prevalence_of_bmi_>=40_kg_m²_morbid_obesity_ |   prevalence_of_bmi_>=40_kg_m²_morbid_obesity_lower_95%_uncertainty_interval |   prevalence_of_bmi_>=40_kg_m²_morbid_obesity_upper_95%_uncertainty_interval | source_file                                             |
|---:|-------:|:------|:-----------------------|:------|--------------------------------------------:|--------------------------------------------------------------------------:|--------------------------------------------------------------------------:|---------------------------------------:|---------------------------------------------------------------------:|---------------------------------------------------------------------:|----------------------------------------------------------------------------------------------------:|----------------------------------------------------------------------------------------------------------------------------------:|----------------------------------------------------------------------------------------------------------------------------------:|-------------------------------------------:|--------------------------------------------------------------------------:|--------------------------------------------------------------------------:|--------------------------------------------:|---------------------------------------------------------------------------:|---------------------------------------------------------------------------:|------------------------------------------:|-------------------------------------------------------------------------:|-------------------------------------------------------------------------:|------------------------------------------:|-------------------------------------------------------------------------:|-------------------------------------------------------------------------:|------------------------------------------:|-------------------------------------------------------------------------:|-------------------------------------------------------------------------:|------------------------------------------:|-------------------------------------------------------------------------:|-------------------------------------------------------------------------:|-----------------------------------------------:|-----------------------------------------------------------------------------:|-----------------------------------------------------------------------------:|:--------------------------------------------------------|
| 56 |   2013 | Men   | Australia              | AUS   |                                  0.00867765 |                                                                0.00654728 |                                                                 0.011325  |                               0.27209  |                                                             0.255908 |                                                             0.290129 |                                                                                            0.280768 |                                                                                                                          0.264319 |                                                                                                                          0.298609 |                                   0.960539 |                                                                  0.948933 |                                                                  0.96981  |                                   0.0187521 |                                                                  0.0160206 |                                                                  0.0216549 |                                  0.276453 |                                                                 0.260926 |                                                                 0.292326 |                                  0.424027 |                                                                 0.406257 |                                                                 0.441538 |                                  0.191664 |                                                                 0.17641  |                                                                 0.207494 |                                 0.0590274 |                                                                0.0501936 |                                                                0.0683022 |                                      0.0213982 |                                                                    0.0164305 |                                                                    0.0272599 | NCD_RisC_Lancet_2024_BMI_age_standardised_Australia.csv |
| 57 |   2014 | Men   | Australia              | AUS   |                                  0.00884146 |                                                                0.0066213  |                                                                 0.011623  |                               0.276681 |                                                             0.259801 |                                                             0.295206 |                                                                                            0.285522 |                                                                                                                          0.268723 |                                                                                                                          0.303982 |                                   0.960496 |                                                                  0.948957 |                                                                  0.97006  |                                   0.0185491 |                                                                  0.0157937 |                                                                  0.0215204 |                                  0.274336 |                                                                 0.257933 |                                                                 0.290861 |                                  0.421592 |                                                                 0.403176 |                                                                 0.439926 |                                  0.194109 |                                                                 0.178355 |                                                                 0.211071 |                                 0.0603624 |                                                                0.0511879 |                                                                0.0701607 |                                      0.0222092 |                                                                    0.016894  |                                                                    0.028348  | NCD_RisC_Lancet_2024_BMI_age_standardised_Australia.csv |
| 58 |   2015 | Men   | Australia              | AUS   |                                  0.00903003 |                                                                0.00666725 |                                                                 0.0119646 |                               0.281588 |                                                             0.263644 |                                                             0.301735 |                                                                                            0.290618 |                                                                                                                          0.272782 |                                                                                                                          0.310489 |                                   0.960405 |                                                                  0.94857  |                                                                  0.970456 |                                   0.0183575 |                                                                  0.0155142 |                                                                  0.0214778 |                                  0.271955 |                                                                 0.254544 |                                                                 0.289555 |                                  0.41907  |                                                                 0.399043 |                                                                 0.438995 |                                  0.196724 |                                                                 0.179993 |                                                                 0.214894 |                                 0.0618432 |                                                                0.0519923 |                                                                0.0723065 |                                      0.0230202 |                                                                    0.0172288 |                                                                    0.0297363 | NCD_RisC_Lancet_2024_BMI_age_standardised_Australia.csv |
| 59 |   2016 | Men   | Australia              | AUS   |                                  0.00924787 |                                                                0.00670224 |                                                                 0.0124311 |                               0.286811 |                                                             0.266882 |                                                             0.308787 |                                                                                            0.296059 |                                                                                                                          0.276269 |                                                                                                                          0.317771 |                                   0.960251 |                                                                  0.947429 |                                                                  0.970954 |                                   0.0181776 |                                                                  0.0151869 |                                                                  0.021487  |                                  0.269304 |                                                                 0.250763 |                                                                 0.288614 |                                  0.416459 |                                                                 0.394989 |                                                                 0.438166 |                                  0.199511 |                                                                 0.181247 |                                                                 0.219194 |                                 0.0634544 |                                                                0.0528999 |                                                                0.0751443 |                                      0.0238463 |                                                                    0.0174532 |                                                                    0.0314075 | NCD_RisC_Lancet_2024_BMI_age_standardised_Australia.csv |
| 60 |   2017 | Men   | Australia              | AUS   |                                  0.00949988 |                                                                0.00668443 |                                                                 0.0130954 |                               0.292209 |                                                             0.270296 |                                                             0.316051 |                                                                                            0.301709 |                                                                                                                          0.27946  |                                                                                                                          0.325806 |                                   0.960001 |                                                                  0.946211 |                                                                  0.971523 |                                   0.0180012 |                                                                  0.0147551 |                                                                  0.0217078 |                                  0.266552 |                                                                 0.24634  |                                                                 0.287747 |                                  0.413738 |                                                                 0.390043 |                                                                 0.437411 |                                  0.202363 |                                                                 0.182128 |                                                                 0.223753 |                                 0.0651595 |                                                                0.0534117 |                                                                0.0782513 |                                      0.0246869 |                                                                    0.0176176 |                                                                    0.033065  | NCD_RisC_Lancet_2024_BMI_age_standardised_Australia.csv |
| 61 |   2018 | Men   | Australia              | AUS   |                                  0.00978968 |                                                                0.00667368 |                                                                 0.0138896 |                               0.297667 |                                                             0.272733 |                                                             0.324219 |                                                                                            0.307456 |                                                                                                                          0.28267  |                                                                                                                          0.334151 |                                   0.959631 |                                                                  0.944341 |                                                                  0.972103 |                                   0.0178239 |                                                                  0.0142947 |                                                                  0.021956  |                                  0.263808 |                                                                 0.241306 |                                                                 0.287147 |                                  0.410911 |                                                                 0.384415 |                                                                 0.437231 |                                  0.205245 |                                                                 0.182577 |                                                                 0.229454 |                                 0.066887  |                                                                0.0533229 |                                                                0.0818754 |                                      0.025535  |                                                                    0.017424  |                                                                    0.0351981 | NCD_RisC_Lancet_2024_BMI_age_standardised_Australia.csv |
| 62 |   2019 | Men   | Australia              | AUS   |                                  0.0101188  |                                                                0.0066245  |                                                                 0.0147579 |                               0.30317  |                                                             0.274609 |                                                             0.333544 |                                                                                            0.313289 |                                                                                                                          0.285248 |                                                                                                                          0.34316  |                                   0.959141 |                                                                  0.942108 |                                                                  0.972915 |                                   0.0176493 |                                                                  0.0137979 |                                                                  0.0223068 |                                  0.261092 |                                                                 0.2351   |                                                                 0.28772  |                                  0.40797  |                                                                 0.378365 |                                                                 0.437408 |                                  0.20812  |                                                                 0.182806 |                                                                 0.235307 |                                 0.0686339 |                                                                0.0529859 |                                                                0.0863742 |                                      0.026416  |                                                                    0.0170497 |                                                                    0.0377272 | NCD_RisC_Lancet_2024_BMI_age_standardised_Australia.csv |
| 63 |   2020 | Men   | Australia              | AUS   |                                  0.01049    |                                                                0.00650592 |                                                                 0.0158825 |                               0.308811 |                                                             0.276308 |                                                             0.34363  |                                                                                            0.319301 |                                                                                                                          0.286753 |                                                                                                                          0.354413 |                                   0.958543 |                                                                  0.939068 |                                                                  0.973791 |                                   0.0174855 |                                                                  0.013272  |                                                                  0.0227549 |                                  0.258314 |                                                                 0.228605 |                                                                 0.288453 |                                  0.4049   |                                                                 0.371489 |                                                                 0.438836 |                                  0.211011 |                                                                 0.182499 |                                                                 0.242311 |                                 0.0704532 |                                                                0.052404  |                                                                0.0910369 |                                      0.0273471 |                                                                    0.016535  |                                                                    0.0408291 | NCD_RisC_Lancet_2024_BMI_age_standardised_Australia.csv |
| 64 |   2021 | Men   | Australia              | AUS   |                                  0.0108971  |                                                                0.00637647 |                                                                 0.0172215 |                               0.314588 |                                                             0.277136 |                                                             0.355094 |                                                                                            0.325485 |                                                                                                                          0.288127 |                                                                                                                          0.365173 |                                   0.957869 |                                                                  0.935489 |                                                                  0.975004 |                                   0.0173281 |                                                                  0.012679  |                                                                  0.0233397 |                                  0.255464 |                                                                 0.221878 |                                                                 0.289958 |                                  0.401723 |                                                                 0.363448 |                                                                 0.440088 |                                  0.213902 |                                                                 0.181329 |                                                                 0.250145 |                                 0.0723502 |                                                                0.0514852 |                                                                0.0964183 |                                      0.0283359 |                                                                    0.0159199 |                                                                    0.0444731 | NCD_RisC_Lancet_2024_BMI_age_standardised_Australia.csv |
| 65 |   2022 | Men   | Australia              | AUS   |                                  0.0113328  |                                                                0.00619101 |                                                                 0.018787  |                               0.32052  |                                                             0.277729 |                                                             0.366721 |                                                                                            0.331853 |                                                                                                                          0.288786 |                                                                                                                          0.377543 |                                   0.957154 |                                                                  0.931758 |                                                                  0.975818 |                                   0.0171755 |                                                                  0.0120389 |                                                                  0.0239324 |                                  0.252539 |                                                                 0.214793 |                                                                 0.291706 |                                  0.398432 |                                                                 0.355029 |                                                                 0.441433 |                                  0.216793 |                                                                 0.179637 |                                                                 0.257904 |                                 0.0743327 |                                                                0.0503158 |                                                                0.10299   |                                      0.0293948 |                                                                    0.0150118 |                                                                    0.0490069 | NCD_RisC_Lancet_2024_BMI_age_standardised_Australia.csv |

---

## ncd_risc_cholesterol.csv

### Dataset Overview
- Total Rows: 78
- Total Columns: 13
- Memory Usage: 0.02 MB
- Missing Values: 0
- Duplicate Rows: 0

### Column Information
| Column | Type | Non-Null | Unique | Memory (MB) | Additional Statistics |
|--------|------|-----------|---------|-------------|---------------------|
| country | object | 78 | 1 | 0.01 | Min Length: 9, Max Length: 9, Avg Length: 9 |
| sex | object | 78 | 2 | 0.00 | Min Length: 3, Max Length: 5, Avg Length: 4 |
| year | int64 | 78 | 39 | 0.00 | Mean: 1999, Std: 11.33, Min: 1980, Max: 2018, Median: 1999 |
| mean_total_cholesterol_mmol_l_ | float64 | 78 | 78 | 0.00 | Mean: 5.226, Std: 0.3142, Min: 4.619, Max: 5.632, Median: 5.27 |
| mean_total_cholesterol_lower_95%_uncertainty_interval_mmol_l_ | float64 | 78 | 78 | 0.00 | Mean: 5.042, Std: 0.3457, Min: 4.243, Max: 5.437, Median: 5.113 |
| mean_total_cholesterol_upper_95%_uncertainty_interval_mmol_l_ | float64 | 78 | 78 | 0.00 | Mean: 5.411, Std: 0.2891, Min: 4.989, Max: 5.901, Median: 5.434 |
| mean_non-hdl_cholesterol_mmol_l_ | float64 | 78 | 78 | 0.00 | Mean: 3.845, Std: 0.3692, Min: 3.107, Max: 4.345, Median: 3.901 |
| mean_non-hdl_cholesterol_lower_95%_uncertainty_interval_mmol_l_ | float64 | 78 | 78 | 0.00 | Mean: 3.73, Std: 0.3767, Min: 2.918, Max: 4.237, Median: 3.802 |
| mean_non-hdl_cholesterol_upper_95%_uncertainty_interval_mmol_l_ | float64 | 78 | 78 | 0.00 | Mean: 3.96, Std: 0.3617, Min: 3.295, Max: 4.485, Median: 4.004 |
| mean_hdl_cholesterol_mmol_l_ | float64 | 78 | 78 | 0.00 | Mean: 1.372, Std: 0.141, Min: 1.202, Max: 1.61, Median: 1.383 |
| mean_hdl_cholesterol_lower_95%_uncertainty_interval_mmol_l_ | float64 | 78 | 78 | 0.00 | Mean: 1.299, Std: 0.1358, Min: 1.141, Max: 1.484, Median: 1.283 |
| mean_hdl_cholesterol_upper_95%_uncertainty_interval_mmol_l_ | float64 | 78 | 78 | 0.00 | Mean: 1.444, Std: 0.1481, Min: 1.259, Max: 1.754, Median: 1.485 |
| source_file | object | 78 | 1 | 0.01 | Min Length: 34, Max Length: 34, Avg Length: 34 |

### Column Value Distributions

#### country

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| Australia | 78 | 100.00% |

#### sex

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| Men | 39 | 50.00% |
| Women | 39 | 50.00% |

#### year

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 1980 | 2 | 2.56% |
| 2009 | 2 | 2.56% |
| 2002 | 2 | 2.56% |
| 2003 | 2 | 2.56% |
| 2004 | 2 | 2.56% |
| 2005 | 2 | 2.56% |
| 2006 | 2 | 2.56% |
| 2007 | 2 | 2.56% |
| 2008 | 2 | 2.56% |
| 2010 | 2 | 2.56% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 1990 | 2 | 2.56% |
| 1998 | 2 | 2.56% |
| 1991 | 2 | 2.56% |
| 1992 | 2 | 2.56% |
| 1993 | 2 | 2.56% |
| 1994 | 2 | 2.56% |
| 1995 | 2 | 2.56% |
| 1996 | 2 | 2.56% |
| 1997 | 2 | 2.56% |
| 2018 | 2 | 2.56% |

#### mean_total_cholesterol_mmol_l_

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 5.59 | 1 | 1.28% |
| 5.529 | 1 | 1.28% |
| 5.327 | 1 | 1.28% |
| 5.359 | 1 | 1.28% |
| 5.391 | 1 | 1.28% |
| 5.422 | 1 | 1.28% |
| 5.451 | 1 | 1.28% |
| 5.479 | 1 | 1.28% |
| 5.505 | 1 | 1.28% |
| 5.55 | 1 | 1.28% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 4.895 | 1 | 1.28% |
| 4.928 | 1 | 1.28% |
| 4.962 | 1 | 1.28% |
| 4.996 | 1 | 1.28% |
| 5.031 | 1 | 1.28% |
| 5.066 | 1 | 1.28% |
| 5.102 | 1 | 1.28% |
| 5.138 | 1 | 1.28% |
| 5.174 | 1 | 1.28% |
| 4.701 | 1 | 1.28% |

#### mean_total_cholesterol_lower_95%_uncertainty_interval_mmol_l_

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 5.325 | 1 | 1.28% |
| 5.381 | 1 | 1.28% |
| 5.171 | 1 | 1.28% |
| 5.204 | 1 | 1.28% |
| 5.236 | 1 | 1.28% |
| 5.272 | 1 | 1.28% |
| 5.301 | 1 | 1.28% |
| 5.329 | 1 | 1.28% |
| 5.356 | 1 | 1.28% |
| 5.402 | 1 | 1.28% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 4.723 | 1 | 1.28% |
| 4.767 | 1 | 1.28% |
| 4.803 | 1 | 1.28% |
| 4.84 | 1 | 1.28% |
| 4.876 | 1 | 1.28% |
| 4.912 | 1 | 1.28% |
| 4.946 | 1 | 1.28% |
| 4.982 | 1 | 1.28% |
| 5.017 | 1 | 1.28% |
| 4.315 | 1 | 1.28% |

#### mean_total_cholesterol_upper_95%_uncertainty_interval_mmol_l_

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 5.848 | 1 | 1.28% |
| 5.672 | 1 | 1.28% |
| 5.487 | 1 | 1.28% |
| 5.519 | 1 | 1.28% |
| 5.546 | 1 | 1.28% |
| 5.572 | 1 | 1.28% |
| 5.601 | 1 | 1.28% |
| 5.626 | 1 | 1.28% |
| 5.648 | 1 | 1.28% |
| 5.697 | 1 | 1.28% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 5.06 | 1 | 1.28% |
| 5.085 | 1 | 1.28% |
| 5.116 | 1 | 1.28% |
| 5.148 | 1 | 1.28% |
| 5.181 | 1 | 1.28% |
| 5.219 | 1 | 1.28% |
| 5.254 | 1 | 1.28% |
| 5.292 | 1 | 1.28% |
| 5.33 | 1 | 1.28% |
| 5.086 | 1 | 1.28% |

#### mean_non-hdl_cholesterol_mmol_l_

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 4.326 | 1 | 1.28% |
| 4.053 | 1 | 1.28% |
| 3.834 | 1 | 1.28% |
| 3.87 | 1 | 1.28% |
| 3.905 | 1 | 1.28% |
| 3.939 | 1 | 1.28% |
| 3.971 | 1 | 1.28% |
| 4.001 | 1 | 1.28% |
| 4.029 | 1 | 1.28% |
| 4.074 | 1 | 1.28% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 3.618 | 1 | 1.28% |
| 3.656 | 1 | 1.28% |
| 3.695 | 1 | 1.28% |
| 3.734 | 1 | 1.28% |
| 3.774 | 1 | 1.28% |
| 3.815 | 1 | 1.28% |
| 3.856 | 1 | 1.28% |
| 3.898 | 1 | 1.28% |
| 3.939 | 1 | 1.28% |
| 3.107 | 1 | 1.28% |

#### mean_non-hdl_cholesterol_lower_95%_uncertainty_interval_mmol_l_

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 4.161 | 1 | 1.28% |
| 3.956 | 1 | 1.28% |
| 3.734 | 1 | 1.28% |
| 3.771 | 1 | 1.28% |
| 3.807 | 1 | 1.28% |
| 3.84 | 1 | 1.28% |
| 3.872 | 1 | 1.28% |
| 3.904 | 1 | 1.28% |
| 3.932 | 1 | 1.28% |
| 3.975 | 1 | 1.28% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 3.518 | 1 | 1.28% |
| 3.557 | 1 | 1.28% |
| 3.594 | 1 | 1.28% |
| 3.633 | 1 | 1.28% |
| 3.673 | 1 | 1.28% |
| 3.714 | 1 | 1.28% |
| 3.755 | 1 | 1.28% |
| 3.796 | 1 | 1.28% |
| 3.837 | 1 | 1.28% |
| 2.918 | 1 | 1.28% |

#### mean_non-hdl_cholesterol_upper_95%_uncertainty_interval_mmol_l_

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 4.485 | 1 | 1.28% |
| 4.151 | 1 | 1.28% |
| 3.938 | 1 | 1.28% |
| 3.973 | 1 | 1.28% |
| 4.008 | 1 | 1.28% |
| 4.04 | 1 | 1.28% |
| 4.072 | 1 | 1.28% |
| 4.1 | 1 | 1.28% |
| 4.126 | 1 | 1.28% |
| 4.174 | 1 | 1.28% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 3.723 | 1 | 1.28% |
| 3.759 | 1 | 1.28% |
| 3.796 | 1 | 1.28% |
| 3.834 | 1 | 1.28% |
| 3.874 | 1 | 1.28% |
| 3.915 | 1 | 1.28% |
| 3.958 | 1 | 1.28% |
| 4 | 1 | 1.28% |
| 4.042 | 1 | 1.28% |
| 3.295 | 1 | 1.28% |

#### mean_hdl_cholesterol_mmol_l_

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 1.231 | 1 | 1.28% |
| 1.467 | 1 | 1.28% |
| 1.475 | 1 | 1.28% |
| 1.471 | 1 | 1.28% |
| 1.468 | 1 | 1.28% |
| 1.466 | 1 | 1.28% |
| 1.465 | 1 | 1.28% |
| 1.465 | 1 | 1.28% |
| 1.466 | 1 | 1.28% |
| 1.468 | 1 | 1.28% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 1.263 | 1 | 1.28% |
| 1.26 | 1 | 1.28% |
| 1.257 | 1 | 1.28% |
| 1.253 | 1 | 1.28% |
| 1.251 | 1 | 1.28% |
| 1.247 | 1 | 1.28% |
| 1.244 | 1 | 1.28% |
| 1.24 | 1 | 1.28% |
| 1.235 | 1 | 1.28% |
| 1.61 | 1 | 1.28% |

#### mean_hdl_cholesterol_lower_95%_uncertainty_interval_mmol_l_

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 1.141 | 1 | 1.28% |
| 1.404 | 1 | 1.28% |
| 1.408 | 1 | 1.28% |
| 1.405 | 1 | 1.28% |
| 1.403 | 1 | 1.28% |
| 1.402 | 1 | 1.28% |
| 1.401 | 1 | 1.28% |
| 1.401 | 1 | 1.28% |
| 1.402 | 1 | 1.28% |
| 1.407 | 1 | 1.28% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 1.199 | 1 | 1.28% |
| 1.198 | 1 | 1.28% |
| 1.196 | 1 | 1.28% |
| 1.194 | 1 | 1.28% |
| 1.192 | 1 | 1.28% |
| 1.188 | 1 | 1.28% |
| 1.185 | 1 | 1.28% |
| 1.18 | 1 | 1.28% |
| 1.174 | 1 | 1.28% |
| 1.468 | 1 | 1.28% |

#### mean_hdl_cholesterol_upper_95%_uncertainty_interval_mmol_l_

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 1.323 | 1 | 1.28% |
| 1.526 | 1 | 1.28% |
| 1.54 | 1 | 1.28% |
| 1.535 | 1 | 1.28% |
| 1.531 | 1 | 1.28% |
| 1.529 | 1 | 1.28% |
| 1.527 | 1 | 1.28% |
| 1.526 | 1 | 1.28% |
| 1.525 | 1 | 1.28% |
| 1.527 | 1 | 1.28% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 1.328 | 1 | 1.28% |
| 1.322 | 1 | 1.28% |
| 1.317 | 1 | 1.28% |
| 1.313 | 1 | 1.28% |
| 1.31 | 1 | 1.28% |
| 1.306 | 1 | 1.28% |
| 1.303 | 1 | 1.28% |
| 1.3 | 1 | 1.28% |
| 1.294 | 1 | 1.28% |
| 1.754 | 1 | 1.28% |

#### source_file

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| NCD_RisC_Cholesterol_Australia.csv | 78 | 100.00% |

### Sample Data

First 10 Rows:
|    | country   | sex   |   year |   mean_total_cholesterol_mmol_l_ |   mean_total_cholesterol_lower_95%_uncertainty_interval_mmol_l_ |   mean_total_cholesterol_upper_95%_uncertainty_interval_mmol_l_ |   mean_non-hdl_cholesterol_mmol_l_ |   mean_non-hdl_cholesterol_lower_95%_uncertainty_interval_mmol_l_ |   mean_non-hdl_cholesterol_upper_95%_uncertainty_interval_mmol_l_ |   mean_hdl_cholesterol_mmol_l_ |   mean_hdl_cholesterol_lower_95%_uncertainty_interval_mmol_l_ |   mean_hdl_cholesterol_upper_95%_uncertainty_interval_mmol_l_ | source_file                        |
|---:|:----------|:------|-------:|---------------------------------:|----------------------------------------------------------------:|----------------------------------------------------------------:|-----------------------------------:|------------------------------------------------------------------:|------------------------------------------------------------------:|-------------------------------:|--------------------------------------------------------------:|--------------------------------------------------------------:|:-----------------------------------|
|  0 | Australia | Men   |   1980 |                          5.59002 |                                                         5.32471 |                                                         5.84822 |                            4.32566 |                                                           4.16105 |                                                           4.48471 |                        1.23097 |                                                       1.14056 |                                                       1.32347 | NCD_RisC_Cholesterol_Australia.csv |
|  1 | Australia | Men   |   1981 |                          5.58728 |                                                         5.35236 |                                                         5.81634 |                            4.33038 |                                                           4.18106 |                                                           4.47635 |                        1.22859 |                                                       1.14686 |                                                       1.31097 | NCD_RisC_Cholesterol_Australia.csv |
|  2 | Australia | Men   |   1982 |                          5.58436 |                                                         5.36721 |                                                         5.79266 |                            4.33487 |                                                           4.19861 |                                                           4.46994 |                        1.2263  |                                                       1.15292 |                                                       1.3004  | NCD_RisC_Cholesterol_Australia.csv |
|  3 | Australia | Men   |   1983 |                          5.58093 |                                                         5.38771 |                                                         5.76971 |                            4.33871 |                                                           4.2103  |                                                           4.46287 |                        1.22391 |                                                       1.15634 |                                                       1.29237 | NCD_RisC_Cholesterol_Australia.csv |
|  4 | Australia | Men   |   1984 |                          5.57715 |                                                         5.40084 |                                                         5.75034 |                            4.34211 |                                                           4.22267 |                                                           4.45898 |                        1.22142 |                                                       1.15746 |                                                       1.28604 | NCD_RisC_Cholesterol_Australia.csv |
|  5 | Australia | Men   |   1985 |                          5.57269 |                                                         5.40917 |                                                         5.73468 |                            4.34456 |                                                           4.23066 |                                                           4.45558 |                        1.21875 |                                                       1.15814 |                                                       1.28049 | NCD_RisC_Cholesterol_Australia.csv |
|  6 | Australia | Men   |   1986 |                          5.56696 |                                                         5.41495 |                                                         5.72337 |                            4.34529 |                                                           4.23612 |                                                           4.45076 |                        1.21606 |                                                       1.15722 |                                                       1.27533 | NCD_RisC_Cholesterol_Australia.csv |
|  7 | Australia | Men   |   1987 |                          5.55947 |                                                         5.41354 |                                                         5.70656 |                            4.34357 |                                                           4.23696 |                                                           4.44855 |                        1.21343 |                                                       1.15539 |                                                       1.27158 | NCD_RisC_Cholesterol_Australia.csv |
|  8 | Australia | Men   |   1988 |                          5.54959 |                                                         5.40723 |                                                         5.69108 |                            4.33861 |                                                           4.23668 |                                                           4.44163 |                        1.21078 |                                                       1.15513 |                                                       1.26729 | NCD_RisC_Cholesterol_Australia.csv |
|  9 | Australia | Men   |   1989 |                          5.5367  |                                                         5.39708 |                                                         5.67659 |                            4.32952 |                                                           4.22853 |                                                           4.43298 |                        1.20817 |                                                       1.15271 |                                                       1.26354 | NCD_RisC_Cholesterol_Australia.csv |

Last 10 Rows:
|    | country   | sex   |   year |   mean_total_cholesterol_mmol_l_ |   mean_total_cholesterol_lower_95%_uncertainty_interval_mmol_l_ |   mean_total_cholesterol_upper_95%_uncertainty_interval_mmol_l_ |   mean_non-hdl_cholesterol_mmol_l_ |   mean_non-hdl_cholesterol_lower_95%_uncertainty_interval_mmol_l_ |   mean_non-hdl_cholesterol_upper_95%_uncertainty_interval_mmol_l_ |   mean_hdl_cholesterol_mmol_l_ |   mean_hdl_cholesterol_lower_95%_uncertainty_interval_mmol_l_ |   mean_hdl_cholesterol_upper_95%_uncertainty_interval_mmol_l_ | source_file                        |
|---:|:----------|:------|-------:|---------------------------------:|----------------------------------------------------------------:|----------------------------------------------------------------:|-----------------------------------:|------------------------------------------------------------------:|------------------------------------------------------------------:|-------------------------------:|--------------------------------------------------------------:|--------------------------------------------------------------:|:-----------------------------------|
| 68 | Australia | Women |   2009 |                          4.94918 |                                                         4.79111 |                                                         5.10947 |                            3.39976 |                                                           3.29172 |                                                           3.50661 |                        1.54059 |                                                       1.4728  |                                                       1.60536 | NCD_RisC_Cholesterol_Australia.csv |
| 69 | Australia | Women |   2010 |                          4.92148 |                                                         4.75913 |                                                         5.08855 |                            3.36755 |                                                           3.25788 |                                                           3.47817 |                        1.54703 |                                                       1.4755  |                                                       1.61536 | NCD_RisC_Cholesterol_Australia.csv |
| 70 | Australia | Women |   2011 |                          4.89424 |                                                         4.72345 |                                                         5.07187 |                            3.33578 |                                                           3.22266 |                                                           3.45156 |                        1.55391 |                                                       1.47775 |                                                       1.62493 | NCD_RisC_Cholesterol_Australia.csv |
| 71 | Australia | Women |   2012 |                          4.86695 |                                                         4.68247 |                                                         5.06081 |                            3.30389 |                                                           3.18361 |                                                           3.42803 |                        1.56125 |                                                       1.4809  |                                                       1.63654 | NCD_RisC_Cholesterol_Australia.csv |
| 72 | Australia | Women |   2013 |                          4.83951 |                                                         4.63079 |                                                         5.05206 |                            3.27163 |                                                           3.1433  |                                                           3.40254 |                        1.56894 |                                                       1.48334 |                                                       1.65157 | NCD_RisC_Cholesterol_Australia.csv |
| 73 | Australia | Women |   2014 |                          4.81195 |                                                         4.58198 |                                                         5.05145 |                            3.23912 |                                                           3.10082 |                                                           3.37659 |                        1.57685 |                                                       1.48389 |                                                       1.66969 | NCD_RisC_Cholesterol_Australia.csv |
| 74 | Australia | Women |   2015 |                          4.78425 |                                                         4.52104 |                                                         5.05348 |                            3.20633 |                                                           3.05619 |                                                           3.35535 |                        1.585   |                                                       1.48207 |                                                       1.68825 | NCD_RisC_Cholesterol_Australia.csv |
| 75 | Australia | Women |   2016 |                          4.75652 |                                                         4.45876 |                                                         5.05838 |                            3.17343 |                                                           3.01222 |                                                           3.33368 |                        1.59318 |                                                       1.47816 |                                                       1.70859 | NCD_RisC_Cholesterol_Australia.csv |
| 76 | Australia | Women |   2017 |                          4.72857 |                                                         4.38454 |                                                         5.07404 |                            3.14024 |                                                           2.96562 |                                                           3.31419 |                        1.60135 |                                                       1.47377 |                                                       1.72909 | NCD_RisC_Cholesterol_Australia.csv |
| 77 | Australia | Women |   2018 |                          4.70054 |                                                         4.31533 |                                                         5.08599 |                            3.10691 |                                                           2.91827 |                                                           3.29467 |                        1.60951 |                                                       1.46828 |                                                       1.75409 | NCD_RisC_Cholesterol_Australia.csv |

---

## ncd_risc_diabetes.csv

### Dataset Overview
- Total Rows: 66
- Total Columns: 17
- Memory Usage: 0.02 MB
- Missing Values: 0
- Duplicate Rows: 0

### Column Information
| Column | Type | Non-Null | Unique | Memory (MB) | Additional Statistics |
|--------|------|-----------|---------|-------------|---------------------|
| country | object | 66 | 1 | 0.00 | Min Length: 9, Max Length: 9, Avg Length: 9 |
| iso | object | 66 | 1 | 0.00 | Min Length: 3, Max Length: 3, Avg Length: 3 |
| sex | object | 66 | 2 | 0.00 | Min Length: 3, Max Length: 5, Avg Length: 4 |
| year | int64 | 66 | 33 | 0.00 | Mean: 2006, Std: 9.595, Min: 1990, Max: 2022, Median: 2006 |
| age-standardised_prevalence_of_diabetes_18+_years_ | float64 | 66 | 66 | 0.00 | Mean: 0.05337, Std: 0.01441, Min: 0.03004, Max: 0.08356, Median: 0.05211 |
| age-standardised_prevalence_of_diabetes_18+_years_lower_95%_uncertainty_interval | float64 | 66 | 66 | 0.00 | Mean: 0.03592, Std: 0.008768, Min: 0.01935, Max: 0.05116, Median: 0.03635 |
| age-standardised_prevalence_of_diabetes_18+_years_upper_95%_uncertainty_interval | float64 | 66 | 66 | 0.00 | Mean: 0.07575, Std: 0.02905, Min: 0.04312, Max: 0.1673, Median: 0.0665 |
| age-standardised_proportion_of_people_with_diabetes_who_were_treated_30+_years_ | float64 | 66 | 66 | 0.00 | Mean: 0.558, Std: 0.0651, Min: 0.4364, Max: 0.6603, Median: 0.5631 |
| age-standardised_proportion_of_people_with_diabetes_who_were_treated_30+_years_lower_95%_uncertainty_interval | float64 | 66 | 66 | 0.00 | Mean: 0.4492, Std: 0.05258, Min: 0.3335, Max: 0.5137, Median: 0.4654 |
| age-standardised_proportion_of_people_with_diabetes_who_were_treated_30+_years_upper_95%_uncertainty_interval | float64 | 66 | 66 | 0.00 | Mean: 0.6613, Std: 0.08269, Min: 0.542, Max: 0.8364, Median: 0.643 |
| crude_prevalence_of_diabetes_18+_years_ | float64 | 66 | 66 | 0.00 | Mean: 0.06456, Std: 0.02011, Min: 0.03431, Max: 0.106, Median: 0.06208 |
| crude_prevalence_of_diabetes_18+_years_lower_95%_uncertainty_interval | float64 | 66 | 66 | 0.00 | Mean: 0.04397, Std: 0.0118, Min: 0.02228, Max: 0.06349, Median: 0.04565 |
| crude_prevalence_of_diabetes_18+_years_upper_95%_uncertainty_interval | float64 | 66 | 66 | 0.00 | Mean: 0.09042, Std: 0.03776, Min: 0.04893, Max: 0.2035, Median: 0.0779 |
| crude_proportion_of_people_with_diabetes_who_were_treated_30+_years_ | float64 | 66 | 66 | 0.00 | Mean: 0.5624, Std: 0.06929, Min: 0.4381, Max: 0.6704, Median: 0.5657 |
| crude_proportion_of_people_with_diabetes_who_were_treated_30+_years_lower_95%_uncertainty_interval | float64 | 66 | 66 | 0.00 | Mean: 0.4533, Std: 0.05548, Min: 0.335, Max: 0.5147, Median: 0.4718 |
| crude_proportion_of_people_with_diabetes_who_were_treated_30+_years_upper_95%_uncertainty_interval | float64 | 66 | 66 | 0.00 | Mean: 0.6655, Std: 0.08583, Min: 0.5436, Max: 0.8526, Median: 0.6453 |
| source_file | object | 66 | 1 | 0.01 | Min Length: 43, Max Length: 43, Avg Length: 43 |

### Column Value Distributions

#### country

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| Australia | 66 | 100.00% |

#### iso

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| AUS | 66 | 100.00% |

#### sex

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| Men | 33 | 50.00% |
| Women | 33 | 50.00% |

#### year

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 1990 | 2 | 3.03% |
| 2007 | 2 | 3.03% |
| 2021 | 2 | 3.03% |
| 2020 | 2 | 3.03% |
| 2019 | 2 | 3.03% |
| 2018 | 2 | 3.03% |
| 2017 | 2 | 3.03% |
| 2016 | 2 | 3.03% |
| 2015 | 2 | 3.03% |
| 2014 | 2 | 3.03% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 2000 | 2 | 3.03% |
| 1999 | 2 | 3.03% |
| 1998 | 2 | 3.03% |
| 1997 | 2 | 3.03% |
| 1996 | 2 | 3.03% |
| 1995 | 2 | 3.03% |
| 1994 | 2 | 3.03% |
| 1993 | 2 | 3.03% |
| 1992 | 2 | 3.03% |
| 2022 | 2 | 3.03% |

#### age-standardised_prevalence_of_diabetes_18+_years_

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.04062 | 1 | 1.52% |
| 0.04356 | 1 | 1.52% |
| 0.03176 | 1 | 1.52% |
| 0.03252 | 1 | 1.52% |
| 0.03321 | 1 | 1.52% |
| 0.03384 | 1 | 1.52% |
| 0.03439 | 1 | 1.52% |
| 0.0349 | 1 | 1.52% |
| 0.03541 | 1 | 1.52% |
| 0.03597 | 1 | 1.52% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.0656 | 1 | 1.52% |
| 0.06666 | 1 | 1.52% |
| 0.06778 | 1 | 1.52% |
| 0.06895 | 1 | 1.52% |
| 0.07017 | 1 | 1.52% |
| 0.07139 | 1 | 1.52% |
| 0.07269 | 1 | 1.52% |
| 0.07406 | 1 | 1.52% |
| 0.07554 | 1 | 1.52% |
| 0.08356 | 1 | 1.52% |

#### age-standardised_prevalence_of_diabetes_18+_years_lower_95%_uncertainty_interval

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.02752 | 1 | 1.52% |
| 0.03342 | 1 | 1.52% |
| 0.02066 | 1 | 1.52% |
| 0.02119 | 1 | 1.52% |
| 0.02162 | 1 | 1.52% |
| 0.02229 | 1 | 1.52% |
| 0.02299 | 1 | 1.52% |
| 0.02366 | 1 | 1.52% |
| 0.02447 | 1 | 1.52% |
| 0.02544 | 1 | 1.52% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.05116 | 1 | 1.52% |
| 0.0507 | 1 | 1.52% |
| 0.04957 | 1 | 1.52% |
| 0.04857 | 1 | 1.52% |
| 0.04676 | 1 | 1.52% |
| 0.04516 | 1 | 1.52% |
| 0.04332 | 1 | 1.52% |
| 0.04124 | 1 | 1.52% |
| 0.03878 | 1 | 1.52% |
| 0.02992 | 1 | 1.52% |

#### age-standardised_prevalence_of_diabetes_18+_years_upper_95%_uncertainty_interval

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.05595 | 1 | 1.52% |
| 0.05526 | 1 | 1.52% |
| 0.04583 | 1 | 1.52% |
| 0.04673 | 1 | 1.52% |
| 0.04757 | 1 | 1.52% |
| 0.04804 | 1 | 1.52% |
| 0.04793 | 1 | 1.52% |
| 0.04816 | 1 | 1.52% |
| 0.04832 | 1 | 1.52% |
| 0.04859 | 1 | 1.52% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.08182 | 1 | 1.52% |
| 0.08469 | 1 | 1.52% |
| 0.08905 | 1 | 1.52% |
| 0.09326 | 1 | 1.52% |
| 0.09875 | 1 | 1.52% |
| 0.1048 | 1 | 1.52% |
| 0.1111 | 1 | 1.52% |
| 0.1193 | 1 | 1.52% |
| 0.1279 | 1 | 1.52% |
| 0.1673 | 1 | 1.52% |

#### age-standardised_proportion_of_people_with_diabetes_who_were_treated_30+_years_

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.4364 | 1 | 1.52% |
| 0.5723 | 1 | 1.52% |
| 0.4794 | 1 | 1.52% |
| 0.4846 | 1 | 1.52% |
| 0.49 | 1 | 1.52% |
| 0.4956 | 1 | 1.52% |
| 0.5016 | 1 | 1.52% |
| 0.5078 | 1 | 1.52% |
| 0.5143 | 1 | 1.52% |
| 0.5212 | 1 | 1.52% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.5943 | 1 | 1.52% |
| 0.6009 | 1 | 1.52% |
| 0.6071 | 1 | 1.52% |
| 0.613 | 1 | 1.52% |
| 0.6187 | 1 | 1.52% |
| 0.6241 | 1 | 1.52% |
| 0.6292 | 1 | 1.52% |
| 0.6341 | 1 | 1.52% |
| 0.6387 | 1 | 1.52% |
| 0.6603 | 1 | 1.52% |

#### age-standardised_proportion_of_people_with_diabetes_who_were_treated_30+_years_lower_95%_uncertainty_interval

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.3335 | 1 | 1.52% |
| 0.4849 | 1 | 1.52% |
| 0.3736 | 1 | 1.52% |
| 0.3798 | 1 | 1.52% |
| 0.3874 | 1 | 1.52% |
| 0.3953 | 1 | 1.52% |
| 0.4029 | 1 | 1.52% |
| 0.4122 | 1 | 1.52% |
| 0.4202 | 1 | 1.52% |
| 0.4285 | 1 | 1.52% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.5008 | 1 | 1.52% |
| 0.4998 | 1 | 1.52% |
| 0.4996 | 1 | 1.52% |
| 0.4976 | 1 | 1.52% |
| 0.4935 | 1 | 1.52% |
| 0.4868 | 1 | 1.52% |
| 0.4788 | 1 | 1.52% |
| 0.4714 | 1 | 1.52% |
| 0.4604 | 1 | 1.52% |
| 0.4569 | 1 | 1.52% |

#### age-standardised_proportion_of_people_with_diabetes_who_were_treated_30+_years_upper_95%_uncertainty_interval

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.542 | 1 | 1.52% |
| 0.6525 | 1 | 1.52% |
| 0.5831 | 1 | 1.52% |
| 0.5871 | 1 | 1.52% |
| 0.5909 | 1 | 1.52% |
| 0.5951 | 1 | 1.52% |
| 0.5985 | 1 | 1.52% |
| 0.6031 | 1 | 1.52% |
| 0.606 | 1 | 1.52% |
| 0.6098 | 1 | 1.52% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.6839 | 1 | 1.52% |
| 0.697 | 1 | 1.52% |
| 0.7094 | 1 | 1.52% |
| 0.7235 | 1 | 1.52% |
| 0.7371 | 1 | 1.52% |
| 0.7533 | 1 | 1.52% |
| 0.7688 | 1 | 1.52% |
| 0.7856 | 1 | 1.52% |
| 0.8036 | 1 | 1.52% |
| 0.8326 | 1 | 1.52% |

#### crude_prevalence_of_diabetes_18+_years_

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.04133 | 1 | 1.52% |
| 0.05418 | 1 | 1.52% |
| 0.03654 | 1 | 1.52% |
| 0.03762 | 1 | 1.52% |
| 0.03864 | 1 | 1.52% |
| 0.03959 | 1 | 1.52% |
| 0.04049 | 1 | 1.52% |
| 0.04139 | 1 | 1.52% |
| 0.04232 | 1 | 1.52% |
| 0.04329 | 1 | 1.52% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.08062 | 1 | 1.52% |
| 0.08246 | 1 | 1.52% |
| 0.08443 | 1 | 1.52% |
| 0.0865 | 1 | 1.52% |
| 0.08859 | 1 | 1.52% |
| 0.09063 | 1 | 1.52% |
| 0.09276 | 1 | 1.52% |
| 0.09518 | 1 | 1.52% |
| 0.09821 | 1 | 1.52% |
| 0.106 | 1 | 1.52% |

#### crude_prevalence_of_diabetes_18+_years_lower_95%_uncertainty_interval

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.02807 | 1 | 1.52% |
| 0.04211 | 1 | 1.52% |
| 0.02393 | 1 | 1.52% |
| 0.02471 | 1 | 1.52% |
| 0.02548 | 1 | 1.52% |
| 0.02636 | 1 | 1.52% |
| 0.02734 | 1 | 1.52% |
| 0.02837 | 1 | 1.52% |
| 0.02966 | 1 | 1.52% |
| 0.03097 | 1 | 1.52% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.06345 | 1 | 1.52% |
| 0.06349 | 1 | 1.52% |
| 0.06261 | 1 | 1.52% |
| 0.06184 | 1 | 1.52% |
| 0.0602 | 1 | 1.52% |
| 0.05842 | 1 | 1.52% |
| 0.05664 | 1 | 1.52% |
| 0.05448 | 1 | 1.52% |
| 0.05216 | 1 | 1.52% |
| 0.04089 | 1 | 1.52% |

#### crude_prevalence_of_diabetes_18+_years_upper_95%_uncertainty_interval

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.05685 | 1 | 1.52% |
| 0.06823 | 1 | 1.52% |
| 0.05226 | 1 | 1.52% |
| 0.05336 | 1 | 1.52% |
| 0.0547 | 1 | 1.52% |
| 0.05566 | 1 | 1.52% |
| 0.05586 | 1 | 1.52% |
| 0.05656 | 1 | 1.52% |
| 0.05699 | 1 | 1.52% |
| 0.05777 | 1 | 1.52% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.09933 | 1 | 1.52% |
| 0.1039 | 1 | 1.52% |
| 0.1092 | 1 | 1.52% |
| 0.1156 | 1 | 1.52% |
| 0.1227 | 1 | 1.52% |
| 0.1305 | 1 | 1.52% |
| 0.1383 | 1 | 1.52% |
| 0.1484 | 1 | 1.52% |
| 0.1604 | 1 | 1.52% |
| 0.2035 | 1 | 1.52% |

#### crude_proportion_of_people_with_diabetes_who_were_treated_30+_years_

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.4381 | 1 | 1.52% |
| 0.5695 | 1 | 1.52% |
| 0.4763 | 1 | 1.52% |
| 0.4813 | 1 | 1.52% |
| 0.4864 | 1 | 1.52% |
| 0.4919 | 1 | 1.52% |
| 0.4977 | 1 | 1.52% |
| 0.5038 | 1 | 1.52% |
| 0.5103 | 1 | 1.52% |
| 0.517 | 1 | 1.52% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.607 | 1 | 1.52% |
| 0.6145 | 1 | 1.52% |
| 0.6218 | 1 | 1.52% |
| 0.6288 | 1 | 1.52% |
| 0.6356 | 1 | 1.52% |
| 0.6421 | 1 | 1.52% |
| 0.6483 | 1 | 1.52% |
| 0.6542 | 1 | 1.52% |
| 0.66 | 1 | 1.52% |
| 0.6667 | 1 | 1.52% |

#### crude_proportion_of_people_with_diabetes_who_were_treated_30+_years_lower_95%_uncertainty_interval

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.335 | 1 | 1.52% |
| 0.4837 | 1 | 1.52% |
| 0.3702 | 1 | 1.52% |
| 0.3755 | 1 | 1.52% |
| 0.3842 | 1 | 1.52% |
| 0.3918 | 1 | 1.52% |
| 0.3987 | 1 | 1.52% |
| 0.4064 | 1 | 1.52% |
| 0.414 | 1 | 1.52% |
| 0.4232 | 1 | 1.52% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.5127 | 1 | 1.52% |
| 0.5142 | 1 | 1.52% |
| 0.5147 | 1 | 1.52% |
| 0.5131 | 1 | 1.52% |
| 0.5105 | 1 | 1.52% |
| 0.5037 | 1 | 1.52% |
| 0.4972 | 1 | 1.52% |
| 0.4907 | 1 | 1.52% |
| 0.4812 | 1 | 1.52% |
| 0.4639 | 1 | 1.52% |

#### crude_proportion_of_people_with_diabetes_who_were_treated_30+_years_upper_95%_uncertainty_interval

Top 10 Most Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.5436 | 1 | 1.52% |
| 0.6518 | 1 | 1.52% |
| 0.5828 | 1 | 1.52% |
| 0.586 | 1 | 1.52% |
| 0.5906 | 1 | 1.52% |
| 0.5937 | 1 | 1.52% |
| 0.5969 | 1 | 1.52% |
| 0.6012 | 1 | 1.52% |
| 0.6042 | 1 | 1.52% |
| 0.6072 | 1 | 1.52% |

Bottom 10 Least Frequent Values:
| Value | Count | Percentage |
|-------|--------|------------|
| 0.6952 | 1 | 1.52% |
| 0.708 | 1 | 1.52% |
| 0.7228 | 1 | 1.52% |
| 0.7366 | 1 | 1.52% |
| 0.7515 | 1 | 1.52% |
| 0.7678 | 1 | 1.52% |
| 0.784 | 1 | 1.52% |
| 0.8002 | 1 | 1.52% |
| 0.8192 | 1 | 1.52% |
| 0.8376 | 1 | 1.52% |

#### source_file

All Unique Values:
| Value | Count | Percentage |
|-------|--------|------------|
| NCD_RisC_Lancet_2024_Diabetes_Australia.csv | 66 | 100.00% |

### Sample Data

First 10 Rows:
|    | country   | iso   | sex   |   year |   age-standardised_prevalence_of_diabetes_18+_years_ |   age-standardised_prevalence_of_diabetes_18+_years_lower_95%_uncertainty_interval |   age-standardised_prevalence_of_diabetes_18+_years_upper_95%_uncertainty_interval |   age-standardised_proportion_of_people_with_diabetes_who_were_treated_30+_years_ |   age-standardised_proportion_of_people_with_diabetes_who_were_treated_30+_years_lower_95%_uncertainty_interval |   age-standardised_proportion_of_people_with_diabetes_who_were_treated_30+_years_upper_95%_uncertainty_interval |   crude_prevalence_of_diabetes_18+_years_ |   crude_prevalence_of_diabetes_18+_years_lower_95%_uncertainty_interval |   crude_prevalence_of_diabetes_18+_years_upper_95%_uncertainty_interval |   crude_proportion_of_people_with_diabetes_who_were_treated_30+_years_ |   crude_proportion_of_people_with_diabetes_who_were_treated_30+_years_lower_95%_uncertainty_interval |   crude_proportion_of_people_with_diabetes_who_were_treated_30+_years_upper_95%_uncertainty_interval | source_file                                 |
|---:|:----------|:------|:------|-------:|-----------------------------------------------------:|-----------------------------------------------------------------------------------:|-----------------------------------------------------------------------------------:|----------------------------------------------------------------------------------:|----------------------------------------------------------------------------------------------------------------:|----------------------------------------------------------------------------------------------------------------:|------------------------------------------:|------------------------------------------------------------------------:|------------------------------------------------------------------------:|-----------------------------------------------------------------------:|-----------------------------------------------------------------------------------------------------:|-----------------------------------------------------------------------------------------------------:|:--------------------------------------------|
|  0 | Australia | AUS   | Men   |   1990 |                                            0.0406242 |                                                                          0.0275236 |                                                                          0.0559548 |                                                                          0.436363 |                                                                                                        0.333477 |                                                                                                        0.541995 |                                 0.041331  |                                                               0.0280736 |                                                               0.0568454 |                                                               0.438135 |                                                                                             0.335002 |                                                                                             0.543589 | NCD_RisC_Lancet_2024_Diabetes_Australia.csv |
|  1 | Australia | AUS   | Men   |   1991 |                                            0.0418022 |                                                                          0.028482  |                                                                          0.0575209 |                                                                          0.441417 |                                                                                                        0.340009 |                                                                                                        0.546162 |                                 0.0428193 |                                                               0.0292139 |                                                               0.058821  |                                                               0.443353 |                                                                                             0.341892 |                                                                                             0.547676 | NCD_RisC_Lancet_2024_Diabetes_Australia.csv |
|  2 | Australia | AUS   | Men   |   1992 |                                            0.0429494 |                                                                          0.0294751 |                                                                          0.0591801 |                                                                          0.446832 |                                                                                                        0.347248 |                                                                                                        0.549039 |                                 0.0443567 |                                                               0.0305113 |                                                               0.0609106 |                                                               0.448943 |                                                                                             0.349352 |                                                                                             0.551284 | NCD_RisC_Lancet_2024_Diabetes_Australia.csv |
|  3 | Australia | AUS   | Men   |   1993 |                                            0.044073  |                                                                          0.0303606 |                                                                          0.0604571 |                                                                          0.452608 |                                                                                                        0.353349 |                                                                                                        0.552929 |                                 0.0459272 |                                                               0.0317547 |                                                               0.0628079 |                                                               0.4549   |                                                                                             0.355754 |                                                                                             0.554813 | NCD_RisC_Lancet_2024_Diabetes_Australia.csv |
|  4 | Australia | AUS   | Men   |   1994 |                                            0.0451564 |                                                                          0.0314183 |                                                                          0.0618482 |                                                                          0.458758 |                                                                                                        0.359884 |                                                                                                        0.556856 |                                 0.047495  |                                                               0.033212  |                                                               0.0648844 |                                                               0.461243 |                                                                                             0.362425 |                                                                                             0.559268 | NCD_RisC_Lancet_2024_Diabetes_Australia.csv |
|  5 | Australia | AUS   | Men   |   1995 |                                            0.0462003 |                                                                          0.0325111 |                                                                          0.0630256 |                                                                          0.465263 |                                                                                                        0.369493 |                                                                                                        0.561164 |                                 0.0490442 |                                                               0.0346417 |                                                               0.0666184 |                                                               0.467953 |                                                                                             0.370414 |                                                                                             0.563862 | NCD_RisC_Lancet_2024_Diabetes_Australia.csv |
|  6 | Australia | AUS   | Men   |   1996 |                                            0.0471933 |                                                                          0.0336215 |                                                                          0.0636909 |                                                                          0.472189 |                                                                                                        0.378522 |                                                                                                        0.566292 |                                 0.0506288 |                                                               0.0361978 |                                                               0.0682062 |                                                               0.475159 |                                                                                             0.380689 |                                                                                             0.569639 | NCD_RisC_Lancet_2024_Diabetes_Australia.csv |
|  7 | Australia | AUS   | Men   |   1997 |                                            0.048154  |                                                                          0.0349273 |                                                                          0.0644311 |                                                                          0.479514 |                                                                                                        0.387949 |                                                                                                        0.571817 |                                 0.0523095 |                                                               0.0381075 |                                                               0.0697074 |                                                               0.482845 |                                                                                             0.390844 |                                                                                             0.575367 | NCD_RisC_Lancet_2024_Diabetes_Australia.csv |
|  8 | Australia | AUS   | Men   |   1998 |                                            0.0491067 |                                                                          0.0361959 |                                                                          0.0647154 |                                                                          0.487178 |                                                                                                        0.397568 |                                                                                                        0.577022 |                                 0.0540524 |                                                               0.0399565 |                                                               0.071011  |                                                               0.490901 |                                                                                             0.401108 |                                                                                             0.5814   | NCD_RisC_Lancet_2024_Diabetes_Australia.csv |
|  9 | Australia | AUS   | Men   |   1999 |                                            0.0500715 |                                                                          0.0373092 |                                                                          0.0651962 |                                                                          0.495214 |                                                                                                        0.408159 |                                                                                                        0.582486 |                                 0.0558082 |                                                               0.0417131 |                                                               0.0723181 |                                                               0.499346 |                                                                                             0.412367 |                                                                                             0.58721  | NCD_RisC_Lancet_2024_Diabetes_Australia.csv |

Last 10 Rows:
|    | country   | iso   | sex   |   year |   age-standardised_prevalence_of_diabetes_18+_years_ |   age-standardised_prevalence_of_diabetes_18+_years_lower_95%_uncertainty_interval |   age-standardised_prevalence_of_diabetes_18+_years_upper_95%_uncertainty_interval |   age-standardised_proportion_of_people_with_diabetes_who_were_treated_30+_years_ |   age-standardised_proportion_of_people_with_diabetes_who_were_treated_30+_years_lower_95%_uncertainty_interval |   age-standardised_proportion_of_people_with_diabetes_who_were_treated_30+_years_upper_95%_uncertainty_interval |   crude_prevalence_of_diabetes_18+_years_ |   crude_prevalence_of_diabetes_18+_years_lower_95%_uncertainty_interval |   crude_prevalence_of_diabetes_18+_years_upper_95%_uncertainty_interval |   crude_proportion_of_people_with_diabetes_who_were_treated_30+_years_ |   crude_proportion_of_people_with_diabetes_who_were_treated_30+_years_lower_95%_uncertainty_interval |   crude_proportion_of_people_with_diabetes_who_were_treated_30+_years_upper_95%_uncertainty_interval | source_file                                 |
|---:|:----------|:------|:------|-------:|-----------------------------------------------------:|-----------------------------------------------------------------------------------:|-----------------------------------------------------------------------------------:|----------------------------------------------------------------------------------:|----------------------------------------------------------------------------------------------------------------:|----------------------------------------------------------------------------------------------------------------:|------------------------------------------:|------------------------------------------------------------------------:|------------------------------------------------------------------------:|-----------------------------------------------------------------------:|-----------------------------------------------------------------------------------------------------:|-----------------------------------------------------------------------------------------------------:|:--------------------------------------------|
| 56 | Australia | AUS   | Women |   2013 |                                            0.0554599 |                                                                          0.0404924 |                                                                          0.0738787 |                                                                          0.617093 |                                                                                                        0.513701 |                                                                                                        0.716423 |                                 0.0693966 |                                                               0.0512792 |                                                               0.0908052 |                                                               0.618249 |                                                                                             0.514237 |                                                                                             0.717533 | NCD_RisC_Lancet_2024_Diabetes_Australia.csv |
| 57 | Australia | AUS   | Women |   2014 |                                            0.0574382 |                                                                          0.0405341 |                                                                          0.0784556 |                                                                          0.62288  |                                                                                                        0.512932 |                                                                                                        0.728112 |                                 0.0719507 |                                                               0.0516146 |                                                               0.0966203 |                                                               0.624686 |                                                                                             0.514065 |                                                                                             0.729839 | NCD_RisC_Lancet_2024_Diabetes_Australia.csv |
| 58 | Australia | AUS   | Women |   2015 |                                            0.0596873 |                                                                          0.0398275 |                                                                          0.0849377 |                                                                          0.628396 |                                                                                                        0.50987  |                                                                                                        0.738864 |                                 0.0748284 |                                                               0.0511548 |                                                               0.104231  |                                                               0.630851 |                                                                                             0.511516 |                                                                                             0.742737 | NCD_RisC_Lancet_2024_Diabetes_Australia.csv |
| 59 | Australia | AUS   | Women |   2016 |                                            0.0622382 |                                                                          0.038922  |                                                                          0.092715  |                                                                          0.63366  |                                                                                                        0.505348 |                                                                                                        0.751239 |                                 0.0780463 |                                                               0.0502679 |                                                               0.11388   |                                                               0.636742 |                                                                                             0.508425 |                                                                                             0.755072 | NCD_RisC_Lancet_2024_Diabetes_Australia.csv |
| 60 | Australia | AUS   | Women |   2017 |                                            0.0650861 |                                                                          0.0378332 |                                                                          0.101625  |                                                                          0.638658 |                                                                                                        0.498959 |                                                                                                        0.763932 |                                 0.0815979 |                                                               0.048771  |                                                               0.123833  |                                                               0.64234  |                                                                                             0.503597 |                                                                                             0.767333 | NCD_RisC_Lancet_2024_Diabetes_Australia.csv |
| 61 | Australia | AUS   | Women |   2018 |                                            0.0682487 |                                                                          0.036413  |                                                                          0.111433  |                                                                          0.643409 |                                                                                                        0.494528 |                                                                                                        0.776221 |                                 0.0855671 |                                                               0.0472179 |                                                               0.135625  |                                                               0.647665 |                                                                                             0.496986 |                                                                                             0.780837 | NCD_RisC_Lancet_2024_Diabetes_Australia.csv |
| 62 | Australia | AUS   | Women |   2019 |                                            0.0717034 |                                                                          0.0348631 |                                                                          0.122724  |                                                                          0.647956 |                                                                                                        0.487949 |                                                                                                        0.790311 |                                 0.0900538 |                                                               0.046028  |                                                               0.149981  |                                                               0.652791 |                                                                                             0.48989  |                                                                                             0.794147 | NCD_RisC_Lancet_2024_Diabetes_Australia.csv |
| 63 | Australia | AUS   | Women |   2020 |                                            0.075397  |                                                                          0.0333886 |                                                                          0.135254  |                                                                          0.652339 |                                                                                                        0.479076 |                                                                                                        0.804257 |                                 0.0951428 |                                                               0.0444901 |                                                               0.165008  |                                                               0.657753 |                                                                                             0.481201 |                                                                                             0.809029 | NCD_RisC_Lancet_2024_Diabetes_Australia.csv |
| 64 | Australia | AUS   | Women |   2021 |                                            0.0793434 |                                                                          0.031884  |                                                                          0.149746  |                                                                          0.656473 |                                                                                                        0.468478 |                                                                                                        0.819473 |                                 0.100554  |                                                               0.0430658 |                                                               0.183541  |                                                               0.662404 |                                                                                             0.472951 |                                                                                             0.823947 | NCD_RisC_Lancet_2024_Diabetes_Australia.csv |
| 65 | Australia | AUS   | Women |   2022 |                                            0.0835641 |                                                                          0.0299152 |                                                                          0.167299  |                                                                          0.660317 |                                                                                                        0.45688  |                                                                                                        0.832587 |                                 0.105989  |                                                               0.0408926 |                                                               0.203481  |                                                               0.666683 |                                                                                             0.463944 |                                                                                             0.837639 | NCD_RisC_Lancet_2024_Diabetes_Australia.csv |

---
