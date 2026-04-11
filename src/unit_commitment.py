import pandas as pd
from pyomo.environ import (
    ConcreteModel, Set, Param, Var, Objective, Constraint, NonNegativeReals, Binary, SolverFactory, summation
)
from src.renewables import compute_renewable_generation

def run_unit_commitment(generators_df, demand_df, renewables_df):
    model = ConcreteModel()

    # Sets
    model.G = Set(initialize=generators_df["generator_id"].tolist())
    model.T = Set(initialize=demand_df["timestamp"].tolist())

    # Parameters
    gen_data = generators_df.set_index("generator_id").to_dict(orient="index")
    demand_data = demand_df.set_index("timestamp")["demand_mw"].to_dict()

    # Capacity limits
    model.Pmax = Param(model.G, initialize={g: gen_data[g]["capacity_mw"] for g in model.G})
    model.Pmin = Param(model.G, initialize={g: gen_data[g]["min_gen_mw"] for g in model.G})
    model.marginal_cost = Param(model.G, initialize={g: gen_data[g]["marginal_cost"] for g in model.G})
    model.startup_cost = Param(model.G, initialize={g: gen_data[g].get("startup_cost", 0) for g in model.G})
    model.ramp_rate = Param(model.G, initialize={g: gen_data[g]["ramp_rate_mw_per_hr"] for g in model.G})

    # Variables
    model.P = Var(model.G, model.T, within=NonNegativeReals)  # MW output
    model.u = Var(model.G, model.T, within=Binary)            # on/off status
    model.v = Var(model.G, model.T, within=Binary)            # startup indicator

    # Objective: Minimize total cost
    def total_cost_rule(m):
        fuel_vom_cost = sum(m.marginal_cost[g] * m.P[g, t] for g in m.G for t in m.T)
        startup_cost = sum(m.startup_cost[g] * m.v[g, t] for g in m.G for t in m.T)
        return fuel_vom_cost + startup_cost

    model.TotalCost = Objective(rule=total_cost_rule, sense=1)  # Minimize

    # Constraints

    # Power balance (demand minus renewable)
    def power_balance_rule(m, t):
        ren_row = renewables_df.loc[renewables_df["timestamp"] == t]
        renewable_gen = compute_renewable_generation(generators_df, ren_row.iloc[0]) if not ren_row.empty else 0
        net_load = max(demand_data[t] - renewable_gen, 0)
        return sum(m.P[g, t] for g in m.G) == net_load

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
    def ramp_rule(m, g, t):
        sorted_t = sorted(model.T)
        idx = sorted_t.index(t)
        if idx == 0:
            return Constraint.Skip  # first hour, no previous
        t_prev = sorted_t[idx - 1]
        return abs(m.P[g, t] - m.P[g, t_prev]) <= m.ramp_rate[g]
    model.RampLimit = Constraint(model.G, model.T, rule=ramp_rule)

    # Solve
    solver = SolverFactory("glpk")  # or CBC
    results = solver.solve(model, tee=True)

    # Extract results
    dispatch_results = []
    for g in model.G:
        for t in model.T:
            dispatch_results.append({
                "generator_id": g,
                "timestamp": t,
                "generation_mw": model.P[g, t].value,
                "on_status": model.u[g, t].value,
                "startup": model.v[g, t].value
            })

    return pd.DataFrame(dispatch_results)
