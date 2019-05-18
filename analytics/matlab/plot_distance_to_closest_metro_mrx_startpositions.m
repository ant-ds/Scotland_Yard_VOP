file = fopen('distance_to_metro_startpositions.txt', 'r');

positions = [35 45 51 71 78 104 106 127 132 146 166 170 172];

formatSpec = '%d %d';
sizeA = [2 Inf];

data = fscanf(file, formatSpec, sizeA);

x = data(1,:);
y = data(2,:);

sz = size(x);

for i=1:sz(2)
    bar(i, y(i));
    hold on;
end
set(gca, 'XTick', 1:length(positions)); % Change x-axis ticks
set(gca, 'XTickLabel', positions); % Change x-axis ticks labels.
xtickangle(45);
set(gca, 'YTick', 1:5);
ylim([0 5]);
ylabel("Afstand [aantal verbindingen]");
xlabel("Mr. X startposities");