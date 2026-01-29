# 💱 Naira Exchange Rate Predictor

An AI-powered forecasting system that predicts USD/NGN exchange rates for the next 30 days with 95% confidence intervals, helping Nigerians and businesses make informed financial decisions.

## Live Demo
[Try it here](#) *(link after deployment)*

## Why This Matters

**The Problem:**
- Exchange rate volatility costs Nigerians billions annually
- Importers struggles to plan costs and pricing
- Individuals lose money on poorly-timed forex purchases
- No accessible tools for rate forecasting

**The Solution:**
This system predicts USD/NGN rates 7-30 days in advance, giving users time to:
- Plan forex purchases strategically
- Budget for import costs accurately
- Time dollar conversions optimally
- Make data-driven financial decisions

**Real Impact:**
- A business importing $50,000 monthly could save ₦400,000+ annually by timing purchases better
- Individuals planning travel or tuition can save 3-6% by acting on predictions
- Remittance recipients can maximize naira value by timing conversions

## Current Predictions (as of Jan 2026)

**Model forecasts naira weakening:**
- Current rate: ₦1,411/USD
- 30-day forecast: ₦1,496/USD
- Expected change: +6% (naira weakening)

**Actionable insight:** If you need dollars in the next month, buy now rather than waiting.

## How It Works

**Technology:**
- **Prophet** (Facebook's time series forecasting algorithm)
- Trained on 2 years of daily USD/NGN exchange rates
- Analyzes trends, weekly patterns, and seasonality
- Provides confidence intervals for predictions

**Data Pipeline:**
1. Fetch historical rates from Yahoo Finance
2. Preprocess and clean data
3. Train Prophet model on patterns
4. Generate 30-day rolling forecasts
5. Display interactive dashboard

## Features

- **7 & 30-day forecasts** with confidence ranges
- **Trend analysis** (strengthening vs weakening)
- **Actionable recommendations** for individuals and businesses
- **Interactive visualizations** showing historical data + predictions
- **Detailed forecast table** with daily predictions

## Model Performance

- **Training data:** 730 days of historical rates
- **Algorithm:** Facebook Prophet (optimized for time series)
- **Confidence intervals:**  95% (upper and lower bounds)
- **Update frequency:** Manual weekly (production would be daily)

## Technical Stacl

- **Python 3.14.1**
- **Prophet** - Time series forecasting
- **yfinance** - Exchange rate data
- **Streamlit** - Interactive web app
- **Plotly** - Data visualization
- **Pandas & NumPy** - Data processing

## Run Locally

```bash
# Clone repository
git clone https://github.com/Prof-Osuns/naira-exchange-rate-predicto.git
cd naira-exchange-rate-predictor

# Install dependencies
pip install -r requirements.txt

# Collect data and train model
python data_collection.py
python train_model.py

# Run application
streamlit run app.py
```

## Project Structure

- data_collection.py # Fetch exchange rate from Yahoo Finance
- train_model.py # Train Prophet forecasting model
- app.py # Streamlit dashboard
- requirements.txt # Dependencies
- README.md # Documentation

## What I Learned

- **Time series forecasting** - Prophet, seasonality, trend analysis
- **Financial data processing** - Working with exchange rates and forex data
- **Production ML considerations** - Data pipelines, model versioning, update schedules
- **Nigeria-specific problem solving** - Understanding local market needs
- **Business value translation** - Converting predictions to actionable insights

## Future Enhancements

- Daily automated data updates via GitHub Actions
- SMS/email alerts for significant rate changes
- API endpoint for integration with fintech apps
- Historical accuracy tracking and model retraining triggers
- Multi-currency support(GBP,EUR,etc.)

## Disclaimer
This tool is for informational purposes only.
Exchange rates are influenced by many unpredictable factors(CBN policy, oil prices, global markets). Always consult financial advisors for major decisions.

## Author
Ayomikun Osunseyi - AI/ML Engineer
[LinkedIn](https://www.linkedin.com/in/ayomikun-osunseyi-bba3a71b3/) [Github](https://github.com/Prof-Osuns)

## Related Projects
- [House Price Predictor](https://github.com/Prof-Osuns/house-price-predictor) - ML regression model
- [Customer Churn Predictor](https://github.com/Prof-Osuns/customer-churn-predictor) - Business ML application