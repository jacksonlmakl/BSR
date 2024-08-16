import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt
from sklearn import metrics
from pg_functions import sql,df_to_table
from sklearn.tree import _tree
import numpy as np


# Load your data from PostgreSQL (if not already loaded)
df = sql('SELECT * FROM ANALYSIS.ENCODED_DATA')

# Assuming df is your DataFrame, with 'REMOTE' being the target column
X = df.drop(columns=['REMOTE'])  # Features (attributes)
y = df['REMOTE']  # Target variable (REMOTE = 1 or 0)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)



# Initialize the Decision Tree Classifier
dt_model = DecisionTreeClassifier(random_state=42, criterion='entropy', max_depth=5)  # You can tune the parameters

# Train the model on the training data
dt_model.fit(X_train, y_train)


# Initialize the Decision Tree Classifier
dt_model = DecisionTreeClassifier(random_state=42, criterion='entropy', max_depth=5)  # You can tune the parameters

# Train the model on the training data
dt_model.fit(X_train, y_train)



# Predict on the test set
y_pred = dt_model.predict(X_test)

# Evaluate the model
print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
print("Confusion Matrix:\n", metrics.confusion_matrix(y_test, y_pred))
print("Classification Report:\n", metrics.classification_report(y_test, y_pred))



# Plot the decision tree
plt.figure(figsize=(20,10))
plot_tree(dt_model, feature_names=X.columns, class_names=['Not Remote', 'Remote'], filled=True)
plt.title('Decision Tree for Remote Worker Classification')
plt.show()


# Feature importance
feature_importances = pd.Series(dt_model.feature_importances_, index=X.columns).sort_values(ascending=False)

print("Feature Importances:")
print(feature_importances)

# Optional: Plot the feature importances
feature_importances.plot(kind='bar', figsize=(12, 6), title='Feature Importances')
plt.show()


importance_df=pd.DataFrame(feature_importances).reset_index(names=['COLUMN'])
importance_df['SCORE']=importance_df[0]
del importance_df[0]
df_to_table(importance_df,'analysis','decision_tree_feature_importance')

# Assuming dt_model is your decision tree model
tree = dt_model.tree_

# Extracting tree structure
n_nodes = tree.node_count
children_left = tree.children_left
children_right = tree.children_right
feature = tree.feature
threshold = tree.threshold
value = tree.value
impurity = tree.impurity
n_samples = tree.n_node_samples

# Lists to hold the hierarchical data
rows = []

# Function to format the node's label
def format_node_label(feature_name, threshold, impurity, n_samples, value, class_name):
    # Convert the value array into a string of integers
    value_str = f"[{', '.join(map(str, map(int, value)))}]"
    return (f"{feature_name} <= {threshold:.2f}\n"
            f"class = {class_name}")

# Function to recursively build the hierarchy
def build_hierarchy(node, path=[]):
    if feature[node] != _tree.TREE_UNDEFINED:  # Decision node
        name = format_node_label(
            X.columns[feature[node]], 
            threshold[node], 
            impurity[node], 
            n_samples[node], 
            value[node][0],  # Extract the array for the node
            'Remote' if np.argmax(value[node]) == 1 else 'Not Remote'
        )
        # Recursively add child nodes
        build_hierarchy(children_left[node], path + [name])
        build_hierarchy(children_right[node], path + [f"{X.columns[feature[node]]} > {threshold[node]:.2f}"])
    else:  # Leaf node
        # Handle the value as an array
        value_str = f"[{', '.join(map(str, map(int, value[node][0])))}]"
        label = (f"class = {'Remote' if np.argmax(value[node]) == 1 else 'Not Remote'}\n")
        rows.append(path + [label])

# Start building the hierarchy from the root node
build_hierarchy(0)

# Create a DataFrame from the list of hierarchical rows
df_tree = pd.DataFrame(rows)

# Handle any None values by replacing them with empty strings
df_tree.fillna('', inplace=True)

# Optionally, rename columns to make them more descriptive
df_tree.columns = [f'Level {i+1}' for i in range(df_tree.shape[1] - 1)] + ['Outcome']



# Exporting to CSV for Tableau
df_tree.to_csv('tree.csv', index=False)

# Exporting to CSV for Tableau
df_to_table(df_tree,'analysis','tree')

# POST_SATISFCATION_QUESTION_1 <= 4.5