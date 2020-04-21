clear
clc

T = readtable('./positives.csv', 'Delimiter', ',');

[r, c] = size(T);
TotalCases = zeros(r, 1);

disp(['n = ', string(r)])

for i=2:length(T.Properties.VariableNames)
    TotalCases = TotalCases + T.(char(T.Properties.VariableNames(i)));
end

NewCases = diff(TotalCases);

plot(TotalCases(2:end, 1), NewCases, '-')

set(gca, 'xscale', 'log')
set(gca, 'yscale', 'log')

xlabel('Total Cases')
ylabel('New Cases')
