import pandas as pd
import sys

def process_and_display_data(file_name):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(file_name, sep=',')

    # Group by 'ClusterID' and 'True Label', then count occurrences
    label_counts = df.groupby(['ClusterID', 'True Label']).size().reset_index(name='Count')

    # Display the result in the terminal without truncation
    print(label_counts)

# Main
if __name__ == "__main__":
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    
    file_name = sys.argv[1] # file name as argument
    process_and_display_data(file_name)