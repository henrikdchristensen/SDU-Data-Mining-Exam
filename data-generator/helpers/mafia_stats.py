import pandas as pd
from sklearn.metrics import normalized_mutual_info_score, adjusted_mutual_info_score, f1_score, jaccard_score, precision_score, adjusted_rand_score, rand_score, silhouette_score, completeness_score, homogeneity_score, v_measure_score
from sklearn.preprocessing import LabelEncoder

file_path = "composed.csv"

# Read the file
df = pd.read_csv(file_path, sep=',')

# Extract the features dynamically based on column names (assuming format: ClusterID, Index, dim1, ..., True Label)
features = df.columns[2:-1]  # Dimensions are in columns starting from dim1 to dimN
true_labels = df['True Label']
predicted_labels = df['ClusterID']  # Assuming ClusterID as predicted labels

# Encode the labels into numeric form
le_true = LabelEncoder()
true_labels_encoded = le_true.fit_transform(true_labels)
le_pred = LabelEncoder()
predicted_labels_encoded = le_pred.fit_transform(predicted_labels)

# Extract feature values for silhouette score calculation
feature_values = df[features].values

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
sil = silhouette_score(feature_values, predicted_labels_encoded, metric='euclidean')
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