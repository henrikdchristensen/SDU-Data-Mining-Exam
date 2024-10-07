import re
import pandas as pd
from sklearn.metrics import normalized_mutual_info_score, adjusted_mutual_info_score, f1_score, jaccard_score, precision_score, adjusted_rand_score, rand_score, silhouette_score, completeness_score, homogeneity_score, v_measure_score
from sklearn.preprocessing import LabelEncoder

# File path
file_path = "elki_test.txt"

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
            cluster_data.append((line.strip(), predicted_cluster))

# Parse the extracted cluster data into a pandas DataFrame
data = []
for entry, cluster in cluster_data:
    parts = re.split(r'\s+', entry)
    true_label = parts[-1]  # true cluster label (e.g., 'cluster1', 'cluster2')
    feature_values = [float(part) for part in parts[1:-1]]  # handle all features (everything between ID and true label)
    data.append([parts[0], true_label, cluster] + feature_values)  # store ID, true label, predicted cluster, and feature values

# Determine the number of features dynamically
num_features = len(data[0]) - 3  # subtracting 3 columns: ID, true_label, predicted_cluster

# Generate column names dynamically for the features
column_names = ["ID", "true_label", "predicted_cluster"] + [f"feature_{i}" for i in range(1, num_features + 1)]

# Convert to DataFrame
df = pd.DataFrame(data, columns=column_names)

# Encode the labels into numeric form
le_true = LabelEncoder()
true_labels_encoded = le_true.fit_transform(df["true_label"])
le_pred = LabelEncoder()
predicted_labels_encoded = le_pred.fit_transform(df["predicted_cluster"])

# Calculate various metrics
nmi_min = normalized_mutual_info_score(true_labels_encoded, predicted_labels_encoded, average_method='arithmetic')
nmi_max = normalized_mutual_info_score(true_labels_encoded, predicted_labels_encoded, average_method='max')
nmi_geo = normalized_mutual_info_score(true_labels_encoded, predicted_labels_encoded, average_method='geometric')
nmi_ari = normalized_mutual_info_score(true_labels_encoded, predicted_labels_encoded, average_method='arithmetic')
ami_min = adjusted_mutual_info_score(true_labels_encoded, predicted_labels_encoded, average_method='arithmetic')
ami_max = adjusted_mutual_info_score(true_labels_encoded, predicted_labels_encoded, average_method='max')
ami_geo = adjusted_mutual_info_score(true_labels_encoded, predicted_labels_encoded, average_method='geometric')
ami_ari = adjusted_mutual_info_score(true_labels_encoded, predicted_labels_encoded, average_method='arithmetic')
f1_weighted_avg = f1_score(true_labels_encoded, predicted_labels_encoded, average='weighted')
jaccard_weighted_avg = jaccard_score(true_labels_encoded, predicted_labels_encoded, average='weighted')
precision = precision_score(true_labels_encoded, predicted_labels_encoded, average='weighted')
ari = adjusted_rand_score(true_labels_encoded, predicted_labels_encoded)
rand = rand_score(true_labels_encoded, predicted_labels_encoded)
features = df[[f"feature_{i}" for i in range(1, num_features + 1)]].values
sil = silhouette_score(features, predicted_labels_encoded, metric='euclidean')
com = completeness_score(true_labels_encoded, predicted_labels_encoded)
hom = homogeneity_score(true_labels_encoded, predicted_labels_encoded)
vm = v_measure_score(true_labels_encoded, predicted_labels_encoded)

# Print results
print(f"Normalized Mutual Information (NMI), min: {nmi_min}")
print(f"Normalized Mutual Information (NMI), max: {nmi_max}")
print(f"Normalized Mutual Information (NMI), geometric: {nmi_geo}")
print(f"Normalized Mutual Information (NMI), arithmetic: {nmi_ari}")
print(f"Adjusted Mutual Information (AMI), min: {ami_min}")
print(f"Adjusted Mutual Information (AMI), max: {ami_max}")
print(f"Adjusted Mutual Information (AMI), geometric: {ami_geo}")
print(f"Adjusted Mutual Information (AMI), arithmetic: {ami_ari}")
print(f"F1 Score (Weighted Avg.): {f1_weighted_avg}")
print(f"Jaccard Score (Weighted Avg.): {jaccard_weighted_avg}")
print(f"Precision Score (Weighted Avg.): {precision}")
print(f"Adjusted Rand Index (ARI): {ari}")
print(f"Rand Index: {rand}")
print(f"Silhouette Score: {sil}")
print(f"Completeness Score: {com}")
print(f"Homogeneity Score: {hom}")
print(f"V-measure Score: {vm}")