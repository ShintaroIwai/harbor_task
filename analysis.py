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
digital_columns_keep = ['Geopolitical entity (reporting)', 'Size classes in number of persons employed',
                        'Information society indicator', 'OBS_VALUE', 'TIME_PERIOD']
digital_df = digital_df[digital_columns_keep]
digital_df['OBS_VALUE'] = pd.to_numeric(digital_df['OBS_VALUE'], errors='coerce')
digital_df = digital_df.dropna()
digital_df = digital_df[digital_df['TIME_PERIOD'].isin([2025])]
digital_df = digital_df[digital_df['Size classes in number of persons employed'].str.contains("From 10 to 249 persons employed")]
digital_df = digital_df[digital_df['Information society indicator'].str.contains('Enterprises with at least basic level of digital intensity')]
digital_df = digital_df.loc[:, ['Geopolitical entity (reporting)', 'OBS_VALUE']]
digital_df.columns = ["country", "digitalization"]

# AI adoption index
ai_df = pd.read_csv("isoc_eb_ai.csv")
ai_columns_keep = ['Information society indicator', 'Geopolitical entity (reporting)', 'OBS_VALUE']
ai_df = ai_df[ai_columns_keep]
ai_df['OBS_VALUE'] = pd.to_numeric(ai_df['OBS_VALUE'], errors='coerce')
ai_df = ai_df[ai_df['Information society indicator'].str.contains('Enterprises that ever considered to use one of the AI technologies: AI_TTM, AI_TSR, AI_TNLG, AI_TIR, AI_TML, AI_TPA, AI_TAR, E_AI_TPVSG')]
ai_df = ai_df.loc[:, ['Geopolitical entity (reporting)', 'OBS_VALUE']]
ai_df.columns = ["country", "AI adoption"]

# startup ecosystem index
startup_df = pd.read_csv("Global Startup Ecosystem Index.csv")
startup_columns_keep = ['Country', 'Total Score']
startup_df = startup_df[startup_columns_keep]
startup_df = startup_df.rename(columns={"Country": "country"})

df = startup_df.merge(digital_df, on='country')
df = df.merge(ai_df, on='country')
df = df.merge(env_df, on='country')

print(df.head(30))