import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Generate dates for 2 years
start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)
date_range = pd.date_range(start=start_date, end=end_date, freq='D')

# Products and categories
products = {
    'Electronics': ['Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Smart Watch'],
    'Clothing': ['T-Shirt', 'Jeans', 'Jacket', 'Sneakers', 'Dress'],
    'Home & Kitchen': ['Coffee Maker', 'Blender', 'Vacuum Cleaner', 'Microwave', 'Air Fryer'],
    'Books': ['Fiction Novel', 'Cookbook', 'Self-Help', 'Biography', 'Science Book'],
    'Sports': ['Yoga Mat', 'Dumbbell Set', 'Running Shoes', 'Fitness Tracker', 'Resistance Bands']
}

# Regions and their characteristics
regions = {
    'North America': {'base_multiplier': 1.2, 'seasonality': 0.15},
    'Europe': {'base_multiplier': 1.0, 'seasonality': 0.12},
    'Asia': {'base_multiplier': 1.3, 'seasonality': 0.10},
    'South America': {'base_multiplier': 0.8, 'seasonality': 0.08},
    'Africa': {'base_multiplier': 0.7, 'seasonality': 0.06}
}

# Customer segments
customer_segments = ['Premium', 'Regular', 'Budget']

# Generate sales data
records = []
transaction_id = 1000

for date in date_range:
    # Number of transactions per day (with weekly pattern)
    day_of_week = date.dayofweek
    if day_of_week in [5, 6]:  # Weekend
        num_transactions = random.randint(50, 100)
    else:  # Weekday
        num_transactions = random.randint(30, 70)
    
    # Add holiday season boost
    if date.month in [11, 12]:  # Holiday season
        num_transactions = int(num_transactions * 1.5)
    
    for _ in range(num_transactions):
        # Select category and product
        category = random.choice(list(products.keys()))
        product = random.choice(products[category])
        
        # Select region
        region = random.choice(list(regions.keys()))
        region_data = regions[region]
        
        # Select customer segment
        segment = random.choice(customer_segments)
        
        # Base price by category
        category_prices = {
            'Electronics': (200, 2000),
            'Clothing': (20, 150),
            'Home & Kitchen': (50, 500),
            'Books': (10, 50),
            'Sports': (15, 200)
        }
        
        base_price = random.uniform(*category_prices[category])
        
        # Adjust price by segment
        if segment == 'Premium':
            base_price *= 1.3
        elif segment == 'Budget':
            base_price *= 0.8
        
        # Quantity (most orders are 1-3 items)
        quantity = np.random.choice([1, 2, 3, 4, 5], p=[0.5, 0.25, 0.15, 0.07, 0.03])
        
        # Discount (random promotions)
        if random.random() < 0.2:  # 20% chance of discount
            discount = random.choice([5, 10, 15, 20, 25])
        else:
            discount = 0
        
        # Calculate final price
        unit_price = base_price * (1 - discount / 100)
        total_price = unit_price * quantity
        
        # Apply regional multiplier and seasonality
        seasonality_factor = 1 + region_data['seasonality'] * np.sin(2 * np.pi * date.dayofyear / 365)
        total_price *= region_data['base_multiplier'] * seasonality_factor
        
        # Payment method
        payment_method = random.choice(['Credit Card', 'PayPal', 'Debit Card', 'Bank Transfer'])
        
        # Shipping method
        shipping_method = random.choice(['Standard', 'Express', 'Premium'])
        
        # Customer ID (returning customers)
        customer_id = f"CUST{random.randint(1, 5000):05d}"
        
        # Record
        records.append({
            'Transaction_ID': f"TXN{transaction_id:06d}",
            'Date': date,
            'Customer_ID': customer_id,
            'Customer_Segment': segment,
            'Product': product,
            'Category': category,
            'Quantity': quantity,
            'Unit_Price': round(unit_price, 2),
            'Discount_Percent': discount,
            'Total_Amount': round(total_price, 2),
            'Region': region,
            'Payment_Method': payment_method,
            'Shipping_Method': shipping_method
        })
        
        transaction_id += 1

# Create DataFrame
df = pd.DataFrame(records)

# Add some missing values (realistic scenario)
missing_indices = np.random.choice(df.index, size=int(len(df) * 0.02), replace=False)
df.loc[missing_indices, 'Customer_Segment'] = np.nan

# Add a few duplicates (data quality issue)
duplicate_rows = df.sample(n=50)
df = pd.concat([df, duplicate_rows], ignore_index=True)

# Save to CSV
df.to_csv('/home/claude/Sales-Dashboard/data/sales_data.csv', index=False)

print(f"Generated {len(df)} sales records")
print(f"\nDataset shape: {df.shape}")
print(f"\nDate range: {df['Date'].min()} to {df['Date'].max()}")
print(f"\nCategories: {df['Category'].unique()}")
print(f"\nRegions: {df['Region'].unique()}")
