import pandas as pd

df = pd.read_excel("data/demand/Native_Load_2024.xlsx")
print("Original df shape:", df.shape)
print("Hour Ending type:", type(df["Hour Ending"].iloc[0]) if not df.empty else "empty")
print("First few Hour Ending:", df["Hour Ending"].head())

df["Hour Ending"] = df["Hour Ending"].str.replace("24:00", "00:00", regex=False)

df = df.rename(columns={'Hour Ending': 'timestamp', 'ERCOT': 'demand_mw'})

#df['Hour Ending'] = pd.to_datetime(df['Hour Ending'], format='%m/%d/%Y %H:%M')

df_1m = df[df['timestamp'] < '02-01-2024 01:00']
print("Filtered df shape:", df_1m.shape)

df_1m_clean = df_1m[["timestamp", "demand_mw"]]
print("Clean df shape:", df_1m_clean.shape)

# Ensure timestamp format is MM/DD/YYYY HH:MM
df_1m_clean["timestamp"] = pd.to_datetime(df_1m_clean["timestamp"], format="%m/%d/%Y %H:%M").dt.strftime("%m/%d/%Y %H:%M")

df_1m_clean.to_csv("data/demand/load_1month_clean.csv", index=False)
print("File saved successfully")