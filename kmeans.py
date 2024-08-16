from pg_functions import sql,df_to_table

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np
from sqlalchemy import create_engine
import matplotlib.pyplot as plt


df=sql('SELECT * FROM ANALYSIS.ENCODED_DATA')

# Separate features and target
X = df.drop(columns=['REMOTE'])
y = df['REMOTE']

# Standardize the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply K-Means with 2 clusters (remote and non-remote)
kmeans = KMeans(n_clusters=2, random_state=42)
kmeans.fit(X_scaled)

# Add the cluster labels to the DataFrame
df['Cluster'] = kmeans.labels_


# Inverse transform the scaled centroids to original scale
centroids = scaler.inverse_transform(kmeans.cluster_centers_)

# Convert centroids to a DataFrame for better visualization
centroid_df = pd.DataFrame(centroids, columns=X.columns)
centroid_df['Cluster'] = ['Cluster 0', 'Cluster 1']

# Determine which cluster is associated with REMOTE=1
remote_cluster = df[df['REMOTE'] == 1]['Cluster'].mode()[0]

# Identify the characteristics of the remote cluster
remote_characteristics = centroid_df.loc[centroid_df['Cluster'] == f'Cluster {remote_cluster}']
non_remote_characteristics = centroid_df.loc[centroid_df['Cluster'] != f'Cluster {remote_cluster}']

print("Characteristics most associated with Remote=1:")
averages=remote_characteristics.T.reset_index(names=['COLUMN_NAME'])
averages['AVG'] = averages[1]
round_avg = lambda x: round(x) if type(x) != str else 0
averages['AVG_ROUNDED']=averages['AVG'].apply(round_avg)
del averages[1]
averages=averages[averages['COLUMN_NAME']!='Cluster']
df_to_table(averages,'analysis','kmeans')