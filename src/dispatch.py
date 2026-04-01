### Economic Dispatch Logic:
#   1. Compute marginal cost
#   2. Sort generators from cheapest to expnsive
#   3. Allocate generation until demand is met

import pandas as pd

def load_data(gen_path, demand_path):
    generators = pd.read_csv(gen_path)
    demand = pd.read_csv(demand_path, parse_dates=['Hour Ending'])
    return generators, demand

def compute_marginal_cost(generators):
    generators["marginal_cost"] = (
        generators["heat_rate_mmbtu_per_mwh"] * generators["fuel_cost_per_mmbtu"] + 
        generators["variable_om_cost"]
    )
    return generators

def economic_dispatch_single_hour(generators, demand_mw):
    gens = generators.sort_values("marginal_cost").copy()

    remaining_demand = demand_mw
    dispatch = []

    for _, gen in gens.iterrows():
        if remaining_demand <= 0:
            dispatch.append(0)
            continue

        available = gen["capacity_mw"]
        generation = min(available, remaining_demand)

        dispatch.append(generation)
        remaining_demand -= generation

    gens["generation_mw"] = dispatch

    if remaining_demand > 0:
        print(f"Warning: Demand not fully met. Remaining: {remaining_demand} MW")

    return gens

def run_dispatch(generators, demand):
    results = []

    for _, row in demand.iterrows():
        timestamp = row["Hour Ending"]
        demand_mw = row["ERCOT"]

        dispatch_result = economic_dispatch_single_hour(generators, demand_mw)
        dispatch_result["Hour Ending"] = timestamp

        results.append(dispatch_result)
    return pd.concat(results)
