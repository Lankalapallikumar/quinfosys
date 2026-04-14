import pygame
import sys
import math
import random
from itertools import permutations
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer

# -----------------------------
# NODES (Cities)
# -----------------------------
nodes = {
    "A": (100, 300),
    "B": (300, 100),
    "C": (500, 300),
    "D": (300, 500),
    "E": (700, 200)
}

node_list = list(nodes.keys())

# -----------------------------
# GENERATE ROUTES DYNAMICALLY
# -----------------------------
start = "A"
end = "D"

all_routes = []

for perm in permutations(node_list):
    if perm[0] == start and perm[-1] == end:
        route = list(perm)
        all_routes.append(route)

# limit routes (for demo)
all_routes = all_routes[:6]

# -----------------------------
# ASSIGN DATA (distance, traffic, weather)
# -----------------------------
routes_data = {}

def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

for route in all_routes:
    dist = 0
    traffic = random.randint(2, 6)
    weather = random.randint(1, 4)

    for i in range(len(route)-1):
        dist += distance(nodes[route[i]], nodes[route[i+1]])

    routes_data["-".join(route)] = {
        "distance": round(dist, 2),
        "traffic": traffic,
        "weather": weather
    }

# -----------------------------
# COST FUNCTION
# -----------------------------
def calculate_cost(data):
    return data["distance"] + (2 * data["traffic"]) + (1.5 * data["weather"])

for r in routes_data:
    routes_data[r]["cost"] = calculate_cost(routes_data[r])

# -----------------------------
# QUANTUM SIMULATION
# -----------------------------
def quantum_selector(n_routes):
    n_qubits = 3
    qc = QuantumCircuit(n_qubits, n_qubits)

    qc.h(range(n_qubits))
    qc.measure(range(n_qubits), range(n_qubits))

    simulator = Aer.get_backend('aer_simulator')
    compiled = transpile(qc, simulator)
    result = simulator.run(compiled, shots=1000).result()

    return result.get_counts()

# map quantum states to routes
def map_states_to_routes(routes, counts):
    route_keys = list(routes.keys())
    mapping = {}
    states = list(counts.keys())

    for i, state in enumerate(states):
        mapping[state] = route_keys[i % len(route_keys)]

    return mapping

# -----------------------------
# SELECT BEST ROUTE
# -----------------------------
quantum_counts = quantum_selector(len(routes_data))
mapping = map_states_to_routes(routes_data, quantum_counts)

best_route = None
best_score = float('inf')

for state, freq in quantum_counts.items():
    route = mapping[state]
    cost = routes_data[route]["cost"]

    score = cost - (freq / 1000)

    if score < best_score:
        best_score = score
        best_route = route

print("Quantum Output:", quantum_counts)
print("Best Route:", best_route)
print("Cost:", routes_data[best_route]["cost"])

route_path = best_route.split("-")

# -----------------------------
# PYGAME VISUALIZATION
# -----------------------------
pygame.init()
screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption("QuantumRoute AI")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
GRAY = (200, 200, 200)

font = pygame.font.Font(None, 24)

vehicle_pos = list(nodes[route_path[0]])
current_index = 1
current_target = nodes[route_path[current_index]]

clock = pygame.time.Clock()

def move_vehicle(pos, target):
    speed = 2
    dx = target[0] - pos[0]
    dy = target[1] - pos[1]
    dist = math.sqrt(dx**2 + dy**2)

    if dist > 1:
        pos[0] += speed * dx / dist
        pos[1] += speed * dy / dist
        return False
    return True

# -----------------------------
# GAME LOOP
# -----------------------------
running = True
while running:
    screen.fill(WHITE)

    # draw all edges
    for n1 in nodes:
        for n2 in nodes:
            if n1 != n2:
                pygame.draw.line(screen, GRAY, nodes[n1], nodes[n2], 1)

    # highlight best route
    for i in range(len(route_path)-1):
        pygame.draw.line(
            screen,
            BLUE,
            nodes[route_path[i]],
            nodes[route_path[i+1]],
            4
        )

    # draw nodes
    for node, pos in nodes.items():
        pygame.draw.circle(screen, BLACK, pos, 10)
        text = font.render(node, True, BLACK)
        screen.blit(text, (pos[0]+5, pos[1]-5))

    # show cost
    cost_text = font.render(f"Best Cost: {round(routes_data[best_route]['cost'],2)}", True, BLACK)
    screen.blit(cost_text, (20, 20))

    # move vehicle
    if current_target:
        reached = move_vehicle(vehicle_pos, current_target)

        if reached:
            current_index += 1
            if current_index < len(route_path):
                current_target = nodes[route_path[current_index]]
            else:
                current_target = None

    pygame.draw.circle(screen, RED, (int(vehicle_pos[0]), int(vehicle_pos[1])), 8)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
