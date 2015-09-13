import netoworkx as nx


def graph_for_problem(name=None):
    """Formulate a problem as a networkx Graph with a goal nodes named 'goal' and start nodes named 'start'"""
    if name in (None, '') or name.lower().strip() in ('', 'null', 'none', 'empty'):
        G = nx.Graph(name=str(name))
        G.add_node(0, name='start')
        G.add_node(1, name='goal')
        G.add_edge(0, 1, action='move')
        return G
    name = str(name).lower().strip()
    if 'mission' in name or 'cani' in name:
        return G 


def search_strategy(frontier):
    """Return the next node in the frontier to explore"""
    return frontier[0]


def path_to_node(node):
    pass


G = graph_for_problem('null')


def plan_path_to_goal(G):
    """Return a list of edges in graph G that connect the node named 'start' to any node named 'goal'"""
    frontier = search_nodes(G.nodes(name='start'))
    node = select_next_node(frontier, strategy)
    if not frontier:
        return None
    if node.name == 'goal':
        return path_to_node(node)
    fringe += [node]

