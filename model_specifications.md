## UC:
It solves a mixed-integer optimization problem that decides:
1. Which generators should be ON/OFF
2. How much each generator should produce
3. While minimizing total system cost
4. Subject to physical and reliability constraints

### Model Parameters:
These are fixed inputs to the optimization:

**Generator-level:**
1. ```Pmax``` $\rightarrow$ max capacity
2. ```Pmin``` $\rightarrow$ minimum stable output
3. ```marginal_cost``` $\rightarrow$ variable cost
4. ```startup_cost``` $\rightarrow$ cost to turn ON
5. ```ramp_rate``` $\rightarrow$ MW/hr constraint
6. ```min_up, min_down``` $\rightarrow$ temporal constraints

**System-level:**
1. ```demand[t]```

### Decision Variables:
**Continuous:** ```model.P[g,t]``` $\rightarrow$ Power output (MW)
**Binary:** ```model.u[g,t], model.v[g,t]``` $\rightarrow$ ON/OFF status, Startup indicator
**Slack Variable:** ```model.LS[t]. model.RS[t]``` $\rightarrow$ Load shedding, Reserve shortfall

### Objective Function:

Minimize Fuel + Startup + Load Shedding + Reserve Shortfall and
* Fuel + VOM = ```marginal_cost + P ```
* Startup Cost = ```startup_cost * v ```
* Load Shedding Penalty = ``` value + LS```
* Reserve Penalty = ```value * RS ```

Priority order is: meet demand $\rightarrow$ maintain reserve $\rightarrow$ minimize cost

### Constraints:
1. Power Balance: $sum$ P + LS = Demand - Renewables
2. Capacity Constraints
3. Startup Logic: ```v[g,t] ≥ u[g,t] − u[g,t−1]```
4. Ramp Constraints: ```|P[g,t] − P[g,t−1]| ≤ ramp_rate```
5. Minimum Up Time: ```Σ u ≥ min_up * (startup event)```
6. Minimum Down Time: ```Σ (1 − u) ≥ min_down * (shutdown event)```
7. Reserve: ```(Pmax - P) + RS ≥ reserve requirement```

### Final output gives:
```
generator_id

timestamp

generation_mw

on_status

startup
demand_mw

renewable_gen_mw

net_load_mw

load_shedding_mw
```

