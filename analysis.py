import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# environmental index
env_df = pd.read_csv("epi2024results.csv")
env_columns_keep = ['country', 'EPI.new']
env_df = env_df[env_columns_keep]
env_df = env_df.sort_values(by=['EPI.new'], ascending=False, ignore_index= True)

# digitalization index
digital_df = pd.read_csv("isoc_e_dii.csv")
digital_columns_keep = ['Geopolitical entity (reporting)', 'OBS_VALUE']
digital_df = digital_df[digital_columns_keep]


# AI adoption index
ai_df = pd.read_csv("isoc_eb_ai.csv")

# startup ecosystem index
startup_df = pd.read.csv("Global Startup Ecosystem Index.csv")

print(env_df.head())