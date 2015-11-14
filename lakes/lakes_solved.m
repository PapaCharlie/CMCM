% initial concentrations of chemicals in each lake
c0 = [1;0;1;0;0;0];
amplitude=1;

n = length(c0); %the number of lakes

% The volumes of lakes in km^3
V = [1,2,3,4,5,6];
r = diag(ones(1,n-1),-1);
r(1,n) = 1;
r = 1e-2 * r;

R = sum(r);

% Build the ODE matrix  
% (note: there are more efficient ways to do this, but this one is simple & readable)
A = r;
for i=1:n
    A(i,i) = - R(i);
    A(i,:) = A(i,:) / V(i);
end

t_star = 300;  %after how many days will we check the concentrations?


% specify some accuracy requirements for the ode solvers
odeopt = odeset('AbsTol', 1e-6, 'RelTol', 1e-12);

[t,cc]=ode45(@(t,c) (2+amplitude*sin(2*pi*t/100)) * A*c, [0:t_star], c0, odeopt);
plot(t,cc);
legend('Lake 1', 'Lake 2', 'Lake 3', 'Lake 4', 'Lake 5', 'Lake 6');
xlabel('t');
ylabel('c');

%let's experimentally test the linear superposition principle when 
%coefficients are time-dependent
cc_alternative=zeros(size(cc));
wvector = zeros(n,n);
for i=1:n
    %prepare the special initial conditions
    e = zeros(n,1);
    e(i) = 1;
    %find the corresponding solution
    [t,w]=ode45(@(t,c) (2+amplitude*sin(2*pi*t/100)) * A*c,[0:t_star], e, odeopt);
    % note that this w is what we called w^i in the lecture
    wvector(i,:) = w(end, :);
    cc_alternative = cc_alternative + c0(i)*w;
end
difference = norm(cc_alternative-cc);

f = [V]; 
Constraint = [-wvector(:,6)'; wvector(:,6)'; wvector(:,1)'; -wvector(:,1)'; wvector(:,2)'; -wvector(:,2)';...
    wvector(:,3)'; -wvector(:,3)'; wvector(:,4)'; -wvector(:,4)'; wvector(:,5)'; -wvector(:,5)'];
bounds = [-.4; .4; .4; -.3; .4; -.3; .4; -.3; .4; -.3; .4; -.3];
LB = [0 0 0 0 0 0];
[X, FVAL] = linprog(f,Constraint,bounds,[],[],LB)

%small difference ==> superposition works

