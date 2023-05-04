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
from feature_extractor import extract_features

# Load config file
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Access variables
url = config['url']
status = config['status']
headers = config['headers']

row = extract_features(url, status)
#print(row)

data = pd.DataFrame(columns=headers)
data.loc[0] = row
data.to_csv('data.csv',index=False)