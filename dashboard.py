import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.set_page_config(page_title="Dewatering AI Dashboard", layout="wide")
st.title("🚰 AI Dewatering Dashboard for Mines")

API_BASE = "https://<YOUR_BACKEND_URL>"

# ---------------- Water Level ---------------- #
st.subheader("Water Level Trend")
try:
    sensor_data = pd.DataFrame(requests.get(f"{API_BASE}/sensor-data").json())
    if not sensor_data.empty:
        fig1 = px.line(sensor_data, x='timestamp', y='water_level', title="Water Level Trend")
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("Waiting for sensor data...")
except:
    st.error("Unable to fetch sensor data.")

# ---------------- Solar Forecast ---------------- #
st.subheader("Solar Power Forecast (Next 24 hrs)")
try:
    solar_forecast = pd.DataFrame(requests.get(f"{API_BASE}/forecast-solar").json())
    fig2 = px.line(solar_forecast, x='ds', y='yhat', title="Predicted Solar Power (kW)")
    st.plotly_chart(fig2, use_container_width=True)
except:
    st.error("Unable to fetch solar forecast.")

# ---------------- Predicted Water Inflow ---------------- #
st.subheader("Predicted Water Inflow (Next Hour)")
try:
    inflow_resp = requests.get(f"{API_BASE}/predict-inflow").json()
    if "predicted_inflow" in inflow_resp:
        st.metric("Next Hour Predicted Inflow (L)", f"{inflow_resp['predicted_inflow']:.2f}")
except:
    st.error("Unable to fetch water inflow prediction.")

# ---------------- Carbon Credits ---------------- #
st.subheader("Carbon Credit Tracking")
try:
    carbon_resp = requests.get(f"{API_BASE}/carbon-credits?saved_energy_kwh=50&diesel_efficiency_l_kwh=2").json()
    st.metric("CO2 Saved (kg)", f"{carbon_resp['carbon_saved_kg']:.2f}")
except:
    st.error("Unable to fetch carbon credit data.")
