# README
Two different data generator programs are used to generate clustered datasets:
- The most data sets are generated using **MDCGEN** (https://link.springer.com/article/10.1007/s00357-019-9312-3) which is very efficient for large scale high-dimensional data by utilizing MATLAB.
- The other program used is **Artifical Cluster** (https://doi.org/10.36227/techrxiv.19091330.v1) which is a little more flexible in terms of cluster shapes (e.g. creation of Bezier curves). However, it should be noticed that I have no success in generating datasets with more than 1 mio. data points, so for large scale data, use "MDCGEN".

## MDCGEN
### Installation
1. Install MATLAB (R2016 or higher).
2. Download **mdcgen-matlab** from https://github.com/CN-TU/mdcgen-matlab and unzip it (version used for this project is from the commit "9b201f9" (from Sep 16, 2019).).
3. Place the content of the unzipped folder in the project folder called `mdcgen`.
4. (Optional) you can remove all the files and folders except from `mdcgen` and `config_build`. But, please do keep `mdc_help.m`.
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
I have make it a little more easier to generate and illustrate the data sets during creation of synthetic data. The extension script called `mdcgen_script.m` is used to save datasets with labels into an .csv file incl. plotting the data.

The script loads a config file (`.mat` file) which tells how the data set should be generated (e.g. number of datapoints, number of outliers, number of clusters, compactness, number of dimensions, etc.).

### Config file
| Field  | Description |
| ------------- | ------------- |
| nDatapoints | Total number of data points |
| nDimensions | Number of dimensions in the data set |
| nClusters | Number of clusters in the data set |
| nDimsPerCluster | Number of dimensions per cluster |
| outliersPercentage | Percentage of outliers in the data set |
| compactness | Compactness of the clusters |
| nNoise | Manual definition of which dimensions that are noise for a cluster. Defined as a matrix, where each column correspond to a cluster and where the rows defines which dims that are noise for that cluster. For example if you write 3 in one of the rows in the second coloumn then dimension 3 will be noise for cluster 2 |
| distribution | Type of distribution to be used. (0) random, (1) Uniform, (2) Gaussian, (3) Logistic, (4) Triangular, (5) Gamma, (6) Gap or ring-shaped. All the data sets generated in this project is from the uniform distribution.
| multivariate | (1) multivariate, (-1) radial based, (0) random. All the data sets generated in this project is from the uniform distribution. |
| diffDimsForClusters | If set to 1, the dimensions for each cluster will be different. |
| equalClusterMass | If set to 1, the mass of each cluster will be equal. |
| maxDistinctClusterDims | Maximum number of distinct dimensions for the clusters. |
| seed | Seed for the random number generator. |
| plot | If set to 1, the data set will be plotted after generation. |

NOTE: If only one dimension is noise for clusters just insert the same dimension in the 2nd row.

Example: 3 dimensions and 2 clusters, where the first cluster and the 3rd dim is noise and for the second cluster the 1st dim is noise:
```matlab
nNoise = [3,1;3,1];
```

## Artifical Cluster
### Installation
1. Install Java 8 or later. Check the version by running `java -version` in the terminal.
1. Download `artificalCluster-1.0.jar` file from https://github.com/wk1lian/ArtificalCluster and place it in the `data-generator` directory (version used in this project is commit "27d7586" (Jan 19, 2024) ).
2. To generate a dataset based on a config file from the `datasets/artificalCluster` folder, we can, for example, run the following command from the `data-generator` directory:
```bash
java -jar artificalCluster-1.0.jar -rg="datasets/artificalCluster/accuracy/bezier/bez.config" -o="datasets/artificalCluster/accuracy/bezier/bez.txt" && python helpers/fix_labels_ac.py datasets/artificalCluster/accuracy/bezier/bez.txt -l 0.1
```

The value is the noise percentage to be added to the data set (0.1 = 10% noise). If the `-l` flag is used, then labels will be added to the dataset.

## ELKI
ELKI is a data mining program written in Java. It can evaluate many different clustering algorithms and outlier detection algorithms. The software is available at https://elki-project.github.io/.

You can download a pre-compiled release at https://elki-project.github.io/releases/. I have used release 0.8.0 (2022, October 5).

After the folder is unzipped you can run elki from the root folder. If you are on a Linux machine use the `elki.sh` file and if you are on a Windows machine use the `elki.bat` file. This will lead you to the main GUI.

### Basic usage
1. Link the data set file at `dbc.in`.
2. Set the flag `time` to true, if you want to measure the time used by the algorithm.
3. Now, choose the `algorithm` you want to use. For example, if you want to use the DBSCAN algorithm, you can choose the `clustering.dbscan.DBSCAN` algorithm. Then, its parameters to be defined will be displayed.
4. Different `evaluator` can be set. For this project, the default `AutomaticEvaluation` was fine.
5. After the evaluation of the algorithm has been run. Then, we can choose to plot the data, by using the default `AutomaticVisualization`. If you want to write output details to a file, use the `ResultWriter` and set the `out` property.

## Using ELKI to plot already clustered (labeled) data
Many algorithms are in ELKI, however, my main concern is the MAFIA algorithm and this is not provided in ELKI.

However, after have used any other program which can cluster the data, then we still can use ELKI to plot the data. This is done by using the `algorithm` called `algorithm.NullAlgorithm`. This algorithm does not do any clustering, but it can still plot the data.

## GPUMAFIA
https://github.com/canonizer/gpumafia/tree/master

### Installation
I have used Ubuntu 24.04.1 LTS installed on a Virtual Box for this project.

Since GPUMAFIA uses and older gcc-compiler, some steps are necessary (otherwise changes to the source code are necessary). The steps are:
1. sudo -i
2. apt install gcc make
3. install gcc4.8. Use the package `gcc48-c++_4.8.4-2ubuntu14_amd64.deb` from `utils` directory and install (double click). This will provides `/usr/local/bin/{gcc48, g++48}`.
4. Update Alternatives (Optional): If you need to switch between multiple GCC versions or set GCC 4.8 as the default, you can use the update-alternatives tool. First, configure alternatives for gcc and g++:
`sudo update-alternatives --install /usr/bin/gcc gcc /usr/local/bin/gcc48 50`
`sudo update-alternatives --install /usr/bin/g++ g++ /usr/local/bin/g++48 50`
Then, select the default version:
`sudo update-alternatives --config gcc`
`sudo update-alternatives --config g++`
5. Change to g++ in `makefile.def`
6. Use the command `make` in project directory with `sudo -i` rights.
7. `make install`
8. `cppmafia <data-file> <commands>`

### Usage
First note that GPUMAFIA is 0-indexed, so the first cluster is index 0 same goes for the dimensions.

Usage: `cppmafia <data-file> <commands>`

Commands:
- -a,--alpha alpha - dense threshold (alpha)
- -b,--beta beta - window merge threshold (alpha)
- -n,--bins nbins - minimum number of bins
- -u,--min-wins nwins - number of windows for uniform dimensions
- -M,--max-wins nwins - maximum number of windows for a dimension
- -h,--help - print this message and exit
- -V,--verbose - print intermediate data as the algorithm runs
- -p,--output-points - output cluster points in addition to indices 
- --no-set-dedup - turns off set deduplication; can degrade speed
- --seq[ential] - forces sequential computation on CPU side
- --no-bitmap,--no-bitmaps - disables point counting with bitmaps; can degrade speed extremely, and does not work on devices
- --timing - prints out additional timing info. `compute time` is the time used by the algorithm.

Note that, I have no succeed if not using the `-M` flag and set it to at least 20. Also note that, the verbose output is disabled by default. If we set the flag `-V`, then all the dimension's histogram values will be outputted. Furthermore, it shows the merged windows sizes for each dimension. And the DUs are shown for each dimension. Finally, the clusters are shown with the corresponding DUs.

The notation "cluster 2 (4): [ [0:0.30..0.60 6:0.00..0.20 7:0.75..1.00 8:0.10..0.40] ]", means that cluster 2 is 4-dimensional defined by the dimensions 0, 6, 7, and 8. The values in the brackets are the DUs for each dimension.

If you want directly write the terminal output to a file, you can use `>`: `cppmafia <data-file> <commands> > out.txt`.

## Helper scripts
### Setup a Python environment
`conda env create -n mining python=3.12`
`conda activate mining`
`pip install -r requirements.txt`

### count_lines.py
This script is used to count the number of data points in a dataset.

Usage: `python helpers/count_lines.py <data-file>`

### fix_labels_ac.py
This script is used fixed the labels generated by the `Artifical Cluster` program. To use this script, the `-l` flag must be used when generating the dataset, see [Artifical Cluster](#artifical-cluster) for more information.

Usage: `python helpers/fix_labels_ac.py <data-file>`

### compose_outputs_mafia.py
GPUMAFIA outputs always a file for each cluster containing the data points indencies. If you want also GPUMAFIA to output the points, then use the `-p` flag.

However, as ELKI and in many other scenarios it is nice to have them into a single composed file. This script does excatly that.

Usage: `python compose_outputs_mafia.py`.

## count_labels_mafia.py
Having a composed mafia file, you can now count how many different labels there are inside each of the clusters.

## count_labels_elki.py
Same as above, just for the ELKI output when using the `ResultWriter`.

## stats_mafia.py
Having a composed mafia file, you can now get some statistics about the clustering results.

## stats_elki.py
Same as above, just for the ELKI output when using the `ResultWriter`.

## .gitignore
All datasets are ignored by git except from config files. This is to avoid committing large files to the repository.

## Evaluation
The main evaluation of the MAFIA algorithm as well as the comparison against CLIQUE and SUBCLU, can be seen in the Jupyter Notebook file `evaluation.ipynb`.

The main evaluations performed:
- Accuracy (clustering quality).
- Scalability in terms of data set size, cluster dimensionality and data dimensionality.
- Sensitivity against choice of parameters.