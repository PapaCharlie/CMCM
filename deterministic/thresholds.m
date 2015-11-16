function th = thresholds(lat, long, rad, cat)
cmd = sprintf('python threshold.py %f %f %d %d', lat, long, rad, cat);
[status, cmdout] = system(cmd);
th = eval(cmdout);
