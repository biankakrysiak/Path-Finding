import numpy as np
import random
import heapq
import time

class BoardState():
    def __init__(self):
        self.DIMENSIONS = 200
        self.texture_difficulty = {
            1: 'grass',
            2: 'sand',
            3: 'mud',
            4: 'rocks'
        }
        self.texture_count = {
            1: 0,  # grass
            2: 0,  # sand
            3: 0,  # mud
            4: 0   # rocks
        }

        self.texture_count2 = {
            1: 0,  # grass
            2: 0,  # sand
            3: 0,  # mud
            4: 0   # rocks
        }

        self.board_difficulty = [[random.randint(1, 4) for _ in range(self.DIMENSIONS)] for _ in range(self.DIMENSIONS)]

        for i in range(self.DIMENSIONS):
            self.board_difficulty[i][i] = 1

        self.board = [[self.texture_difficulty[self.board_difficulty[r][c]] for c in range(self.DIMENSIONS)] for r in range(self.DIMENSIONS)]

        self.playerPos = (self.DIMENSIONS - 1, 0)
        self.playerPos2 = (self.DIMENSIONS - 1, 0)
        self.end = (0, self.DIMENSIONS - 1)
        self.moveLog = []
        self.moveLog2 = []

        self.astar_time = 0
        self.dijkstra_time = 0
        self.path = []
        self.path2 = []
        self.started = False

    def start_pathfinding(self):
        start_time = time.time()
        self.path = self.a_star()
        self.astar_time = time.time() - start_time

        start_time = time.time()
        self.path2 = self.dijkstra()
        self.dijkstra_time = time.time() - start_time
        self.started = True

    def get_neighbors(self, node):
        r, c = node
        directions = [(-1,0), (1,0), (0,-1), (0,1)]
        neighbors = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.DIMENSIONS and 0 <= nc < self.DIMENSIONS:
                neighbors.append((nr, nc))
        return neighbors

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def a_star(self):
        start = self.playerPos
        goal = self.end
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        while open_set:
            _, current = heapq.heappop(open_set)
            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            for neighbor in self.get_neighbors(current):
                r, c = neighbor
                move_cost = self.board_difficulty[r][c]
                tentative_g_score = g_score[current] + move_cost
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + 1.5*self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return []

    def dijkstra(self):
        start = self.playerPos2
        goal = self.end
        visited = set()
        distances = {start: 0}
        came_from = {}
        pq = [(0, start)]

        while pq:
            current_dist, current = heapq.heappop(pq)
            visited = set()
            ...
            if current in visited:
                continue
            visited.add(current)
            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            for neighbor in self.get_neighbors(current):
                r, c = neighbor
                cost = self.board_difficulty[r][c]
                new_dist = current_dist + cost
                if neighbor not in distances or new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    came_from[neighbor] = current
                    heapq.heappush(pq, (new_dist, neighbor))

        return []

    def stepTowardsEnd(self):
        if self.path:
            next_step = self.path.pop(0)
            self.moveLog.append(self.playerPos)
            self.playerPos = next_step
            r, c = self.playerPos
            texture = self.board_difficulty[r][c]
            if texture in self.texture_count:
                self.texture_count[texture] += 1

    def stepTowardsEnd2(self):
        if self.path2:
            next_step2 = self.path2.pop(0)
            self.moveLog2.append(self.playerPos2)
            self.playerPos2 = next_step2
            r, c = self.playerPos2
            texture = self.board_difficulty[r][c]
            if texture in self.texture_count2:
                self.texture_count2[texture] += 1

    def getScore(self):
        return sum(self.board_difficulty[r][c] for r, c in self.moveLog)