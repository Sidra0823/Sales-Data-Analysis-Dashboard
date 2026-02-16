import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

class SalesAnalyzer:
    def __init__(self, data_path):
        """Initialize the analyzer with data"""
        self.df = pd.read_csv(data_path)
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        self.clean_data()
        
    def clean_data(self):
        """Clean and preprocess the data"""
        # Remove duplicates
        initial_rows = len(self.df)
        self.df = self.df.drop_duplicates()
        print(f"Removed {initial_rows - len(self.df)} duplicate rows")
        
        # Handle missing values
        self.df['Customer_Segment'].fillna('Regular', inplace=True)
        
        # Create additional time features
        self.df['Year'] = self.df['Date'].dt.year
        self.df['Month'] = self.df['Date'].dt.month
        self.df['Month_Name'] = self.df['Date'].dt.strftime('%B')
        self.df['Quarter'] = self.df['Date'].dt.quarter
        self.df['Day_of_Week'] = self.df['Date'].dt.day_name()
        self.df['Week'] = self.df['Date'].dt.isocalendar().week
        
        # Calculate profit margin (simplified - assuming 30% average margin)
        self.df['Profit'] = self.df['Total_Amount'] * 0.30
        
        # Sort by date
        self.df = self.df.sort_values('Date').reset_index(drop=True)
        
    def get_summary_stats(self):
        """Get overall summary statistics"""
        stats = {
            'total_sales': self.df['Total_Amount'].sum(),
            'total_transactions': len(self.df),
            'avg_order_value': self.df['Total_Amount'].mean(),
            'total_quantity_sold': self.df['Quantity'].sum(),
            'unique_customers': self.df['Customer_ID'].nunique(),
            'total_profit': self.df['Profit'].sum(),
            'avg_discount': self.df['Discount_Percent'].mean(),
            'date_range': f"{self.df['Date'].min().strftime('%Y-%m-%d')} to {self.df['Date'].max().strftime('%Y-%m-%d')}"
        }
        return stats
    
    def sales_by_time(self, period='month'):
        """Aggregate sales by time period"""
        if period == 'month':
            return self.df.groupby(['Year', 'Month', 'Month_Name'])['Total_Amount'].sum().reset_index()
        elif period == 'quarter':
            return self.df.groupby(['Year', 'Quarter'])['Total_Amount'].sum().reset_index()
        elif period == 'week':
            return self.df.groupby('Week')['Total_Amount'].sum().reset_index()
        elif period == 'day':
            return self.df.groupby('Date')['Total_Amount'].sum().reset_index()
        
    def sales_by_category(self):
        """Sales breakdown by product category"""
        return self.df.groupby('Category').agg({
            'Total_Amount': 'sum',
            'Quantity': 'sum',
            'Transaction_ID': 'count',
            'Profit': 'sum'
        }).reset_index().sort_values('Total_Amount', ascending=False)
    
    def sales_by_region(self):
        """Sales breakdown by region"""
        return self.df.groupby('Region').agg({
            'Total_Amount': 'sum',
            'Quantity': 'sum',
            'Transaction_ID': 'count',
            'Profit': 'sum'
        }).reset_index().sort_values('Total_Amount', ascending=False)
    
    def top_products(self, n=10):
        """Get top N products by sales"""
        return self.df.groupby('Product').agg({
            'Total_Amount': 'sum',
            'Quantity': 'sum',
            'Transaction_ID': 'count'
        }).reset_index().sort_values('Total_Amount', ascending=False).head(n)
    
    def customer_segment_analysis(self):
        """Analyze customer segments"""
        result = self.df.groupby('Customer_Segment').agg({
            'Total_Amount': 'sum',
            'Profit': 'sum',
            'Discount_Percent': 'mean'
        }).reset_index()
        return result
    
    def payment_method_analysis(self):
        """Analyze payment methods"""
        return self.df.groupby('Payment_Method').agg({
            'Total_Amount': 'sum',
            'Transaction_ID': 'count'
        }).reset_index().sort_values('Total_Amount', ascending=False)
    
    def monthly_growth_rate(self):
        """Calculate month-over-month growth rate"""
        monthly = self.df.groupby(['Year', 'Month'])['Total_Amount'].sum().reset_index()
        monthly['Growth_Rate'] = monthly['Total_Amount'].pct_change() * 100
        return monthly
    
    def cohort_analysis(self):
        """Simple cohort analysis - customer retention"""
        # First purchase date for each customer
        first_purchase = self.df.groupby('Customer_ID')['Date'].min().reset_index()
        first_purchase.columns = ['Customer_ID', 'First_Purchase_Date']
        
        # Merge with main data
        df_cohort = self.df.merge(first_purchase, on='Customer_ID')
        df_cohort['Cohort_Month'] = df_cohort['First_Purchase_Date'].dt.to_period('M')
        df_cohort['Purchase_Month'] = df_cohort['Date'].dt.to_period('M')
        
        # Calculate months since first purchase
        df_cohort['Months_Since_First'] = (
            (df_cohort['Purchase_Month'] - df_cohort['Cohort_Month']).apply(lambda x: x.n)
        )
        
        # Cohort size
        cohort_size = df_cohort.groupby('Cohort_Month')['Customer_ID'].nunique().reset_index()
        cohort_size.columns = ['Cohort_Month', 'Cohort_Size']
        
        return df_cohort, cohort_size
    
    def seasonal_analysis(self):
        """Analyze seasonal patterns"""
        seasonal = self.df.groupby('Month_Name').agg({
            'Total_Amount': 'sum',
            'Transaction_ID': 'count'
        }).reset_index()
        
        # Reorder by month
        month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']
        seasonal['Month_Name'] = pd.Categorical(seasonal['Month_Name'], categories=month_order, ordered=True)
        seasonal = seasonal.sort_values('Month_Name')
        
        return seasonal
    
    def discount_impact_analysis(self):
        """Analyze impact of discounts on sales"""
        self.df['Discount_Category'] = pd.cut(
            self.df['Discount_Percent'],
            bins=[-1, 0, 10, 20, 100],
            labels=['No Discount', '1-10%', '11-20%', '20%+']
        )
        
        result = self.df.groupby('Discount_Category').agg({
            'Total_Amount': 'sum',
            'Quantity': 'sum',
            'Transaction_ID': 'count'
        }).reset_index()
        return result
    
    def get_filtered_data(self, start_date=None, end_date=None, 
                         categories=None, regions=None):
        """Filter data based on parameters"""
        df_filtered = self.df.copy()
        
        if start_date:
            df_filtered = df_filtered[df_filtered['Date'] >= pd.to_datetime(start_date)]
        if end_date:
            df_filtered = df_filtered[df_filtered['Date'] <= pd.to_datetime(end_date)]
        if categories:
            df_filtered = df_filtered[df_filtered['Category'].isin(categories)]
        if regions:
            df_filtered = df_filtered[df_filtered['Region'].isin(regions)]
            
        return df_filtered
    
    def export_analysis_report(self, output_path):
        """Export comprehensive analysis report"""
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Summary stats
            summary = pd.DataFrame([self.get_summary_stats()])
            summary.to_excel(writer, sheet_name='Summary', index=False)
            
            # Time series
            self.sales_by_time('month').to_excel(writer, sheet_name='Monthly_Sales', index=False)
            
            # Category analysis
            self.sales_by_category().to_excel(writer, sheet_name='Category_Sales', index=False)
            
            # Region analysis
            self.sales_by_region().to_excel(writer, sheet_name='Region_Sales', index=False)
            
            # Top products
            self.top_products(20).to_excel(writer, sheet_name='Top_Products', index=False)
            
            # Customer segments
            self.customer_segment_analysis().to_excel(writer, sheet_name='Customer_Segments', index=False)
            
        print(f"Analysis report exported to {output_path}")
