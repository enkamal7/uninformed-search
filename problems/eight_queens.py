"""
problems/eight_queens.py

Eight Queens Problem
=====================
Place 8 queens on an 8×8 chessboard so no two queens attack each other.
Queens attack along rows, columns, and diagonals.

State  : tuple of length ≤ 8.
         state[col] = row where queen is placed in column col.
         Partial states are built column by column.

Goal   : len(state) == 8 and no conflicts.

This is a CSP-style formulation — we add one queen per column,
so column conflicts are eliminated by construction.
"""

from typing import Any, List, Tuple
from engine.problem import Problem

N = 8


class EightQueensProblem(Problem):

    def initial_state(self) -> tuple:
        return ()   # no queens placed yet

    def goal_test(self, state: tuple) -> bool:
        return len(state) == N   # conflicts already prevented by actions()

    def actions(self, state: tuple) -> List[int]:
        """Return valid row placements for the next column."""
        col = len(state)
        if col >= N:
            return []
        valid_rows = []
        for row in range(N):
            if self._no_conflict(state, col, row):
                valid_rows.append(row)
        return valid_rows

    def _no_conflict(self, state: tuple, col: int, row: int) -> bool:
        for c, r in enumerate(state):
            if r == row:                       return False  # same row
            if abs(r - row) == abs(c - col):   return False  # diagonal
        return True

    def result(self, state: tuple, action: int) -> tuple:
        return state + (action,)

    def action_label(self, action: int) -> str:
        col = "ABCDEFGH"[len("")]   # placeholder — shown properly in solution display
        return f"row {action+1}"

    # ── display ───────────────────────────────────────────────────────────────

    def display_state(self, state: tuple) -> str:
        lines = []
        for row in range(N):
            rank = N - row
            line_chars = [f" {rank} "]
            for col in range(N):
                if col < len(state) and state[col] == row:
                    line_chars.append(" Q ")
                else:
                    shade = "░░░" if (row + col) % 2 == 0 else "▓▓▓"
                    line_chars.append(shade)
            lines.append("".join(line_chars))
        lines.append("    " + "".join(f" {'ABCDEFGH'[c]} " for c in range(N)))
        return "\n".join(lines)
