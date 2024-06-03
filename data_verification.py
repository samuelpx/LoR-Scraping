import pandas as pd 

df = pd.read_parquet("./transformed_data.parquet")

print(df.info())

