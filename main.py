#!/usr/bin/env python3

import requests
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd
import numpy as np
import json
import os, sys

os.chdir("/home/samuelpx/Documents/Projects/python/LoR-Scraping")

url = "https://americas.api.riotgames.com/lor/ranked/v1/leaderboards"  # Replace with your API endpoint URL

load_dotenv('/home/samuelpx/Documents/Projects/python/LoR-Scraping/.env')

API_KEY = os.getenv('RIOT_KEY')

print(f'DEBUG {API_KEY}')

headers = {
    "X-Riot-Token": f'{API_KEY}',  # Replace with your authentication token
}
# Checking if previous data exists:
SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = "transformed_data.csv"
OLD_FILE_PATH = os.path.join(SCRIPT_DIRECTORY, FILE_NAME)
print(OLD_FILE_PATH)

if not os.path.isfile(OLD_FILE_PATH):
    try:
        response = requests.get(url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            with open("response.json", "w") as file:
                json.dump(data, file)
            data_pandas = pd.read_json("response.json")
            for i in data_pandas["players"]:
                i["date"] = datetime.today().strftime("%d-%m-%Y, %Hh")
            normalized = pd.json_normalize(data_pandas["players"])
            normalized.to_csv("transformed_data.csv")
            normalized.to_csv("transformed_data_temporary.csv")
            print("No old data found! Initializing csv.")
        else:
            # Print an error message for unsuccessful requests
            print(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        # Print an error message for network errors
        if e:
            print(f"Error: {e}")

else:
    try:
        response = requests.get(url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Load up old data
            old_data = pd.read_csv("transformed_data.csv", index_col=0)
            temporary_old_data = pd.read_csv(
                "transformed_data_temporary.csv", index_col=0
            )

            # Parse and use the response data
            data = response.json()
            with open("response.json", "w") as file:
                json.dump(data, file)
            data_pandas = pd.read_json("response.json")
            for i in data_pandas["players"]:
                i["date"] = datetime.today().strftime("%d-%m-%Y, %Hh")
            normalized = pd.json_normalize(data_pandas["players"])

            if np.array_equal(temporary_old_data.values, normalized.values):
                print("\nThese data-frames are the same!!")
                sys.exit(0)

            print(f'\n This is the "normalized" variable\n')
            print(normalized, "\n")
            print(f' This is the "old_data" variable\n')
            print(old_data, "\n")
            print(f' This is the "temporary_old_data" variable\n')
            print(temporary_old_data, "\n")

            # Joining data so we can save & update
            joined_data = pd.concat([old_data, normalized])
            print(f' This is "joined_data.describe()" \n')
            print(joined_data.describe(), "\n")
            print(f' This is "joined_data.info()" \n')
            print(joined_data.info(), "\n")
            print("\n\n Sucessfully updated the csv with new data!")
            normalized.to_csv("transformed_data_temporary.csv")

            # Creating the final finals, HTML and CSV 
            # joined_data.to_html("transfomred_data.html")
            # NOT A GOOD IDEA ^ ^ ^ ^ ^ ^ ^ ^
            joined_data.to_csv("transformed_data.csv")

        else:
            # Print an error message for unsuccessful requests
            print(f"Error: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        # Print an error message for network errors
        if e:
            print(f"Error: {e}")
