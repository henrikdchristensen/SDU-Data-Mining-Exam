import os
import pandas as pd
import matplotlib.pyplot as plt

def read_cluster_files(directory):
    """Read cluster files from the given directory and separate them into MAFIA and CLIQUE clusters."""
    # Separate dat (MAFIA) and txt (CLIQUE) files, and sort them in descending order
    mafia_files = sorted([f for f in os.listdir(directory) if f.endswith('.dat')])
    clique_files = sorted([f for f in os.listdir(directory) if f.endswith('.txt')])
    
    mafia_clusters = [(filename, pd.read_csv(os.path.join(directory, filename), delimiter='\t', header=None))
                      for filename in mafia_files]
    clique_clusters = [(filename, pd.read_csv(os.path.join(directory, filename), delimiter='\t', header=None))
                       for filename in clique_files]

    return mafia_clusters, clique_clusters

def plot_clusters(mafia_clusters, clique_clusters):
    """Plot MAFIA and CLIQUE clusters with distinct colors and borders."""
    plt.figure(figsize=(4, 4))
    cmap = plt.get_cmap('tab20')  # Use tab20 colormap for distinct colors

    # Plot CLIQUE clusters with borders
    for i, (filename, cluster) in enumerate(clique_clusters):
        x = cluster.iloc[:, 0]
        y = cluster.iloc[:, 1]
        if i == 1:
            # Set marker size to 10

            plt.scatter(x, y, color='red', label=f'CLIQUE cluster {i+1} ({filename})', alpha=0.2, marker='s', s=30)
        else:
            # triangle marker
            
            plt.scatter(x, y, color='blue', label=f'CLIQUE cluster {i+1} ({filename})', alpha=0.4, marker='s', s=30)
    
    # Plot MAFIA clusters with borders
    for i, (filename, cluster) in enumerate(mafia_clusters):
        x = cluster.iloc[:, 0]
        y = cluster.iloc[:, 1]
        plt.scatter(x, y, color='black', label=f'MAFIA cluster {i+1} ({filename})', alpha=1, marker='x', s=15)

    plt.xlabel('Dimension 0')
    plt.ylabel('Dimension 1')
    plt.legend()
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.show()

if __name__ == "__main__":
    mafia_clusters, clique_clusters = read_cluster_files('.') # Read cluster files from the directory
    if mafia_clusters or clique_clusters:
        plot_clusters(mafia_clusters, clique_clusters)
    else:
        print("No valid cluster files found in the directory.")
