from pg_functions import sql,df_to_table
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from sqlalchemy import create_engine

df=sql('SELECT * FROM ANALYSIS.ENCODED_DATA')

# Do not filter out REMOTE; include it in the dataset
df_binarized = df.apply(lambda x: x > x.mean() if x.dtype != 'object' else x, axis=0)

# Ensure all values are boolean 
df_binarized = df_binarized.astype(int)

# Apply the Apriori algorithm to find frequent itemsets
frequent_itemsets = apriori(df_binarized, min_support=0.2, use_colnames=True)

# Generate association rules
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)

rules_with_remote=rules
# Sort rules by confidence
rules_with_remote = rules_with_remote.sort_values(by='confidence', ascending=False)

#Clean data and store in postgres
to_list=lambda x: list(x)
rules_with_remote['antecedents']=rules_with_remote['antecedents'].apply(to_list)
rules_with_remote['consequents']=rules_with_remote['consequents'].apply(to_list)

rules_with_remote = rules_with_remote[
    rules_with_remote['antecedents'].apply(lambda x: 'REMOTE' in x) |
    rules_with_remote['consequents'].apply(lambda x: 'REMOTE' in x)
]
data=[]
for row in rules_with_remote.to_dict(orient='records'):
    row['antecedents']=str(row['antecedents']).replace("]",'').replace("[",'').replace("'",'')
    row['consequents']=str(row['consequents']).replace("]",'').replace("[",'').replace("'",'')
    data.append(row)
rules_with_remote=pd.DataFrame(data)


df_to_table(rules_with_remote,'analysis','apriori')