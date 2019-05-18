fileAI = fopen('startPosWinrate_full.txt', 'r');
fileRandom = fopen('startPosWinrateRandom_full.txt', 'r');
fileDist = fopen('distance_to_metro_startpositions.txt', 'r');

formatSpec = '%d %f %f %f %f %f %f %f %f %f %f %f %f %f';
sizeA = [14 Inf];

AI = fscanf(fileAI, formatSpec, sizeA);
Random = fscanf(fileRandom, formatSpec, sizeA);
Dist = fscanf(fileDist, '%d %d', [2 Inf]);
xAI = AI(1,:);
xRandom = AI(1,:);

% get index for the 25k-th episode
startAI = 0;
sz = size(AI);
sz = sz(2);
for i=1:sz
    if xAI(i) >= 25000
        startAI = i;
        break
    end
end

startRandom = 0;
sz = size(Random);
sz = sz(2);
for i=1:sz
    if xRandom(i) >= 25000
        startRandom = i;
        break
    end
end
%

positions = [35 45 51 71 78 104 106 127 132 146 166 170 172];

szAI = size(AI);
szRandom = size(Random);

for i=1:numel(positions)
    scatter(Dist(2,i), (mean(Random(i+1,startRandom:szRandom(2))) - mean(AI(i+1,startAI:szAI(2))))*100, 100, 'filled');
    hold on;
end
ylim([0 35]);
ylabel("\Delta_{win%} [%]");
xlabel("Afstand tot dichtste metrostation");