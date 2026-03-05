"""
engine/metrics.py
Collects performance data during a search run.
"""

import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Metrics:
    """
    Performance metrics for one search run.

    nodes_expanded   : number of nodes popped from the frontier
    nodes_generated  : number of child nodes created
    max_frontier     : peak frontier size
    max_depth        : deepest node ever generated
    solution_depth   : depth of solution found (None = no solution)
    solution_cost    : path cost of solution   (None = no solution)
    elapsed_ms       : wall-clock time in milliseconds
    found            : True if a solution was found
    """
    strategy         : str   = ""
    problem          : str   = ""
    nodes_expanded   : int   = 0
    nodes_generated  : int   = 0
    max_frontier     : int   = 0
    max_depth        : int   = 0
    solution_depth   : Optional[int]   = None
    solution_cost    : Optional[float] = None
    elapsed_ms       : float = 0.0
    found            : bool  = False

    # ── timing helpers ────────────────────────────────────────────────────────

    _start: float = field(default=0.0, repr=False)

    def start_timer(self):
        self._start = time.perf_counter()

    def stop_timer(self):
        self.elapsed_ms = (time.perf_counter() - self._start) * 1000

    # ── display ───────────────────────────────────────────────────────────────

    def row(self) -> dict:
        return {
            "Strategy"        : self.strategy,
            "Found"           : "Yes" if self.found else "No",
            "Depth"           : str(self.solution_depth) if self.found else "-",
            "Cost"            : str(self.solution_cost)  if self.found else "-",
            "Expanded"        : str(self.nodes_expanded),
            "Generated"       : str(self.nodes_generated),
            "Max Frontier"    : str(self.max_frontier),
            "Max Depth"       : str(self.max_depth),
            "Time (ms)"       : f"{self.elapsed_ms:.2f}",
        }
