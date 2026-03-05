# Uninformed Search Strategies — Terminal Implementation

Artificial Intelligence course demonstration. - Individual Assignment
BFS, DFS, and their variants applied to four classical AI problems.

---

## Members

| Name | Roll Number |
|---|---|
| Kamal Kumar Nampally | SE24UCSE110 |

---

## Concept

### Uninformed (Blind) Search

Uninformed search strategies have no additional information about states beyond the problem definition. They cannot estimate how far they are from the goal. They explore the state space purely through expansion — generating children, checking for goals, and managing frontiers.

This implementation covers six strategies across two families:

```
BFS Family (breadth-based)          DFS Family (depth-based)
──────────────────────────          ──────────────────────────
BFS   Breadth-First Search          DFS   Depth-First Search
UCS   Uniform-Cost Search           DLS   Depth-Limited Search
BDS   Bidirectional Search          IDDFS Iterative Deepening DFS
```

---

## Strategies

### 1. BFS — Breadth-First Search

Explores all nodes at depth d before any node at depth d+1. Uses a FIFO queue.

- **Complete**: Yes (finds a solution if one exists)
- **Optimal**: Yes (unit step costs)
- **Time**: O(b^d)
- **Space**: O(b^d) — keeps all nodes in memory

### 2. DFS — Depth-First Search

Explores as deep as possible before backtracking. Uses a LIFO stack.

- **Complete**: Only on finite, acyclic graphs
- **Optimal**: No
- **Time**: O(b^m)
- **Space**: O(b·m) — only stores current path

### 3. DLS — Depth-Limited Search *(DFS variant)*

DFS with a hard depth cutoff L. Returns CUTOFF if no solution found within L.

- **Complete**: Only if solution exists within depth L
- **Optimal**: No
- **Time**: O(b^L)
- **Space**: O(b·L)

### 4. IDDFS — Iterative Deepening DFS *(DFS variant)*

Runs DLS repeatedly with increasing limits (0, 1, 2, …). Combines DFS space efficiency with BFS completeness.

- **Complete**: Yes
- **Optimal**: Yes (unit costs)
- **Time**: O(b^d) — repeated work is asymptotically insignificant
- **Space**: O(b·d)

### 5. UCS — Uniform-Cost Search *(BFS variant)*

Expands the node with the lowest cumulative path cost. Uses a priority queue. Equivalent to BFS when all step costs are equal.

- **Complete**: Yes (non-negative costs)
- **Optimal**: Yes
- **Time**: O(b^(1 + ⌊C*/ε⌋))
- **Space**: O(b^(1 + ⌊C*/ε⌋))

### 6. BDS — Bidirectional Search *(BFS variant)*

Runs two simultaneous BFS — forward from the initial state and backward from the goal — stopping when the frontiers meet.

- **Complete**: Yes
- **Optimal**: Yes (unit costs, when supported)
- **Time**: O(b^(d/2))
- **Space**: O(b^(d/2))
- **Note**: Falls back to BFS if the problem does not expose a concrete goal state

---

## Architecture

```
+------------------------------------------------------------------+
|                        SEARCH ENGINE                             |
|                                                                  |
|   Problem (abstract)                                             |
|     initial_state()  goal_test()  actions()  result()           |
|         |                                                        |
|         v                                                        |
|   Node                                                           |
|     state  parent  action  depth  cost                          |
|     path_states()   path_actions()                              |
|         |                                                        |
|         v                                                        |
|   Strategy                                                       |
|     BFS → deque (FIFO)                                           |
|     DFS → list  (LIFO stack)                                    |
|     DLS → recursive DFS with depth counter                      |
|     IDDFS → DLS with increasing limit                           |
|     UCS → heapq (priority by cost)                              |
|     BDS → two deques, forward + backward                        |
|         |                                                        |
|         v                                                        |
|   Metrics                                                        |
|     nodes_expanded  nodes_generated  max_frontier               |
|     solution_depth  solution_cost    elapsed_ms                  |
+------------------------------------------------------------------+

+------------------------------------------------------------------+
|                         PROBLEMS                                 |
|                                                                  |
|   WaterJugProblem          MissionariesProblem                   |
|   EightQueensProblem       TicTacToeProblem                      |
|                                                                  |
|   All implement Problem interface:                               |
|     initial_state() → start state                                |
|     goal_test(s)    → bool                                       |
|     actions(s)      → list of valid actions                      |
|     result(s,a)     → new state                                  |
|     step_cost(s,a)  → float (default 1)                         |
+------------------------------------------------------------------+
```

---

## Project Structure

```
uninformed-search/
|
+-- main.py                     Entry point, menus, solution display
|
+-- engine/
|   +-- node.py                 Search node: state, parent, depth, cost
|   +-- problem.py              Abstract Problem base class
|   +-- metrics.py              Performance data collection
|   +-- strategies.py           All 6 strategies (BFS/DFS/DLS/IDDFS/UCS/BDS)
|
+-- problems/
|   +-- water_jug.py            Water Jug problem (4L + 3L, goal 2L)
|   +-- missionaries.py         Missionaries and Cannibals
|   +-- eight_queens.py         Eight Queens (N=8)
|   +-- tic_tac_toe.py          Tic-Tac-Toe (X wins from empty board)
|
+-- compare/
|   +-- table.py                Terminal comparison table + winner analysis
```

---

## Problems

### 1. Water Jug Problem

Two jugs (4L and 3L) with no measuring marks. Goal: measure exactly 2L.

**State**: `(a, b)` — current fill of each jug
**Actions**: fill, empty, pour A→B, pour B→A
**Goal**: 2 appears in either jug

BFS finds the optimal 4-step path. DFS may take a longer route.

```
Initial:  Jug A [░░░░] 0/4L   Jug B [░░░] 0/3L
Step 1:   Fill A             → (4, 0)
Step 2:   Pour A → B         → (1, 3)
Step 3:   Empty B            → (1, 0)
Step 4:   Pour A → B         → (0, 1)   ← 2 not reached this path
          ...
Goal:     Jug B holds 2L ✔
```

### 2. Missionaries and Cannibals

3 missionaries + 3 cannibals must cross a river. Boat holds 1–2 people. Cannibals must never outnumber missionaries on either bank.

**State**: `(m_left, c_left, boat_side)`
**Actions**: move 1M, 1C, 1M+1C, 2M, or 2C across
**Goal**: `(0, 0, R)` — everyone on the right bank

The optimal solution has 11 moves. BFS and IDDFS both find it.

### 3. Eight Queens

Place 8 queens on an 8×8 chessboard so no two queens attack each other (no shared row, column, or diagonal).

**State**: tuple of length 0–8, `state[col] = row`
**Actions**: valid row placements for the next column
**Goal**: 8 queens placed with no conflicts

DFS finds a solution extremely fast (114 node expansions). BFS is prohibitively expensive and is noted in the comparison.

One solution: `Q at (A1, B5, C8, D6, E3, F7, G2, H4)`

### 4. Tic-Tac-Toe

Search for a sequence of moves where X wins from an empty board, with O playing optimally in response.

**State**: 9-tuple of `' '`, `'X'`, `'O'`
**Actions**: empty cell indices
**Goal**: X has three in a row

BFS finds the shortest (depth-5) X-win. DFS finds any win very quickly.

---

## Performance Summary (representative results)

### Water Jug

| Strategy | Found | Depth | Expanded | Time (ms) |
|---|---|---|---|---|
| BFS | Yes | 4 | 8 | ~0.1 |
| DFS | Yes | 6 | 7 | ~0.1 |
| DLS | Yes | 6 | 6 | ~0.1 |
| IDDFS | Yes | 4 | 25 | ~0.2 |
| UCS | Yes | 4 | 11 | ~0.1 |
| BDS | Yes | 2 | 2 | ~0.1 |

### Missionaries and Cannibals

| Strategy | Found | Depth | Expanded | Time (ms) |
|---|---|---|---|---|
| BFS | Yes | 11 | 13 | ~0.2 |
| DFS | Yes | 11 | 14 | ~0.2 |
| IDDFS | Yes | 11 | 136 | ~1.0 |
| UCS | Yes | 11 | 15 | ~0.3 |

### Eight Queens

| Strategy | Found | Depth | Expanded |
|---|---|---|---|
| DFS | Yes | 8 | 114 |
| DLS(L=8) | Yes | 8 | 113 |
| IDDFS | Yes | 8 | 3656 |
| BFS | Very slow | — | — |

### Tic-Tac-Toe

| Strategy | Found | Depth | Expanded |
|---|---|---|---|
| BFS | Yes | 5 | 341 |
| DFS | Yes | 7 | 8 |
| DLS(L=9) | Yes | 7 | 7 |

---

## Setup

No external libraries required. Pure Python standard library.

```bash
python main.py
```

### Step 1 — Clone the repository

```bash
git clone https://github.com/enkamal7/uninformed-search.git
cd uninformed-search
```

### Step 2 — Usage

```
MAIN MENU
  [1]  Water Jug Problem
  [2]  Missionaries & Cannibals
  [3]  Eight Queens
  [4]  Tic-Tac-Toe
  [5]  Compare All Problems
  [Q]  Quit
```

Each option runs all six strategies on the selected problem, prints a comparison table, and shows the solution path.

Option 5 runs all strategies on all four problems for a comprehensive cross-problem comparison.

---

## Key Observations

**BFS** is optimal and complete but stores exponentially many nodes. Best for small search spaces where the shortest path matters.

**DFS** uses minimal memory (only the current path). Best when any solution is acceptable and the search space is deep (e.g., Eight Queens).

**DLS** is useful when the solution depth is approximately known in advance. Avoids wasted exploration beyond the limit.

**IDDFS** is the preferred general-purpose uninformed strategy — space-efficient like DFS, optimal like BFS. The repeated work (re-expanding shallow nodes) is asymptotically negligible.

**UCS** generalises BFS to non-uniform costs. Identical to BFS on unit-cost problems; essential when step costs vary.

**BDS** is the most efficient when applicable, halving the effective search depth. Requires a concrete, reachable goal state and reverse operators.

---

## Extending the Project

**Add a new problem:**
```
1. Create a file in problems/
2. Inherit from engine.problem.Problem
3. Implement: initial_state, goal_test, actions, result
4. Add it to the menu in main.py
```

**Add a new strategy:**
```
1. Add a function to engine/strategies.py
2. Return (node_or_None, Metrics)
3. Register it in the STRATEGIES dict at the bottom
4. Add it to the runs list in run_all_strategies() in main.py
```

---

## References

- Russell, S. & Norvig, P. *Artificial Intelligence: A Modern Approach*, 4th Ed. Chapter 3: Solving Problems by Searching.
- Korf, R. E. (1985). Depth-first iterative-deepening: An optimal admissible tree search. *Artificial Intelligence*, 27(1), 97–109.
- von Ahn, L. et al. CAPTCHA: Using Hard AI Problems for Security. (background on problem difficulty)
