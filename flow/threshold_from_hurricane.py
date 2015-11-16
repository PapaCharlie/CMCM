
from colornodes import *
from threshold import *

if __name__ == "__main__":
    clat = float(sys.argv[1])
    clong = float(sys.argv[2])
    rad = float(sys.argv[3])
    cat = int(sys.argv[4])

    th = compute_thresholds(clat, clong, rad, cat)
    create_graph_weights(th)
