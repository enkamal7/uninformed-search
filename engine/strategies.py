"""
engine/strategies.py

All six uninformed search strategies.

  1. BFS   — Breadth-First Search
  2. DFS   — Depth-First Search
  3. DLS   — Depth-Limited Search       (DFS variant)
  4. IDDFS — Iterative Deepening DFS    (DFS variant)
  5. UCS   — Uniform-Cost Search        (BFS variant — cost-aware)
  6. BDS   — Bidirectional Search       (BFS variant — two frontiers)

Each function signature:
    strategy(problem, **kwargs) -> (solution_node | None, Metrics)
"""

from __future__ import annotations

import heapq
from collections import deque
from typing import Optional, Tuple

from engine.node    import Node
from engine.problem import Problem
from engine.metrics import Metrics

# sentinel returned when DLS hits depth limit without finding goal
_CUTOFF = object()

# ── helper ────────────────────────────────────────────────────────────────────

def _expand(node: Node, problem: Problem, metrics: Metrics):
    """Yield child nodes and update generation counter."""
    for action in problem.actions(node.state):
        child_state = problem.result(node.state, action)
        child_cost  = node.cost + problem.step_cost(node.state, action)
        child = Node(child_state, node, action, child_cost)
        metrics.nodes_generated += 1
        metrics.max_depth = max(metrics.max_depth, child.depth)
        yield child


# ══════════════════════════════════════════════════════════════════════════════
# 1. BFS — Breadth-First Search
# ══════════════════════════════════════════════════════════════════════════════

def bfs(problem: Problem, **_) -> Tuple[Optional[Node], Metrics]:
    """
    Explores nodes level by level (FIFO queue).
    Complete and optimal (unit costs).
    Time & Space: O(b^d)
    """
    m = Metrics(strategy="BFS", problem=type(problem).__name__)
    m.start_timer()

    root = Node(problem.initial_state())
    if problem.goal_test(root.state):
        m.found = True; m.solution_depth = 0; m.solution_cost = 0
        m.stop_timer(); return root, m

    frontier = deque([root])
    explored = {root.state}

    while frontier:
        m.max_frontier = max(m.max_frontier, len(frontier))
        node = frontier.popleft()
        m.nodes_expanded += 1

        for child in _expand(node, problem, m):
            if child.state in explored:
                continue
            if problem.goal_test(child.state):
                m.found = True
                m.solution_depth = child.depth
                m.solution_cost  = child.cost
                m.stop_timer(); return child, m
            explored.add(child.state)
            frontier.append(child)

    m.stop_timer(); return None, m


# ══════════════════════════════════════════════════════════════════════════════
# 2. DFS — Depth-First Search
# ══════════════════════════════════════════════════════════════════════════════

def dfs(problem: Problem, max_depth: int = 500, **_) -> Tuple[Optional[Node], Metrics]:
    """
    Explores as deep as possible before backtracking (LIFO stack).
    Complete only on finite acyclic spaces.
    Time: O(b^m)  Space: O(b·m)
    """
    m = Metrics(strategy="DFS", problem=type(problem).__name__)
    m.start_timer()

    root = Node(problem.initial_state())
    frontier = [root]          # Python list as stack
    explored = set()

    while frontier:
        m.max_frontier = max(m.max_frontier, len(frontier))
        node = frontier.pop()

        if node.state in explored:
            continue
        explored.add(node.state)
        m.nodes_expanded += 1

        if problem.goal_test(node.state):
            m.found = True
            m.solution_depth = node.depth
            m.solution_cost  = node.cost
            m.stop_timer(); return node, m

        if node.depth < max_depth:
            for child in reversed(list(_expand(node, problem, m))):
                if child.state not in explored:
                    frontier.append(child)

    m.stop_timer(); return None, m


# ══════════════════════════════════════════════════════════════════════════════
# 3. DLS — Depth-Limited Search  (DFS variant)
# ══════════════════════════════════════════════════════════════════════════════

def dls(problem: Problem, limit: int = 10, **_) -> Tuple[Optional[Node], Metrics]:
    """
    DFS with a hard depth cutoff.
    Useful when solution depth is roughly known.
    Returns (None, metrics) if goal not found within limit.
    """
    m = Metrics(strategy=f"DLS(L={limit})", problem=type(problem).__name__)
    m.start_timer()

    result = _dls_recursive(Node(problem.initial_state()), problem, limit, set(), m)

    if isinstance(result, Node):
        m.found = True
        m.solution_depth = result.depth
        m.solution_cost  = result.cost
        m.stop_timer(); return result, m

    m.stop_timer(); return None, m


def _dls_recursive(node, problem, limit, visited, m):
    if problem.goal_test(node.state):
        return node
    if limit == 0:
        return _CUTOFF

    visited = visited | {node.state}
    m.nodes_expanded += 1
    cutoff_occurred = False

    for child in _expand(node, problem, m):
        if child.state in visited:
            continue
        result = _dls_recursive(child, problem, limit - 1, visited, m)
        if result is _CUTOFF:
            cutoff_occurred = True
        elif result is not None:
            return result

    return _CUTOFF if cutoff_occurred else None


# ══════════════════════════════════════════════════════════════════════════════
# 4. IDDFS — Iterative Deepening DFS  (DFS variant)
# ══════════════════════════════════════════════════════════════════════════════

def iddfs(problem: Problem, max_limit: int = 50, **_) -> Tuple[Optional[Node], Metrics]:
    """
    Runs DLS with increasing depth limits (0, 1, 2, …).
    Combines space efficiency of DFS with completeness of BFS.
    Optimal for unit costs.
    Time: O(b^d)  Space: O(b·d)
    """
    m = Metrics(strategy="IDDFS", problem=type(problem).__name__)
    m.start_timer()

    for depth in range(max_limit + 1):
        visited = set()
        result = _dls_recursive(Node(problem.initial_state()), problem, depth, visited, m)
        if result is not _CUTOFF and result is not None:
            m.found = True
            m.solution_depth = result.depth
            m.solution_cost  = result.cost
            m.stop_timer(); return result, m

    m.stop_timer(); return None, m


# ══════════════════════════════════════════════════════════════════════════════
# 5. UCS — Uniform-Cost Search  (BFS variant)
# ══════════════════════════════════════════════════════════════════════════════

def ucs(problem: Problem, **_) -> Tuple[Optional[Node], Metrics]:
    """
    Expands the node with lowest cumulative cost first (priority queue).
    Optimal for non-negative step costs.
    Equivalent to BFS when all costs are equal.
    Time & Space: O(b^(1 + C*/ε))
    """
    m = Metrics(strategy="UCS", problem=type(problem).__name__)
    m.start_timer()

    root = Node(problem.initial_state())
    frontier = [(0, root)]          # (cost, node) min-heap
    explored = {}                   # state → best cost seen

    while frontier:
        m.max_frontier = max(m.max_frontier, len(frontier))
        cost, node = heapq.heappop(frontier)

        if node.state in explored and explored[node.state] < cost:
            continue
        explored[node.state] = cost
        m.nodes_expanded += 1

        if problem.goal_test(node.state):
            m.found = True
            m.solution_depth = node.depth
            m.solution_cost  = node.cost
            m.stop_timer(); return node, m

        for child in _expand(node, problem, m):
            if child.state not in explored:
                heapq.heappush(frontier, (child.cost, child))

    m.stop_timer(); return None, m


# ══════════════════════════════════════════════════════════════════════════════
# 6. BDS — Bidirectional Search  (BFS variant)
# ══════════════════════════════════════════════════════════════════════════════

def bds(problem: Problem, **_) -> Tuple[Optional[Node], Metrics]:
    """
    Runs two simultaneous BFS — one from the initial state, one from the
    goal state — and stops when the frontiers meet.
    Requires the problem to expose goal_state() and reverse_actions().
    Falls back to regular BFS if not supported.
    Time & Space: O(b^(d/2))
    """
    m = Metrics(strategy="BDS", problem=type(problem).__name__)
    m.start_timer()

    # Check if problem supports bidirectional search
    if not (hasattr(problem, 'goal_state') and hasattr(problem, 'reverse_result')):
        # Fall back to BFS with a note
        m.strategy = "BDS→BFS"
        node, bfs_m = bfs(problem)
        m.found           = bfs_m.found
        m.nodes_expanded  = bfs_m.nodes_expanded
        m.nodes_generated = bfs_m.nodes_generated
        m.max_frontier    = bfs_m.max_frontier
        m.max_depth       = bfs_m.max_depth
        m.solution_depth  = bfs_m.solution_depth
        m.solution_cost   = bfs_m.solution_cost
        m.stop_timer(); return node, m

    # Forward frontier: initial → goal
    fwd_root   = Node(problem.initial_state())
    fwd_front  = deque([fwd_root])
    fwd_visited = {fwd_root.state: fwd_root}

    # Backward frontier: goal → initial
    bwd_root   = Node(problem.goal_state())
    bwd_front  = deque([bwd_root])
    bwd_visited = {bwd_root.state: bwd_root}

    def _bfs_step(frontier, visited, other_visited, forward):
        if not frontier:
            return None
        node = frontier.popleft()
        m.nodes_expanded += 1

        actions = problem.actions(node.state) if forward else problem.reverse_actions(node.state)
        for action in actions:
            child_state = (problem.result(node.state, action) if forward
                           else problem.reverse_result(node.state, action))
            cost = node.cost + problem.step_cost(node.state, action)
            child = Node(child_state, node, action, cost)
            m.nodes_generated += 1
            m.max_depth = max(m.max_depth, child.depth)

            if child_state not in visited:
                visited[child_state] = child
                frontier.append(child)
                m.max_frontier = max(m.max_frontier, len(frontier))

            if child_state in other_visited:
                return child_state   # meeting point found

        return None

    while fwd_front or bwd_front:
        meet = _bfs_step(fwd_front, fwd_visited, bwd_visited, forward=True)
        if meet:
            # stitch path: forward half + reversed backward half
            fwd_node = fwd_visited[meet]
            bwd_node = bwd_visited[meet]
            m.found = True
            m.solution_depth = fwd_node.depth + bwd_node.depth
            m.solution_cost  = fwd_node.cost  + bwd_node.cost
            m.stop_timer(); return fwd_node, m   # return fwd half

        meet = _bfs_step(bwd_front, bwd_visited, fwd_visited, forward=False)
        if meet:
            fwd_node = fwd_visited[meet]
            bwd_node = bwd_visited[meet]
            m.found = True
            m.solution_depth = fwd_node.depth + bwd_node.depth
            m.solution_cost  = fwd_node.cost  + bwd_node.cost
            m.stop_timer(); return fwd_node, m

    m.stop_timer(); return None, m


# ── registry ──────────────────────────────────────────────────────────────────

STRATEGIES = {
    "BFS"   : bfs,
    "DFS"   : dfs,
    "DLS"   : dls,
    "IDDFS" : iddfs,
    "UCS"   : ucs,
    "BDS"   : bds,
}
