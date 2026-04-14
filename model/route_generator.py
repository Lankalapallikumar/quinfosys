from itertools import permutations

def generate_routes(nodes, start="A", end="D", limit=6):
    node_list = list(nodes.keys())
    routes = []

    for perm in permutations(node_list):
        if perm[0] == start and perm[-1] == end:
            routes.append(list(perm))

    return routes[:limit]