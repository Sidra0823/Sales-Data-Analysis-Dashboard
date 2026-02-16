import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analysis.eda import SalesAnalyzer
from analysis.model import SalesForecastModel

# Page configuration
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    with open('assets/styles.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

try:
    load_css()
except:
    pass

# Color scheme
COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'accent': '#F18F01',
    'success': '#06A77D',
    'danger': '#D62246',
    'chart_colors': ['#2E86AB', '#A23B72', '#F18F01', '#06A77D', '#D62246', 
                     '#6C5CE7', '#00B894', '#FDCB6E', '#E17055', '#0984E3']
}

@st.cache_data
def load_data():
    """Load and cache data"""
    analyzer = SalesAnalyzer('data/sales_data.csv')
    return analyzer

def create_metric_card(label, value, delta=None, delta_color="normal"):
    """Create a custom metric card"""
    delta_html = ""
    if delta:
        color = "green" if delta_color == "normal" else "red"
        arrow = "↑" if delta_color == "normal" else "↓"
        delta_html = f'<div class="delta" style="color: {color};">{arrow} {delta}</div>'
    
    card_html = f"""
    <div class="custom-metric">
        <h3>{label}</h3>
        <div class="value">{value}</div>
        {delta_html}
    </div>
    """
    return card_html

def format_currency(value):
    """Format value as currency"""
    return f"${value:,.2f}"

def format_number(value):
    """Format large numbers"""
    if value >= 1_000_000:
        return f"{value/1_000_000:.2f}M"
    elif value >= 1_000:
        return f"{value/1_000:.2f}K"
    return f"{value:.0f}"

def main():
    # Header
    st.markdown("""
        <h1 style='text-align: center; color: white; padding: 20px; 
        background: linear-gradient(90deg, #2E86AB 0%, #A23B72 100%); 
        border-radius: 10px; margin-bottom: 30px;'>
        📊 Sales Analytics Dashboard
        </h1>
    """, unsafe_allow_html=True)
    
    # Load data
    with st.spinner("Loading data..."):
        analyzer = load_data()
    
    # Sidebar filters
    st.sidebar.markdown("## 🎯 Filters")
    
    # Date range filter
    min_date = analyzer.df['Date'].min().date()
    max_date = analyzer.df['Date'].max().date()
    
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Category filter
    categories = st.sidebar.multiselect(
        "Select Categories",
        options=analyzer.df['Category'].unique(),
        default=analyzer.df['Category'].unique()
    )
    
    # Region filter
    regions = st.sidebar.multiselect(
        "Select Regions",
        options=analyzer.df['Region'].unique(),
        default=analyzer.df['Region'].unique()
    )
    
    # Apply filters
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = analyzer.get_filtered_data(
            start_date=start_date,
            end_date=end_date,
            categories=categories,
            regions=regions
        )
    else:
        filtered_df = analyzer.df
    
    # Update analyzer with filtered data
    analyzer.df = filtered_df
    
    # Get summary stats
    stats = analyzer.get_summary_stats()
    
    # KPI Section
    st.markdown("## 📈 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💰 Total Sales",
            value=format_currency(stats['total_sales']),
            delta=f"{format_currency(stats['total_sales']/365)} avg/day"
        )
    
    with col2:
        st.metric(
            label="🛍️ Total Transactions",
            value=format_number(stats['total_transactions']),
            delta=f"{stats['total_transactions']/730:.0f} avg/day"
        )
    
    with col3:
        st.metric(
            label="📦 Average Order Value",
            value=format_currency(stats['avg_order_value']),
            delta=f"Discount: {stats['avg_discount']:.1f}%"
        )
    
    with col4:
        st.metric(
            label="👥 Unique Customers",
            value=format_number(stats['unique_customers']),
            delta=f"Profit: {format_currency(stats['total_profit'])}"
        )
    
    st.markdown("---")
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview", "📈 Trends", "🎯 Products & Categories", 
        "🌍 Regional Analysis", "🔮 Forecasting"
    ])
    
    with tab1:
        st.markdown("### Sales Overview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Monthly sales trend
            monthly_sales = analyzer.sales_by_time('month')
            fig_monthly = px.line(
                monthly_sales,
                x='Month_Name',
                y='Total_Amount',
                color='Year',
                title='Monthly Sales Trend',
                labels={'Total_Amount': 'Sales ($)', 'Month_Name': 'Month'},
                color_discrete_sequence=COLORS['chart_colors']
            )
            fig_monthly.update_layout(
                height=400,
                hovermode='x unified',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_monthly, use_container_width=True)
        
        with col2:
            # Sales by category
            category_sales = analyzer.sales_by_category()
            fig_category = px.pie(
                category_sales,
                values='Total_Amount',
                names='Category',
                title='Sales Distribution by Category',
                color_discrete_sequence=COLORS['chart_colors']
            )
            fig_category.update_traces(textposition='inside', textinfo='percent+label')
            fig_category.update_layout(height=400)
            st.plotly_chart(fig_category, use_container_width=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            # Customer segment analysis
            segment_analysis = analyzer.customer_segment_analysis()
            fig_segment = px.bar(
                segment_analysis,
                x='Customer_Segment',
                y='Total_Amount',
                title='Sales by Customer Segment',
                labels={'Customer_Segment': 'Segment', 'Total_Amount': 'Total Sales ($)'},
                color='Customer_Segment',
                color_discrete_sequence=COLORS['chart_colors']
            )
            fig_segment.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_segment, use_container_width=True)
        
        with col4:
            # Payment method distribution
            payment_analysis = analyzer.payment_method_analysis()
            fig_payment = px.bar(
                payment_analysis,
                x='Payment_Method',
                y='Total_Amount',
                title='Sales by Payment Method',
                labels={'Payment_Method': 'Payment Method', 'Total_Amount': 'Sales ($)'},
                color='Payment_Method',
                color_discrete_sequence=COLORS['chart_colors']
            )
            fig_payment.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_payment, use_container_width=True)
    
    with tab2:
        st.markdown("### Trend Analysis")
        
        # Daily sales trend with moving average
        daily_sales = analyzer.sales_by_time('day')
        daily_sales['MA_7'] = daily_sales['Total_Amount'].rolling(window=7).mean()
        daily_sales['MA_30'] = daily_sales['Total_Amount'].rolling(window=30).mean()
        
        fig_daily = go.Figure()
        fig_daily.add_trace(go.Scatter(
            x=daily_sales['Date'],
            y=daily_sales['Total_Amount'],
            name='Daily Sales',
            line=dict(color='lightgray', width=1),
            opacity=0.5
        ))
        fig_daily.add_trace(go.Scatter(
            x=daily_sales['Date'],
            y=daily_sales['MA_7'],
            name='7-Day MA',
            line=dict(color=COLORS['primary'], width=2)
        ))
        fig_daily.add_trace(go.Scatter(
            x=daily_sales['Date'],
            y=daily_sales['MA_30'],
            name='30-Day MA',
            line=dict(color=COLORS['secondary'], width=2)
        ))
        fig_daily.update_layout(
            title='Daily Sales with Moving Averages',
            xaxis_title='Date',
            yaxis_title='Sales ($)',
            height=500,
            hovermode='x unified'
        )
        st.plotly_chart(fig_daily, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Seasonal analysis
            seasonal = analyzer.seasonal_analysis()
            fig_seasonal = px.bar(
                seasonal,
                x='Month_Name',
                y='Total_Amount',
                title='Seasonal Sales Pattern',
                labels={'Month_Name': 'Month', 'Total_Amount': 'Total Sales ($)'},
                color='Total_Amount',
                color_continuous_scale='Blues'
            )
            fig_seasonal.update_layout(height=400)
            st.plotly_chart(fig_seasonal, use_container_width=True)
        
        with col2:
            # Growth rate
            growth = analyzer.monthly_growth_rate()
            growth['Period'] = growth['Year'].astype(str) + '-' + growth['Month'].astype(str).str.zfill(2)
            fig_growth = px.line(
                growth,
                x='Period',
                y='Growth_Rate',
                title='Month-over-Month Growth Rate',
                labels={'Period': 'Period', 'Growth_Rate': 'Growth Rate (%)'},
                markers=True
            )
            fig_growth.add_hline(y=0, line_dash="dash", line_color="red")
            fig_growth.update_layout(height=400)
            st.plotly_chart(fig_growth, use_container_width=True)
    
    with tab3:
        st.markdown("### Products & Categories Analysis")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Top products
            top_n = st.slider("Number of top products to display", 5, 20, 10)
            top_products = analyzer.top_products(n=top_n)
            
            fig_top = px.bar(
                top_products,
                x='Total_Amount',
                y='Product',
                orientation='h',
                title=f'Top {top_n} Products by Sales',
                labels={'Total_Amount': 'Total Sales ($)', 'Product': ''},
                color='Total_Amount',
                color_continuous_scale='Viridis'
            )
            fig_top.update_layout(height=600)
            st.plotly_chart(fig_top, use_container_width=True)
        
        with col2:
            # Category statistics
            category_stats = analyzer.sales_by_category()
            st.markdown("#### Category Performance")
            
            for _, row in category_stats.iterrows():
                with st.expander(f"**{row['Category']}**"):
                    st.metric("Total Sales", format_currency(row['Total_Amount']))
                    st.metric("Quantity Sold", format_number(row['Quantity']))
                    st.metric("Transactions", format_number(row['Transaction_ID']))
                    st.metric("Profit", format_currency(row['Profit']))
        
        # Discount impact
        st.markdown("#### 💸 Discount Impact Analysis")
        discount_impact = analyzer.discount_impact_analysis()
        
        fig_discount = px.bar(
            discount_impact,
            x='Discount_Category',
            y='Total_Amount',
            title='Sales by Discount Level',
            labels={'Discount_Category': 'Discount Category', 'Total_Amount': 'Total Sales ($)'},
            color='Discount_Category',
            color_discrete_sequence=COLORS['chart_colors']
        )
        fig_discount.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_discount, use_container_width=True)
    
    with tab4:
        st.markdown("### Regional Analysis")
        
        # Regional sales
        region_sales = analyzer.sales_by_region()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_region = px.bar(
                region_sales,
                x='Region',
                y='Total_Amount',
                title='Sales by Region',
                labels={'Region': '', 'Total_Amount': 'Total Sales ($)'},
                color='Total_Amount',
                color_continuous_scale='RdYlGn'
            )
            fig_region.update_layout(height=400)
            st.plotly_chart(fig_region, use_container_width=True)
        
        with col2:
            # Regional profit comparison
            fig_region_profit = px.scatter(
                region_sales,
                x='Total_Amount',
                y='Profit',
                size='Transaction_ID',
                color='Region',
                title='Regional Sales vs Profit',
                labels={'Total_Amount': 'Total Sales ($)', 'Profit': 'Profit ($)'},
                color_discrete_sequence=COLORS['chart_colors']
            )
            fig_region_profit.update_layout(height=400)
            st.plotly_chart(fig_region_profit, use_container_width=True)
        
        # Regional details table
        st.markdown("#### Regional Performance Details")
        region_display = region_sales.copy()
        region_display['Total_Amount'] = region_display['Total_Amount'].apply(format_currency)
        region_display['Profit'] = region_display['Profit'].apply(format_currency)
        region_display = region_display.rename(columns={
            'Total_Amount': 'Total Sales',
            'Quantity': 'Units Sold',
            'Transaction_ID': 'Transactions'
        })
        st.dataframe(region_display, use_container_width=True, hide_index=True)
    
    with tab5:
        st.markdown("### Sales Forecasting")
        
        st.info("🔮 Using Machine Learning to predict future sales trends")
        
        col1, col2 = st.columns([2, 1])
        
        with col2:
            forecast_days = st.slider("Forecast Period (days)", 7, 90, 30)
            model_type = st.selectbox(
                "Select Model",
                ["Random Forest", "Gradient Boosting", "Linear Regression"]
            )
            
            if st.button("🚀 Generate Forecast", type="primary"):
                with st.spinner("Training model and generating forecast..."):
                    # Train model
                    model_type_map = {
                        "Random Forest": "random_forest",
                        "Gradient Boosting": "gradient_boosting",
                        "Linear Regression": "linear_regression"
                    }
                    
                    forecaster = SalesForecastModel(analyzer.df)
                    metrics = forecaster.train_model(model_type=model_type_map[model_type])
                    forecast_df = forecaster.predict_future(days_ahead=forecast_days)
                    
                    # Store in session state
                    st.session_state['forecast'] = forecast_df
                    st.session_state['metrics'] = metrics
                    st.session_state['forecaster'] = forecaster
                    
                    st.success("✅ Forecast generated successfully!")
        
        with col1:
            if 'forecast' in st.session_state:
                forecast_df = st.session_state['forecast']
                
                # Plot forecast
                historical = analyzer.sales_by_time('day')
                
                fig_forecast = go.Figure()
                
                # Historical data
                fig_forecast.add_trace(go.Scatter(
                    x=historical['Date'],
                    y=historical['Total_Amount'],
                    name='Historical Sales',
                    line=dict(color=COLORS['primary'], width=2)
                ))
                
                # Forecast
                fig_forecast.add_trace(go.Scatter(
                    x=forecast_df['Date'],
                    y=forecast_df['Predicted_Sales'],
                    name='Forecasted Sales',
                    line=dict(color=COLORS['accent'], width=2, dash='dash')
                ))
                
                fig_forecast.update_layout(
                    title=f'{forecast_days}-Day Sales Forecast',
                    xaxis_title='Date',
                    yaxis_title='Sales ($)',
                    height=500,
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig_forecast, use_container_width=True)
                
                # Model metrics
                if 'metrics' in st.session_state:
                    st.markdown("#### Model Performance Metrics")
                    metrics = st.session_state['metrics']
                    
                    metric_col1, metric_col2, metric_col3 = st.columns(3)
                    with metric_col1:
                        st.metric("Test R² Score", f"{metrics['test_r2']:.4f}")
                    with metric_col2:
                        st.metric("Test MAE", format_currency(metrics['test_mae']))
                    with metric_col3:
                        st.metric("Test RMSE", format_currency(metrics['test_rmse']))
                
                # Feature importance
                if 'forecaster' in st.session_state:
                    importance = st.session_state['forecaster'].get_feature_importance(top_n=10)
                    if importance is not None:
                        st.markdown("#### Top Feature Importance")
                        fig_importance = px.bar(
                            importance,
                            x='Importance',
                            y='Feature',
                            orientation='h',
                            title='Top 10 Most Important Features',
                            color='Importance',
                            color_continuous_scale='Viridis'
                        )
                        fig_importance.update_layout(height=400)
                        st.plotly_chart(fig_importance, use_container_width=True)
            else:
                st.info("👈 Click 'Generate Forecast' to see predictions")
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #666; padding: 20px;'>
            <p>📊 Sales Analytics Dashboard | Built with Streamlit & Plotly</p>
            <p>Data updated through December 2024</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
