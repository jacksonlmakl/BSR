from lifelines import KaplanMeierFitter
from pg_functions import sql,df_to_table

df = sql('SELECT * FROM ANALYSIS.ENCODED_DATA')
kmf = KaplanMeierFitter()
kmf.fit(durations=df['TENURE_YEARS'], event_observed=df['REMOTE'])
kmf.plot_survival_function()

kmf_df=kmf.survival_function_.reset_index(names=['TIMELINE'])
kmf_df['KM_ESTIMATE']=kmf_df['KM_estimate']
del kmf_df['KM_estimate']

df_to_table(kmf_df,'analysis','survival_analysis')