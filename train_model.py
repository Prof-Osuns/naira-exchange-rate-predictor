import pandas as pd
import numpy as np
from prophet import Prophet
import pickle
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

print("Loading data...")
df = pd.read_csv('exchange_rates.csv')

print(f"\nDataset: {len(df)} days of exchange rates")
print(f"Date range: {df['date'].min()} to {df['date'].max()}")
print(f"Rate range: {df['rate'].min():.2f} to {df['rate'].max():.2f} NGN/USD")

# Prophet requires specific column names: 'ds' for date, 'y' for value
df_prophet = df.copy()
df_prophet.columns = ['ds', 'y']
df_prophet['ds'] = pd.to_datetime(df_prophet['ds'])

print("\n=== Training Prophet Model ===")
print("This will take 1-2 minutes...")

# Initialize and train model
model = Prophet(
    daily_seasonality=False,
    weekly_seasonality=True,
    yearly_seasonality=True,
    changepoint_prior_scale=0.05 # Makes model more flexible to changes
)

model.fit(df_prophet)

print("Model trained successfully!")

# Make predictions for the next 30 days
future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)

# Get latest actual rate and predictions
lastest_actual = df['rate'].iloc[-1]
latest_date = df['date'].iloc[-1]

print(f"\n=== Current Rate ===")
print(f"Date: {latest_date}")
print(f"Rate: {lastest_actual:.2f} NGN/USD")

print(f"\n=== 7-Day Forecast ===")
future_7_days = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(37).head(7)
for _, row in future_7_days.iterrows():
    if row['ds'] > pd.to_datetime(latest_date):
        print(f"{row['ds'].strftime('%Y-%m-%d')}: {row['yhat']:.2f} NGN/USD (range: {row['yhat_lower']:.2f} - {row['yhat_upper']:.2f})")

print(f"\n=== 30-Day Forecast ===")
predicted_30_days = forecast['yhat'].iloc[-1]
lower_bound = forecast['yhat_lower'].iloc[-1]
upper_bound = forecast['yhat_upper'].iloc[-1]

print(f"Predicted rate in 30 days: {predicted_30_days:.2f} NGN/USD")
print(f"Confidence range: {lower_bound:.2f} - {upper_bound:.2f} NGN/USD")

# Calculate change
change = predicted_30_days - lastest_actual
change_percent = (change / lastest_actual) * 100

if change > 0:
    print(f"Expected change: +{change:.2f} NGN ({change_percent:+.2f}%) - Naira weakening")
else:
    print(f"Expected change: {change:.2f} NGN ({change_percent:+.2f}%) - Naira strengthening")

# Save model
with open('prophet_model.pkl', 'wb') as f:
    pickle.dump(model, f)

# Save forecast
forecast.to_csv('forecast.csv', index=False)

print("\n Model and forecast saved!")
print("Files created: prophet_model.pkl, forecast.csv")