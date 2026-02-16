# 📊 Sales Data Analysis Dashboard

A comprehensive, interactive sales analytics dashboard built with Python, Streamlit, and Machine Learning. Features beautiful visualizations, real-time filtering, and sales forecasting capabilities.

![Dashboard Preview](https://img.shields.io/badge/Status-Production%20Ready-success)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## 🌟 Features

### 📈 Analytics & Insights
- **Real-time KPI Tracking**: Monitor total sales, transactions, average order value, and customer metrics
- **Trend Analysis**: Daily, weekly, monthly sales trends with moving averages
- **Seasonal Patterns**: Identify peak sales periods and seasonal variations
- **Growth Metrics**: Month-over-month growth rate analysis

### 🎯 Product & Category Analysis
- **Top Products**: Identify best-selling products with customizable rankings
- **Category Performance**: Detailed breakdown by product categories
- **Discount Impact**: Analyze how discounts affect sales performance

### 🌍 Regional Intelligence
- **Geographic Distribution**: Sales performance across different regions
- **Regional Comparison**: Compare sales, profit, and transactions by region
- **Market Insights**: Identify growth opportunities in different markets

### 🔮 Machine Learning Forecasting
- **Sales Prediction**: Forecast future sales using advanced ML algorithms
- **Multiple Models**: Choose between Random Forest, Gradient Boosting, or Linear Regression
- **Feature Importance**: Understand which factors drive sales predictions
- **Customizable Timeframes**: Generate forecasts from 7 to 90 days ahead

### 🎨 Interactive Features
- **Dynamic Filtering**: Filter by date range, categories, and regions
- **Beautiful Visualizations**: Professional charts and graphs using Plotly
- **Responsive Design**: Works seamlessly on desktop and mobile
- **Export Capabilities**: Download analysis reports and forecasts

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download this repository**
   ```bash
   cd Sales-Dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the dashboard**
   ```bash
   streamlit run dashboard/app.py
   ```

4. **Open in browser**
   - The dashboard will automatically open at `http://localhost:8501`
   - If not, manually navigate to the URL shown in terminal

## 📂 Project Structure

```
Sales-Dashboard/
│
├── data/
│   ├── sales_data.csv          # Sample sales dataset (45K+ records)
│   └── generate_data.py        # Script to regenerate sample data
│
├── dashboard/
│   └── app.py                  # Main Streamlit application
│
├── analysis/
│   ├── eda.py                  # Exploratory Data Analysis module
│   └── model.py                # Machine Learning forecasting models
│
├── assets/
│   └── styles.css              # Custom CSS styling
│
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 📊 Dataset Information

The included sample dataset contains **45,000+ sales transactions** spanning 2 years (2023-2024) with the following features:

- **Transaction Details**: Transaction ID, Date, Customer ID
- **Product Information**: Product name, Category (Electronics, Clothing, Home & Kitchen, Books, Sports)
- **Sales Metrics**: Quantity, Unit Price, Discount, Total Amount
- **Geography**: 5 regions (North America, Europe, Asia, South America, Africa)
- **Customer Data**: Customer segments (Premium, Regular, Budget)
- **Payment & Shipping**: Payment methods and shipping preferences

### Data Generation
To regenerate the sample dataset with different parameters:
```bash
cd data
python generate_data.py
```

## 🎯 Usage Guide

### Navigation
The dashboard is organized into 5 main tabs:

1. **📊 Overview**: High-level KPIs and distribution charts
2. **📈 Trends**: Time-series analysis with moving averages
3. **🎯 Products & Categories**: Product performance and discount analysis
4. **🌍 Regional Analysis**: Geographic sales breakdown
5. **🔮 Forecasting**: ML-powered sales predictions

### Filtering Data
Use the sidebar to filter data:
- **Date Range**: Select custom date ranges
- **Categories**: Filter by product categories
- **Regions**: Focus on specific geographic regions

### Generating Forecasts
1. Navigate to the **Forecasting** tab
2. Select forecast period (7-90 days)
3. Choose ML model (Random Forest recommended)
4. Click **Generate Forecast**
5. View predictions and model performance metrics

## 🔧 Customization

### Adding Your Own Data
Replace `data/sales_data.csv` with your own dataset. Ensure it has these columns:
- `Date`: Transaction date
- `Total_Amount`: Sales amount
- `Category`: Product category
- `Region`: Geographic region
- `Quantity`: Number of items
- Additional columns as needed

### Modifying Visualizations
Edit `dashboard/app.py` to customize:
- Chart types and colors (see `COLORS` dictionary)
- KPI metrics
- Analysis methods
- Layout and styling

### Extending Analysis
Add new analysis methods in `analysis/eda.py`:
```python
def custom_analysis(self):
    # Your custom analysis logic
    return results
```

## 📈 Key Metrics Explained

- **Total Sales**: Sum of all transaction amounts
- **Average Order Value (AOV)**: Average transaction amount
- **Growth Rate**: Month-over-month percentage change
- **Customer Segments**: Premium, Regular, and Budget customer classification
- **Profit Margin**: Calculated as 30% of sales (configurable)

## 🤖 ML Models

### Random Forest (Recommended)
- Ensemble method using multiple decision trees
- Best for capturing non-linear patterns
- Robust to outliers

### Gradient Boosting
- Sequential ensemble method
- High accuracy for complex patterns
- Longer training time

### Linear Regression
- Simple baseline model
- Fast training and prediction
- Good for linear trends

## 🎨 Technologies Used

- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualizations
- **Scikit-learn**: Machine learning models
- **NumPy**: Numerical computations

## 📝 Future Enhancements

- [ ] Real-time data integration
- [ ] Advanced customer segmentation
- [ ] Inventory management features
- [ ] Email report scheduling
- [ ] Multi-currency support
- [ ] Export to PDF/Excel
- [ ] User authentication
- [ ] Database integration

## 🤝 Contributing

Contributions are welcome! Feel free to:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with ❤️ using Streamlit
- Sample data generated using realistic business patterns
- Inspired by modern business intelligence tools

## 📧 Contact

For questions, suggestions, or feedback:
- Open an issue on GitHub
- Star ⭐ this repository if you found it helpful!

---

**Happy Analyzing! 📊✨**
