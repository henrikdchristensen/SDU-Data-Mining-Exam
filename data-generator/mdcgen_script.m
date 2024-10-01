%% Clear, paths, seed
clear;
warning off;
warning('backtrace', 'off');
addpath(genpath('mdcgen/config_build/src/'));
addpath(genpath('mdcgen/mdcgen/src/'));

%% Dataset directory
dir = 'datasets/mdcgen/accuracy/';

%% Load config
configFile = strcat(dir, 'config.mat');
outFileWithoutLabels = strcat(dir, 'data.txt');
outFileWithLabels = strcat(dir, 'data_labels.csv');
load(configFile, 'config'); % "save(configFile, 'config')" can be used after making changes to config in workspace explorer.

%% Don't plot if dimensions are high or too many points
if config.nDimensions > 10 || config.nDatapoints > 500000
    config.plot = false;
    save(configFile, 'config');
end

%% Copy config
c = config;

%% Set seed
rng(c.seed); % set seed

%% Determine number of outliers and subtract from "normal" datapoints
c.nOutliers = round(c.nDatapoints * c.outliersPercentage);
c.nDatapoints = c.nDatapoints - c.nOutliers;

%% Assign noise dimensions to clusters
if c.nNoise == 0 % if nNoise==0, then use the manual defined noise dims
    noiseDimsPerCluster = c.nDimensions - c.nDimsPerCluster;
    if c.diffDimsForClusters % each column corresponds to a cluster
        noiseMatrix = zeros(noiseDimsPerCluster, c.nClusters);
        for k = 1:c.nClusters % loop through each cluster
            noiseMatrix(1:noiseDimsPerCluster, k) = randperm(c.nDimensions, noiseDimsPerCluster)';
        end
        c.nNoise = noiseMatrix;
    else
        c.nNoise = noiseDimsPerCluster;
    end
end

%% Equal cluster mass
if c.equalClusterMass
    c.minimumClusterMass = floor(c.nDatapoints / c.nClusters);
end

%% Generate data using MDCGen and config
[result] = mdcgen(c);

%% Assign cluster labels ("cluster1", "cluster2", etc.") and "noise" for outliers (label 0)
labels = strings(size(result.label));
for k = 1:c.nClusters
    labels(result.label == k) = strcat("cluster", num2str(k));  % assign cluster labels
end
labels(result.label == 0) = "noise";
data = result.dataPoints;

%% Plot if requested
if c.plot
    markerSize = 20;  % marker size for cluster points
    markerSizeNoise = markerSize / 8;  % smaller marker size for noise points
    dimLabels = strcat('dim', string(1:c.nDimensions));
    clusterColors = lines(c.nClusters);  % distinct colors for each cluster
    figure;
    hold on;
    switch c.nDimensions
        case 2
            % Loop through each cluster point and plot
            for k = 1:c.nClusters
                clusterPoints = data(labels == strcat("cluster", num2str(k)), :);
                scatter(clusterPoints(:, 1), clusterPoints(:, 2), markerSize, clusterColors(k, :), 'filled', 'DisplayName', ['Cluster ' num2str(k)]);
            end
            % Plot noise points
            noisePoints = data(labels == "noise", :);
            if ~isempty(noisePoints)
                scatter(noisePoints(:, 1), noisePoints(:, 2), markerSizeNoise, 'black', 'filled', 'DisplayName', 'Noise');
            end
            % Labels and legend
            xlabel('dim1');
            ylabel('dim2');
            legend('show');
        case 3
            % Loop through each cluster point and plot
            for k = 1:c.nClusters
                clusterPoints = data(labels == strcat("cluster", num2str(k)), :);
                scatter3(clusterPoints(:, 1), clusterPoints(:, 2), clusterPoints(:, 3), markerSize, clusterColors(k, :), 'filled', 'DisplayName', ['Cluster ' num2str(k)]);
            end
            % Plot noise points
            noisePoints = data(labels == "noise", :);
            if ~isempty(noisePoints)
                scatter3(noisePoints(:, 1), noisePoints(:, 2), noisePoints(:, 3), markerSizeNoise, 'black', 'filled', 'DisplayName', 'Noise');
            end
            % Set 3D view
            view(3);  
            % Labels and legend
            xlabel('dim1');
            ylabel('dim2');
            zlabel('dim3');
            legend('show');
        otherwise
            % For dimensions >3, use plotmatrix
            [h, ax] = plotmatrix(data);
            for i = 1:c.nDimensions
                xlabel(ax(c.nDimensions, i), dimLabels{i});
                ylabel(ax(i, 1), dimLabels{i});
            end
    end
    hold off;
end

%% Write data to .csv file (comma delimited)
% TODO: could be improved since the file with labels cuts of some precion of records
writematrix(data, outFileWithoutLabels,'Delimiter','\t');
dataAndLabels = [data, labels];
writematrix(dataAndLabels, outFileWithLabels,'Delimiter',',');

disp('Synthetic data is generated and saved.');
