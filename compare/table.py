"""
compare/table.py
Renders a comparison table of Metrics objects to the terminal.
"""

from typing import List
from engine.metrics import Metrics

COLS = ["Strategy", "Found", "Depth", "Cost",
        "Expanded", "Generated", "Max Frontier", "Max Depth", "Time (ms)"]


def _col_widths(rows: List[dict]) -> dict:
    widths = {c: len(c) for c in COLS}
    for row in rows:
        for c in COLS:
            widths[c] = max(widths[c], len(str(row.get(c, ""))))
    return widths


def print_table(metrics_list: List[Metrics], title: str = "") -> None:
    if not metrics_list:
        return

    rows = [m.row() for m in metrics_list]
    widths = _col_widths(rows)

    sep = "─"
    total = sum(widths.values()) + len(COLS) * 3 + 1

    # ── header ────────────────────────────────────────────────────────────────
    if title:
        print(f"\n  ╔{'═' * (total - 2)}╗")
        print(f"  ║  {title:<{total-4}}║")
        print(f"  ╚{'═' * (total - 2)}╝")

    # ── column headers ────────────────────────────────────────────────────────
    header = "  │ " + " │ ".join(f"{c:<{widths[c]}}" for c in COLS) + " │"
    divider = "  ├─" + "─┼─".join(sep * widths[c] for c in COLS) + "─┤"
    top     = "  ┌─" + "─┬─".join(sep * widths[c] for c in COLS) + "─┐"
    bottom  = "  └─" + "─┴─".join(sep * widths[c] for c in COLS) + "─┘"

    print(top)
    print(header)
    print(divider)

    # ── data rows ─────────────────────────────────────────────────────────────
    for row in rows:
        line = "  │ " + " │ ".join(f"{str(row.get(c,'')):<{widths[c]}}" for c in COLS) + " │"
        print(line)

    print(bottom)
    print()


def print_winner(metrics_list: List[Metrics]) -> None:
    """Print a short analysis of which strategy performed best."""
    solved = [m for m in metrics_list if m.found]
    if not solved:
        print("  No strategy found a solution.\n")
        return

    best_cost     = min(solved, key=lambda m: (m.solution_cost or 999))
    best_expanded = min(solved, key=lambda m: m.nodes_expanded)
    best_time     = min(solved, key=lambda m: m.elapsed_ms)

    print("  ── Analysis ──────────────────────────────────────────")
    print(f"  Optimal cost      : {best_cost.strategy}  "
          f"(cost = {best_cost.solution_cost})")
    print(f"  Fewest expansions : {best_expanded.strategy}  "
          f"({best_expanded.nodes_expanded} nodes)")
    print(f"  Fastest wall time : {best_time.strategy}  "
          f"({best_time.elapsed_ms:.2f} ms)")
    print()
