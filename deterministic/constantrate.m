populations % pops
adjacency % adj

% pops = [100; 10; 10];
% adj = [ 0, 0, 0; 0.1, 0, 0; 0, 0.1, 0; ];

for i=1:length(adj)
    adj(:,i) = adj(:,i) * 3000 / pops(i);
    s = sum(adj);
    if s(i) > 0.95
        adj(:,i) = adj(:, i) * 0.95 / s(i);
    end
end
R = sum(adj);

A = adj;
for i=1:length(A)
    A(i,i) = 1-R(i);
end

curr_pop = pops;
interest = [];
max_t = 97;
for t=0:1:max_t
    interest = [interest; (curr_pop ./ pops)'];
    curr_pop = A * curr_pop;
end

figure
plot(interest(:,40))
