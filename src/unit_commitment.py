from pyexpat import model

import pandas as pd
from pyomo.environ import (
    ConcreteModel, Set, Param, Var, Objective, Constraint, NonNegativeReals, Binary, SolverFactory, summation
)
from src.renewables import compute_renewable_generation
from src.cost_functions import compute_marginal_cost

def run_unit_commitment(generators_df, demand_df, renewables_df):

    generators_df = compute_marginal_cost(generators_df)

    required_cols = [
    "capacity_mw",
    "min_gen_mw",
    "ramp_rate_mw_per_hr",
    "marginal_cost"]

    for col in required_cols:
        if col not in generators_df.columns:
            raise ValueError(f"Missing required column: {col}")

    model = ConcreteModel()

    # Sets
    model.G = Set(initialize=generators_df["generator_id"].tolist())
    time_list = sorted(demand_df["timestamp"].tolist())
    model.T = Set(initialize=time_list, ordered=True)

    first_t = time_list[0] 

    # Parameters
    gen_data = generators_df.set_index("generator_id").to_dict(orient="index")
    demand_data = demand_df.set_index("timestamp")["demand_mw"].to_dict()

    # Capacity limits
    model.Pmax = Param(model.G, initialize={g: gen_data[g]["capacity_mw"] for g in model.G})
    model.Pmin = Param(model.G, initialize={g: gen_data[g]["min_gen_mw"] for g in model.G})
    model.marginal_cost = Param(model.G, initialize={g: gen_data[g]["marginal_cost"] for g in model.G})
    model.startup_cost = Param(model.G, initialize={g: gen_data[g].get("startup_cost", 0) for g in model.G})
    model.ramp_rate = Param(model.G, initialize={g: gen_data[g]["ramp_rate_mw_per_hr"] for g in model.G})
    model.min_up = Param(model.G, initialize={g: gen_data[g].get("min_up_time", 1) for g in model.G})
    model.min_down = Param(model.G, initialize={g: gen_data[g].get("min_down_time", 1) for g in model.G})

    model.demand = Param(model.T, initialize=demand_data)

    # Variables
    model.P = Var(model.G, model.T, within=NonNegativeReals)  # MW output
    model.u = Var(model.G, model.T, within=Binary)            # on/off status
    model.v = Var(model.G, model.T, within=Binary)            # startup indicator
    model.LS = Var(model.T, within=NonNegativeReals)  # Load shedding
    model.RS = Var(model.T, within=NonNegativeReals)  # reserve shortfall
    
    
    # Reserve Requirement
    reserve_margin = 0.05  # 5% spinning reserve (configurable)
    def reserve_constraint(m, t):
        required_reserve = reserve_margin * m.demand[t]

        available_reserve = sum(
            (m.Pmax[g] - m.P[g, t]) for g in m.G
        )

        return available_reserve + m.RS[t] >= required_reserve

    model.ReserveRequirement = Constraint(model.T, rule=reserve_constraint)

    # Objective: Minimize total cost
    LOAD_SHEDDING_COST = 10000  # very high penalty

    RESERVE_PENALTY = 5000  # lower than load shedding, but still high

    def total_cost_rule(m):
        fuel_vom_cost = sum(m.marginal_cost[g] * m.P[g, t] for g in m.G for t in m.T)
        startup_cost = sum(m.startup_cost[g] * m.v[g, t] for g in m.G for t in m.T)
        load_shedding_cost = sum(LOAD_SHEDDING_COST * m.LS[t] for t in m.T)
        reserve_penalty = sum(RESERVE_PENALTY * m.RS[t] for t in m.T)

        return fuel_vom_cost + startup_cost + load_shedding_cost + reserve_penalty

    model.TotalCost = Objective(rule=total_cost_rule, sense=1)  # Minimize

    # Constraints

    # Power balance (demand minus renewable)
    def power_balance_rule(m, t):
        ren_row = renewables_df.loc[renewables_df["timestamp"] == t]
        renewable_gen = compute_renewable_generation(generators_df, ren_row.iloc[0]) if not ren_row.empty else 0
        net_load = max(demand_data[t] - renewable_gen, 0)
        return sum(m.P[g, t] for g in m.G) + m.LS[t] >= net_load

    model.PowerBalance = Constraint(model.T, rule=power_balance_rule)

    # Capacity limits
    def capacity_rule(m, g, t):
        return m.Pmin[g] * m.u[g, t] <= m.P[g, t]
    model.MinGen = Constraint(model.G, model.T, rule=capacity_rule)

    def capacity_max_rule(m, g, t):
        return m.P[g, t] <= m.Pmax[g] * m.u[g, t]
    model.MaxGen = Constraint(model.G, model.T, rule=capacity_max_rule)

    # Startup logic
    def startup_rule(m, g, t):
        sorted_t = sorted(model.T)
        idx = sorted_t.index(t)
        if idx == 0:
            return m.v[g, t] >= m.u[g, t]  # assume off initially
        t_prev = sorted_t[idx - 1]
        return m.v[g, t] >= m.u[g, t] - m.u[g, t_prev]
    model.StartupLogic = Constraint(model.G, model.T, rule=startup_rule)

    # Ramp constraints
    def ramp_up_rule(m, g, t):
        if t == first_t:
            return Constraint.Skip

        t_prev = m.T.prev(t)
        return m.P[g, t] - m.P[g, t_prev] <= m.ramp_rate[g]


    def ramp_down_rule(m, g, t):
        if t == first_t:
            return Constraint.Skip

        t_prev = m.T.prev(t)
        return m.P[g, t_prev] - m.P[g, t] <= m.ramp_rate[g]


    model.RampUp = Constraint(model.G, model.T, rule=ramp_up_rule)
    model.RampDown = Constraint(model.G, model.T, rule=ramp_down_rule)
    
    # Minimum up time
    def min_up_time_rule(m, g, t):
        t_index = time_list.index(t)

        # skip early hours
        if t_index < m.min_up[g]:
            return Constraint.Skip

        return sum(m.u[g, time_list[k]] for k in range(t_index - int(m.min_up[g]) + 1, t_index + 1)) >= \
            m.min_up[g] * (m.u[g, t] - m.u[g, time_list[t_index - 1]])

    model.MinUpTime = Constraint(model.G, model.T, rule=min_up_time_rule)

    # Minimum down time
    def min_down_time_rule(m, g, t):
        t_index = time_list.index(t)

        if t_index < m.min_down[g]:
            return Constraint.Skip

        return sum(1 - m.u[g, time_list[k]] for k in range(t_index - int(m.min_down[g]) + 1, t_index + 1)) >= \
            m.min_down[g] * (m.u[g, time_list[t_index - 1]] - m.u[g, t])

    model.MinDownTime = Constraint(model.G, model.T, rule=min_down_time_rule)
    
    # Solve
    solver = SolverFactory("cbc") # cbc or highs
    results = solver.solve(model, tee=True)

    # adding more details to the result
    renewable_dict = {}
    net_load_dict = {}

    for t in model.T:
        renewables_map = renewables_df.set_index("timestamp")

        if t in renewables_map.index:
            renewable_gen = compute_renewable_generation(generators_df, renewables_map.loc[t])
        else:
            renewable_gen = 0

        renewable_dict[t] = renewable_gen
        net_load_dict[t] = max(demand_data[t] - renewable_gen, 0)

    load_shedding_dict = {t: model.LS[t].value for t in model.T}

    # Extract results
    dispatch_results = []

    for g in model.G:
        for t in model.T:
            dispatch_results.append({
                "generator_id": g,
                "timestamp": t,
                "generation_mw": model.P[g, t].value,
                "on_status": model.u[g, t].value,
                "startup": model.v[g, t].value,

                # Align with dispatch output
                "demand_mw": demand_data[t],
                "renewable_gen_mw": renewable_dict[t],
                "net_load_mw": net_load_dict[t],
                "load_shedding_mw": load_shedding_dict[t]
            })

    return pd.DataFrame(dispatch_results)
