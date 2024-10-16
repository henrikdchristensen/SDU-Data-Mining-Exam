import sys
import os
import random
import argparse

def normalize_data(data):
    """Normalize the data to the range [0, 1] for each dimension."""
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
            normalized_dimension = [0.5] * len(dimension_values)  # handle case where all values are the same
        normalized_data.append(normalized_dimension)

    # Add labels back to the normalized data
    normalized_data.append(data_transposed[-1])  # Add the labels (last column) back

    # Transpose back to the original row format
    return list(zip(*normalized_data))

def normalize_data_modify_labels_and_add_noise(file_path, noise_percentage, include_labels):
    """Add noise points to a dataset and write to a new .txt file."""
    txt_separator = ' '  # '\t' for tab-based txt file or ' ' for space-separated file

    with open(file_path, 'r') as infile:
        lines = infile.readlines()

    # Skip the header and split data into columns (tab-separated)
    data_lines = [line for line in lines if not line.startswith("dimension")]
    data = [line.strip().split('\t') for line in data_lines if line.strip()]

    # Normalize the data
    data = normalize_data(data)

    # Convert each row (which is a tuple) to a list for modification
    data = [list(row) for row in data]

    # Get the number of dimensions (excluding the label column)
    num_dimensions = len(data[0]) - 1

    # Remove the label column if labels are not included
    if not include_labels:
        data = [row[:-1] for row in data]

    # Calculate the number of noise points to generate
    num_noise_points = int(len(data) * noise_percentage)

    # Modify the labels by adding "cluster" in front of each unique label number if labels are included
    if include_labels:
        for row in data:
            row[-1] = f"cluster{int(row[-1])}"  # Convert the label in the last column

    noise_points = []
    for _ in range(num_noise_points):
        # Generate random noise point within [0, 1] for each dimension, rounded to 3 decimals
        noise_point = [str(round(random.uniform(0, 1), 3)) for _ in range(num_dimensions)]
        if include_labels:
            noise_point.append('noise')  # Add the "noise" label as the last column
        noise_points.append(noise_point)

    # Generate new file name for the txt output file
    base_name = os.path.splitext(file_path)[0]
    new_txt_output_path = base_name + '_fixed.txt'

    # Write the original + noise data to the txt file
    with open(new_txt_output_path, 'w') as txtfile:
        for row in data:
            # Join the columns and write to txt file
            row = [str(value) for value in row]
            txtfile.write(txt_separator.join(row) + '\n')

        # Now add noise points to the txt file
        for noise_point in noise_points:
            txtfile.write(txt_separator.join(noise_point) + '\n')

    print(f"Added {noise_percentage*100}% noise points successfully to '{new_txt_output_path}'.")

# Main
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add noise to a dataset.")
    parser.add_argument("file_path", help="The path to the input txt file")
    parser.add_argument("noise_percentage", type=float, help="Percentage of noise points to add (0 to 1)")
    parser.add_argument("-l", "--labels", action="store_true", help="Include (true) 'label' prefix in the labels column")

    args = parser.parse_args()

    # Check if the noise percentage is within the valid range
    if not (0 <= args.noise_percentage <= 1):
        print("Error: noise_percentage must be a valid number between 0 and 1.")
        sys.exit(1)

    # Call the function to process the file
    normalize_data_modify_labels_and_add_noise(args.file_path, args.noise_percentage, args.labels)