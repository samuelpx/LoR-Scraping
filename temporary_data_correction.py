#!/usr/bin/python3

'''
Program to correctly transform any response.json into parquet,
used mostly for when unknown errors make reading transformed_data_temporary.parquet impossible
'''

from datetime import datetime
import pandas as pd

    
data_pandas = pd.read_json("response.json")
for i in data_pandas["players"]:
    i["date"] = datetime.today().strftime("%d-%m-%Y, %Hh")
normalized = pd.json_normalize(data_pandas["players"])
# Initialize permanent dataset and temporary dataset
normalized.to_parquet("transformed_data_temporary.parquet")

