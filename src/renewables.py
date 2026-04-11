#renewables.py:
import pandas as pd

def load_renewables(path):
    return pd.read_csv(path, parse_dates=["timestamp"])


def compute_renewable_generation(generators, renewables_row):
    """
    Computes total renewable generation from wind and solar.
    """
    wind_capacity = generators.loc[generators["fuel_type"] == "Wind", "capacity_mw"].sum()
    solar_capacity = generators.loc[generators["fuel_type"] == "Solar", "capacity_mw"].sum()

    wind_gen = wind_capacity * renewables_row.get("wind_cf", 0)
    solar_gen = solar_capacity * renewables_row.get("solar_cf", 0)

    return wind_gen + solar_gen


def compute_net_load(demand_mw, renewable_gen, reserve_margin=0.05):
    """
    Net load = demand - renewable, plus reserve margin.
    """
    net_load = max(demand_mw - renewable_gen, 0)
    net_load_with_reserve = net_load * (1 + reserve_margin)
    return net_load_with_reserve