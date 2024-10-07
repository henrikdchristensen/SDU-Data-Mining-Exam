import re
import pandas as pd

# Set pandas options to display all rows and columns
pd.set_option('display.max_rows', None)  # Display all rows
pd.set_option('display.max_columns', None)  # Display all columns
pd.set_option('display.width', None)  # Set no limit on column width

# File path
file_path = "out.txt"

# Initialize an empty list to hold the parsed data
cluster_data = []
predicted_cluster = None

# Read the file and parse the data
with open(file_path, 'r') as file:
    for line in file:
        # Detect cluster sections in the file (e.g., # Cluster: Cluster 1)
        cluster_match = re.match(r'# Cluster: Cluster (\d+)', line)
        if cluster_match:
            predicted_cluster = cluster_match.group(1)
        # Regular expression to match lines that contain data (e.g., ID=...)
        elif re.match(r'ID=\d+', line):
            parts = re.split(r'\s+', line.strip())
            cluster_data.append({
                'ID': parts[0],  # Store ID (e.g., 'ID=123')
                'True Label': parts[-1],  # Store the true label (e.g., 'cluster1', 'cluster2')
                'ClusterID': predicted_cluster  # Store the predicted cluster
            })

# Convert the parsed data into a pandas DataFrame
df = pd.DataFrame(cluster_data)

# Group by 'ClusterID' and 'True Label', then count occurrences
label_counts = df.groupby(['ClusterID', 'True Label']).size().reset_index(name='Count')

# Display the result in the terminal without truncation
print(label_counts.to_string(index=False))
