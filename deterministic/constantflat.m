populations % pops
adjacency % adj

% pops = [100; 10; 10];
% adj = [ 0, 0, 0; 0.1, 0, 0; 0, 0.1, 0; ];

orig_adj = adj;
for i=1:length(adj)
    adj(:,i) = adj(:,i) * 3000 / pops(i);
end

A = getA(adj);

curr_pop = pops;
interests = [];
max_t = 97;
for t=0:1:max_t
    for i=1:length(adj)
        adj(:,i) = orig_adj(:,i) * 3000 / max(0.01, curr_pop(i));
        s = sum(adj);
        if s(i) > 1
            adj(:,i) = adj(:, i) / s(i);
        end
    end
    A = getA(adj);
    interests = [interests; (curr_pop ./ pops)'];
    curr_pop = A * curr_pop;
end

figure
plot(interests(:,30))
