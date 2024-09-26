%% Clear
clear
warning on
warning('backtrace', 'off');
addpath(genpath('mdcgen/config_build/src/'));
addpath(genpath('mdcgen/mdcgen/src'));

%% Load config
plot = true;  % true if generate plots
config_file = 'datasets/mdcgen/adaptive_grids_effect/dataset_A/config.mat';  % path to config file
out_file = 'datasets/mdcgen/adaptive_grids_effect/dataset_A/dataset.csv';    % output dataset file
load(config_file, 'config');

%% Save config (can be used during testing/changes)
%save(config_file, 'config');

%% Generate data using MDCGen and config
[result] = mdcgen(config);

% Assign cluster labels ("cluster1", "cluster2", etc.) and "noise" for outliers (label 0)
labels_str = strings(size(result.label));
for k = 1:config.nClusters
    labels_str(result.label == k) = strcat("cluster", num2str(k));  % assign cluster labels
end
labels_str(result.label == 0) = "noise";  % assign "noise" to outliers

% Just remove the few points that are outside the [0, 1] range
valid_indices = all(result.dataPoints >= 0 & result.dataPoints <= 1, 2);
filtered_data = result.dataPoints(valid_indices, :);
filtered_labels = labels_str(valid_indices);  % use string labels

%% Plot if requested
if plot
    marker_size = 10;
    labels = strcat('dim', string(1:config.nDimensions));
    data = filtered_data(:, 1:config.nDimensions);
    cluster_colors = lines(config.nClusters);  % distinct colors for each cluster
    noise_color = [0 0 0];  % black color for noise
    figure;
    hold on;
    switch config.nDimensions
        case 2
            % Loop through each cluster and plot
            for k = 1:config.nClusters
                cluster_points = data(filtered_labels == strcat("cluster", num2str(k)), :);
                scatter(cluster_points(:, 1), cluster_points(:, 2), marker_size, cluster_colors(k, :), 'filled', 'DisplayName', ['Cluster ' num2str(k)]);
            end

            % Plot noise points in black
            noise_points = data(filtered_labels == "noise", :);
            if ~isempty(noise_points)
                scatter(noise_points(:, 1), noise_points(:, 2), marker_size, noise_color, 'filled', 'DisplayName', 'Noise');
            end

            % Labels and legend
            xlabel('dim1');
            ylabel('dim2');
            legend('show');

        case 3
            % Loop through each cluster and plot
            for k = 1:config.nClusters
                cluster_points = data(filtered_labels == strcat("cluster", num2str(k)), :);
                scatter3(cluster_points(:, 1), cluster_points(:, 2), cluster_points(:, 3), marker_size, cluster_colors(k, :), 'filled', 'DisplayName', ['Cluster ' num2str(k)]);
            end

            % Plot noise points in black
            noise_points = data(filtered_labels == "noise", :);
            if ~isempty(noise_points)
                scatter3(noise_points(:, 1), noise_points(:, 2), noise_points(:, 3), marker_size, noise_color, 'filled', 'DisplayName', 'Noise');
            end
            
            view(3);  % set default 3D view

            % Labels and legend
            xlabel('dim1');
            ylabel('dim2');
            zlabel('dim3');
            legend('show');

        otherwise
            % For dimensions >3, use plotmatrix
            [h, ax] = plotmatrix(data);
            for i = 1:config.nDimensions
                xlabel(ax(config.nDimensions, i), labels{i});
                ylabel(ax(i, 1), labels{i});
            end
    end
    hold off;
end

%% Write data to a CSV file (comma delimited)
data_and_labels = [filtered_data, filtered_labels];
writematrix(data_and_labels, out_file);
disp('Synthetic data is generated and saved.'); % notify