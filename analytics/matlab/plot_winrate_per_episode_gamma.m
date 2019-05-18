gammas = [
    "045"
    "070"
    "085"
    "09"
    "095"
    "0975"
    "099"
];

formatSpec = '%d %f';
sizeA = [2 Inf];

for i=1:numel(gammas)
    
fileAI = fopen('gamma/winrate_gamma'+gammas(i)+'.txt', 'r');

AI = fscanf(fileAI, formatSpec, sizeA);

xAI = AI(1,:);
yAI = AI(2,:)*100;

plot(xAI, yAI);
hold on;

end

xlabel("Trainingstijd [aantal iteraties]");
ylabel("Detective winstpercentage [%]");
legend("\gamma = 0.45","\gamma = 0.70","\gamma = 0.85","\gamma = 0.90","\gamma = 0.95","\gamma = 0.975","\gamma = 0.99");
ylim([0 100]);