import pandas as pd
from pg_functions import sql,df_to_table
from scipy.stats import chi2_contingency
df = sql('SELECT * FROM ANALYSIS.BSR_DATA')

data=[]
to_test= ['Race','Office Location','Employee Level','Employee Job Family']
for column_name in to_test:
    #CHAI SQUARED INDEPENDENCE TEST
    contingency_table = pd.crosstab(df['Remote'], df[column_name])
    chi2, p, dof, expected = chi2_contingency(contingency_table)
    
    row={"COLUMN_1":"Remote","COLUMN_2":column_name,"CHI2_STATISTIC": chi2,"P_VALUE": p}
    data.append(row)
chai_squared_df=pd.DataFrame(data)
df_to_table(chai_squared_df,'analysis','chai_squared')