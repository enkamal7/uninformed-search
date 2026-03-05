"""
engine/problem.py
Abstract base class for all search problems.
Every problem must implement these five methods.
"""

from abc import ABC, abstractmethod
from typing import Any, List, Tuple


class Problem(ABC):
    """
    Formal definition of a search problem.

    Subclasses implement:
        initial_state()   → starting state
        goal_test(s)      → True if s is a goal
        actions(s)        → list of valid actions from state s
        result(s, a)      → state reached by applying action a to s
        step_cost(s, a)   → cost of one step (default 1)
    """

    @abstractmethod
    def initial_state(self) -> Any:
        """Return the initial state."""

    @abstractmethod
    def goal_test(self, state: Any) -> bool:
        """Return True if state is a goal state."""

    @abstractmethod
    def actions(self, state: Any) -> List[Any]:
        """Return a list of actions applicable in state."""

    @abstractmethod
    def result(self, state: Any, action: Any) -> Any:
        """Return the state resulting from applying action to state."""

    def step_cost(self, state: Any, action: Any) -> float:
        """Cost of taking action in state. Default = 1."""
        return 1.0

    def action_label(self, action: Any) -> str:
        """Human-readable label for an action (used in display)."""
        return str(action)
