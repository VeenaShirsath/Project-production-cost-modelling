# Project-production-cost-modelling
Economic Dispatch, Unit Commitment, and Renewable Integration in Python

## Step 1: Building a working PCM with simple synthetic data

## Data Sources
1. Demand data: [ERCOT Hourly Load Data for 2024](https://www.ercot.com/gridinfo/load/load_hist)
2. Generator data: [Form EIA-860 data for 2024](https://www.eia.gov/electricity/data/eia860/) and [Form EIA-923](https://www.eia.gov/electricity/data/eia923/)
    * LayoutYyyyy — Provides a directory of all (published) data elements collected on the Form EIA-860 together with the related description, specific file location(s), and, where appropriate, an explanation of codes.
    * 1___UtilityYyyyy — Contains utility-level data for the plants and generators surveyed in the reporting year.
    * 2___PlantYyyyy — Contains plant-level data for the generators surveyed in all available years.
    * 3_1_GeneratorYyyyy — Contains generator-level data for the surveyed generators, split into three tabs.
        * The Operable tab includes those generators which are currently operating, out of service or on standby;
        * The Proposed tab includes those generators which are planned and not yet in operation; and
        * The Retired and Canceled tab includes those generators which were cancelled prior to completion and operation and retired generators at existing plants.
    * 3_2_WindYyyyy — Contains additional details for surveyed generators that use wind as an energy source, split into two tabs:
        * The Operable tab includes those generators which are currently operating, out of service or on standby; and
        * The Retired and Canceled tab includes those generators which were cancelled prior to completion and operation and retired generators at existing plants.
    * 3_3_SolarYyyyy — Contains additional details for surveyed generators that use solar as an energy source, split into two tabs:
        * The Operable tab includes those generators which are currently operating, out of service or on standby;
        * The Retired and Canceled tab includes those generators which were cancelled prior to completion and operation and retired generators at existing plants.
    * 3_4_Energy_StorageYyyyy — Contains additional details of surveyed generators for the energy storage technology, split into two tabs:
        * The Operable tab includes those generators which are currently operating, out of service or on standby;
        * The Retired and Canceled tab includes those generators which were cancelled prior to completion and operation and retired generators at existing plants.
    * 3_5_MultiFuelYyyyy — Contains data on fuel-switching and the use of multiple fuels by surveyed generators, split into three tabs:
        * The Operable tab includes those generators which are currently operating, out of service or on standby; and
        * The Proposed tab includes those generators which are planned and not yet in operation; and
        * The Retired and Canceled tab includes those generators which were cancelled prior to completion and operation and retired generators at existing plants.
    * 4___OwnerYyyyy — Contains owner and/or operator data for generators with shared ownership and generators that are wholly-owned by an entity other than the operator (generators not appearing in the file are wholly-owned by their operator).
    * 6_1_EnviroAssocYyyyy — Contains boiler association data for the environmental equipment data collected on the Form EIA-860.
    * 6_2_EnviroEquipYyyyy — Contains environmental equipment data for the surveyed generators.
3. Renewable Generation Profiles: Capacity factor data [NREL 2024](https://atb.nrel.gov/electricity/2024/data)
    * For three different scenarios, there is a CF for each technology in 2024.
    * Alternative: [NSRDB](https://nsrdb.nlr.gov/data-viewer)

c