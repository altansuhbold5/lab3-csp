import networkx as nx
import matplotlib.pyplot as plt

def is_valid_coloring(graph, coloring):
    for u, v in graph.edges():
        if u in coloring and v in coloring:
            if coloring[u] == coloring[v]:
                return False
    return True

def get_available_colors(graph, node, coloring, colors):
    used = set()

    for neighbor in graph.neighbors(node):
        if neighbor in coloring:
            used.add(coloring[neighbor])

    return [color for color in colors if color not in used]

def select_node(graph, coloring):
    order = ["WA", "NT", "SA", "Q", "NSW", "V", "T"]

    for node in order:
        if node not in coloring:
            return node

def backtracking(graph, coloring, colors):
    if len(coloring) == len(graph.nodes()):
        return coloring.copy()

    node = select_node(graph, coloring)
    available_colors = get_available_colors(
        graph, node, coloring, colors
    )

    for color in available_colors:
        coloring[node] = color

        if is_valid_coloring(graph, coloring):
            result = backtracking(graph, coloring, colors)

            if result:
                return result

        del coloring[node]

    return None


G = nx.Graph()

G.add_edges_from([
    ("WA", "NT"),
    ("WA", "SA"),
    ("NT", "SA"),
    ("NT", "Q"),
    ("SA", "Q"),
    ("SA", "NSW"),
    ("SA", "V"),
    ("Q", "NSW"),
    ("NSW", "V")
])

G.add_node("T")

colors = ["red", "green", "blue"]

coloring_result = backtracking(G, {}, colors)

print("Coloring:")

for node in ["WA", "NT", "SA", "Q", "NSW", "V", "T"]:
    print(node, ":", coloring_result[node])

print("Valid:", is_valid_coloring(G, coloring_result))

color_map = [
    coloring_result[node]
    for node in G.nodes()
]

pos = {
    "WA": (0, 1),
    "NT": (1, 2),
    "Q": (2, 2),
    "SA": (1, 1),
    "NSW": (2, 1),
    "V": (2, 0),
    "T": (3, 0)
}

nx.draw(
    G,
    pos,
    node_color=color_map,
    with_labels=True,
    font_weight="bold"
)

plt.show()