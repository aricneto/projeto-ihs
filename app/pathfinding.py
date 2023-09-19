import heapq

from utils import BLOCKING_TILES, DOOR_TILE, WALL_TILE
# A* adapted from: https://saturncloud.io/blog/implementing-the-a-algorithm-in-python-a-stepbystep-guide/

class Node:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent
        self.cost = 0
        self.h = 0

    # comparison magic: defines < for priority queue
    def __lt__(self, other):
        return (self.cost + self.h) < (other.cost + other.h)

def heuristic(node, goal):
    # manhattan distance
    return abs(node.x - goal.x) + abs(node.y - goal.y)

def find_path(start_x, start_y, goal_x, goal_y, map_data):
    open_list = []
    closed_set = set()

    start_node = Node(start_x, start_y)
    goal_node = Node(goal_x, goal_y)

    heapq.heappush(open_list, start_node)

    while open_list: # while there are still open nodes
        current_node = heapq.heappop(open_list)

        if current_node.x == goal_x and current_node.y == goal_y:
            # goal reached, return reverse path
            path = []
            while current_node:
                path.append((current_node.x, current_node.y))
                current_node = current_node.parent
            return path[::-1]  

        closed_set.add((current_node.x, current_node.y)) # explored nodes

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_x = current_node.x + dx
            new_y = current_node.y + dy

            if (
                0 <= new_x < len(map_data[0]) # check if inside map
                and 0 <= new_y < len(map_data)
                and map_data[new_y][new_x] not in BLOCKING_TILES # check if wall
                and (new_x, new_y) not in closed_set
            ):
                new_node = Node(new_x, new_y, current_node)
                new_node.cost = current_node.cost + 1
                new_node.h = heuristic(new_node, goal_node)
                heapq.heappush(open_list, new_node)

    return None  # No path found
