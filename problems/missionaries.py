"""
problems/missionaries.py

Missionaries and Cannibals
===========================
3 missionaries + 3 cannibals must cross a river.
Boat holds at most 2 people, at least 1.
Cannibals must never outnumber missionaries on either bank.

State  : (m_left, c_left, boat)
         m_left  = missionaries on left bank
         c_left  = cannibals    on left bank
         boat    = 'L' or 'R'

Goal   : (0, 0, 'R')  — everyone on right bank
"""

from typing import Any, List, Tuple
from engine.problem import Problem

TOTAL_M = 3
TOTAL_C = 3


class MissionariesProblem(Problem):

    def initial_state(self) -> Tuple[int, int, str]:
        return (TOTAL_M, TOTAL_C, 'L')

    def goal_test(self, state) -> bool:
        return state == (0, 0, 'R')

    def _safe(self, m, c) -> bool:
        """No side is unsafe: missionaries are outnumbered only if there are any."""
        if m > 0 and c > m:  return False
        rm, rc = TOTAL_M - m, TOTAL_C - c
        if rm > 0 and rc > rm: return False
        return True

    def actions(self, state) -> List[Tuple[int, int]]:
        m, c, boat = state
        moves = [(1,0),(0,1),(1,1),(2,0),(0,2)]
        valid = []
        for dm, dc in moves:
            if boat == 'L':
                nm, nc = m - dm, c - dc
            else:
                nm, nc = m + dm, c + dc
            if 0 <= nm <= TOTAL_M and 0 <= nc <= TOTAL_C:
                if self._safe(nm, nc):
                    valid.append((dm, dc))
        return valid

    def result(self, state, action) -> Tuple[int, int, str]:
        m, c, boat = state
        dm, dc = action
        if boat == 'L':
            return (m - dm, c - dc, 'R')
        else:
            return (m + dm, c + dc, 'L')

    def action_label(self, action) -> str:
        dm, dc = action
        parts = []
        if dm: parts.append(f"{dm}M")
        if dc: parts.append(f"{dc}C")
        return "+".join(parts) if parts else "?"

    # ── BDS support ───────────────────────────────────────────────────────────

    def goal_state(self):
        return (0, 0, 'R')

    def reverse_actions(self, state):
        return self.actions(state)

    def reverse_result(self, state, action):
        return self.result(state, action)

    # ── display ───────────────────────────────────────────────────────────────

    def display_state(self, state) -> str:
        m, c, boat = state
        rm, rc = TOTAL_M - m, TOTAL_C - c
        b = "⛵ " if boat == 'L' else "  "
        b2= "  " if boat == 'L' else " ⛵"
        return (f"  LEFT {b}[M:{m} C:{c}]  ~~~river~~~  "
                f"[M:{rm} C:{rc}]{b2} RIGHT")
