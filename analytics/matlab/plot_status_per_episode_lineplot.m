fileID = fopen('status_occurencesAI.txt', 'r');

formatSpec = '%d %f %f %f %f';
sizeA = [5 Inf];

data = fscanf(fileID, formatSpec, sizeA);
episodes = data(1,:);

statuses = [
    "Detective vangt Mr. X"
    "Mr. X is ingesloten"
    "Alle Detectives zijn verslagen"
    "Mr. X heeft overleefd"
    ];

colors = [
    "b"
    "r"
    "g"
    "y"
    ];

for i=1:4
    p = plot(episodes, data(i+1,:)*100);
    hold on;
end

legend(statuses);
ylim([0 100]);
xlabel("Trainingstijd [aantal iteraties]");
ylabel("Aandeel in voorkomen[%]");