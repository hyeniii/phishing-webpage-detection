# -*- coding: utf-8 -*-
"""
Created on Thu May  4 13:59:49 2023

@author: Blunders
"""

#################################################################################################################################
#             Intialization
#################################################################################################################################
import pandas as pd
import yaml
from src.feature_extractor import extract_features

# Load config file
with open('/src/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Access variables
urls = config['url']
headers = config['headers']
count = 0
data = pd.DataFrame(columns=headers)

for u in urls:
    row = extract_features(u['url'], u['status'])
    #print(row)
    data.loc[count] = row
    count+=1

data.to_csv('data.csv',index=False)