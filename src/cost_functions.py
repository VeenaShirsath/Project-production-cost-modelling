def compute_marginal_cost(generators):
    generators = generators.copy()

    generators["marginal_cost"] = (
        generators["heat_rate_mmbtu_per_mwh"] * generators["fuel_cost_per_mmbtu"]
        + generators["variable_om_cost"]
    )

    return generators
