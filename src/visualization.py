import pandas as pd
import matplotlib.pyplot as plt
import os

def load_results(file_path):
    df = pd.read_csv(file_path, parse_dates=["timestamp"])
    return df


def plot_system_balance(df, save_path=None):
    agg_dict = {
        "generation_mw": "sum",
        "demand_mw": "mean",
        "renewable_gen_mw": "mean"
    }

    # Only include load shedding if it exists
    if "load_shedding_mw" in df.columns:
        agg_dict["load_shedding_mw"] = "mean"

    system = df.groupby("timestamp").agg(agg_dict)

    plt.figure(figsize=(12,6))
    plt.plot(system.index, system["demand_mw"], label="Demand")
    plt.plot(system.index, system["generation_mw"], label="Total Generation")
    plt.plot(system.index, system["renewable_gen_mw"], label="Renewables")

    # Plot only if available
    if "load_shedding_mw" in system.columns:
        plt.plot(system.index, system["load_shedding_mw"], label="Load Shedding")

    plt.legend()
    plt.title("System Balance")
    plt.xlabel("Time")
    plt.ylabel("MW")
    plt.grid()

    if save_path:
        plt.savefig(save_path)
    plt.close()


def plot_generation_stack(df, save_path=None):
    pivot = df.pivot_table(
        index="timestamp",
        columns="generator_id",
        values="generation_mw",
        aggfunc="sum"
    )

    pivot.plot.area(figsize=(12,6))
    plt.title("Generation Stack")
    plt.xlabel("Time")
    plt.ylabel("MW")

    if save_path:
        plt.savefig(save_path)
    plt.close()


def plot_unit_status(df, save_path=None):
    pivot = df.pivot_table(
        index="timestamp",
        columns="generator_id",
        values="on_status",
        aggfunc="mean"
    )

    plt.figure(figsize=(12,6))
    plt.imshow(pivot.T, aspect="auto", interpolation="none")
    plt.colorbar(label="On Status")
    plt.yticks(range(len(pivot.columns)), pivot.columns)
    plt.title("Unit Commitment Status")

    if save_path:
        plt.savefig(save_path)
    plt.close()


def plot_startups(df, save_path=None):
    startup_counts = df.groupby("generator_id")["startup"].sum()

    startup_counts.plot(kind="bar", figsize=(10,5))
    plt.title("Startup Counts by Generator")

    if save_path:
        plt.savefig(save_path)
    plt.close()