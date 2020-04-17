clear
clc

T = readtable('./positives.csv', 'Delimiter', ',');

for i=2:length(T.Properties.VariableNames)
    TotalCases = T.(char(T.Properties.VariableNames(i)));
    NewCases = [TotalCases(1)];
    for j=2:length(TotalCases)
        NewCases(j) = TotalCases(j) - TotalCases(j-1);
    end

    % Optional data smoothing
    % TotalCases = smoothdata(TotalCases);
    % NewCases = smoothdata(NewCases);

    % Plot each county on its own Y value to be able to see patterns by moving around
    % (Data is pretty noisy so it'd be hard to smash it all into one 2d chart)
    plot3(TotalCases, i*ones(length(TotalCases), 1), NewCases, '-o', 'MarkerSize', 5);

    hold on
end
set(gca, 'xscale', 'log')
set(gca, 'zscale', 'log')
xlabel('Total Cases')
ylabel('County ID (Alphabetical Order of PA Counties)')
zlabel('New Cases')

% Currently a really jank way of looking up a value in question
% Basically click a point on the line you want to identify, call countyID() with the Y value for that line
countyID = @(y) char(T.Properties.VariableNames(y));
