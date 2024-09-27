# SDU-Data-Mining-Exam

Two different data generator programs are used to generate clustered datasets.

"MDCGEN" (https://link.springer.com/article/10.1007/s00357-019-9312-3) which is very efficient for large scale high-dimensional data and "Artifical Cluster" (https://doi.org/10.36227/techrxiv.19091330.v1) which is more flexible in terms of cluster shapes. It should be noticed that I have no success in generating datasets >1 mio. data points using "Artifical Cluster", so for large scale data, "MDCGEN" is the way to go, that why most of the datasets are generated using "MDCGEN".


## MDCGEN
Download `mdcgen-matlab` from https://github.com/CN-TU/mdcgen-matlab and unzip it. Place the content of the unzipped folder in a folder in root called `mdcgen`. You can remove all the files and folders except from `mdcgen` and `config_build`. But do also keep `mdc_help.m`.

The folder structure should look like this:
```bash
.
├── mdcgen
│   ├── mdcgen
│   │   ├── ...
│   ├── config_build
│   │   ├── ...
│   ├── mdc_help.m
```

The version used for the development of this project is from the commit "9b201f9" (from Sep 16, 2019).

A written extension script called `mdcgen_script.m` is used to save datasets with labels into an .csv file incl. plotting the data.

This extension script program loads a config file from `datasets/mdcgen/<dataset>` and generates a dataset based on the config file.

Did not have any success in generating datasets >4 mio. data points using on my local machine with 16GB RAM. Instead, I have used the MATLAB Online service to generate the large datasets.

## Artifical Cluster
Download `artificalCluster-1.0.jar` file from https://github.com/wk1lian/ArtificalCluster and place it in the `data-generator` directory.

The version used for the development of this project is from the commit "27d7586" (Jan 19, 2024).

To generate a dataset based on a config file from the `datasets/artificalCluster` folder, we can, for example, run the following command from the `data-generator` directory:
```bash
java -jar artificalCluster-1.0.jar -rg="datasets/artificalCluster/bez/bez.config" -o="datasets/artificalCluster/bez/bez.txt" && python helpers/fix_labels.py datasets/artificalCluster/bez/bez.txt -l -n 0.1
```

Here the `-n` flag is used to add noise to the dataset. The value is the percentage of noise to add (0.1 = 10% noise). The `-l` flag is used to add labels to the dataset.

## Helper scripts

### count_datapoints.py
This script is used to count the number of data points in a dataset. From the `data-generator` directory, run, for example, the following command:
```bash
python helpers/count_datapoints.py datasets/artificalCluster/bez/bez.txt
```

### fix_labels.py
This script is used fixed the labels generated by the `Artifical Cluster` program. See under [Artifical Cluster](#artifical-cluster) for more information.

## .gitignore
All datasets are ignored by git except from config files. This is to avoid committing large files to the repository.