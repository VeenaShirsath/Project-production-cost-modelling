#dispatch.py:

import pandas as pd
from src.renewables import compute_renewable_generation, compute_net_load
from src.constraints import apply_ramp_constraints, enforce_min_max, apply_availability


def economic_dispatch_single_hour(generators, demand_mw):
    gens = generators.sort_values("marginal_cost").copy()
    remaining_demand = demand_mw
    dispatch = []

    for _, gen in gens.iterrows():
        if remaining_demand <= 0:
            dispatch.append(0)
            continue

        requested = min(gen["capacity_mw"], remaining_demand)
        # Apply forced outage / availability
        generation = apply_availability(gen, requested)

        dispatch.append(generation)
        remaining_demand -= generation

    gens["generation_mw"] = dispatch

    if remaining_demand > 0:
        print(f"⚠️ Warning: Unmet demand = {remaining_demand:.2f} MW")

    return gens


def run_dispatch(generators, demand, renewables, reserve_margin=0.05):
    results = []
    prev_dispatch = {gen: 0 for gen in generators["generator_id"]}

    for _, row in demand.iterrows():
        timestamp = row["timestamp"]
        demand_mw = row["demand_mw"]

        ren_row = renewables.loc[renewables["timestamp"] == timestamp]
        if ren_row.empty:
            raise ValueError(f"No renewable data for timestamp {timestamp}")
        ren_row = ren_row.iloc[0]

        renewable_gen = compute_renewable_generation(generators, ren_row)
        net_load = compute_net_load(demand_mw, renewable_gen, reserve_margin)

        thermal_gens = generators[generators["is_renewable"] == 0].copy()
        dispatch_result = economic_dispatch_single_hour(thermal_gens, net_load)

        # Apply ramp constraints and update previous generation
        for idx, gen in dispatch_result.iterrows():
            gen_id = gen["generator_id"]
            prev = prev_dispatch[gen_id]
            ramp = gen["ramp_rate_mw_per_hr"]
            current = gen["generation_mw"]
            adjusted = apply_ramp_constraints(prev, current, ramp)

            dispatch_result.at[idx, "generation_mw"] = adjusted
            prev_dispatch[gen_id] = adjusted

            # Compute emissions if emission_rate is present
            if "emission_rate_ton_per_mwh" in gen:
                dispatch_result.at[idx, "emissions_ton"] = adjusted * gen["emission_rate_ton_per_mwh"]

        # Add metadata
        dispatch_result["timestamp"] = timestamp
        dispatch_result["demand_mw"] = demand_mw
        dispatch_result["renewable_gen_mw"] = renewable_gen
        dispatch_result["net_load_mw"] = net_load
        dispatch_result["curtailment_mw"] = max(renewable_gen - demand_mw, 0)

        results.append(dispatch_result)

    return pd.concat(results, ignore_index=True)