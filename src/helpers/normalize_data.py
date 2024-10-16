import sys
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def normalize(file_path, output_file):
    # Load the data using pandas
    data = pd.read_csv(file_path, delimiter='\t', header=None)
    
    # Separate features and labels
    features = data.iloc[:, :-1]
    labels = data.iloc[:, -1]
    
    # Apply min-max normalization to the feature columns
    scaler = MinMaxScaler()
    normalized_features = scaler.fit_transform(features)
    
    # Combine the normalized features and the labels back into a DataFrame
    normalized_data = pd.DataFrame(normalized_features)
    normalized_data[len(normalized_data.columns)] = labels  # Add the label column back
    
    # Save the normalized data to a new file
    normalized_data.to_csv(output_file, sep='\t', header=False, index=False, float_format='%.6f')

if __name__ == "__main__":
    input_file = sys.argv[1] # file name as argument (must be txt file)
    output_file = input_file.split('.')[0] + '_normalized.txt' # strip the file extension from the input file name and add '_normalized.txt' to create the output file name
    normalize(input_file, output_file)