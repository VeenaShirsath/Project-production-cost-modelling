from src.unit_commitment import run_unit_commitment
import pandas as pd
from src.utils import save_results

# Load data
generators = pd.read_csv("data/generators/synthetic_ercot_fleet.csv")
demand = pd.read_csv("data/demand/load_2week_clean.csv", parse_dates=["timestamp"])
renewables = pd.read_csv("data/renewables/synthetic_renewables.csv", parse_dates=["timestamp"])

# Run Unit Commitment
dispatch_results = run_unit_commitment(generators, demand, renewables)

df = pd.DataFrame(dispatch_results)

# total generation per timestamp
df["total_generation_mw"] = df.groupby("timestamp")["generation_mw"].transform("sum")

# curtailment = excess renewables
df["curtailment_mw"] = (
    df["renewable_gen_mw"] - (df["demand_mw"] - df["total_generation_mw"])
).clip(lower=0)

# Save results (same style as dispatch.py)
save_results(df)