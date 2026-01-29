import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

def fetch_exchange_rates():
    """
    Fetch USD/NGN exchange rate data using Yahoo Finance
    """
    print("Fetching exchange rate data from Yahoo Finance...")

    # Get 2 years of data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)

    # Yahoo Finance ticker for USD/NGN
    ticker = "NGN=X"

    try:
        # Download data
        df = yf.download(ticker, start=start_date, end=end_date, progress=False)

        # Reset index to make date a column
        df = df.reset_index()

        # Keep only date and closing
        df = df[['Date', 'Close']]
        df.columns = ['date', 'rate']

        # Remove any NaN values
        df = df.dropna()

        print(f"\n Fetched {len(df)} data points")
        print(f"Date range: {df['date'].min()} to {df['date'].max()}")
        print(f"Rate range: {df['rate'].min():.2f} to {df['rate'].max():.2f} NGN/USD")
        print(f"\nFirst few rows:")
        print(df.head())
        print(f"\nLast few rows:")
        print(df.tail())

        # Save to CSV
        df.to_csv('exchange_rates.csv', index=False)
        print(f"\n Saved to exchange_rates.csv")

        return df
    
    except Exception as e:
            print(f"Error: {e}")
            return None

if __name__ == "__main__":
    df = fetch_exchange_rates()