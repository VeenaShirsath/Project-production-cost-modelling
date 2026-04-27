import yaml
import os
from src.visualization import *

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

results_path = config["results_path"]
plots_path = config["plots_path"]

os.makedirs(plots_path, exist_ok=True)

# Economic Dispatch
ed_file = os.path.join(results_path, config["runs"]["economic_dispatch"])
df_ed = load_results(ed_file)

plot_system_balance(df_ed, f"{plots_path}/ed_balance.png")
plot_generation_stack(df_ed, f"{plots_path}/ed_stack.png")

# Unit Commitment
for i, uc_file in enumerate(config["runs"]["unit_commitment"]):
    path = os.path.join(results_path, uc_file)
    df_uc = load_results(path)

    plot_system_balance(df_uc, f"{plots_path}/uc{i}_balance.png")
    plot_generation_stack(df_uc, f"{plots_path}/uc{i}_stack.png")
    plot_unit_status(df_uc, f"{plots_path}/uc{i}_status.png")
    plot_startups(df_uc, f"{plots_path}/uc{i}_startups.png")