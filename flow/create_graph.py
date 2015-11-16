
import utils
from graph_tool.all import *
import graph_tool.flow as gt
import pickle as pk


if __name__ == "__main__":
    positions = pk.load(open("county_locations.dict"))
    positions = sorted(positions.items(), key=lambda (k, v) : k)
    positions = map(lambda (k, v) : (v[1], v[0]), positions)

    names = utils.get_name_map("../mississippi_county.list")
    edges = utils.get_edges("../mississippi_graph_NS.csv", names)
    # edges += utils.get_edges("../mississippi_graph_EW.csv", names)

    g = Graph()
    g.set_directed(True)
    vertices = g.add_vertex(len(names))
    cap = g.new_edge_property("double")
    pos = g.new_vertex_property("vector<double>")

    for p in range(len(positions)):
        (x, y) = positions[p]
        pos[p] = [x, -y]

    for e in edges:
        edge = g.add_edge(e[0], e[1])
        cap[edge] = e[2]

    graph_draw(g, pos=pos, edge_pen_width=prop_to_size(cap, mi=1, ma=10, power=1),
            vertex_text=g.vertex_index,
            vertex_font_size=15, output="full_directed.pdf",
            fit_view=True, output_size=(800, 1200))

