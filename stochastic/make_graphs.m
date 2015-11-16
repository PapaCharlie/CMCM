addpath('predictions');

pred_hancock;
fig = figure;
plot(m, 'LineWidth', 2);
legend Forrest George Greene Hancock Harrison Jackson Lamar Marion PearlRiver Perry Stone;
xlabel Hours;
ylabel 'County Population';
saveas(fig, 'predictions/pred_hancock.pdf');

pred_jackson;
fig = figure;
plot(m, 'LineWidth', 2);
legend George Greene Hancock Harrison Jackson Stone;
xlabel Hours;
ylabel 'County Population';
saveas(fig, 'predictions/pred_jackson.pdf');