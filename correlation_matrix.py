from pg_functions import sql,df_to_table
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df=sql('SELECT * FROM ANALYSIS.ENCODED_DATA')


# Drop non-numeric columns if any (e.g., categorical columns that aren't encoded)
# You can adjust this step depending on your dataset's structure
df_numeric = df.select_dtypes(include=['float64', 'int64'])

# Calculate the correlation matrix
correlation_matrix = df_numeric.corr()

# Plot the heatmap
correlation_matrix_df=correlation_matrix.reset_index(names=['INDEX'])
df_to_table(correlation_matrix_df,'analysis','correlation_matrix')
