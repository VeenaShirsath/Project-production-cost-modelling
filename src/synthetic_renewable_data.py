import pandas as pd
import numpy as np

def generate_renewables(start="2024-01-01", hours=168):
    timestamps = pd.date_range(start=start, periods=hours, freq="h")

    solar_cf = []
    wind_cf = []

    for t in timestamps:
        hour = t.hour

        # Solar: bell curve
        solar = max(0, np.sin((hour - 6) / 12 * np.pi))
        solar_cf.append(round(solar, 2))

        # Wind: random but stable
        wind = np.clip(np.random.normal(0.45, 0.1), 0.1, 0.8)
        wind_cf.append(round(wind, 2))

    df = pd.DataFrame({
        "timestamp": timestamps,
        "wind_cf": wind_cf,
        "solar_cf": solar_cf
    })

    return df

# Load demand data to determine time period
demand = pd.read_csv("data/demand/load_1month_clean.csv")
num_hours = len(demand)
start_date = pd.to_datetime(demand["timestamp"].iloc[0], format="%m/%d/%Y %H:%M")

# Generate renewable data for the same period as demand
df = generate_renewables(start=start_date.strftime("%Y-%m-%d"), hours=num_hours)
print(f"Generated df shape: {df.shape} for {num_hours} hours starting from {start_date}")

# Format timestamp to MM/DD/YYYY HH:MM format
df["timestamp"] = df["timestamp"].dt.strftime("%m/%d/%Y %H:%M")

df.to_csv("data/renewables/synthetic_renewables.csv", index=False)
print("File saved successfully")