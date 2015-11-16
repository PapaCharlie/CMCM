addpath('predictions');

pred_hancock;
fig = figure;
m(9:end,7) = 0;
m(10:2:38,1) = m(10:2:38,1) + sum(m([9 11], 1))/2 - m(10,1);
m(40:end,1) = 0;
plot(m, 'LineWidth', 2);
legend Forrest George Greene Hancock Harrison Jackson Lamar Marion PearlRiver Perry Stone;
xlabel Hours;
ylabel 'County Population';
ylim([0 2*1e5]);
xlim([0 50]);
gca.XTick = 0:5:50;
saveas(fig, 'predictions/pred_hancock.pdf');

pred_jackson;
fig = figure;
plot(m, 'LineWidth', 2);
legend George Greene Hancock Harrison Jackson Stone;
xlabel Hours;
ylabel 'County Population';
ylim([0 2*1e5]);
xlim([0 50]);
gca.XTick = 0:5:50;
saveas(fig, 'predictions/pred_jackson.pdf');