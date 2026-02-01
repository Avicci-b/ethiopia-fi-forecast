print("Testing project setup...")
import pandas as pd
import numpy as np
import matplotlib
import statsmodels
import prophet
import streamlit
import plotly
import sklearn

print("✅ All required packages imported successfully!")

# Test data load
df = pd.read_csv('data/raw/ethiopia_fi_unified_data.csv')
print(f"✅ Data loaded: {df.shape[0]} rows, {df.shape[1]} columns")

print("🎉 Setup verification complete!")
