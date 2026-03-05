"""
engine/node.py
Search node used by all strategies.
Tracks state, parent, action taken, depth, and path cost.
"""

from __future__ import annotations
from typing import Any, Optional


class Node:
    """
    A single node in the search tree.

    Attributes
    ----------
    state  : problem state (hashable)
    parent : parent Node or None for the root
    action : action that produced this node
    depth  : depth from root (0 = root)
    cost   : cumulative path cost
    """

    __slots__ = ("state", "parent", "action", "depth", "cost")

    def __init__(
        self,
        state: Any,
        parent: Optional["Node"] = None,
        action: Any = None,
        cost: float = 0.0,
    ):
        self.state  = state
        self.parent = parent
        self.action = action
        self.depth  = 0 if parent is None else parent.depth + 1
        self.cost   = cost

    # ── path reconstruction ───────────────────────────────────────────────────

    def path_states(self) -> list:
        """Return list of states from root to this node."""
        states, node = [], self
        while node:
            states.append(node.state)
            node = node.parent
        return list(reversed(states))

    def path_actions(self) -> list:
        """Return list of actions from root to this node (excludes root None)."""
        actions, node = [], self
        while node.parent:
            actions.append(node.action)
            node = node.parent
        return list(reversed(actions))

    # ── comparison (needed by priority queues) ────────────────────────────────

    def __lt__(self, other: "Node") -> bool:
        return self.cost < other.cost

    def __repr__(self) -> str:
        return f"Node(state={self.state!r}, depth={self.depth}, cost={self.cost})"
