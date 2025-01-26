import heapq
import logging

def a_star(map, start, goal):
    open_list = []
    heapq.heappush(open_list, (0, 0, start))
   
    came_from = {}
    g_costs = {start: 0}
   
    while open_list:
        _, g, current = heapq.heappop(open_list)
       
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]
        
        for dx, dy in directions:
            nx, ny = current[0] + dx, current[1] + dy
            if est_valide(map.map, nx, ny):
                new_g = g + (1.414 if dx != 0 and dy != 0 else 1)  # Diagonal movement costs more
                if (nx, ny) not in g_costs or new_g < g_costs[(nx, ny)]:
                    g_costs[(nx, ny)] = new_g
                    f = new_g + heuristique((nx, ny), goal)
                    heapq.heappush(open_list, (f, new_g, (nx, ny)))
                    came_from[(nx, ny)] = current
    
    logging.error("Aucun chemin trouvé")
    return None

def heuristique(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def est_valide(map, x, y):
    return 0 <= x < len(map) and 0 <= y < len(map[0]) and map[x][y] == " "

directions = [
    (0, 1), (1, 0), (0, -1), (-1, 0),  # Orthogonal directions
    (1, 1), (1, -1), (-1, 1), (-1, -1)  # Diagonal directions
]