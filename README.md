# A* vs Dijkstra Pathfinding Visualizer

A Python and pygame visualization that compares the A* and Dijkstra pathfinding algorithms on a randomly generated 200x200 terrain grid. Both algorithms search for the lowest-cost path from the bottom-left corner to the top-right corner, moving through terrain of varying difficulty.

---

## Features

- Side-by-side comparison of A* (red) and Dijkstra (blue) on the same map
- Random 200x200 terrain grid with four terrain types of different movement costs
- Real-time visualization with auto-zoom that follows both characters during pathfinding
- Sidebar with live stats: steps, path cost, terrain usage, and execution time for each algorithm
- Start and Restart buttons

---

## How It Works

The board is a 200x200 grid where each cell has a terrain type assigned a movement cost. Both algorithms find the path with the lowest total cost from the starting position to the goal. The diagonal of the map is always set to grass (cost 1) to guarantee a path exists.

Each frame, both characters advance one step along their pre-calculated paths. Visited cells are highlighted with a semi-transparent overlay: red for A*, blue for Dijkstra.

**A*** uses a priority queue with a Manhattan distance heuristic to guide the search toward the goal, making it generally faster in practice.

**Dijkstra** explores nodes purely by accumulated cost with no heuristic, guaranteeing the optimal path but typically visiting more nodes.

---

## Terrain Types

| Terrain | Movement Cost |
|---------|:-------------:|
| Grass   | 1             |
| Sand    | 2             |
| Mud     | 3             |
| Rocks   | 4             |

---

## Project Structure

```
├── main.py        # Visualization, game loop, rendering, UI
├── engine.py      # BoardState class, A* and Dijkstra implementations
└── img/
    ├── grass.png
    ├── sand.png
    ├── mud.png
    ├── rocks.png
    ├── player.png
    ├── player2.png
    └── end.png
```

---

## Requirements

- Python 3.x
- Pygame

Install dependencies with:

```bash
pip install pygame
```

---

## Running

```bash
python main.py
```

Press **Start** to begin pathfinding. Press **Restart** to generate a new random map.

---

## Performance

Average execution time for each algorithm across 10 runs at different grid sizes:

| Grid Size | A* avg [s] | Dijkstra avg [s] |
|-----------|:----------:|:----------------:|
| 50x50     | 0.00300    | 0.00327          |
| 100x100   | 0.01173    | 0.01556          |
| 200x200   | 0.05304    | 0.06510          |
| 300x300   | 0.13800    | 0.15612          |

A* is consistently faster than Dijkstra due to the heuristic reducing the number of nodes explored, despite having a more complex implementation. Both algorithms typically find paths within 1-2 steps of each other, with the total path cost being the same in the majority of runs.

At grid sizes of 500x500 and above, both computation time and rendering performance degrade significantly.

---

## References

- [A* Search Algorithm](https://www.geeksforgeeks.org/a-search-algorithm/) - GeeksForGeeks, A* implementation
- [Dijkstra's Shortest Path Algorithm](https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-greedy-algo-7/) - GeeksForGeeks, Dijkstra implementation
- [Count Paths with Distance Equal to Manhattan Distance](https://www.geeksforgeeks.org/count-paths-with-distance-equal-to-manhattandistance/) - GeeksForGeeks, Manhattan heuristic
- [Manhattan Distance](https://www.datacamp.com/tutorial/manhattandistance) - DataCamp, Manhattan distance definition
