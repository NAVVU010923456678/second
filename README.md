# Dewatering AI Dashboard

This project is a fully AI-integrated dashboard for solar-powered dewatering in mines.

## Features
- Real-time water level monitoring
- Water inflow prediction using LSTM
- Solar power forecasting using Prophet
- Carbon credit tracking
- Fully integrated with IoT sensors (ESP32)

## Deployment
1. Train the AI models using 'data/water_inflow.csv' and 'data/solar_power.csv'.
2. Run 'Backend/app.py' (Flask API).
3. Run 'Dashboard/dashboard.py' (Streamlit) or deploy on Streamlit Cloud.
4. Update ESP32 IoT code with the deployed backend URL.
