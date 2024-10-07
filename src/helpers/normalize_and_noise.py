import numpy as np
import pandas as pd

def add_noise(data, noise_level=0.1):
    noise = np.random.normal(0, noise_level, data.shape)
    return data + noise

def normalize(data):
    min_vals = data.min(axis=0)
    max_vals = data.max(axis=0)
    return (data - min_vals) / (max_vals - min_vals)

# Reading the dataset from a file
# Replace 'dataset.txt' with your file path
data = pd.read_csv('data.txt', sep='\t', header=None)

# Convert to a numpy array for easier manipulation
data_np = data.values

# Add noise to the data
data_with_noise = add_noise(data_np, noise_level=0.05)

# Normalize the noisy data
normalized_data = normalize(data_with_noise)

# Convert the normalized data back to a DataFrame for easier output handling
normalized_df = pd.DataFrame(normalized_data, columns=['Feature1', 'Feature2'])

# Save the modified dataset to a new file
normalized_df.to_csv('normalized_dataset_with_noise.txt', sep='\t', index=False, header=False)

print("Data has been normalized and saved with noise added.")