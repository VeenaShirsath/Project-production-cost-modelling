from src.unit_commitment import run_unit_commitment
import pandas as pd

# Load data
generators = pd.read_csv("data/generators/synthetic_generator_data.csv")
demand = pd.read_csv("data/demand/load_1month_clean.csv", parse_dates=["timestamp"])
renewables = pd.read_csv("data/renewables/synthetic_renewables.csv", parse_dates=["timestamp"])

# Run Unit Commitment
uc_results = run_unit_commitment(generators, demand, renewables)

uc_results["total_generation_mw"] = uc_results.groupby("timestamp")["generation_mw"].transform("sum")
uc_results["curtailment_mw"] = (renewables_total - (demand["demand_mw"] - uc_results["total_generation_mw"])).clip(lower=0)

# Save results (same style as dispatch.py)
uc_results.to_csv("results/dispatch_runs/uc_dispatch.csv", index=False)