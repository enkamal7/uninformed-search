"""
main.py — Entry point.

Uninformed Search Strategies — Terminal Implementation
Artificial Intelligence — Individual Assignment

Usage:
    python main.py
"""

import sys
import os
import time

# ── terminal helpers (inline, no extra file needed) ───────────────────────────

class C:
    R="\033[0m";B="\033[1m";DM="\033[2m";IT="\033[3m"
    RED="\033[31m";GRN="\033[32m";YLW="\033[33m"
    BLU="\033[34m";MAG="\033[35m";CYN="\033[36m"
    WHT="\033[37m";GRY="\033[90m"

def c(col,t): return f"{col}{t}{C.R}"
def clr(): os.system("cls" if os.name=="nt" else "clear")
def line(ch="─",n=72,col=C.GRY): print(c(col,ch*n))
def ask(p,col=C.B+C.WHT):
    try: return input(f"\n  {c(col,'▶')}  {p}  ").strip()
    except: print(); return "q"
def pause(m="  Press ENTER to continue…"): input(c(C.GRY,m))

# ── imports ───────────────────────────────────────────────────────────────────

from engine.strategies import STRATEGIES, bfs, dfs, dls, iddfs, ucs, bds
from engine.metrics    import Metrics
from compare.table     import print_table, print_winner

from problems.water_jug    import WaterJugProblem
from problems.missionaries import MissionariesProblem
from problems.eight_queens import EightQueensProblem
from problems.tic_tac_toe  import TicTacToeProblem


# ── strategy runner ───────────────────────────────────────────────────────────

def run_all_strategies(problem, dls_limit=10, iddfs_max=30, skip_bds=False):
    """Run all 6 strategies on a problem; return list of Metrics."""
    runs = [
        ("BFS",   bfs,   {}),
        ("DFS",   dfs,   {}),
        ("DLS",   dls,   {"limit": dls_limit}),
        ("IDDFS", iddfs, {"max_limit": iddfs_max}),
        ("UCS",   ucs,   {}),
        ("BDS",   bds,   {}),
    ]
    results = []
    for name, fn, kwargs in runs:
        print(f"  Running {c(C.YLW,name)}…", end="\r")
        node, m = fn(problem, **kwargs)
        m.strategy = name
        results.append((node, m))
        status = c(C.GRN,"✔ found") if m.found else c(C.RED,"✘ not found")
        print(f"  {c(C.YLW,name):<6}  {status}   "
              f"expanded={m.nodes_expanded}  time={m.elapsed_ms:.1f}ms      ")
    return results


# ── solution display ──────────────────────────────────────────────────────────

def show_solution(node, problem, label="BFS"):
    """Print the solution path with state visualisation."""
    if node is None:
        print(c(C.RED, f"  No solution found by {label}."))
        return

    states  = node.path_states()
    actions = node.path_actions()

    print(c(C.B+C.CYN, f"\n  Solution path ({label})  —  {len(actions)} step(s):\n"))

    for i, state in enumerate(states):
        if i == 0:
            print(c(C.GRY, f"  ── Initial state ──"))
        else:
            act_lbl = problem.action_label(actions[i-1]) if hasattr(problem,'action_label') else str(actions[i-1])
            print(c(C.YLW, f"  ── Step {i}: {act_lbl} ──"))

        if hasattr(problem, 'display_state'):
            print(problem.display_state(state))
        else:
            print(f"  {state}")
        print()


# ══════════════════════════════════════════════════════════════════════════════
# Problem runners
# ══════════════════════════════════════════════════════════════════════════════

def run_water_jug():
    clr()
    line("═",col=C.B+C.BLU)
    print(c(C.B+C.BLU,"  PROBLEM 1 — Water Jug"))
    print(c(C.GRY,    "  Jug A: 4L  |  Jug B: 3L  |  Goal: measure 2L"))
    line("═",col=C.B+C.BLU)
    print()
    print(c(C.DM,"  Available actions: fill, empty, pour between jugs."))
    print(c(C.DM,"  Constraints: no measuring marks on jugs."))
    print()

    prob = WaterJugProblem(cap_a=4, cap_b=3, goal=2)
    results = run_all_strategies(prob, dls_limit=8, iddfs_max=15)
    print()

    all_m = [m for _,m in results]
    print_table(all_m, "Water Jug — Strategy Comparison")
    print_winner(all_m)

    # show BFS solution
    bfs_node = next((n for n,m in results if m.strategy=="BFS" and m.found), None)
    show_solution(bfs_node, prob, "BFS")
    pause()


def run_missionaries():
    clr()
    line("═",col=C.B+C.RED)
    print(c(C.B+C.RED,"  PROBLEM 2 — Missionaries and Cannibals"))
    print(c(C.GRY,    "  3 missionaries + 3 cannibals must cross the river."))
    line("═",col=C.B+C.RED)
    print()
    print(c(C.DM,"  Boat holds 1–2 people."))
    print(c(C.DM,"  Cannibals must never outnumber missionaries on either bank."))
    print()

    prob = MissionariesProblem()
    results = run_all_strategies(prob, dls_limit=12, iddfs_max=15)
    print()

    all_m = [m for _,m in results]
    print_table(all_m, "Missionaries & Cannibals — Strategy Comparison")
    print_winner(all_m)

    bfs_node = next((n for n,m in results if m.strategy=="BFS" and m.found), None)
    show_solution(bfs_node, prob, "BFS")
    pause()


def run_eight_queens():
    clr()
    line("═",col=C.B+C.MAG)
    print(c(C.B+C.MAG,"  PROBLEM 3 — Eight Queens"))
    print(c(C.GRY,    "  Place 8 queens on an 8×8 board — no two attack each other."))
    line("═",col=C.B+C.MAG)
    print()
    print(c(C.DM,"  Queens are placed column by column."))
    print(c(C.DM,"  Row and diagonal conflicts are checked at each step."))
    print(c(C.YLW,"  Note: DFS finds first solution fastest for this problem."))
    print(c(C.YLW,"        BFS/UCS may be slow — press Ctrl+C to skip if needed."))
    print()

    prob = EightQueensProblem()
    # BFS is very expensive for 8-queens — use a node limit
    results = []
    runs = [
        ("BFS",   bfs,   {}),
        ("DFS",   dfs,   {}),
        ("DLS",   dls,   {"limit": 8}),
        ("IDDFS", iddfs, {"max_limit": 8}),
        ("UCS",   ucs,   {}),
        ("BDS",   bds,   {}),
    ]
    for name, fn, kwargs in runs:
        print(f"  Running {c(C.YLW,name)}…", end="\r")
        try:
            node, m = fn(prob, **kwargs)
        except KeyboardInterrupt:
            print(f"\n  {c(C.YLW,name)} interrupted by user.")
            from engine.metrics import Metrics
            m = Metrics(strategy=name, problem="EightQueens")
            node = None
        m.strategy = name
        results.append((node, m))
        status = c(C.GRN,"✔ found") if m.found else c(C.RED,"✘ not found")
        print(f"  {c(C.YLW,name):<6}  {status}   "
              f"expanded={m.nodes_expanded}  time={m.elapsed_ms:.1f}ms      ")
    print()

    all_m = [m for _,m in results]
    print_table(all_m, "Eight Queens — Strategy Comparison")
    print_winner(all_m)

    # show DFS solution (fastest for this problem)
    dfs_node = next((n for n,m in results if m.strategy=="DFS" and m.found), None)
    if dfs_node:
        print(c(C.B+C.CYN,"\n  Solution board (DFS):\n"))
        print(prob.display_state(dfs_node.state))
        print()
    pause()


def run_tic_tac_toe():
    clr()
    line("═",col=C.B+C.GRN)
    print(c(C.B+C.GRN,"  PROBLEM 4 — Tic-Tac-Toe"))
    print(c(C.GRY,    "  Search for a winning sequence for X from empty board."))
    line("═",col=C.B+C.GRN)
    print()
    print(c(C.DM,"  X and O alternate. X moves first."))
    print(c(C.DM,"  Goal: X achieves three-in-a-row."))
    print()

    prob = TicTacToeProblem()
    results = run_all_strategies(prob, dls_limit=9, iddfs_max=9)
    print()

    all_m = [m for _,m in results]
    print_table(all_m, "Tic-Tac-Toe — Strategy Comparison")
    print_winner(all_m)

    bfs_node = next((n for n,m in results if m.strategy=="BFS" and m.found), None)
    if bfs_node:
        states  = bfs_node.path_states()
        actions = bfs_node.path_actions()
        print(c(C.B+C.CYN,f"\n  Winning path for X ({len(actions)} moves):\n"))
        for i, state in enumerate(states):
            label = "Initial" if i == 0 else f"Move {i}"
            player = "X" if i % 2 == 0 else "O"
            if i > 0:
                pos = actions[i-1]
                r,cl = divmod(pos,3)
                print(c(C.YLW,f"  ── {label}: {player} plays ({r+1},{cl+1}) ──"))
            else:
                print(c(C.GRY,"  ── Initial board ──"))
            print(prob.display_state(state))
            print()
    pause()


def run_compare_all():
    """Run BFS vs DFS on all 4 problems side-by-side."""
    clr()
    line("═",col=C.B+C.CYN)
    print(c(C.B+C.CYN,"  CROSS-PROBLEM COMPARISON  —  BFS vs DFS"))
    line("═",col=C.B+C.CYN)
    print()

    problems = [
        ("Water Jug",          WaterJugProblem(),    {"dls_limit":8, "iddfs_max":15}),
        ("Missionaries",       MissionariesProblem(),{"dls_limit":12,"iddfs_max":15}),
        ("Eight Queens",       EightQueensProblem(), {"dls_limit":8, "iddfs_max":8}),
        ("Tic-Tac-Toe",        TicTacToeProblem(),   {"dls_limit":9, "iddfs_max":9}),
    ]

    all_metrics = []
    for pname, prob, kwargs in problems:
        print(c(C.YLW, f"  {pname}"))
        results = run_all_strategies(prob, **kwargs)
        for _, m in results:
            m.problem = pname
            all_metrics.append(m)
        print()

    # grouped by problem
    for pname, _, _ in problems:
        pm = [m for m in all_metrics if m.problem == pname]
        print_table(pm, f"{pname} — All Strategies")

    pause()


# ══════════════════════════════════════════════════════════════════════════════
# Main menu
# ══════════════════════════════════════════════════════════════════════════════

def banner():
    clr()
    line("═",col=C.B+C.CYN)
    print(c(C.B+C.CYN,"  UNINFORMED SEARCH STRATEGIES"))
    print(c(C.GRY,    "  BFS · DFS · DLS · IDDFS · UCS · BDS"))
    print(c(C.GRY,    "  Artificial Intelligence — Individual Assignment"))
    line("═",col=C.B+C.CYN)
    print()


def main():
    while True:
        banner()
        print(c(C.B,"  SELECT A PROBLEM / MODE\n"))
        menu = [
            ("1", "Water Jug Problem",            "4L + 3L jugs, measure 2L"),
            ("2", "Missionaries & Cannibals",      "3+3 river crossing"),
            ("3", "Eight Queens",                  "8 queens, no attacks"),
            ("4", "Tic-Tac-Toe",                   "X wins from empty board"),
            ("5", "Compare All Problems",           "BFS/DFS/DLS/IDDFS/UCS/BDS on all 4"),
            ("Q", "Quit",                           ""),
        ]
        for key, label, hint in menu:
            h = c(C.GRY, f"  — {hint}") if hint else ""
            print(f"    {c(C.B+C.YLW,f'[{key}]')}  {label}{h}")
        print()
        line(col=C.GRY)

        choice = ask("Select",col=C.B+C.WHT).upper()

        if   choice == "1": run_water_jug()
        elif choice == "2": run_missionaries()
        elif choice == "3": run_eight_queens()
        elif choice == "4": run_tic_tac_toe()
        elif choice == "5": run_compare_all()
        elif choice in ("Q","QUIT","EXIT"):
            clr(); banner()
            print(c(C.GRY,"  Goodbye.\n")); sys.exit(0)
        else:
            print(c(C.YLW,"  Invalid selection."))
            time.sleep(0.8)


if __name__ == "__main__":
    main()
