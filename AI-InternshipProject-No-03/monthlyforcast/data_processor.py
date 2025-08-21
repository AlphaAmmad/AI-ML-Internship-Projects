import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re

class DataProcessor:
    def __init__(self):
        self.required_columns = ['Month', 'Miscellaneous', 'Financial', 'CapEx', 'COGS', 'Operating', 'Total']
        self.expense_columns = ['Miscellaneous', 'Financial', 'CapEx', 'COGS', 'Operating', 'Total']
    
    def process_csv(self, filepath):
        """
        Process and validate CSV file
        Returns: (processed_dataframe, validation_results)
        """
        validation_results = {
            'is_valid': False,
            'errors': [],
            'warnings': [],
            'data_info': {}
        }
        
        try:
            # Read CSV file
            df = pd.read_csv(filepath)
            
            # Validate structure
            structure_valid, structure_errors = self._validate_structure(df)
            if not structure_valid:
                validation_results['errors'].extend(structure_errors)
                return None, validation_results
            
            # Clean and process data
            df_cleaned = self._clean_data(df, validation_results)
            
            # Validate data quality
            quality_valid, quality_errors, quality_warnings = self._validate_data_quality(df_cleaned)
            validation_results['errors'].extend(quality_errors)
            validation_results['warnings'].extend(quality_warnings)
            
            if quality_errors:
                return None, validation_results
            
            # Sort by date
            df_cleaned = df_cleaned.sort_values('Month').reset_index(drop=True)
            
            # Add data info
            validation_results['data_info'] = {
                'total_records': len(df_cleaned),
                'date_range': f"{df_cleaned['Month'].min()} to {df_cleaned['Month'].max()}",
                'missing_values_filled': validation_results.get('missing_filled', 0)
            }
            
            validation_results['is_valid'] = True
            return df_cleaned, validation_results
            
        except Exception as e:
            validation_results['errors'].append(f"Error reading CSV file: {str(e)}")
            return None, validation_results
    
    def _validate_structure(self, df):
        """Validate CSV structure and columns"""
        errors = []
        
        # Check if dataframe is empty
        if df.empty:
            errors.append("CSV file is empty")
            return False, errors
        
        # Check for required columns
        missing_columns = set(self.required_columns) - set(df.columns)
        if missing_columns:
            errors.append(f"Missing required columns: {', '.join(missing_columns)}")
        
        # Check for extra columns (warn but don't fail)
        extra_columns = set(df.columns) - set(self.required_columns)
        if extra_columns:
            # This is just a warning, not an error
            pass
        
        # Check minimum number of records
        if len(df) < 12:
            errors.append("CSV must contain at least 12 months of data for meaningful forecasting")
        
        return len(errors) == 0, errors
    
    def _clean_data(self, df, validation_results):
        """Clean and preprocess the data"""
        df_clean = df.copy()
        missing_filled = 0
        
        # Clean column names (remove extra spaces, standardize case)
        df_clean.columns = df_clean.columns.str.strip()
        
        # Process Month column
        df_clean['Month'] = self._process_date_column(df_clean['Month'])
        
        # Process expense columns
        for col in self.expense_columns:
            if col in df_clean.columns:
                # Convert to numeric, handling various formats
                df_clean[col] = self._clean_numeric_column(df_clean[col])
                
                # Fill missing values with interpolation
                missing_count = df_clean[col].isnull().sum()
                if missing_count > 0:
                    df_clean[col] = df_clean[col].interpolate(method='linear')
                    missing_filled += missing_count
        
        # Recalculate Total if it doesn't match sum of categories
        calculated_total = df_clean[['Miscellaneous', 'Financial', 'CapEx', 'COGS', 'Operating']].sum(axis=1)
        total_diff = abs(df_clean['Total'] - calculated_total)
        
        # If difference is significant (>1% or >100), recalculate
        if (total_diff > calculated_total * 0.01).any() or (total_diff > 100).any():
            df_clean['Total'] = calculated_total
            validation_results['warnings'].append("Total column recalculated from category sums")
        
        validation_results['missing_filled'] = missing_filled
        return df_clean
    
    def _process_date_column(self, date_series):
        """Process and standardize date column"""
        processed_dates = []
        
        for date_val in date_series:
            try:
                # Handle various date formats
                if pd.isna(date_val):
                    processed_dates.append(pd.NaT)
                    continue
                
                # Convert to string for processing
                date_str = str(date_val).strip()
                
                # Try different date formats
                date_formats = [
                    '%Y-%m-%d',
                    '%Y-%m-%d %H:%M:%S',
                    '%m/%d/%Y',
                    '%d/%m/%Y',
                    '%Y-%m',
                    '%m/%Y',
                    '%B %Y',
                    '%b %Y'
                ]
                
                parsed_date = None
                for fmt in date_formats:
                    try:
                        parsed_date = pd.to_datetime(date_str, format=fmt)
                        break
                    except:
                        continue
                
                if parsed_date is None:
                    # Try pandas automatic parsing as last resort
                    parsed_date = pd.to_datetime(date_str, errors='coerce')
                
                processed_dates.append(parsed_date)
                
            except Exception:
                processed_dates.append(pd.NaT)
        
        return pd.Series(processed_dates)
    
    def _clean_numeric_column(self, series):
        """Clean numeric columns, handling various formats"""
        cleaned_values = []
        
        for val in series:
            try:
                if pd.isna(val):
                    cleaned_values.append(np.nan)
                    continue
                
                # Convert to string for cleaning
                val_str = str(val).strip()
                
                # Remove common non-numeric characters
                val_str = re.sub(r'[$,\s]', '', val_str)
                
                # Handle parentheses (negative values)
                if val_str.startswith('(') and val_str.endswith(')'):
                    val_str = '-' + val_str[1:-1]
                
                # Convert to float
                cleaned_val = float(val_str)
                cleaned_values.append(cleaned_val)
                
            except (ValueError, TypeError):
                cleaned_values.append(np.nan)
        
        return pd.Series(cleaned_values)
    
    def _validate_data_quality(self, df):
        """Validate data quality and consistency"""
        errors = []
        warnings = []
        
        # Check for missing dates
        if df['Month'].isnull().any():
            errors.append("Some dates could not be parsed. Please check date format.")
        
        # Check for negative values (might be valid, but warn)
        for col in self.expense_columns:
            if col in df.columns:
                negative_count = (df[col] < 0).sum()
                if negative_count > 0:
                    warnings.append(f"Column '{col}' contains {negative_count} negative values")
        
        # Check for extreme outliers (values > 10x median)
        for col in self.expense_columns:
            if col in df.columns and not df[col].empty:
                median_val = df[col].median()
                if median_val > 0:
                    outliers = df[col] > (median_val * 10)
                    if outliers.any():
                        warnings.append(f"Column '{col}' contains potential outliers")
        
        # Check date continuity
        df_sorted = df.sort_values('Month')
        date_gaps = []
        for i in range(1, len(df_sorted)):
            prev_date = df_sorted.iloc[i-1]['Month']
            curr_date = df_sorted.iloc[i]['Month']
            
            # Calculate expected next month
            if pd.notna(prev_date) and pd.notna(curr_date):
                expected_date = prev_date + pd.DateOffset(months=1)
                if abs((curr_date - expected_date).days) > 5:  # Allow 5 days tolerance
                    date_gaps.append(f"{prev_date.strftime('%Y-%m')} to {curr_date.strftime('%Y-%m')}")
        
        if date_gaps:
            warnings.append(f"Date gaps detected: {', '.join(date_gaps[:3])}")
        
        # Check for sufficient data
        if len(df) < 24:
            warnings.append(f"Only {len(df)} months of data available. More data will improve forecast accuracy.")
        
        return len(errors) == 0, errors, warnings
