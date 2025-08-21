import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

class ModelTrainer:
    def __init__(self):
        self.models = {
            'Linear Regression': LinearRegression(),
            'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42)
        }
        self.scalers = {}
        self.best_models = {}
        self.feature_columns = ['Miscellaneous', 'Financial', 'CapEx', 'COGS', 'Operating']
    
    def train_and_forecast(self, df, forecast_months):
        """
        Train models and generate forecasts
        Returns: dict with forecast dataframe and performance metrics
        """
        # Use simple time-based features only
        df_work = df.copy()
        df_work['Month_dt'] = pd.to_datetime(df_work['Month'])
        df_work['Month_num'] = range(len(df_work))  # Simple sequential numbering
        df_work['Year'] = df_work['Month_dt'].dt.year
        df_work['Month_of_year'] = df_work['Month_dt'].dt.month

        # Simple features matrix
        X = df_work[['Month_num', 'Year', 'Month_of_year']].values

        # Train models for each expense category and total
        model_performance = {}
        forecasts = {}

        # Train models for each category
        for category in self.feature_columns + ['Total']:               
            if category in df.columns:
                y = df[category].values

                # Ensure X and y have same length
                min_len = min(len(X), len(y))
                X_cat = X[:min_len]
                y_cat = y[:min_len]

                # Split data for validation
                split_idx = int(len(X_cat) * 0.8)
                X_train, X_test = X_cat[:split_idx], X_cat[split_idx:]
                y_train, y_test = y_cat[:split_idx], y_cat[split_idx:]

                # Train and evaluate models
                best_model, best_score, category_performance = self._train_category_models(
                    X_train, X_test, y_train, y_test, category
                )

                self.best_models[category] = best_model
                model_performance[category] = category_performance

                # Generate forecast for this category
                forecast_values = self._generate_simple_forecast(
                    best_model, df_work, category, forecast_months
                )
                forecasts[category] = forecast_values

        # Create forecast dataframe
        forecast_df = self._create_forecast_dataframe(df, forecasts, forecast_months)

        return {
            'forecast_df': forecast_df,
            'performance': model_performance
        }
    

    
    def _train_category_models(self, X_train, X_test, y_train, y_test, category):
        """Train and evaluate models for a specific category"""
        best_model = None
        best_score = float('inf')
        performance_results = {}
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        self.scalers[category] = scaler
        
        for model_name, model in self.models.items():
            # Train model
            model.fit(X_train_scaled, y_train)
            
            # Make predictions
            y_pred = model.predict(X_test_scaled)
            
            # Calculate metrics
            mae = mean_absolute_error(y_test, y_pred)
            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            r2 = r2_score(y_test, y_pred)
            
            performance_results[model_name] = {
                'MAE': round(mae, 2),
                'RMSE': round(rmse, 2),
                'R²': round(r2, 4)
            }
            
            # Select best model based on RMSE
            if rmse < best_score:
                best_score = rmse
                best_model = model
        
        return best_model, best_score, performance_results
    


    def _generate_simple_forecast(self, model, df_work, category, forecast_months):
        """Generate forecast using simple time-based features with trend analysis"""
        forecasts = []
        last_month_num = df_work['Month_num'].iloc[-1]
        last_year = df_work['Year'].iloc[-1]
        last_month_of_year = df_work['Month_of_year'].iloc[-1]

        # Get recent trend from actual data
        recent_values = df_work[category].tail(12).values  # Last 12 months
        if len(recent_values) > 1:
            # Calculate trend using linear regression on recent data
            x_trend = np.arange(len(recent_values))
            trend_slope = np.polyfit(x_trend, recent_values, 1)[0]
            last_value = recent_values[-1]
        else:
            trend_slope = 0
            last_value = df_work[category].iloc[-1]

        for i in range(forecast_months):
            # Calculate next month features
            next_month_num = last_month_num + i + 1
            next_month_of_year = ((last_month_of_year + i) % 12) + 1
            next_year = last_year + ((last_month_of_year + i) // 12)

            # Prepare features
            features = [[next_month_num, next_year, next_month_of_year]]

            # Scale features if scaler exists
            if category in self.scalers:
                features = self.scalers[category].transform(features)

            # Make ML prediction
            ml_prediction = model.predict(features)[0]

            # Make trend-based prediction
            trend_prediction = last_value + (trend_slope * (i + 1))

            # Combine both predictions (weighted average)
            # Give more weight to trend for better accuracy
            combined_prediction = (0.3 * ml_prediction) + (0.7 * trend_prediction)

            # Ensure positive prediction and reasonable bounds
            prediction = max(last_value * 0.5, combined_prediction)  # At least 50% of last value
            prediction = min(last_value * 2.0, prediction)  # At most 200% of last value

            forecasts.append(prediction)

        return forecasts


    
    def _create_forecast_dataframe(self, df, forecasts, forecast_months):
        """Create forecast dataframe with all categories"""
        # Get the last date from historical data
        last_date = pd.to_datetime(df['Month'].iloc[-1])
        
        # Generate future dates
        future_dates = []
        for i in range(1, forecast_months + 1):
            future_date = last_date + pd.DateOffset(months=i)
            future_dates.append(future_date.strftime('%Y-%m-%d'))
        
        # Create forecast dataframe
        forecast_data = {'Month': future_dates}
        
        # Add forecasts for each category
        for category in self.feature_columns:
            if category in forecasts:
                forecast_data[category] = forecasts[category]
            else:
                # If no forecast available, use trend-based prediction
                recent_values = df[category].tail(6)
                growth_rate = recent_values.pct_change().mean()
                if pd.isna(growth_rate):
                    growth_rate = 0
                
                last_value = df[category].iloc[-1]
                category_forecast = []
                for i in range(forecast_months):
                    predicted_value = last_value * ((1 + growth_rate) ** (i + 1))
                    category_forecast.append(max(0, predicted_value))
                
                forecast_data[category] = category_forecast
        
        # Calculate total
        forecast_data['Total'] = [
            sum(forecast_data[cat][i] for cat in self.feature_columns if cat in forecast_data)
            for i in range(forecast_months)
        ]
        
        return pd.DataFrame(forecast_data)
