from scipy.stats import ttest_ind
from pg_functions import sql, df_to_table
import pandas as pd

# Fetch data from the SQL database
df = sql('SELECT * FROM ANALYSIS.ENCODED_DATA')

# List of columns to test, excluding "POST_INTENTION_TO_STAY"
to_test = [i for i in list(df.columns) if i != "POST_INTENTION_TO_STAY"]

data = []
for column_name in to_test:
    # Define two groups: low intention (1-3) vs. high intention (4-5)
    low_intention = df[df['POST_INTENTION_TO_STAY'].isin([1, 2, 3])][column_name]
    high_intention = df[df['POST_INTENTION_TO_STAY'].isin([4, 5])][column_name]

    # Perform T-test between the two groups
    t_stat, p_val = ttest_ind(low_intention, high_intention)
    
    # Store the results in a dictionary
    row = {'COLUMN_1': 'POST_INTENTION_TO_STAY', 'COLUMN_2': column_name, 'T_STATISTIC': t_stat, 'P_VALUE': p_val}
    data.append(row)

# Create a DataFrame for the hypothesis test results
hypothesis_test_df = pd.DataFrame(data)

# Optionally save the results back to the database
df_to_table(hypothesis_test_df, 'analysis', 'hypothesis_test_satisfaction')
