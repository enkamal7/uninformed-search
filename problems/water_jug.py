"""
problems/water_jug.py

Water (& Milk) Jug Problem
===========================
Two jugs: capacity JUG_A and JUG_B litres.
No measuring marks. Goal: measure exactly GOAL litres in either jug.

State  : (a, b)  — current fill levels
Actions:
  fill_a    fill_b    empty_a   empty_b
  pour_a_to_b         pour_b_to_a

Supports BDS via goal_state() / reverse_result().
"""

from typing import Any, List, Tuple
from engine.problem import Problem


class WaterJugProblem(Problem):

    def __init__(self, cap_a: int = 4, cap_b: int = 3, goal: int = 2):
        self.cap_a = cap_a
        self.cap_b = cap_b
        self.goal  = goal

    # ── Problem interface ─────────────────────────────────────────────────────

    def initial_state(self) -> Tuple[int, int]:
        return (0, 0)

    def goal_test(self, state: Tuple[int, int]) -> bool:
        return self.goal in state

    def actions(self, state: Tuple[int, int]) -> List[str]:
        a, b = state
        acts = []
        if a < self.cap_a:            acts.append("fill_a")
        if b < self.cap_b:            acts.append("fill_b")
        if a > 0:                     acts.append("empty_a")
        if b > 0:                     acts.append("empty_b")
        if a > 0 and b < self.cap_b:  acts.append("pour_a→b")
        if b > 0 and a < self.cap_a:  acts.append("pour_b→a")
        return acts

    def result(self, state: Tuple[int, int], action: str) -> Tuple[int, int]:
        a, b = state
        if action == "fill_a":   return (self.cap_a, b)
        if action == "fill_b":   return (a, self.cap_b)
        if action == "empty_a":  return (0, b)
        if action == "empty_b":  return (a, 0)
        if action == "pour_a→b":
            pour = min(a, self.cap_b - b)
            return (a - pour, b + pour)
        if action == "pour_b→a":
            pour = min(b, self.cap_a - a)
            return (a + pour, b - pour)
        return state

    def action_label(self, action: str) -> str:
        labels = {
            "fill_a"  : f"Fill jug A (cap {self.cap_a}L)",
            "fill_b"  : f"Fill jug B (cap {self.cap_b}L)",
            "empty_a" : "Empty jug A",
            "empty_b" : "Empty jug B",
            "pour_a→b": "Pour A → B",
            "pour_b→a": "Pour B → A",
        }
        return labels.get(action, action)

    # ── BDS support ───────────────────────────────────────────────────────────

    def goal_state(self):
        """One concrete goal state for backward search."""
        return (self.goal, 0)

    def reverse_actions(self, state):
        return self.actions(state)   # actions are reversible

    def reverse_result(self, state, action):
        return self.result(state, action)

    # ── display ───────────────────────────────────────────────────────────────

    def display_state(self, state: Tuple[int, int]) -> str:
        a, b = state
        bar_a = "█" * a + "░" * (self.cap_a - a)
        bar_b = "█" * b + "░" * (self.cap_b - b)
        return (f"  Jug A [{bar_a}] {a}/{self.cap_a}L   "
                f"Jug B [{bar_b}] {b}/{self.cap_b}L")
