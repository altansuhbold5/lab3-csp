import random
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


def select_node(graph, coloring, colors):
    uncolored = [node for node in graph.nodes() if node not in coloring]

    if not uncolored:
        return None

    return min(
        uncolored,
        key=lambda node: (
            len(get_available_colors(graph, node, coloring, colors)),
            -graph.degree(node)
        )
    )


def backtracking(graph, coloring, colors):
    if len(coloring) == len(graph.nodes()):
        return coloring

    node = select_node(graph, coloring, colors)

    available_colors = get_available_colors(
        graph, node, coloring, colors
    )

    for color in available_colors:
        coloring[node] = color

        result = backtracking(graph, coloring, colors)

        if result:
            return result

        del coloring[node]

    return None


n_nodes = 10

G = nx.Graph()
G.add_nodes_from(range(n_nodes))

for i in range(n_nodes):
    for j in range(i + 1, n_nodes):
        if random.random() < 0.5:
            G.add_edge(i, j)

colors = range(n_nodes)

coloring_result = backtracking(G, {}, colors)

print("Degree:", dict(G.degree()))
print("Coloring:", coloring_result)
print("Valid:", is_valid_coloring(G, coloring_result))
print("K:", len(set(coloring_result.values())))

color_map = [coloring_result[node] for node in G.nodes()]

nx.draw(
    G,
    node_color=color_map,
    with_labels=True,
    font_weight="bold"
)

plt.show()