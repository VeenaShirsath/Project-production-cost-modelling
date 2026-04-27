import pandas as pd
import numpy as np

generators = []

def add_units(prefix, fuel, count, cap_range, min_frac, heat_rate, fuel_cost,
              vom, startup, ramp, min_up, min_down, renewable):
    for i in range(count):
        cap = np.random.randint(*cap_range)
        generators.append({
            "generator_id": f"{prefix}_{i+1}",
            "fuel_type": fuel,
            "capacity_mw": cap,
            "min_gen_mw": int(cap * min_frac),
            "heat_rate_mmbtu_per_mwh": heat_rate,
            "fuel_cost_per_mmbtu": fuel_cost,
            "variable_om_cost": vom,
            "startup_cost": startup,
            "ramp_rate_mw_per_hr": ramp,
            "is_renewable": renewable,
            "min_up_time": min_up,
            "min_down_time": min_down,
        })

# ------------------------
# Nuclear (~5 GW)
# ------------------------
add_units("Nuke", "Nuclear", 4, (1200, 1400), 0.9, 10, 0.7, 2, 80000, 50, 24, 24, 0)

# ------------------------
# Coal (~8 GW)
# ------------------------
add_units("Coal", "Coal", 10, (600, 900), 0.4, 10.5, 2.5, 4, 30000, 100, 12, 10, 0)

# ------------------------
# CCGT (~35 GW)
# ------------------------
add_units("CCGT", "Gas", 25, (800, 1200), 0.3, 7, 3, 3, 15000, 300, 6, 4, 0)

# ------------------------
# Gas CT (~20 GW)
# ------------------------
add_units("CT", "Gas", 40, (200, 400), 0.05, 10, 3.5, 6, 5000, 600, 1, 1, 0)

# ------------------------
# Wind (~20 GW)
# ------------------------
add_units("Wind", "Wind", 50, (200, 500), 0.0, 0, 0, 0, 0, 1000, 0, 0, 1)

# ------------------------
# Solar (~10 GW)
# ------------------------
add_units("Solar", "Solar", 40, (100, 300), 0.0, 0, 0, 0, 0, 1000, 0, 0, 1)

df = pd.DataFrame(generators)

print("Total capacity:", df["capacity_mw"].sum())
print(df.groupby("fuel_type")["capacity_mw"].sum())

df.to_csv("data/generators/synthetic_ercot_fleet.csv", index=False)

"""
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
"min_up_time": [24, 12, 10, 6, 5, 1, 1, 0, 0], # in hours 
"min_down_time": [24, 10, 8, 4, 4, 1, 1, 0, 0], } 

df = pd.DataFrame(data) 
print("Generated df shape:", df.shape) 
df.to_csv("data/generators/synthetic_generator_data.csv", index=False) 
print("File saved successfully")
"""