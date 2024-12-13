import logging
import pandas as pd
from datetime import datetime
from dateutil.parser import parse

class SchemaInferrer:
    def __init__(self):
        self.date_formats = [
            '%Y-%m-%d',
            '%m/%d/%Y',
            '%d/%m/%Y',
            '%Y/%m/%d',
            '%m-%d-%Y',
            '%d-%m-%Y',
        ]
        
    def infer_and_apply_schema(self, df: pd.DataFrame) -> pd.DataFrame:
        """Infer and apply schema to the dataframe."""
        for column in df.columns:
            df[column] = self._infer_and_convert_column(df[column])
            
        return df
        
    def _infer_and_convert_column(self, series: pd.Series) -> pd.Series:
        """Infer and convert a single column to the appropriate type."""
        # Skip if the series is empty
        if series.empty:
            return series
            
        # Try numeric conversion first
        try:
            # Check if all values (excluding NaN) are integers
            non_null = series.dropna()
            if non_null.apply(lambda x: float(x).is_integer()).all():
                return pd.to_numeric(series, errors='coerce').astype('Int64')
            
            # Try float conversion
            return pd.to_numeric(series, errors='coerce')
        except:
            pass
            
        # Try date conversion
        try:
            return self._convert_dates(series)
        except:
            pass
            
        # Default to string
        return series.astype(str)
        
    def _convert_dates(self, series: pd.Series) -> pd.Series:
        """Convert a series to datetime, handling multiple formats."""
        # First try pandas automatic parsing
        try:
            return pd.to_datetime(series)
        except:
            pass
            
        # Try our known formats
        for date_format in self.date_formats:
            try:
                return pd.to_datetime(series, format=date_format)
            except:
                continue
                
        # If all else fails, try parsing each value individually
        def safe_parse_date(value):
            try:
                return parse(str(value))
            except:
                return pd.NaT
                
        parsed_series = series.apply(safe_parse_date)
        if not parsed_series.isna().all():
            return parsed_series
            
        raise ValueError("Could not parse as dates") 