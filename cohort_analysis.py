import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pg_functions import sql,df_to_table

#IS REMOTE
df=sql('SELECT * FROM ANALYSIS.BSR_DATA')
# Assuming df is your DataFrame
# Convert START_DATE to datetime format
df['Start Date'] = pd.to_datetime(df['Start Date'])

# Create a cohort based on the month and year of the START_DATE
df['COHORT_MONTH'] = df['Start Date'].dt.to_period('M')


# Group by Cohort Month and Gender, then calculate the average tenure
cohort_analysis = df.groupby(['COHORT_MONTH', 'Remote'])['Tenure (Years)'].mean().unstack().reset_index(names=['Cohort Month']).to_dict(orient='records')
data=[]
for row in cohort_analysis:
    row['Cohort Month'] = row['Cohort Month'].__str__()
    data.append(row)
cohort_df = pd.DataFrame(data)
cohort_df

df_to_table(cohort_df,'analysis','cohort_analysis_remote')



#IS REMOTE & IS WOMAN
df=sql("""SELECT * FROM ANALYSIS.BSR_DATA WHERE "Gender" = 'Female' """)
# Assuming df is your DataFrame
# Convert START_DATE to datetime format
df['Start Date'] = pd.to_datetime(df['Start Date'])

# Create a cohort based on the month and year of the START_DATE
df['COHORT_MONTH'] = df['Start Date'].dt.to_period('M')


# Group by Cohort Month and Gender, then calculate the average tenure
cohort_analysis = df.groupby(['COHORT_MONTH', 'Remote'])['Tenure (Years)'].mean().unstack().reset_index(names=['Cohort Month']).to_dict(orient='records')
data=[]
for row in cohort_analysis:
    row['Cohort Month'] = row['Cohort Month'].__str__()
    data.append(row)
cohort_df = pd.DataFrame(data)
cohort_df

df_to_table(cohort_df,'analysis','cohort_analysis_remote_female')


#IS REMOTE & IS MALE
df=sql("""SELECT * FROM ANALYSIS.BSR_DATA WHERE "Gender" = 'Male' """)
# Assuming df is your DataFrame
# Convert START_DATE to datetime format
df['Start Date'] = pd.to_datetime(df['Start Date'])

# Create a cohort based on the month and year of the START_DATE
df['COHORT_MONTH'] = df['Start Date'].dt.to_period('M')


# Group by Cohort Month and Gender, then calculate the average tenure
cohort_analysis = df.groupby(['COHORT_MONTH', 'Remote'])['Tenure (Years)'].mean().unstack().reset_index(names=['Cohort Month']).to_dict(orient='records')
data=[]
for row in cohort_analysis:
    row['Cohort Month'] = row['Cohort Month'].__str__()
    data.append(row)
cohort_df = pd.DataFrame(data)
cohort_df

df_to_table(cohort_df,'analysis','cohort_analysis_remote_male')