import pandas as pd
import numpy as np
from pg_functions import df_to_table

# Function to convert to screaming snake case
def to_screaming_snake_case(col_name):
    return col_name.strip().upper().replace(' (days/month)','').replace(' (1-5)','').replace(' ', '_').replace('(', '').replace(')', '').replace(':', '').replace('-', '_').replace('Y/N','').replace('_Y=1,_N=0','').replace('/','_').replace('_Y=1,N=0','')
    
#Load data from database
df=sql("SELECT * FROM ANALYSIS.BSR_DATA")

#List of categorical columns
categorical=['Gender','Children (Y/N)','Race','Office Location', 'Employee Level', 'Employee Job Family']

#One-hot-encode categorical variables
df_encoded=pd.get_dummies(data=df,columns=categorical,dtype=int)

#Convert dates to unix timestamps
df_encoded['Start Date']=pd.to_datetime(df['Start Date']).astype(int) // 10**9

#Encode target variable
encode_target = lambda x: 1 if x =='remote' else 0

df_encoded['Remote']=df_encoded['Remote'].apply(encode_target)

#Select columns to keep
keep_columns=['Remote','Start Date','Tenure (Years)','Salary ','Age','Distance from home to office (Miles) if not remote','Average commute (minutes) if not remote','Change readiness 1 (1-5)','Change readiness 2 (1-5)','Change readiness 3 (1-5)','Change readiness 4 (1-5)','Change readiness 5 (1-5)','Change commitment 1 (1-5)','Change commitment 2 (1-5)','Change commitment 3 (1-5)','Change commitment 4 (1-5)','Change commitment 5 (1-5)','Sleep intervention (Y=1, N=0)','Exercise intervention (Y=1, N=0)','Smoking intervention (Y=1,N=0)','Pre: Hours of sleep','Pre: Quality of sleep','Pre: Daily exercise (Min)','Pre: BMI','Pre: Smoking','Post: Hours of sleep','Post: Quality of sleep','Post: Daily exercise','Post: BMI','Post: Smoking','Pre: Absenteeism (days/month)','Pre: Performance','Pre: Intention to Stay','Post: Intention to Stay','Post: Absenteeism','Post: Performance','Pre Engagement question 1','Pre Engagement question 2','Pre Engagement question 3','Pre Satisfaction question 1','Pre Satisfaction question 2','Pre Satisfaction question 3','Post Engagement question 1','Post Engagement question 2','Post Engagement question 3','Post Satisfaction question 1','Post Satisfaction question 2','Post Satisfaction question 3','Gender_Female','Gender_Male','Children (Y/N)_N','Children (Y/N)_Y','Race_Asian','Race_Black','Race_Hispanic','Race_Native American','Race_Two or More Races','Race_White','Office Location_CO','Office Location_IL','Office Location_MN','Office Location_UT','Employee Level_Director','Employee Level_Junior','Employee Level_Manager','Employee Job Family_Accounting and Finance','Employee Job Family_Administrative','Employee Job Family_Customer Service','Employee Job Family_Legal','Employee Job Family_Marketing and Sales']

df_clean=df_encoded[keep_columns]
df_clean.columns = [to_screaming_snake_case(col) for col in df_clean.columns]

#Load DF to table analysis.encoded_data
df_to_table(df_clean,'analysis','encoded_data')


