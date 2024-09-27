%% Clear, paths, seed
clear;
warning off;
warning('backtrace', 'off');
addpath(genpath('mdcgen/config_build/src/'));
addpath(genpath('mdcgen/mdcgen/src/'));
rng(122); % set seed

%% Dataset directory
dir = 'datasets/mdcgen/database_size/1.5mio/';

%% Load config
configFile = strcat(dir, 'config.mat');
outFile = strcat(dir, 'dataset.csv');
load(configFile, 'config'); % "save(configFile, 'config')" can be used after making changes to config in workspace explorer.
c = config;

%% Don't plot if dimensions are high or too many points
if c.nDimensions > 10 || c.nDatapoints > 500000
    c.plot = false;
    save(configFile, 'config');
end

%% Assign noise dimensions to clusters
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

%% Determine number of outliers
c.nOutliers = round(c.nDatapoints * c.outliersPercentage);

%% Equal cluster mass
if c.equalClusterMass
    c.minimumClusterMass = floor(c.nDatapoints / c.nClusters);
end

%% Generate data using MDCGen and config
[result] = mdcgen(c);

%% Assign cluster labels ("cluster1", "cluster2", etc.") and "noise" for outliers (label 0)
labelsStr = strings(size(result.label));
for k = 1:c.nClusters
    labelsStr(result.label == k) = strcat("cluster", num2str(k));  % assign cluster labels
end
labelsStr(result.label == 0) = "noise";

%% Apply filtering of points outside [0, 1] range if requested
if c.filtering
    validIndices = all(result.dataPoints >= 0 & result.dataPoints <= 1, 2);
    data = result.dataPoints(validIndices, :);
    labels = labelsStr(validIndices);
else
    data = result.dataPoints;
    labels = labelsStr;
end

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
dataAndLabels = [data, labels];
writematrix(dataAndLabels, outFile);
disp('Synthetic data is generated and saved.');
