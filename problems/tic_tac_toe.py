"""
problems/tic_tac_toe.py

Tic-Tac-Toe Search Problem
============================
Search for a winning move sequence for X starting from an empty board.
Goal: X wins (3-in-a-row).

State  : 9-tuple of ' ', 'X', 'O'  (positions 0-8, row-major)
         + whose turn it is encoded as the parity of filled cells.

Actions: index (0-8) of an empty cell.

Players alternate. X always moves first.
Goal: any board where X has three in a row.
"""

from typing import Any, List, Tuple
from engine.problem import Problem

WINS = [
    (0,1,2),(3,4,5),(6,7,8),   # rows
    (0,3,6),(1,4,7),(2,5,8),   # cols
    (0,4,8),(2,4,6),           # diagonals
]


def _winner(board):
    for a,b,c in WINS:
        if board[a] == board[b] == board[c] != ' ':
            return board[a]
    return None


def _turn(board):
    """Returns whose turn it is based on piece counts."""
    xs = board.count('X')
    os = board.count('O')
    return 'X' if xs == os else 'O'


class TicTacToeProblem(Problem):

    def initial_state(self) -> tuple:
        return tuple([' '] * 9)

    def goal_test(self, state: tuple) -> bool:
        return _winner(state) == 'X'

    def actions(self, state: tuple) -> List[int]:
        if _winner(state):
            return []
        if ' ' not in state:
            return []
        return [i for i, v in enumerate(state) if v == ' ']

    def result(self, state: tuple, action: int) -> tuple:
        board = list(state)
        board[action] = _turn(state)
        return tuple(board)

    def action_label(self, action: int) -> str:
        row, col = divmod(action, 3)
        return f"{'XO'[0]} → ({row+1},{col+1})"

    # ── BDS support ───────────────────────────────────────────────────────────

    def goal_state(self):
        # One concrete win for X: top row
        b = [' '] * 9
        b[0] = b[1] = b[2] = 'X'
        b[3] = b[4] = 'O'
        return tuple(b)

    # ── display ───────────────────────────────────────────────────────────────

    def display_state(self, state: tuple) -> str:
        rows = []
        for r in range(3):
            cells = [f" {state[r*3+c]} " for c in range(3)]
            rows.append("  " + "|".join(cells))
            if r < 2:
                rows.append("  ---+---+---")
        return "\n".join(rows)
