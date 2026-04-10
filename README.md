# Production Cost Modeling in Power Systems

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A comprehensive Python-based framework for production cost modeling in power systems, featuring economic dispatch, unit commitment, and renewable energy integration optimization.

## Overview

This project implements advanced power system optimization techniques to model electricity production costs, incorporating both conventional thermal generation and renewable energy sources. Designed for power systems engineers and researchers, it provides tools for analyzing dispatch strategies, evaluating renewable integration impacts, and conducting scenario-based analyses.

## Key Features

- **Economic Dispatch**: Optimal allocation of generation resources to meet demand at minimum cost
- **Unit Commitment**: Strategic scheduling of power plants considering startup/shutdown costs and constraints
- **Renewable Integration**: Incorporation of wind and solar capacity factors with realistic generation profiles
- **Constraint Modeling**: Ramp rates, minimum/maximum generation limits, and operational constraints
- **Scenario Analysis**: Comparative evaluation of different operational strategies and market conditions
- **Data-Driven Approach**: Integration with real ERCOT and EIA datasets for authentic modeling

## Current Development Status

- ✅ **Phase 1**: Basic Economic Dispatch implementation
- ✅ **Phase 2**: Advanced constraints and optimization 
- 🔄 **Phase 3**: Unit Commitment with Pyomo optimization (in progress)
- ⏳ **Phase 4**: Large-scale real-world dataset integration
- ⏳ **Phase 5**: Comprehensive scenario analysis
- ⏳ **Phase 6**: Interactive visualizations and reporting

## 🛠 Installation

```bash
# Clone the repository
git clone https://github.com/VeenaShirsath/Project-production-cost-modelling.git
cd Project-production-cost-modelling

# Install dependencies
pip install -r requirements.txt

# Optional: Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 🚀 Usage

### Basic Economic Dispatch
```python
python main.py
```

### Jupyter Notebook Analysis
```bash
jupyter notebook notebooks/
```

### Data Processing
```python
# Clean ERCOT load data
python src/clean_ercot_load_data.py

# Generate synthetic renewable data
python src/synthetic_renewable_data.py
```

## Project Structure

```
├── config.yaml                 # Configuration settings
├── main.py                     # Main execution script
├── requirements.txt            # Python dependencies
├── data/                       # Input data directory
│   ├── demand/                 # Load/demand data
│   ├── generators/             # Generation facility data
│   └── renewables/             # Renewable energy profiles
├── src/                        # Source code
│   ├── dispatch.py             # Economic dispatch algorithms
│   ├── unit_commitment.py      # Unit commitment models
│   ├── cost_functions.py       # Cost calculation utilities
│   ├── constraints.py          # Operational constraints
│   ├── renewables.py           # Renewable energy modeling
│   ├── scenarios.py            # Scenario analysis tools
│   └── utils.py                # Helper functions
├── notebooks/                  # Jupyter notebooks for analysis
│   ├── 01_baseline_dispatch.ipynb
│   ├── 02_unit_commitment.ipynb
│   └── 03_scenario_analysis.ipynb
└── results/                    # Output results and reports
```

## Data Sources

### Demand Data
- **ERCOT Hourly Load Data**: Real-time and historical load profiles from the Electric Reliability Council of Texas
- Source: [ERCOT Load History](https://www.ercot.com/gridinfo/load/load_hist)

### Generator Data
- **EIA Form 860**: Detailed generator characteristics including capacity, fuel type, and operational parameters
- **EIA Form 923**: Monthly generation and fuel consumption data
- Source: [U.S. Energy Information Administration](https://www.eia.gov/electricity/data/)

### Renewable Profiles
- **NREL Annual Technology Baseline (ATB)**: Capacity factor data for wind and solar technologies
- Alternative: **NSRDB** (National Solar Radiation Database) for site-specific solar irradiance
- Source: [NREL ATB](https://atb.nrel.gov/electricity/2024/data)

## Technologies

- **Python 3.8+**: Core programming language
- **Pandas & NumPy**: Data manipulation and numerical computing
- **Pyomo**: Mathematical optimization modeling
- **Jupyter**: Interactive analysis and visualization
- **Matplotlib/Seaborn**: Data visualization