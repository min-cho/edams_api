# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 14:07:14 2021

@author: MR004CHM
"""
import os
import numpy as np
import pandas as pd
import sklearn
import json
import requests

os.chdir('C:\\Users\\MR004CHM\\Desktop\\TFcode\\2021-EDAMS')


#%% Data Selection

data_raw = pd.read_csv("sampled_boiler_normal.csv")
data_raw = data_raw.iloc[0:96]
data_raw = data_raw[["Date/Time",
                    "HOT WATER LOOP:Plant Supply Side Inlet Mass Flow Rate [kg/s](TimeStep)",
                    "HOT WATER LOOP:Plant Supply Side Inlet Temperature [C](TimeStep)",
                    "HOT WATER LOOP:Plant Supply Side Outlet Temperature [C](TimeStep)",
                    "CENTRAL BOILER:Boiler Gas Energy [J](TimeStep)"]]


### Temporary Column Names - should be Korean UTF-8
data_raw.columns = ["time",
           "Hot Water Inlet Mass Flow Rate (kg/s)",
           "Hot Water Inlet Temperature[C]",
           "Hot water Outlet Temperature[C]",
           "Boiler Gas Energy [J]"
           ]

dID= "F210223F80012"


#%% PLAN A: daily POST

data = {'detectionID':"NA",'var_names':[],'var_data':[]}

# 1: detectionID
data["detectionID"] = dID

# 2: var_names
data["var_names"]   = list(data_raw.columns)

# 3: var_data
data_raw.columns = ["v1","v2","v3","v4","v5"]
data_raw_dict = data_raw.to_dict(orient='records')
data["var_data"]    = data_raw_dict

data_json = json.dumps(data, indent="\t")


#%% API POST

### API Access Adress

url = 'http://localhost:3000/api/values'
Header = {'Content-Type':'application/json; charset=utf-8'}

### Define the Data to POST via API
### In this phase, whole data is uploaded at the last minute of the day

response = requests.post(url, data=data_json, headers=Header)

print("=== response json data start ===")
print(response.text)
print("=== response json data end ===")
print()


#%% API GET - to test (like Postman)

url = 'http://localhost:3000/api/values'
Header = {'Content-Type':'application/json; charset=utf-8'}
response = requests.get(url,headers=Header)
print(response.text)
