fileAI = fopen('winrate_corrtestAI.txt', 'r');
fileTargetNN10 = fopen('targetNN/winrate_target10.txt', 'r');

formatSpec = '%d %f';
sizeA = [2 Inf];

AI = fscanf(fileAI, formatSpec, sizeA);
TargetNN10 = fscanf(fileTargetNN10, formatSpec, sizeA);

xAI = AI(1,:);
xTargetNN10 = TargetNN10(1,:);

yAI = AI(2,:)*100;
yTargetNN10 = TargetNN10(2,:)*100;

plot(xAI, yAI, xTargetNN10, yTargetNN10);
xlabel("Trainingstijd [aantal iteraties]");
ylabel("Detective winstpercentage [%]");
legend("no experience replay", "with experience replay");
xlim([0 15000]);
ylim([0 100]);