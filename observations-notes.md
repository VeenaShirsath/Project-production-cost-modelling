# With synthetic data:
## Economic Dispatch
- demand is not being  met with the current generation mix

## Unit Commitment
- adding loadshedding helps to make the solution feasible
- adding Reserve Requirement + Mim up/down times makes it infeasible, RR is the culprit
- Previous definition of RR: Any committed unit can instantly provide full spare capacity.

New definition of RR: Unused headroom from running generators, adding a reserve slack variable and reserve penalty -- feasible 

Main results:
1. ED - dispatch_20260406_164837.csv
2. UC (no RR and up/down limit, feasible) - dispatch_20260424_160905.csv
3. UC (RR and up/down limit, infeasible) - dispatch_20260424_161046.csv
4. UC (all above, feasible) - dispatch_20260424_163348.csv