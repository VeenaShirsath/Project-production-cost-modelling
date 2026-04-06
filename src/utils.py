import pandas as pd
from datetime import datetime
from pathlib import Path


def save_results(dispatch_df):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output_dir = Path("results/dispatch_runs")
    output_dir.mkdir(parents=True, exist_ok=True)

    file_path = output_dir / f"dispatch_{timestamp}.csv"

    dispatch_df.to_csv(file_path, index=False)

    print(f"Results saved to: {file_path}")