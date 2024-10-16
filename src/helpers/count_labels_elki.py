import re
import sys
import pandas as pd

def parse_cluster_file(file_path):
    """Parse the cluster file and extract cluster data."""
    cluster_data = []
    predicted_cluster = None
    
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
    return cluster_data

def process_and_display_data(cluster_data):
    """Process and display the cluster data."""
    # Convert the parsed data into a pandas DataFrame
    df = pd.DataFrame(cluster_data)

    # Group by 'ClusterID' and 'True Label', then count occurrences
    label_counts = df.groupby(['ClusterID', 'True Label']).size().reset_index(name='Count')

    # Display the result in the terminal without truncation
    print(label_counts.to_string(index=False))

# Main
if __name__ == "__main__":
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    
    file_name = sys.argv[1] # file name as argument
    cluster_data = parse_cluster_file(file_name)
    process_and_display_data(cluster_data)