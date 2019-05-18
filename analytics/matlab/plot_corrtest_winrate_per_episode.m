fileAI = fopen('winrate_corrtestAI.txt', 'r');
fileRandom = fopen('winrate_corrtestRandom.txt', 'r');

formatSpec = '%d %f';
sizeA = [2 Inf];

AI = fscanf(fileAI, formatSpec, sizeA);
Random = fscanf(fileRandom, formatSpec, sizeA);

xAI = AI(1,:);
xRandom = Random(1,:);

yAI = AI(2,:)*100;
yRandom = Random(2,:)*100;

plot(xAI, yAI, xRandom, yRandom);
xlabel("Trainingstijd [aantal iteraties]");
ylabel("Detective winstpercentage [%]");
legend("vs. AI Mr. X", "vs. Random Mr. X");
ylim([0 100]);