%% Clear, paths, seed
clear;
warning off;
warning('backtrace', 'off');
addpath(genpath('mdcgen/config_build/src/'));
addpath(genpath('mdcgen/mdcgen/src/'));

%% General settings
maxPlotPoints = 10000;  % max. number of points to plot, if max is reached, we sample
maxPlotDims = 10; % only plot first 10 dimensions (if available)

%% Dataset directory
dir = 'datasets/mdcgen/cluster_dimensionality/500k/20d/';

%% Load config
configFile = strcat(dir, 'config.mat');
outFileWithoutLabels = strcat(dir, 'data.txt');
outFileWithLabels = strcat(dir, 'data_labels.csv');
outFileNoiseMatrix = strcat(dir, 'noise.csv');
load(configFile, 'config');
% "save(configFile, 'config')" can be used after making changes to config in workspace explorer.

%% Copy config
c = config;

%% Set seed
rng(c.seed);

%% Determine number of outliers and subtract from cluster datapoints
c.nOutliers = round(c.nDatapoints * c.outliersPercentage);
c.nDatapoints = c.nDatapoints - c.nOutliers;

%% Assign noise dimensions to clusters
if c.nNoise == 0 % if nNoise==0, use manually defined noise dimensions
    noiseDimsPerCluster = c.nDimensions - c.nDimsPerCluster;
    if c.diffDimsForClusters % each column corresponds to a cluster
        noiseMatrix = zeros(noiseDimsPerCluster, c.nClusters);
        if c.maxDistinctClusterDims > 0 && c.nDimensions > c.maxDistinctClusterDims
            distinctClusterDims = randperm(c.nDimensions, c.maxDistinctClusterDims);
            for k = 1:c.nClusters
                clusterDims = randsample(distinctClusterDims, c.nDimsPerCluster);
                noisePool = setdiff(1:c.nDimensions, clusterDims);
                noiseMatrix(:, k) = randsample(noisePool, noiseDimsPerCluster)';
            end
        else % if no maxDistinctClusterDims is set, use all dimensions for noise
            for k = 1:c.nClusters
                noiseMatrix(:, k) = randperm(c.nDimensions, noiseDimsPerCluster)';
            end
        end
        c.nNoise = noiseMatrix;
        
    else
        c.nNoise = noiseDimsPerCluster;
    end
end
writematrix(sort(c.nNoise), outFileNoiseMatrix); % save noise matrix

%% Equal cluster mass
if c.equalClusterMass
    c.minimumClusterMass = floor(c.nDatapoints / c.nClusters);
end

%% Generate data based on config
[result] = mdcgen(c);

%% Assign cluster labels ("cluster1", "cluster2", etc.") and "noise" for outliers (label 0)
labels = strings(size(result.label));
for k = 1:c.nClusters
    labels(result.label == k) = strcat("cluster", num2str(k));  % assign cluster labels
end
labels(result.label == 0) = "noise";
data = result.dataPoints;

%% Write data to .csv file (comma delimited)
% TODO: could be improved since the file with labels cuts of some precion of records
disp('write data to file...');
writematrix(data, outFileWithoutLabels,'Delimiter','\t');
dataAndLabels = [data, labels];
writematrix(dataAndLabels, outFileWithLabels,'Delimiter',',');
disp('synthetic data is generated and saved.');

%% Plot if requested
if c.plot
    totalPoints = size(data, 1); % determine total number of points
    dataToPlot = data(:, 1:min(maxPlotDims, c.nDimensions)); % select only the first 10 dimensions
    dimLabels = strcat('dim', string(1:maxPlotDims)); % update the dimension labels
    if totalPoints > maxPlotPoints % if more than maxPlotPoints, randomly sample
        plotIndices = randperm(totalPoints, maxPlotPoints); % randomly select indices
        dataToPlot = dataToPlot(plotIndices, :); % subset the data for plotting
        labels = labels(plotIndices); % subset the labels for plotting
    end
    markerSize = 20; % marker size for cluster points
    markerSizeNoise = markerSize / 8; % smaller marker size for noise points
    clusterColors = lines(c.nClusters); % distinct colors for each cluster (can only be done in <=3d)
    figure;
    hold on;
    
    % Handle different dimensionalities (only plot the first 10 dimensions)
    switch maxPlotDims
        case 2 % 2d
            % 2D plot for the first two dimensions
            for k = 1:c.nClusters
                clusterPoints = dataToPlot(labels == strcat("cluster", num2str(k)), :);
                scatter(clusterPoints(:, 1), clusterPoints(:, 2), markerSize, clusterColors(k, :), 'filled', 'DisplayName', ['Cluster ' num2str(k)]);
            end
            noisePoints = dataToPlot(labels == "noise", :);
            if ~isempty(noisePoints)
                scatter(noisePoints(:, 1), noisePoints(:, 2), markerSizeNoise, 'black', 'filled', 'DisplayName', 'Noise');
            end
            xlabel('dim1');
            ylabel('dim2');
            legend('show');
        case 3 % 3d
            for k = 1:c.nClusters
                clusterPoints = dataToPlot(labels == strcat("cluster", num2str(k)), :);
                scatter3(clusterPoints(:, 1), clusterPoints(:, 2), clusterPoints(:, 3), markerSize, clusterColors(k, :), 'filled', 'DisplayName', ['Cluster ' num2str(k)]);
            end
            noisePoints = dataToPlot(labels == "noise", :);
            if ~isempty(noisePoints)
                scatter3(noisePoints(:, 1), noisePoints(:, 2), noisePoints(:, 3), markerSizeNoise, 'black', 'filled', 'DisplayName', 'Noise');
            end
            view(3);  
            xlabel('dim1');
            ylabel('dim2');
            zlabel('dim3');
            legend('show');
        otherwise % >3d
            [h, ax] = plotmatrix(dataToPlot);
            for i = 1:maxPlotDims
                xlabel(ax(maxPlotDims, i), dimLabels{i});
                ylabel(ax(i, 1), dimLabels{i});
            end
    end
    hold off;
end