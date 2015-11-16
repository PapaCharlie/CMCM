
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

    g = Graph()
    g.set_directed(True)
    source = g.add_vertex()
    vertices = g.add_vertex(len(names))
    sink = g.add_vertex()
    cap = g.new_edge_property("double")
    pos = g.new_vertex_property("vector<double>")
    edge_cap_text = g.new_edge_property("string")

    pos[0] = [-90, -29.7]
    pos[len(positions) + 1] = [-90, -36]
    for p in range(len(positions)):
        (x, y) = positions[p]
        pos[p+1] = [x, -y]

    for e in edges:
        edge = g.add_edge(e[0]+1, e[1]+1)
        cap[edge] = e[2]
        edge_cap_text[edge] = str(e[2])

    bottom_states = [23, 24, 30, 46, 74, 57, 3, 79]
    top_states = [17, 47, 5, 70, 2, 71, 14, 72]
    for i in bottom_states:
        e = g.add_edge(0, i)
        cap[e] = 7

    for i in top_states:
        e = g.add_edge(i, len(names)+1)
        cap[e] = 7

    res = gt.boykov_kolmogorov_max_flow(g, source, sink, cap)
    part = gt.min_st_cut(g, source, cap, res)
    mc = sum([cap[e] - res[e] for e in g.edges() if part[e.source()] != part[e.target()]])
    res.a = cap.a - res.a  # the actual flow

    color = g.new_vertex_property("string")
    for i in range(len(names)+2):
        e = g.vertex(i)
        if part[e]:
            color[i] = 'b'
        else:
            color[i] = 'r'
    color[0] = 'black'
    color[len(names)+1] = 'black'

    graph_draw(g, pos=pos, edge_pen_width=prop_to_size(cap, mi=1, ma=10, power=1),
            vertex_fill_color=color, vertex_text=g.vertex_index,
            vertex_font_size=15, output="maxflow_directed.pdf",
            fit_view=True, output_size=(800, 1200))

    print mc
