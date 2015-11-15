
import utils
from graph_tool.all import *
import graph_tool.flow as gt

if __name__ == "__main__":
    names = utils.get_name_map("../mississippi_county.list")
    edges = utils.get_edges("../mississippi_graph_NS.csv", names)
    g = Graph()
    g.set_directed(True)
    source = g.add_vertex()
    vertices = g.add_vertex(len(names))
    sink = g.add_vertex()
    cap = g.new_edge_property("double")
    for e in edges:
        edge = g.add_edge(e[0]+1, e[1])
        cap[edge] = e[2]

    bottom_states = [23, 24, 30, 46, 74, 57, 3, 79]
    top_states = [17, 47, 5, 70, 2, 71]
    for i in bottom_states:
        e = g.add_edge(0, i)
        cap[e] = 10000

    for i in top_states:
        e = g.add_edge(i, len(names)+1)
        cap[e] = 10000

    res = gt.boykov_kolmogorov_max_flow(g, source, sink, cap)
    part = gt.min_st_cut(g, source, cap, res)
    mc = sum([cap[e] - res[e] for e in g.edges() if part[e.source()] != part[e.target()]])
    # mc, part = gt.min_cut(g, cap)
    print(mc)

    res.a = cap.a - res.a  # the actual flow
    gt.graph_draw(g, pos=pos, edge_pen_width=gt.prop_to_size(cap, mi=3, ma=10, power=1),
            edge_text=res, vertex_fill_color=part, vertex_text=g.vertex_index,
            vertex_font_size=18, edge_font_size=18, output="example-min-st-cut.pdf")
