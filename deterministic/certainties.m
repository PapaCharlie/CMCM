populations % pops
adjacency % adj
thresholds % percentage of people we allow in the county

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
max_t = 96;
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
