fileAI = fopen('winrate_7layermodelAI.txt', 'r');

formatSpec = '%d %f';
sizeA = [2 Inf];

AI = fscanf(fileAI, formatSpec, sizeA);

xAI = AI(1,:);

yAI = AI(2,:)*100;

plot(xAI, yAI);
xlabel("Trainingstijd [aantal iteraties]");
ylabel("Detective winstpercentage [%]");
ylim([0 100]);