import sys
import os
import random
import argparse

# Function to normalize the data within [0, 1] range for each dimension
def normalize_data(data):
    # Convert data to float and calculate min and max for each dimension
    data = [[float(value) for value in row] for row in data]
    num_dimensions = len(data[0]) - 1  # Exclude the last column (label)
    
    # Transpose the data to work on each dimension separately
    data_transposed = list(zip(*data))
    
    # Normalize each dimension
    normalized_data = []
    for i in range(num_dimensions):
        dimension_values = data_transposed[i]
        min_val = min(dimension_values)
        max_val = max(dimension_values)
        # Apply normalization: (x - min) / (max - min)
        if max_val > min_val:
            normalized_dimension = [(x - min_val) / (max_val - min_val) for x in dimension_values]
        else:
            normalized_dimension = [0.5] * len(dimension_values)  # Handle case where all values are the same
        normalized_data.append(normalized_dimension)

    # Add labels back to the normalized data
    normalized_data.append(data_transposed[-1])  # Add the labels (last column) back

    # Transpose back to the original row format
    return list(zip(*normalized_data))

# Function to process the file and add noise points within [0, 1], rounded to 3 decimals
def add_noise(file_path, noise_percentage, include_labels, normalize):
    # Set this variable to either '\t' for tab or ' ' for space separation in the TXT file
    txt_separator = ' '  # '\t' for tab-based txt file or ' ' for space-separated file

    with open(file_path, 'r') as infile:
        lines = infile.readlines()

    # Skip the header and split data into columns (tab-separated)
    data_lines = [line for line in lines if not line.startswith("dimension")]
    data = [line.strip().split('\t') for line in data_lines if line.strip()]

    # Normalize the data if requested
    if normalize:
        data = normalize_data(data)

    # Convert each row (which is a tuple) to a list for modification
    data = [list(row) for row in data]

    # Get the number of dimensions (excluding the label column)
    num_dimensions = len(data[0]) - 1

    # Calculate the number of noise points to generate
    num_noise_points = int(len(data) * noise_percentage)

    # Modify the labels by adding "label" in front of each unique label number if labels are included
    if include_labels:
        for row in data:
            row[-1] = f"label{int(row[-1])}"  # Convert the label in the last column

    noise_points = []
    for _ in range(num_noise_points):
        # Generate random noise point within [0, 1] for each dimension, rounded to 3 decimals
        noise_point = [str(round(random.uniform(0, 1), 3)) for _ in range(num_dimensions)]
        noise_point.append('label_noise')  # Add the "noise" label as the last column
        noise_points.append(noise_point)

    # Generate new file names for the output files
    base_name = os.path.splitext(file_path)[0]
    new_txt_output_path = base_name + '_fixed.txt'
    new_csv_output_path = base_name + '_fixed.csv'

    # Write the original + noise data to both CSV and TXT files
    with open(new_csv_output_path, 'w') as csvfile, open(new_txt_output_path, 'w') as txtfile:
        for row in data:
            # Join the columns and write to files
            row = [str(value) for value in row]
            csvfile.write(','.join(row) + '\n')
            txtfile.write(txt_separator.join(row) + '\n')

        # Now add noise points to both files
        for noise_point in noise_points:
            csvfile.write(','.join(noise_point) + '\n')
            txtfile.write(txt_separator.join(noise_point) + '\n')

    print(f"Added {noise_percentage*100}% noise points successfully to '{new_csv_output_path}' and '{new_txt_output_path}'.")

# Main block to handle command-line arguments
if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Add noise to a dataset and optionally normalize the data.")
    parser.add_argument("file_path", help="The path to the input TXT file")
    parser.add_argument("noise_percentage", type=float, help="The percentage of noise points to add (0 to 1)")
    parser.add_argument("-l", "--labels", action="store_true", help="Include 'label' prefix in the labels column")
    parser.add_argument("-n", "--normalize", action="store_true", help="Normalize the data to [0, 1] range")

    args = parser.parse_args()

    # Check if the noise percentage is within the valid range
    if not (0 <= args.noise_percentage <= 1):
        print("Error: noise_percentage must be a valid number between 0 and 1.")
        sys.exit(1)

    # Check if the file exists
    if not os.path.isfile(args.file_path):
        print(f"Error: The file '{args.file_path}' does not exist.")
        sys.exit(1)

    # Call the function to process the file
    add_noise(args.file_path, args.noise_percentage, args.labels, args.normalize)
