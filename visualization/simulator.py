import pygame
import math

def run_simulation(nodes, route_path, cost):
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

    running = True
    while running:
        screen.fill(WHITE)

        for n1 in nodes:
            for n2 in nodes:
                if n1 != n2:
                    pygame.draw.line(screen, GRAY, nodes[n1], nodes[n2], 1)

        for i in range(len(route_path)-1):
            pygame.draw.line(screen, BLUE,
                             nodes[route_path[i]],
                             nodes[route_path[i+1]], 4)

        for node, pos in nodes.items():
            pygame.draw.circle(screen, BLACK, pos, 10)
            text = font.render(node, True, BLACK)
            screen.blit(text, (pos[0]+5, pos[1]-5))

        cost_text = font.render(f"Cost: {round(cost,2)}", True, BLACK)
        screen.blit(cost_text, (20, 20))

        if current_target:
            reached = move_vehicle(vehicle_pos, current_target)
            if reached:
                current_index += 1
                if current_index < len(route_path):
                    current_target = nodes[route_path[current_index]]
                else:
                    current_target = None

        pygame.draw.circle(screen, RED,
                           (int(vehicle_pos[0]), int(vehicle_pos[1])), 8)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()
        clock.tick(60)

    pygame.quit()