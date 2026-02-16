import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
import joblib
import warnings
warnings.filterwarnings('ignore')

class SalesForecastModel:
    def __init__(self, df):
        """Initialize forecast model with data"""
        self.df = df.copy()
        self.model = None
        self.feature_columns = None
        self.label_encoders = {}
        
    def prepare_features(self):
        """Prepare features for modeling"""
        # Aggregate to daily level
        daily_sales = self.df.groupby('Date').agg({
            'Total_Amount': 'sum',
            'Quantity': 'sum',
            'Transaction_ID': 'count',
            'Discount_Percent': 'mean'
        }).reset_index()
        
        daily_sales.columns = ['Date', 'Total_Sales', 'Total_Quantity', 'Num_Transactions', 'Avg_Discount']
        
        # Create time-based features
        daily_sales['Year'] = daily_sales['Date'].dt.year
        daily_sales['Month'] = daily_sales['Date'].dt.month
        daily_sales['Day'] = daily_sales['Date'].dt.day
        daily_sales['DayOfWeek'] = daily_sales['Date'].dt.dayofweek
        daily_sales['DayOfYear'] = daily_sales['Date'].dt.dayofyear
        daily_sales['WeekOfYear'] = daily_sales['Date'].dt.isocalendar().week
        daily_sales['Quarter'] = daily_sales['Date'].dt.quarter
        daily_sales['IsWeekend'] = (daily_sales['DayOfWeek'] >= 5).astype(int)
        daily_sales['IsMonthStart'] = daily_sales['Date'].dt.is_month_start.astype(int)
        daily_sales['IsMonthEnd'] = daily_sales['Date'].dt.is_month_end.astype(int)
        
        # Lag features
        daily_sales['Sales_Lag_1'] = daily_sales['Total_Sales'].shift(1)
        daily_sales['Sales_Lag_7'] = daily_sales['Total_Sales'].shift(7)
        daily_sales['Sales_Lag_30'] = daily_sales['Total_Sales'].shift(30)
        
        # Rolling averages
        daily_sales['Sales_MA_7'] = daily_sales['Total_Sales'].rolling(window=7, min_periods=1).mean()
        daily_sales['Sales_MA_30'] = daily_sales['Total_Sales'].rolling(window=30, min_periods=1).mean()
        
        # Trend
        daily_sales['Trend'] = range(len(daily_sales))
        
        # Drop NaN values
        daily_sales = daily_sales.dropna()
        
        self.daily_sales = daily_sales
        return daily_sales
    
    def train_model(self, model_type='random_forest', test_size=0.2):
        """Train forecasting model"""
        # Prepare features
        df_model = self.prepare_features()
        
        # Define features and target
        self.feature_columns = [
            'Year', 'Month', 'Day', 'DayOfWeek', 'DayOfYear', 'WeekOfYear', 
            'Quarter', 'IsWeekend', 'IsMonthStart', 'IsMonthEnd',
            'Total_Quantity', 'Num_Transactions', 'Avg_Discount',
            'Sales_Lag_1', 'Sales_Lag_7', 'Sales_Lag_30',
            'Sales_MA_7', 'Sales_MA_30', 'Trend'
        ]
        
        X = df_model[self.feature_columns]
        y = df_model['Total_Sales']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, shuffle=False
        )
        
        # Train model
        if model_type == 'random_forest':
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=15,
                min_samples_split=5,
                random_state=42,
                n_jobs=-1
            )
        elif model_type == 'gradient_boosting':
            self.model = GradientBoostingRegressor(
                n_estimators=100,
                max_depth=5,
                learning_rate=0.1,
                random_state=42
            )
        else:
            self.model = LinearRegression()
        
        self.model.fit(X_train, y_train)
        
        # Evaluate
        train_pred = self.model.predict(X_train)
        test_pred = self.model.predict(X_test)
        
        metrics = {
            'train_mae': mean_absolute_error(y_train, train_pred),
            'train_rmse': np.sqrt(mean_squared_error(y_train, train_pred)),
            'train_r2': r2_score(y_train, train_pred),
            'test_mae': mean_absolute_error(y_test, test_pred),
            'test_rmse': np.sqrt(mean_squared_error(y_test, test_pred)),
            'test_r2': r2_score(y_test, test_pred)
        }
        
        # Store predictions for visualization
        self.X_test = X_test
        self.y_test = y_test
        self.test_pred = test_pred
        self.test_dates = df_model.loc[X_test.index, 'Date']
        
        return metrics
    
    def predict_future(self, days_ahead=30):
        """Predict future sales"""
        if self.model is None:
            raise ValueError("Model not trained yet. Call train_model() first.")
        
        # Get last date and data
        last_date = self.daily_sales['Date'].max()
        last_row = self.daily_sales.iloc[-1]
        
        # Generate future dates
        future_dates = pd.date_range(
            start=last_date + pd.Timedelta(days=1),
            periods=days_ahead,
            freq='D'
        )
        
        predictions = []
        
        for i, date in enumerate(future_dates):
            # Create features for future date
            features = {
                'Year': date.year,
                'Month': date.month,
                'Day': date.day,
                'DayOfWeek': date.dayofweek,
                'DayOfYear': date.dayofyear,
                'WeekOfYear': date.isocalendar().week,
                'Quarter': date.quarter,
                'IsWeekend': 1 if date.dayofweek >= 5 else 0,
                'IsMonthStart': 1 if date.is_month_start else 0,
                'IsMonthEnd': 1 if date.is_month_end else 0,
                'Total_Quantity': last_row['Total_Quantity'],
                'Num_Transactions': last_row['Num_Transactions'],
                'Avg_Discount': last_row['Avg_Discount'],
                'Sales_Lag_1': last_row['Total_Sales'] if i == 0 else predictions[-1],
                'Sales_Lag_7': last_row['Sales_Lag_7'],
                'Sales_Lag_30': last_row['Sales_Lag_30'],
                'Sales_MA_7': last_row['Sales_MA_7'],
                'Sales_MA_30': last_row['Sales_MA_30'],
                'Trend': last_row['Trend'] + i + 1
            }
            
            # Predict
            X_future = pd.DataFrame([features])[self.feature_columns]
            pred = self.model.predict(X_future)[0]
            predictions.append(max(0, pred))  # Ensure non-negative
        
        # Create forecast dataframe
        forecast_df = pd.DataFrame({
            'Date': future_dates,
            'Predicted_Sales': predictions
        })
        
        return forecast_df
    
    def get_feature_importance(self, top_n=10):
        """Get feature importance from the model"""
        if self.model is None or not hasattr(self.model, 'feature_importances_'):
            return None
        
        importance = pd.DataFrame({
            'Feature': self.feature_columns,
            'Importance': self.model.feature_importances_
        }).sort_values('Importance', ascending=False).head(top_n)
        
        return importance
    
    def save_model(self, path):
        """Save trained model"""
        if self.model is None:
            raise ValueError("No model to save. Train a model first.")
        
        model_data = {
            'model': self.model,
            'feature_columns': self.feature_columns,
            'label_encoders': self.label_encoders
        }
        joblib.dump(model_data, path)
        print(f"Model saved to {path}")
    
    def load_model(self, path):
        """Load trained model"""
        model_data = joblib.load(path)
        self.model = model_data['model']
        self.feature_columns = model_data['feature_columns']
        self.label_encoders = model_data['label_encoders']
        print(f"Model loaded from {path}")

# Utility function for quick forecasting
def generate_forecast(data_path, days_ahead=30, model_type='random_forest'):
    """Generate sales forecast"""
    df = pd.read_csv(data_path)
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Train model
    forecaster = SalesForecastModel(df)
    metrics = forecaster.train_model(model_type=model_type)
    
    # Generate predictions
    forecast = forecaster.predict_future(days_ahead=days_ahead)
    
    return forecaster, forecast, metrics
