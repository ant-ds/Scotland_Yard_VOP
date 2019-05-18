fileID = fopen('startPosWinrateRandom_full.txt', 'r');
fileSims = fopen('startpos_stats_simulation.txt', 'r');

formatSpec = '%d %f %f %f %f %f %f %f %f %f %f %f %f %f';
sizeA = [14 Inf];

A = fscanf(fileID, formatSpec, sizeA);
Sim = fscanf(fileSims, '%f %f %f %f %f %f %f %f %f %f %f %f %f', [13 Inf]);
% randomVRandom
% randomVGuil
% advVRandom
% advVGuil


x = A(1,:);

% get index for the 25k-th episode
start = 0;
sz = size(A);
sz = sz(2);
for i=1:sz
    if x(i) >= 25000
        start = i;
        break
    end
end
%

positions = [35 45 51 71 78 104 106 127 132 146 166 170 172];

sz = size(A);

% construct the matrix of y-values needed for the bar plot
% structure y = [...;...;...;...;...], one ';' per x
Y(1:numel(positions),1:3) = 0;
for i=1:numel(positions)
    Y(i,1) = mean(A(i+1,start:end)); % ML Det
    Y(i,2) = Sim(i,3); % Adv_Scoring Det
    Y(i,3) = Sim(i,1); % Random Det
end

bar(1:numel(positions), Y*100);

set(gca, 'XTick', 1:length(positions)); % Change x-axis ticks
set(gca, 'XTickLabel', positions); % Change x-axis ticks labels.
xtickangle(45);
ylim([0 100]);
ylabel("ML Detective winstpercentage [%]");
xlabel("Mr. X startpositie");
legend("ML detective", "AI detective", "Random detective");
