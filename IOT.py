import urequests
import ujson
import machine
import time

# Pin setup
WATER_LEVEL_SENSOR_PIN = 34
SOLAR_SENSOR_PIN = 35

def read_sensors():
    water_level = machine.ADC(machine.Pin(WATER_LEVEL_SENSOR_PIN)).read()
    solar_voltage = machine.ADC(machine.Pin(SOLAR_SENSOR_PIN)).read()
    return water_level, solar_voltage

def send_data():
    url = "https://<YOUR_BACKEND_URL>/sensor-data"
    water, solar = read_sensors()
    payload = {
        "timestamp": time.time(),
        "water_level": water,
        "solar_voltage": solar
    }
    headers = {'Content-Type': 'application/json'}
    response = urequests.post(url, data=ujson.dumps(payload), headers=headers)
    print(response.text)

while True:
    send_data()
    time.sleep(60)  # send data every 1 min
