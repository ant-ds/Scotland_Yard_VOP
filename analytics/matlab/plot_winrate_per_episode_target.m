targets = [
    "No"
    "10"
    "20"
    "50"
    "100"
];

formatSpec = '%d %f';
sizeA = [2 Inf];

for i=1:numel(targets)
    
fileAI = fopen('targetNN/winrate_target'+targets(i)+'.txt', 'r');

AI = fscanf(fileAI, formatSpec, sizeA);

xAI = AI(1,:);
yAI = AI(2,:)*100;

plot(xAI, yAI);
hold on;

end

xlabel("Trainingstijd [aantal iteraties]");
ylabel("Detective winstpercentage [%]");
legend("No", "10", "20", "50", "100");
ylim([0 100]);