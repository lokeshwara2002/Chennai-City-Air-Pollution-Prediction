import json
import numpy as np
import datetime

# Set parameters
num_days = 120  # Forecast length
start_date = datetime.date.today()
mean_pm25 = 60  # Base PM2.5 level
variance = 30  # Allowed fluctuation

# Generate fluctuating PM2.5 values
np.random.seed(42)  # Ensures repeatability
pm25_forecast = np.round(np.random.normal(loc=mean_pm25, scale=variance, size=num_days), 2)

# Ensure values remain realistic (above 10 and below 300)
pm25_forecast = np.clip(pm25_forecast, 30, 300)

# Create forecast data
forecast_data = [
    {"date": (start_date + datetime.timedelta(days=i)).strftime("%Y-%m-%d"), "predicted_pm25": float(pm25_forecast[i])}
    for i in range(num_days)
]

# Save to JSON file
with open("C:/Users/ruchi/OneDrive/Desktop/chennai city project/backend/static/forecast.json", "w") as f:
    json.dump(forecast_data, f, indent=4)

print("✅ Forecast data saved successfully!")
