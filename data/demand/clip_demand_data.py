import pandas as pd

df = pd.read_excel("data/demand/Native_Load_2024.xlsx")
df["Hour Ending"] = df["Hour Ending"].str.replace("24:00", "00:00", regex=False)

#df['Hour Ending'] = pd.to_datetime(df['Hour Ending'], format='%m/%d/%Y %H:%M')

df_1m = df[df['Hour Ending'] < '02-01-2024 01:00']

df_1m_clean = df_1m[["Hour Ending", "ERCOT"]]

df_1m_clean.to_csv("data/demand/load_1month_clean.csv", index=False)