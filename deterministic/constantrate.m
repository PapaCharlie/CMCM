populations % pops
adjacency % adj
adj = 0.01 * adj;

% pops = [100; 10; 10];
% adj = [ 0, 0, 0; 0.1, 0, 0; 0, 0.1, 0; ];

R = sum(adj);

A = adj;
for i=1:length(A)
    A(i,i) = 1-R(i);
end

curr_pop = pops;
interest = [];
max_t = 3000;
for t=0:1:max_t
    interest = [interest curr_pop(5)];
    curr_pop = A * curr_pop;
end

figure
plot(interest)
