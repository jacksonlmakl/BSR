from scipy.stats import ttest_ind
from pg_functions import sql,df_to_table
df = sql('SELECT * FROM ANALYSIS.ENCODED_DATA')

to_test= [i for i in list(df.columns) if i != "REMOTE"]
data=[]
for column_name in to_test:
    # Example: T-test for job satisfaction between remote and non-remote workers
    t_stat, p_val = ttest_ind(df[df['REMOTE'] == 1][column_name],
                              df[df['REMOTE'] == 0][column_name])
    row = {'COLUMN_1':'REMOTE','COLUMN_2':column_name,'T_STATISTIC':t_stat,"P_VALUE": p_val}
    data.append(row)
hypothesis_test_df = pd.DataFrame(data)
df_to_table(hypothesis_test_df,'analysis','hypothesis_test')