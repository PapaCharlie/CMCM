function A = getA(adj)
R = sum(adj);
A = adj;
for i=1:length(A)
    A(i,i) = 1-R(i);
end

