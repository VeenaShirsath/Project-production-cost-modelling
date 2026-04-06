def apply_ramp_constraints(prev_gen, current_gen, ramp_rate):
    max_up = prev_gen + ramp_rate
    max_down = prev_gen - ramp_rate

    return max(min(current_gen, max_up), max_down)


def enforce_min_max(gen, requested):
    if requested == 0:
        return 0

    return max(gen["min_gen_mw"], min(requested, gen["capacity_mw"]))