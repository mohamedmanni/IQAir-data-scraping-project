import requests
import csv
import os
from datetime import datetime, timezone

# The API configuration
api_key = os.environ.get('IQAIR_API_KEY', 'f8d9c115-5bd6-4cda-8335-45fc46aaf2b8')
base_url = 'https://api.airvisual.com/v2/city'
params = {
    'city': 'London',
    'state': 'England',
    'country': 'United Kingdom',
    'key': api_key
}

# To fetch the data from the API
response = requests.get(base_url, params=params)

if response.status_code != 200:
    print(f"API request failed: {response.status_code} - {response.text}")
    exit()

data = response.json()

if data['status'] != 'success':
    print(f"API error: {data.get('data', 'No data')}")
    exit()

# To extract current data
current = data['data']['current']
pollution = current['pollution']
weather = current['weather']
aqi_us = pollution['aqius']
main_pollutant = pollution['mainus']
ts = datetime.now(timezone.utc).isoformat()

# The pollutant concentrations
pollutants = {
    'PM2.5': pollution.get('pm2_5', 'N/A'),
    'PM10': pollution.get('pm10', 'N/A'),
    'O3': pollution.get('o3', 'N/A'),
    'NO2': pollution.get('no2', 'N/A'),
    'SO2': pollution.get('so2', 'N/A'),
    'CO': pollution.get('co', 'N/A')
}

# The weather data
temp = weather['tp']
humidity = weather['hu']
wind_speed = weather['ws']

# Create output directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# Write current data to CSV
csv_file = 'data/london_bloomsbury.csv'
file_exists = os.path.exists(csv_file)

row_data = {
    'Timestamp': ts,
    'AQI (US)': aqi_us,
    'Main Pollutant': main_pollutant,
    'PM2.5 (µg/m³)': pollutants['PM2.5'],
    'PM10 (µg/m³)': pollutants['PM10'],
    'O3 (µg/m³)': pollutants['O3'],
    'NO2 (µg/m³)': pollutants['NO2'],
    'SO2 (µg/m³)': pollutants['SO2'],
    'CO (µg/m³)': pollutants['CO'],
    'Temperature (°C)': temp,
    'Humidity (%)': humidity,
    'Wind Speed (m/s)': wind_speed
}

fieldnames = list(row_data.keys())

with open(csv_file, 'a', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    if not file_exists:
        writer.writeheader()
    writer.writerow(row_data)

print(f"Data fetched from API and appended to {csv_file}")