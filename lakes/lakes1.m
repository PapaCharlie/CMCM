% The chemical dissolving in interconnected "lakes" problem.
%
% Our basic assumption is that the volume of each "lake" 
% stays constant.  Can you re-write the system of ODEs to
% handle the more general case?


%initial concentrations of chemicals in each lake
c0 = [1;0;1;0;0;0];
%c0 = [3;0;0;0;1;0];
%c0 = [2;0;0;0;1;0];


n = length(c0); %the number of lakes

% The volumes of lakes in km^3
V = ones(1,n+1);
V(n+1) = 1e8;

% The mutal flow rates matrix
% r(i,j) = # of (km^3) of water passing from lake j to lake i per day.
%
% Note: all entries are non-negative (the direction of flow is specified).
% A zero entry means no channel.  If both r(i,j) and r(j,i) are non-zero,
% this means that there are two separate uni-directional channels: 
% from i to j and from j to i.

% The loop of channels. 
% Lake 1 feeds into Lake 2, which feeds into Lake 3, etc...
r = diag(ones(1,n-1),-1);
r(1,n) = 1;
r = 1e-2 * r;
r = [r zeros(6,1); zeros(1,7)];
r(n+1,1) = 0.005;
r(1,n+1) = 0.005;

R = sum(r);

%Build the ODE matrix  
%(note: there are more efficient ways to do this, but this one is simple & readable)
A = r;
for i=1:n+1
    A(i,i) = - R(i);
    A(i,:) = A(i,:) / V(i);
end

t_star = 1000;  %after how many days will we check the concentrations?


%The ODE system is c'(t) = A c(t)

cc=[];  %the history of concentrations
opttime = 0;
for t=0:t_star
    B = expm(t*A);
    c = B * [c0; 0];
    %Note: for every i, the i-th column of B can be interpreted as c(t) 
    %corresponding to a very special initial condition: 
    %concentration 1 in the i-th lake & concentration 0 everywhere else.
    %In fact, c=B*c0 is the "linear superposition principle" at work!
    
    cc= [cc c];
    m = max(c(1:n));
    if m <= 0.2 && opttime == 0
        opttime = t;
    end
end

close all;
hold on;
plot(cc');
legend('Lake 1', 'Lake 2', 'Lake 3', 'Lake 4', 'Lake 5', 'Lake 6');
xlabel('t');
ylabel('c');
