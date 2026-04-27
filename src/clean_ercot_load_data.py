import pandas as pd

df = pd.read_excel("data/demand/Native_Load_2024.xlsx")
print("Original df shape:", df.shape)
print("Hour Ending type:", type(df["Hour Ending"].iloc[0]) if not df.empty else "empty")
print("First few Hour Ending:", df["Hour Ending"].head())

df["Hour Ending"] = df["Hour Ending"].str.replace("24:00", "00:00", regex=False)

df = df.rename(columns={'Hour Ending': 'timestamp', 'ERCOT': 'demand_mw'})

df["timestamp"] = df["timestamp"].str.replace(" DST", "", regex=False)
df["timestamp"] = pd.to_datetime(df["timestamp"], format="%m/%d/%Y %H:%M")

df_2w = df[df['timestamp'] < '01-15-2024 01:00']
print("Filtered df shape:", df_2w.shape)

df_2w_clean = df_2w[["timestamp", "demand_mw"]]
print("Clean df shape:", df_2w_clean.shape)

# Ensure timestamp format is MM/DD/YYYY HH:MM
df_2w_clean["timestamp"] = pd.to_datetime(df_2w_clean["timestamp"], format="%m/%d/%Y %H:%M").dt.strftime("%m/%d/%Y %H:%M")

df_2w_clean.to_csv("data/demand/load_2week_clean.csv", index=False)
print("File saved successfully")
