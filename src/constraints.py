#constriaints.py:

def apply_ramp_constraints(prev_gen, current_gen, ramp_rate):
    """
    Enforce ramp rate limits.
    """
    max_up = prev_gen + ramp_rate
    max_down = prev_gen - ramp_rate
    return max(min(current_gen, max_up), max_down)


def enforce_min_max(gen, requested):
    """
    Enforce min/max generation limits.
    """
    if requested == 0:
        return 0
    return max(gen["min_gen_mw"], min(requested, gen["capacity_mw"]))


def apply_availability(gen, requested):
    """
    Apply forced outage probability (availability_factor 0-1).
    Reduces max possible output proportionally.
    """
    effective_capacity = gen["capacity_mw"] * gen.get("availability_factor", 1.0)
    # Clamp requested to effective capacity
    requested = min(requested, effective_capacity)
    return enforce_min_max(gen, requested)