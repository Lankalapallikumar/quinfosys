def map_states(routes, probs):
    route_keys = list(routes.keys())
    mapping = {}

    for i, state in enumerate(probs.keys()):
        mapping[state] = route_keys[i % len(route_keys)]

    return mapping

def select_best_route(routes_data, probs):
    mapping = map_states(routes_data, probs)

    best_route = None
    best_score = float('inf')

    for state, prob in probs.items():
        route = mapping[state]
        cost = routes_data[route]["cost"]

        score = cost - prob

        if score < best_score:
            best_score = score
            best_route = route

    return best_route