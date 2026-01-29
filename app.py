import streamlit as st
import pandas as pd
import pickle
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(page_title="Naira Exchange Rate Predictor", page_icon="💱", layout="wide")

# Load data and model
@st.cache_resource
def load_model_and_data():
    # Load model
    with open('prophet_model.pkl', 'rb') as f:
        model = pickle.load(f)

    # Load historical data
    df_historical = pd.read_csv('exchange_rates.csv')
    df_historical['date'] = pd.to_datetime(df_historical['date'])

    #Load forecast
    df_forecast = pd.read_csv('forecast.csv')
    df_forecast['ds'] = pd.to_datetime(df_forecast['ds'])

    return model, df_historical, df_forecast

# Load data
try:
    model, df_historical, df_forecast = load_model_and_data()
    
    # Get key metrics
    latest_rate = df_historical['rate'].iloc[-1]
    latest_date = df_historical['date'].iloc[-1]
    
    # Get predictions 
    prediction_7d = df_forecast[df_forecast['ds'] > latest_date].iloc[6]
    prediction_30d = df_forecast[df_forecast['ds'] > latest_date].iloc[29]
    
    change_7d = prediction_7d['yhat'] - latest_rate
    change_30d = prediction_30d['yhat'] - latest_rate
    change_7d_pct = (change_7d / latest_rate) * 100
    change_30d_pct = (change_30d / latest_rate) * 100
    
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Title
st.title("💱 Naira Exchange Rate Predictor")
st.markdown("### AI-Powered USD/NGN Forecasting System")

#Current rate display
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Current Rate",
        f"₦{latest_rate:.2f}",
        f"As of {latest_date.strftime('%b %d, %Y')}"
    )

with col2:
    st.metric(
        "7-Day Forecast",
        f"₦{prediction_7d['yhat']:.2f}",
        f"{change_7d_pct:+.2f}%",
        delta_color="inverse"
    )

with col3:
    st.metric(
        "30-Day Forcast",
        f"₦{prediction_30d['yhat']:.2f}",
        f"{change_30d_pct:+.2f}%",
        delta_color="inverse"
    )

with col4:
    trend = "Weakening 📉" if change_30d > 0 else "Strengthening 📈"
    st.metric(
        "30-Day Trend",
        trend,
        f"₦{abs(change_30d):.2f}"
    )

st.markdown("---")

# Actionable insights
st.subheader("What This Means For You")

if change_30d > 0:
    st.warning(f"""
    ** Naira Expected to Weaken by {abs(change_30d_pct):.2f}%**
    
    **For Individuals:**
    - Consider buying dollars NOW if you have upcoming foreign expenses
    - Book international trips soon before prices increase
    - Online shopping from abroad? Buy now rather than later
    
    **For Businesses:**
    - Importers: Lock in current rates or hedge against increases
    - Budget for {abs(change_30d_pct):.1f}% increase in dollar-denominated costs
    - Exporters: Consider delaying dollar-to-naira conversions
    """)
else:
    st.success(f"""
    ** Naira Expected to Strengthen by {abs(change_30d_pct):.2f}%**
    
    **For Individuals:**
    - Wait to buy dollars if not urgent - you'll get better rates
    - Good time to convert dollars to naira
    
    **For Businesses:**
    - Importers: Prices may decrease, consider delaying major purchases
    - Exporters: Convert foreign earnings to naira sooner
    """)

st.markdown("---")

# Interactive chart
st.subheader("Historical Rates & Forecast")

# Create figure
fig = go.Figure()

# Historical data
fig.add_trace(go.Scatter(
    x=df_historical['date'],
    y=df_historical['rate'],
    name='Historical Rate',
    line=dict(color='#1f77b4', width=2),
    mode='lines'
))

# Future predictions
future_dates = df_forecast[df_forecast['ds'] > latest_date]

fig.add_trace(go.Scatter(
    x=future_dates['ds'],
    y=future_dates['yhat'],
    name='Predicted Rate',
    line=dict(color='#ff7f0e', width=2, dash='dash'),
    mode='lines'
))

# Confidence interval
fig.add_trace(go.Scatter(
    x=future_dates['ds'],
    y=future_dates['yhat_upper'],
    fill=None,
    mode='lines',
    line=dict(color='rgba(255,127,14,0)'),
    showlegend=False,
    hoverinfo='skip'
))

fig.add_trace(go.Scatter(
    x=future_dates['ds'],
    y=future_dates['yhat_lower'],
    fill='tonexty',
    mode='lines',
    line=dict(color='rgba(255,127,14,0)'),
    fillcolor='rgba(255,127,14,0.2)',
    name='Confidence Range',
    hoverinfo='skip'
))

# Update layout
fig.update_layout(
    title='USD/NGN Exchange Rate: Historical & 30-Day Forecast',
    xaxis_title='Date',
    yaxis_title='Exchange Rate (NGN per USD)',
    hovermode='x unified',
    height=500,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig, use_container_width=True)

# Detailed forecast table
st.markdown("---")
st.subheader("Detailed 30-Day Forecast")

forecast_display = future_dates[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
forecast_display.columns = ['Date', 'Predicted Rate', 'Lower Bound', 'Upper Bound']
forecast_display['Date'] = forecast_display['Date'].dt.strftime('%b %d, %Y')
forecast_display['Predicted Rate'] = forecast_display['Predicted Rate'].apply(lambda x: f"₦{x:.2f}")
forecast_display['Lower Bound'] = forecast_display['Lower Bound'].apply(lambda x: f"₦{x:.2f}")
forecast_display['Upper Bound'] = forecast_display['Upper Bound'].apply(lambda x: f"₦{x:.2f}")

st.dataframe(forecast_display, use_container_width=True, hide_index=True)

#Model info
st.markdown("---")
st.subheader("About This Prediction System")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    **How It Works:**
    - Uses Facebook Prophet time series algorithm
    - Trained on 2 years of historical USD/NGN data
    - Analyzes trends, weekly patterns, and seasonality
    - Provides 30-Day rolling forcast with confidence intervals
                
    **Data Source:**
    - Yahoo Finance (official exchange rates)
    - Trained on 2 years of historical data (2023-2025)
    - Model last trained: {latest_date.strftime('%b %d, %Y')}
    - Predictions valid for short-term forecasting (7-30 days)
    """)

with col2:
    st.markdown("""
    **Use Cases:**
    - Personal finance planning (travel, remittances, savings)
    - Import/export business decisions
    - Forex trading insights
    - Budget forecasting for dollar expenses
                
    **Accuracy Note:**
    - Exchange rates are influenced by many factors (policy, oil prices, global markets)
    - This model captures historical patterns but cannot predict sudden policy changes
    - Use as a guide, not absolute truth
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Built with Prophet, Streamlit & Python | Data updated daily from Yahoo Finance</p>
    <p>⚠️ This is a forecasting tool. Always consult financial advisors for major decisions. </p>
</div>
""", unsafe_allow_html=True)