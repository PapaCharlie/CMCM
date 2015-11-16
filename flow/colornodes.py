
import utils
from graph_tool.all import *
import graph_tool.flow as gt
import pickle as pk

def color_from_weight(w):
    w = min(1, w)
    color = [1-w, w, 0, 1]
    return color

def create_graph_weights(nodeweights, fname):
    positions = pk.load(open("county_locations.dict"))
    positions = sorted(positions.items(), key=lambda (k, v) : k)
    positions = map(lambda (k, v) : (v[1], v[0]), positions)

    names = utils.get_name_map("../mississippi_county.list")
    edges = utils.get_edges("../mississippi_graph_NS.csv", names)

    g = Graph()
    g.set_directed(True)
    vertices = g.add_vertex(len(names))
    cap = g.new_edge_property("double")
    pos = g.new_vertex_property("vector<double>")
    colors = g.new_vertex_property("vector<double>")

    for i in range(len(nodeweights)):
        colors[i] = color_from_weight(nodeweights[i])

    for p in range(len(positions)):
        (x, y) = positions[p]
        pos[p] = [x, -y]

    for e in edges:
        edge = g.add_edge(e[0], e[1])
        cap[edge] = e[2]

    graph_draw(g, pos=pos, edge_pen_width=prop_to_size(cap, mi=1, ma=10, power=1),
            vertex_fill_color=colors,
            vertex_text=g.vertex_index,
            vertex_font_size=15, output=fname,
            fit_view=True, output_size=(800, 1200))

