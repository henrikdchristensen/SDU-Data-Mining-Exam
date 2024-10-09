# README

Two different data generation tools is used to create clustered datasets:

- Most datasets are generated using **MDCGen** ([Link](https://link.springer.com/article/10.1007/s00357-019-9312-3)), which is very efficient for large-scale, high-dimensional data using MATLAB.
- The other program used is **Artificial Cluster** ([Link](https://doi.org/10.36227/techrxiv.19091330.v1)), which offers more flexibility in terms of cluster shapes (e.g., creation of Bezier curves). However, note that I have not been successful in generating datasets larger than 1 million data points with this program. For larger datasets, use **MDCGen**.

---

## MDCGen

### Installation

1. Install MATLAB (R2016 or higher).
2. Download **mdcgen-matlab** from [this repository](https://github.com/CN-TU/mdcgen-matlab) and unzip it (the version used in this project is from commit `9b201f9` on Sep 16, 2019).
3. Place the contents of the unzipped folder in the project directory under `src/mdcgen`.
4. (Optional) You can remove unnecessary files and folders, except for `mdcgen` and `config_build`. Make sure to keep `mdc_help.m`.
5. The folder structure should look like this:
    ```bash
    .
    ├── mdcgen
    │   ├── mdcgen
    │   │   ├── ...
    │   ├── config_build
    │   │   ├── ...
    │   ├── mdc_help.m
    ```

### Usage

An extension script, `mdcgen_script.m`, simplifies the process of generating and visualizing datasets during synthetic data creation. This script saves datasets with labels into a `.csv` file and plots the data.

The script loads a configuration file (`.mat` file), which defines how the dataset should be generated (e.g., number of data points, clusters, outliers, dimensions, etc.).

### Configuration File

| Field               | Description                                                                                              |
|---------------------|----------------------------------------------------------------------------------------------------------|
| nDatapoints         | Total number of data points                                                                              |
| nDimensions         | Number of dimensions in the dataset                                                                      |
| nClusters           | Number of clusters in the dataset                                                                        |
| nDimsPerCluster     | Number of dimensions per cluster                                                                         |
| outliersPercentage  | Percentage of outliers in the dataset                                                                    |
| compactness         | Compactness of the clusters                                                                              |
| nNoise              | Matrix defining which dimensions are noise for each cluster. See example below.                          |
| distribution        | Distribution type: (0) random, (1) uniform, (2) Gaussian, etc. All datasets in this project use uniform. |
| multivariate        | (1) multivariate, (-1) radial, (0) random. All datasets in this project use uniform distribution.        |
| diffDimsForClusters | Set to 1 if each cluster has different dimensions.                                                       |
| equalClusterMass    | Set to 1 for equal mass across clusters.                                                                 |
| maxDistinctClusterDims | Maximum number of distinct dimensions across clusters.                                                |
| seed                | Seed for the random number generator.                                                                    |
| plot                | Set to 1 to plot the generated dataset.                                                                  |

Example: For 3 dimensions and 2 clusters, where the 3rd dimension is noise for the 1st cluster and the 1st dimension is noise for the 2nd cluster:

```matlab
nNoise = [3,1;3,1];
```

---

## Artificial Cluster

### Installation

1. Install Java 8 or later. Verify by running `java -version` in the terminal.
2. Download the `artificalCluster-1.0.jar` file from [this repository](https://github.com/wk1lian/ArtificalCluster) and place it in the root directory (version used: commit `27d7586`, Jan 19, 2024).
3. Generate a dataset based on a config file from the `src/datasets/artificalCluster` folder by running in the folder `src`:
    ```bash
    java -jar artificalCluster-1.0.jar -rg="datasets/artificalCluster/accuracy/bezier/bez.config" -o="datasets/artificalCluster/accuracy/bezier/bez.txt" && python helpers/fix_labels_ac.py datasets/artificalCluster/accuracy/bezier/bez.txt -l 0.1
    ```
    The `-l` flag adds labels to the dataset, and the value indicates the noise percentage (0.1 = 10%).

---

## ELKI

**ELKI** is a data mining framework written in Java that evaluates clustering and outlier detection algorithms. It can be downloaded from [ELKI Project](https://elki-project.github.io/).

### Installation

Download release 0.8.0 from [here](https://elki-project.github.io/releases/) (version used in this project) and unzip it. You can run ELKI from the root folder using:
- `elki.sh` for Linux
- `elki.bat` for Windows

### Basic Usage

1. Link the dataset file to `-dbc.in`.
2. Set the `-time` flag to true to measure algorithm execution time.
3. Choose the desired clustering `-algorithm` (e.g., `clustering.dbscan.DBSCAN`).
4. Set the parameters for the algorithm.
5. Optionally, use the `-resulthandler ResultWriter` to save output details to a file or `-resulthandler AutomaticVisualization` for plotting the data.
6. If you need to normalize the data set before clustering (e.g., for DBSCAN), use `-dbc.filter normalization.columnwise.AttributeWiseMinMaxNormalization`.

### Plotting Labeled Data

ELKI does not provide the MAFIA algorithm, but you can use the `-algorithm algorithm.NullAlgorithm` to visualize pre-clustered data from other programs.

---

## GPUMAFIA

### Installation

GPUMAFIA is installed on Ubuntu 24.04.1 LTS in a Virtual Box. Follow these steps for installation:

1. Download Virtual Box from [here](https://www.virtualbox.org/wiki/Downloads).
2. Download Ubuntu 24.04.1 LTS from [here](https://releases.ubuntu.com/24.04/).
3. Install Ubuntu on Virtual Box.
   1. Add a new virtual machine.
   2. Select the downloaded Ubuntu ISO file.
   3. Specs: 4 CPUs, 4 GB RAM, 50 GB storage and select a shared folder.
4. After installation, update Ubuntu:
    ```bash
    sudo apt update
    sudo apt upgrade
    ```
5. mount the shared folder (called `src/datasets` in this case) to the home directory:
    ```bash
    sudo mount -t vboxsf -o uid=1000,gid=1000 datasets /home/user/vboxshare
    ```
6. Install GCC and Make:
    ```bash
    sudo apt install gcc make
    ```
7. Install GCC 4.8 (`gcc48-c++_4.8.4-2ubuntu14_amd64.deb`) from the `utils` directory.
8. Use `update-alternatives` to manage multiple GCC versions (optional):
    ```bash
    sudo update-alternatives --install /usr/bin/gcc gcc /usr/local/bin/gcc48 50
    sudo update-alternatives --install /usr/bin/g++ g++ /usr/local/bin/g++48 50
    sudo update-alternatives --config gcc
    sudo update-alternatives --config g++
    ```
9. Modify `makefile.def` to use `g++`.
10. Build and install:
    ```bash
    sudo make
    sudo make install
    ```
11. Run GPUMAFIA using:
    ```bash
    cppmafia <data-file> <commands>
    ```

### Usage

GPUMAFIA uses 0-based indexing. The command structure is:

```bash
cppmafia <data-file> <commands>
```

Common commands:
- `-a` - alpha (dense threshold)
- `-b` - beta (window merge threshold)
- `-n` - minimum number of bins
- `-M` - maximum number of windows (set to at least 20)

---

## Helper Scripts

### Setup Python Environment
```bash
conda env create -n mining python=3.12
conda activate mining
pip install -r requirements.txt
```

### count_lines.py
Count the number of data points in a dataset:
```bash
python helpers/count_lines.py <data-file>
```

### fix_labels_ac.py
Fix the labels generated by the Artificial Cluster program:
```bash
python helpers/fix_labels_ac.py <data-file>
```

### compose_outputs_mafia.py
Combine multiple GPUMAFIA cluster files into a single output file. Just place this python in the same directory as the output files and run:
```bash
python compose_outputs_mafia.py
```

---

## .gitignore

All datasets are ignored by git, except for configuration files, to avoid committing large files.

---

## Evaluation

The primary evaluation of the MAFIA algorithm, along with comparisons to CLIQUE and SUBCLU, is presented in the Jupyter Notebook `evaluation.ipynb`. The evaluation includes:

- Accuracy (clustering quality)
- Scalability (dataset size, dimensionality, and clusters)
- Sensitivity to parameter choices

### Export to pdf
1. Install a LaTeX distribution.
   - Windows: MikTeX
   - Mac: MacTeX
   - Linux: TeX Live
2.  Install pandoc (https://pandoc.org/), make sure it can be found using `pandoc --version`. Otherwise, try to re-open terminal.
3.  Convert to pdf by running the following command from the `src` folder: `jupyter nbconvert --to pdf evaluation.ipynb`. 