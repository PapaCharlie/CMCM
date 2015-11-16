 M = csvread('wind_radii.csv');
 M = M(M(:,1) >= 64,:);
 x = M(:,1);
 y = M(:,2);
 scatter(x,y);
 hold on
 p = polyfit(x,y,1);
 bounds = [min(x),max(x)];
 plot(bounds, p(1)*bounds + p(2))