import os
import pandas as pd

def load_data_with_labels(csv_filename):
    """Load data points with true labels from .txt file."""
    return pd.read_csv(csv_filename, delimiter='\t', header=None)

def parse_idx_file(idx_filename):
    """Parse .idx file to get indices of points in corresponding cluster."""
    with open(idx_filename, 'r') as idx_file:
        indices = [int(line.strip()) for line in idx_file.readlines()]
    return indices

def collect_clusters(data_folder):
    """Collect clusters from .idx and .dat files in folder."""
    clusters = {}
    for filename in os.listdir(data_folder):
        if filename.endswith(".idx"):
            cluster_index = filename.split("-")[-1].split(".")[0]
            idx_filename = os.path.join(data_folder, filename)
            indices = parse_idx_file(idx_filename)
            clusters[int(cluster_index)] = indices
    return clusters

def compose_single_file(csv_filename, data_folder, output_filename):
    """Compose a single file for clusters/noise points with predicted labels."""
    # Load full data file (.csv file) with labels
    full_data = load_data_with_labels(csv_filename)
    data_points_total = len(full_data)
    
    # Collect all clusters from .idx files
    clusters = collect_clusters(data_folder)
    
    # Sort clusters by cluster index
    sorted_cluster_indices = sorted(clusters.keys())
    
    # Open both the full output file and the simplified elki output
    with open(output_filename, 'w') as output_file:
        used_indices = set()

        # Prepare header text based on number of dimensions
        num_dims = full_data.shape[1] - 1  # last column is the label
        header_dims = [f"dim{i+1}" for i in range(num_dims)]
        
        # Write header for the full output file
        output_file.write("ClusterID Index " + " ".join(header_dims) + " True Label\n")

        # Write clusters in numerical order (Cluster 1, 2, ...)
        for cluster_index in sorted_cluster_indices:
            indices = clusters[cluster_index]
            for idx in indices:
                used_indices.add(idx)
                data_point = full_data.iloc[idx, :-1].tolist()  # extract all dimensions
                data_point_str = " ".join(map(str, data_point))
                label = full_data.iloc[idx, -1]  # true label is last column
                
                # Write full details to the output file
                output_file.write(f"cluster{cluster_index} {idx} {data_point_str} {label}\n")
        
        # Write noise points
        for idx in range(data_points_total):
            if idx not in used_indices:
                data_point = full_data.iloc[idx, :-1].tolist()  # extract all dimensions
                data_point_str = " ".join(map(str, data_point))
                label = full_data.iloc[idx, -1]  # true label is last column

                # Write noise details to the full output file
                output_file.write(f"noise {idx} {data_point_str} {label}\n")

# Input and output filenames
in_filename = 'data_labels.txt'  # file with data points and labels
data_folder = '.'  # folder with .dat and .idx files
output_filename = 'composed.txt'  # output file with full details

compose_single_file(in_filename, data_folder, output_filename)
