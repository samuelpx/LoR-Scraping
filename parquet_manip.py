import pandas as pd

df = pd.read_parquet("transformed_data.parquet")

print(df.head())

df_csv = pd.read_csv("transformed_data.csv", index_col=0)

print(df_csv.head())


