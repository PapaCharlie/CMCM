populations % pops
adjacency % adj

% percentage of people we allow in the county
% ths = thresholds(31.8,-91.0,43.0,1);
% ths = thresholds(30.4,-88.8,51.0,1);
% ths = thresholds(30.3,-88.4,43.0,1);
% ths = thresholds(30.8,-88.6,56.0,1);
% ths = thresholds(30.8,-88.5,69.0,2);
% ths = thresholds(30.1,-89.4,64.0,2);
% ths = thresholds(30.3,-88.9,69.0,2);
% ths = thresholds(30.2,-88.6,69.0,2);
% ths = thresholds(30.4,-88.9,64.0,2);
% ths = thresholds(30.4,-89.2,73.0,3);
% ths = thresholds(30.2,-89.6,78.0,3);
% ths = thresholds(30.2,-88.6,73.0,3);
% ths = thresholds(30.2,-89.4,73.0,3);
% ths = thresholds(30.5,-88.9,73.0,3);
ths = thresholds(30.3,-89.4,117.,5);

for i=1:length(adj)
    adj(:,i) = adj(:,i) * 3000 / pops(i);
    s = sum(adj);
    if s(i) > 0.95
        adj(:,i) = adj(:, i) * 0.95 / s(i);
    end
end
R = sum(adj);

A = getA(adj);

curr_pop = pops;
interests = [];
max_t = 24*5;
for t=1:1:max_t
    curr_pop = A * curr_pop;
    % percentage of people still in counties
    percs = (curr_pop ./ pops);
    percs = percs - ths;
    count = 0;
    for i=1:length(percs)
        if percs(i) > 0
            count = count + 1;
        end
    end
    interests = [interests count];
    if count == 0 % All counties are all good
        t
        break;
    end
end

figure
plot(interests)
