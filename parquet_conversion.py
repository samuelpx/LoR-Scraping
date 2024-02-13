import pandas as pd 

df = pd.read_csv("transformed_data_temporary.csv", index_col=0)

df.to_parquet("transformed_data_temporary.parquet")
