import pandas as pd

# Set pandas options to display all rows and columns
pd.set_option('display.max_rows', None)  # Display all rows
pd.set_option('display.max_columns', None)  # Display all columns
pd.set_option('display.width', None)  # Set no limit on column width

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('composed.csv', sep=',')  # Assuming the file is tab-separated

# Group by 'ClusterID' and 'True Label', then count occurrences
label_counts = df.groupby(['ClusterID', 'True Label']).size().reset_index(name='Count')

# Display the result in the terminal without truncation
print(label_counts)