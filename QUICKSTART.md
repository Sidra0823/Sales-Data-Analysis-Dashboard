# 🚀 Quick Start Guide

Get your Sales Dashboard running in 3 minutes!

## Step 1: Install Python Dependencies

Open terminal/command prompt in the project folder and run:

```bash
pip install -r requirements.txt
```

## Step 2: Run the Dashboard

```bash
streamlit run dashboard/app.py
```

## Step 3: Open in Browser

The dashboard will automatically open at:
```
http://localhost:8501
```

If it doesn't open automatically, copy the URL from your terminal.

## 🎯 What You'll See

1. **KPI Cards**: Total sales, transactions, average order value, and customer count
2. **5 Interactive Tabs**:
   - Overview: General sales statistics
   - Trends: Time-series analysis
   - Products & Categories: Product performance
   - Regional Analysis: Geographic breakdown
   - Forecasting: ML-powered predictions

## 🎨 Try These Features

### Filter Data
Use the sidebar (left) to:
- Select custom date ranges
- Filter by product categories
- Focus on specific regions

### Generate Sales Forecast
1. Go to the "Forecasting" tab
2. Choose forecast period (7-90 days)
3. Select a model (Random Forest recommended)
4. Click "Generate Forecast"

### Explore Charts
- Hover over charts for detailed values
- Click legend items to show/hide data
- Use zoom and pan tools on charts

## 🔧 Troubleshooting

### Module Not Found Error
```bash
pip install --upgrade -r requirements.txt
```

### Port Already in Use
```bash
streamlit run dashboard/app.py --server.port 8502
```

### Can't Find Data File
Make sure you're running the command from the `Sales-Dashboard` directory:
```bash
cd Sales-Dashboard
streamlit run dashboard/app.py
```

## 📱 Sharing Your Dashboard

### Local Network
Share with devices on your network:
```bash
streamlit run dashboard/app.py --server.address 0.0.0.0
```

### Deploy to Cloud
Deploy for free on:
- [Streamlit Cloud](https://streamlit.io/cloud)
- [Heroku](https://www.heroku.com/)
- [AWS](https://aws.amazon.com/)

## 📊 Using Your Own Data

1. Replace `data/sales_data.csv` with your CSV file
2. Ensure it has these columns:
   - Date
   - Total_Amount
   - Category
   - Region
   - Quantity
3. Restart the dashboard

## 🎓 Learning Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Charts](https://plotly.com/python/)
- [Pandas Guide](https://pandas.pydata.org/docs/)

## 🆘 Need Help?

- Check the main README.md for detailed documentation
- Open an issue on GitHub
- Review sample code in `dashboard/app.py`

---

**Enjoy your dashboard! 🎉**
