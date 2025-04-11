"""
Models for validating AIHW health data.

The models handle various types of health statistics from AIHW Excel files,
including prevalence, mortality, and other health metrics.
"""
from enum import Enum
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, ConfigDict

class MetricType(str, Enum):
    """Types of health metrics in AIHW data.

    Includes number, rate, percentage, crude rate, standardised rate,
    prevalence, mortality, and incidence. All values use Australian English spelling.
    """
    NUMBER = "number"
    RATE = "rate"
    PERCENTAGE = "percentage"
    CRUDE_RATE = "crude_rate"
    STANDARDISED_RATE = "standardised_rate"
    PREVALENCE = "prevalence"
    MORTALITY = "mortality"
    INCIDENCE = "incidence"

class AIHWRecord(BaseModel):
    """A single record of AIHW health data."""
    
    # Required fields
    year: int = Field(..., description="Year of the data point", le=2025)
    value: float = Field(..., description="The numeric value of the metric")
    metric_type: MetricType = Field(..., description="Type of metric (e.g. number, rate)")
    source_sheet: str = Field(..., description="Sheet name in Excel file")
    
    # Demographic fields (all optional)
    sex: Optional[str] = Field(None, description="Sex category (male, female, persons)")
    age_group: Optional[str] = Field(None, description="Age group (e.g. 30-59, 60-64)")
    region: Optional[str] = Field(None, description="Geographic region")
    indigenous_status: Optional[str] = Field(None, description="Indigenous status if applicable")
    condition: Optional[str] = Field(None, description="Health condition being measured")
    
    # Additional metadata
    table_name: Optional[str] = Field(None, description="Name of the table in the sheet")
    notes: Optional[List[str]] = Field(None, description="Any notes associated with the data point")
    
    @field_validator('sex')
    def validate_sex(cls, v):
        """Standardise sex values."""
        if not v:
            return None
        v = v.lower().strip()
        if v in ['m', 'male', 'males', 'men']:
            return 'male'
        if v in ['f', 'female', 'females', 'women']:
            return 'female'
        if v in ['p', 'person', 'persons', 'people', 'all']:
            return 'persons'
        return v
    
    @field_validator('age_group')
    def validate_age_group(cls, v):
        """Standardise age group format."""
        if not v:
            return None
        v = v.lower().strip()
        if v == 'total':
            return 'all_ages'
        # Convert various formats to standard
        v = v.replace('years', '').replace('yrs', '').strip()
        v = v.replace(' ', '').replace('–', '-')  # standardise dash
        return v
    
    @field_validator('value')
    def validate_value(cls, v):
        """Ensure value is numeric and non-negative."""
        if v is None:
            raise ValueError("Value cannot be None")
        try:
            v = float(v)
            if v < 0:
                raise ValueError("Value cannot be negative")
            return v
        except (TypeError, ValueError):
            raise ValueError("Value must be a non-negative number")

class AIHWDataset(BaseModel):
    """A collection of AIHW health records."""
    
    records: List[AIHWRecord] = Field(..., description="List of AIHW records")
    source_file: str = Field(..., description="Name of the source Excel file")
    processed_date: datetime = Field(default_factory=datetime.now, description="When the data was processed")
    
    model_config: ConfigDict = ConfigDict(
        json_schema_extra={
            "example": {
                "records": [{
                    "year": 2023,
                    "value": 10306.0,
                    "metric_type": "number",
                    "source_sheet": "S2.1",
                    "sex": "male",
                    "age_group": "60-64",
                    "condition": "dementia",
                    "table_name": "Prevalence of dementia in 2023"
                }],
                "source_file": "AIHW-DEM-02-S2-Prevalence.xlsx",
                "processed_date": "2024-04-05T11:57:51"
            }
        }
    )