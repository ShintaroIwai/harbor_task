import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# environmental index
env_df = pd.read_csv("epi2024results.csv")
env_columns_keep = ['country', 'EPI.new']
env_df = env_df[env_columns_keep]
env_df = env_df.rename(columns = {'EPI.new': 'EPI'})
# env_df = env_df.sort_values(by=['EPI'], ascending=False, ignore_index= True)

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
startup_df = startup_df.rename(columns={"Country": "country", "Total Score":"startup environment"})

df = startup_df.merge(digital_df, on='country')
df = df.merge(ai_df, on='country')
df = df.merge(env_df, on='country')

df["startup_norm"] = (df['startup environment'] - df['startup environment'].min()) / (df['startup environment'].max() - df['startup environment'].min())
df["digital_norm"] = (df["digitalization"] - df["digitalization"].min()) / (df["digitalization"].max() - df["digitalization"].min())
df["ai_norm"] = (df["AI adoption"] - df["AI adoption"].min()) / (df["AI adoption"].max() - df["AI adoption"].min())
df["env_norm"] = (df["EPI"] - df["EPI"].min()) / (df["EPI"].max() - df["EPI"].min())
df["weighted"] = df['startup_norm'] * 0.3 + df['digital_norm'] * 0.3 + df['ai_norm'] * 0.3 + df['env_norm'] * 0.1
df = df.sort_values(by='weighted', ascending=False, ignore_index=True)

table_columns_keep = ['country','weighted', 'startup_norm', 'digital_norm', 'ai_norm', 'env_norm']
table_df = df[table_columns_keep]
table_df = table_df.rename(columns={'country': 'Country', 'weighted': 'Overall Score', 'startup_norm':
    'Startup Environment', 'digital_norm': 'Firm Digitalization', 'ai_norm': 'Firm AI Adoption', 'env_norm': 'Environmental Sustainability'})

print(df.head(30))

fig, ax = plt.subplots(figsize=(12, 5))
ax.axis('off')
table = ax.table(cellText=table_df.values, colLabels=table_df.columns, loc='center')

columns = len(table_df.iloc[0,:])

header_colors = ["#FFFFFF", "#2F4B7C", "#F8961E", "#277DA1", "#9D4EDD", "#43AA8B"]

for i in range(columns):
    header = table[0, i]
    header.set_facecolor(header_colors[i])
    if i == 0:
        header.set_text_props(weight='bold')
    else:
        header.set_text_props(color="white", weight="bold")

# fig.savefig("startup_analysis.png", dpi=300, bbox_inches='tight')

plt.show()