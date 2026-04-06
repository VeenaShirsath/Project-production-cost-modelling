import pandas as pd


def load_renewables(path):
    return pd.read_csv(path, parse_dates=["timestamp"])


def compute_renewable_generation(generators, renewables_row):
    wind_capacity = generators.loc[
        generators["fuel_type"] == "Wind", "capacity_mw"
    ].sum()

    solar_capacity = generators.loc[
        generators["fuel_type"] == "Solar", "capacity_mw"
    ].sum()

    wind_gen = wind_capacity * renewables_row["wind_cf"]
    solar_gen = solar_capacity * renewables_row["solar_cf"]

    return wind_gen + solar_gen


def compute_net_load(demand_mw, renewable_gen):
    return max(demand_mw - renewable_gen, 0)