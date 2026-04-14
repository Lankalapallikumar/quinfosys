import pygame
import sys
import math
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer

# -----------------------------
# NODES (Cities)
# -----------------------------
nodes = {
    "A": (100, 300),   # Start
    "B": (300, 100),
    "C": (500, 300),
    "D": (300, 500),
    "E": (700, 200)
}

# -----------------------------
# ROUTES (Multiple possibilities)
# -----------------------------
routes = {
    "A-B-C-D": {"distance": 18, "traffic": 6, "weather": 2},
    "A-C-E-D": {"distance": 20, "traffic": 3, "weather": 1},
    "A-B-E-D": {"distance": 22, "traffic": 4, "weather": 2},
    "A-D-C-B": {"distance": 19, "traffic": 5, "weather": 3}
}

# -----------------------------
# COST FUNCTION
# -----------------------------
def calculate_cost(route):
    return route["distance"] + (2 * route["traffic"]) + (1.5 * route["weather"])

for r in routes:
    routes[r]["cost"] = calculate_cost(routes[r])

# -----------------------------
# QUANTUM PART (3 QUBITS)
# -----------------------------
def quantum_route_selector():
    qc = QuantumCircuit(3, 3)

    qc.h([0, 1, 2])  # superposition
    qc.measure([0, 1, 2], [0, 1, 2])

    simulator = Aer.get_backend('aer_simulator')
    compiled = transpile(qc, simulator)
    result = simulator.run(compiled, shots=1000).result()

    return result.get_counts()

# Map quantum states → routes
routes_map = {
    "000": "A-B-C-D",
    "001": "A-C-E-D",
    "010": "A-B-E-D",
    "011": "A-D-C-B",
    "100": "A-B-C-D",
    "101": "A-C-E-D",
    "110": "A-B-E-D",
    "111": "A-D-C-B"
}

# -----------------------------
# SELECT BEST ROUTE
# -----------------------------
def select_best_route(routes, quantum_counts):
    best_route = None
    best_score = float('inf')

    for state, freq in quantum_counts.items():
        route = routes_map.get(state)

        if route in routes:
            cost = routes[route]["cost"]

            # combine cost + quantum probability
            score = cost - (freq / 1000)

            if score < best_score:
                best_score = score
                best_route = route

    return best_route

# -----------------------------
# VEHICLE MOVEMENT
# -----------------------------
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
# MAIN LOGIC
# -----------------------------
quantum_counts = quantum_route_selector()
best_route = select_best_route(routes, quantum_counts)

print("Quantum Output:", quantum_counts)
print("Best Route:", best_route)
print("Cost:", routes[best_route]["cost"])

route_path = best_route.split("-")

# -----------------------------
# PYGAME SETUP
# -----------------------------
pygame.init()
screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption("Quantum Delivery Optimization")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
GRAY = (200, 200, 200)

vehicle_pos = list(nodes[route_path[0]])
current_index = 1
current_target = nodes[route_path[current_index]]

clock = pygame.time.Clock()

# -----------------------------
# GAME LOOP
# -----------------------------
running = True
while running:
    screen.fill(WHITE)

    # Draw all edges
    for n1 in nodes:
        for n2 in nodes:
            if n1 != n2:
                pygame.draw.line(screen, GRAY, nodes[n1], nodes[n2], 1)

    # Highlight best route
    for i in range(len(route_path) - 1):
        pygame.draw.line(
            screen,
            BLUE,
            nodes[route_path[i]],
            nodes[route_path[i + 1]],
            4
        )

    # Draw nodes
    for node, pos in nodes.items():
        pygame.draw.circle(screen, BLACK, pos, 10)
        font = pygame.font.Font(None, 24)
        text = font.render(node, True, BLACK)
        screen.blit(text, (pos[0] + 5, pos[1] - 5))

    # Move vehicle
    if current_target:
        reached = move_vehicle(vehicle_pos, current_target)

        if reached:
            current_index += 1
            if current_index < len(route_path):
                current_target = nodes[route_path[current_index]]
            else:
                current_target = None

    # Draw vehicle
    pygame.draw.circle(screen, RED, (int(vehicle_pos[0]), int(vehicle_pos[1])), 8)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()