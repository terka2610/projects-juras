#ELSA Wave 8: merge survey data with frailty categorization data
# Created by Prof Hughes and Terezia Jurasova


############################################################################################
#Import libraries
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')
pd.set_option('display.max_rows', None)

############################################################################################
#Step 1: Set up initial data and conditions

#### Load frailty categorization (based on Fried Criterion)
df_frail = pd.read_csv("/Users/AHMS/Documents/Python Scripts/fried_criteria_wave8.csv")

#Encode frailty categories then drop everything but idauniq and frail_cat1
label_encoder = LabelEncoder()
df_frail['frail_cat1'] = label_encoder.fit_transform(df_frail['frail_cat'])
df_frail1 = df_frail[['idauniq', 'frail_cat1']]

#df_frail1 = df_frail1[df_frail1['frail_cat1'] != 1]

####
#### Prof Hughes add: changed to complete wave 8 data
df = pd.read_csv("/Users/AHMS/Documents/Python Scripts/wave8_cleaneddata.csv")

# Convert all values to numeric, forcing errors to NaN
df = df.apply(pd.to_numeric, errors='coerce')

############################################################################################
#Step 2: Deal with negative values in the df

# Check for negative values and replace with NaN value
df[df < 0] = np.nan
nan_percentage_after = df.isnull().sum().sort_values(ascending=False) / len(df) * 100
print(nan_percentage_after)

############################################################################################
#Step 3: Check and deal with NaN and missing value

# for NaN values
df.isnull().sum().sort_values(ascending=False) / len(df.shape) * 100
nan_percentage = df.isnull().sum() / len(df) * 100
print("NaN percentage per column:", nan_percentage.sort_values(ascending=False))


############################################################################################
#Step 4: Tidy it all up a bit now
 
# Concatenate the two dfs then drop PID
df_merged = pd.merge(df, df_frail1, on='idauniq', how='inner')
columns_to_drop = ['idauniq']
df_merged1 = df_merged.drop(columns=columns_to_drop)

print(f"Rows Removed df: {df_merged1.shape}")

#Save as CSV for EDA and Pre-processing
df_merged1.to_csv('wave8_readyforML.csv', index=False)

############################################################################################
