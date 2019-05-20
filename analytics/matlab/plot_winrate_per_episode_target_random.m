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
fileRandom = fopen('targetNN/winrateRandom_target'+targets(i)+'.txt', 'r');

Random = fscanf(fileRandom, formatSpec, sizeA);

xRandom = Random(1,:);
yRandom = Random(2,:)*100;

plot(xRandom, yRandom);
hold on;

end

xlabel("Trainingstijd [aantal iteraties]");
ylabel("Detective winstpercentage [%]");
legend("No", "10", "20", "50", "100");
ylim([0 100]);