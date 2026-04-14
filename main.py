from model.graph_model import nodes
from model.route_generator import generate_routes
from model.cost_model import assign_route_data, calculate_cost
from quantum.quantum_selector import run_quantum
from optimization.route_selector import select_best_route
from visualization.simulator import run_simulation

# Generate routes
routes = generate_routes(nodes)

# Assign data
routes_data = assign_route_data(routes, nodes)

# Calculate cost
for r in routes_data:
    routes_data[r]["cost"] = calculate_cost(routes_data[r])

# Quantum probabilities
probs = run_quantum()

# Select best route
best_route = select_best_route(routes_data, probs)

print("Best Route:", best_route)
print("Cost:", routes_data[best_route]["cost"])

route_path = best_route.split("-")

# Run visualization
run_simulation(nodes, route_path, routes_data[best_route]["cost"])