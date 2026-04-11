from src.dispatch import run_dispatch
from src.utils import save_results
from src.cost_functions import compute_marginal_cost
from src.renewables import load_renewables

import pandas as pd

def main():
    generators = pd.read_csv("data/generators/synthetic_generator_data.csv")
    demand = pd.read_csv("data/demand/load_1month_clean.csv")
    renewables = load_renewables("data/renewables/synthetic_renewables.csv")
    
    # Convert timestamps to datetime for proper alignment
    demand["timestamp"] = pd.to_datetime(demand["timestamp"], format="%m/%d/%Y %H:%M")
    renewables["timestamp"] = pd.to_datetime(renewables["timestamp"], format="%m/%d/%Y %H:%M")

    # Ensure timestamps align
    demand = demand.sort_values("timestamp")
    renewables = renewables.sort_values("timestamp")

    generators = compute_marginal_cost(generators)

    dispatch_df = run_dispatch(generators, demand, renewables)

    save_results(dispatch_df)

if __name__ == "__main__":
    main()

