function lakes_test
c0 = [1;0;1;0;0;0];
%c0 = [3;0;0;0;1;0];
%c0 = [2;0;0;0;1;0];

n = length(c0); %the number of lakes

% The volumes of lakes in km^3
V = ones(1,n);
V = [1, 2, 3, 4, 5, 6];

% The loop of channels. 
% Lake 1 feeds into Lake 2, which feeds into Lake 3, etc...
r = diag(ones(1,n-1),-1);
r(1,n) = 1;
r = 1e-2 * r;

R = sum(r);

%Build the ODE matrix  
%(note: there are more efficient ways to do this, but this one is simple & readable)
A = r;
for i=1:n
    A(i,i) = - R(i);
    A(i,:) = A(i,:) / V(i);
end

amplitude = 1;
t_star = 300;  %after how many days will we check the concentrations?

%specify some accuracy requirements for the ode solvers
odeopt = odeset('AbsTol', 1e-6, 'RelTol', 1e-12);
c_ode = @(t, c) (2+amplitude*sin(2*pi*t/100)) * A*c;

[t,cc] = ode45(c_ode, [0:t_star], c0, odeopt);
% close all;
plot(t,cc);
legend('Lake 1', 'Lake 2', 'Lake 3', 'Lake 4', 'Lake 5', 'Lake 6');
xlabel('t'); ylabel('c');

% let's experimentally test the linear superposition principle when 
% coefficients are time-dependent
cc_alternative=zeros(size(cc));
for i=1:n
    e = zeros(n,1);
    e(i) = 1;
    [t,w] = ode45(c_ode,[0:t_star], e, odeopt);

    cc_alternative = cc_alternative + c0(i)*w;
end
difference = norm(cc_alternative-cc)
% small difference ==> superposition works

