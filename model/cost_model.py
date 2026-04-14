import math
import random

def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def assign_route_data(routes, nodes):
    routes_data = {}

    for route in routes:
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

    return routes_data

def calculate_cost(data):
    return data["distance"] + (2 * data["traffic"]) + (1.5 * data["weather"])