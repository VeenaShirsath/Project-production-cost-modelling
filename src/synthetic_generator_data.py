import pandas as pd

data = {
  "generator_id": ["Nuke_1", "Coal_1", "Coal_2", "GasCC_1", "GasCC_2", "GasCT_1", "GasCT_2", "Wind_1", "Solar_1"],
  "fuel_type": ["Nuclear", "Coal", "Coal", "Gas", "Gas", "Gas", "Gas", "Wind", "Solar"],
  "capacity_mw": [1000, 600, 400, 500, 400, 200, 150, 300, 250],
  "min_gen_mw": [900, 300, 200, 200, 150, 0, 0, 0, 0],
  "heat_rate_mmbtu_per_mwh": [10, 10.5, 10.8, 7, 7.2, 10, 10.5, 0, 0],
  "fuel_cost_per_mmbtu": [0.7, 2.5, 2.5, 3, 3, 3, 3, 0, 0],
  "variable_om_cost": [2, 4, 4, 3, 3, 5, 5, 0, 0],
  "startup_cost": [50000, 20000, 15000, 10000, 8000, 2000, 1500, 0, 0],
  "ramp_rate_mw_per_hr": [50, 100, 80, 200, 180, 300, 300, 1000, 1000],
  "is_renewable": [0, 0, 0, 0, 0, 0, 0, 1, 1],
  "min_up_time":    [24, 12, 10, 6, 5, 1, 1, 0, 0], # in hours
  "min_down_time":  [24, 10, 8, 4, 4, 1, 1, 0, 0],
}

df = pd.DataFrame(data)

print("Generated df shape:", df.shape)

df.to_csv("data/generators/synthetic_generator_data.csv", index=False)
print("File saved successfully")