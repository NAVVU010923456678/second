from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import joblib

app = Flask(__name__)

# Load pre-trained models
water_model = load_model("water_model.h5")
scaler = MinMaxScaler()
solar_model = joblib.load("solar_model.pkl")

# Temporary in-memory storage for sensor data
sensor_data = pd.DataFrame(columns=['timestamp', 'water_level', 'solar_voltage'])

DIESEL_CO2_FACTOR = 2.68  # 1L diesel ~ 2.68kg CO2

# ---------------- Routes ---------------- #
@app.route("/sensor-data", methods=["POST"])
def receive_sensor_data():
    global sensor_data
    data = request.json
    sensor_data = pd.concat([sensor_data, pd.DataFrame([data])], ignore_index=True)
    return jsonify({"status":"success"}), 200

@app.route("/predict-inflow", methods=["GET"])
def predict_inflow():
    if len(sensor_data) < 10:
        return jsonify({"error":"Not enough data"}), 400
    last_seq = sensor_data['water_level'].values[-10:].reshape(-1,1)
    scaled_seq = scaler.fit_transform(last_seq)
    scaled_seq = scaled_seq.reshape((1, 10, 1))
    pred_scaled = water_model.predict(scaled_seq)
    pred = scaler.inverse_transform(pred_scaled)[0][0]
    return jsonify({"predicted_inflow": float(pred)})

@app.route("/forecast-solar", methods=["GET"])
def forecast_solar():
    future = solar_model.make_future_dataframe(periods=24, freq='H')
    forecast = solar_model.predict(future)
    result = forecast[['ds','yhat']].tail(24).to_dict(orient='records')
    return jsonify(result)

@app.route("/carbon-credits", methods=["GET"])
def carbon_credits():
    saved_energy_kwh = float(request.args.get('saved_energy_kwh', 0))
    diesel_efficiency_l_kwh = float(request.args.get('diesel_efficiency_l_kwh', 2))
    diesel_saved = saved_energy_kwh / diesel_efficiency_l_kwh
    carbon_saved = diesel_saved * DIESEL_CO2_FACTOR
    return jsonify({"carbon_saved_kg": carbon_saved})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
