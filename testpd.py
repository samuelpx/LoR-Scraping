import pandas as pd 
import requests 
import json 
import numpy as np
from datetime import datetime

old_data = pd.read_csv('test.csv', index_col = 0)


data_pandas = pd.read_json("response.json")
for i in data_pandas['players']:
    i['date'] = datetime.today().strftime('%d-%m-%Y, %H:%M') 
normalized = pd.json_normalize(data_pandas['players'])
# normalized = normalized.set_index('rank')

joined_data = pd.concat([old_data,normalized])

joined_data.to_csv('test.csv')



print("old data describe: \n\n",old_data.describe())
print("old data describe: \n\n",old_data.head())
print("old data describe: \n\n",old_data.info())
print("normalized data describe: \n\n",normalized.describe())
print("normalized data describe: \n\n",normalized.head())
print("normalized data describe: \n\n",normalized.info())
print("joined data describe: \n\n",joined_data.info())

