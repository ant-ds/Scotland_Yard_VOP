formatSpec = '%d %f %f %f %f';
sizeA = [5 Inf];

fileAI = fopen('avg_game_length_AI.txt', 'r');
fileRandom = fopen('avg_game_length_Random.txt', 'r');
fileWeightsAI = fopen('status_occurencesAI.txt', 'r');
fileWeightsRandom = fopen('status_occurencesRandom.txt', 'r');

AI = fscanf(fileAI, formatSpec, sizeA);
Random = fscanf(fileRandom, formatSpec, sizeA);
weightsAI = fscanf(fileWeightsAI, formatSpec, sizeA);
weightsRandom = fscanf(fileWeightsRandom, formatSpec, sizeA);

xAI = AI(1,:);
yAI = AI(2,:).*weightsAI(2,:)+AI(3,:).*weightsAI(3,:)+AI(4,:).*weightsAI(4,:)+AI(5,:).*weightsAI(5,:); % calc average

xRandom = Random(1,:);
yRandom = Random(2,:).*weightsRandom(2,:)+Random(3,:).*weightsRandom(3,:)+Random(4,:).*weightsRandom(4,:)+Random(5,:).*weightsRandom(5,:); % calc average

plot(xAI, yAI, xRandom, yRandom);

xlabel("Trainingstijd [aantal iteraties]");
ylabel("Aantal beurten");
legend("vs. AI Mr. X", "vs. Random Mr. X");
ylim([0 22]);