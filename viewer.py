#!/usr/bin/env python3
"""
viewer.py – pretty-print a calendar-puzzle solution for any date

Usage (CLI):
    ./viewer.py 2024-01-01
"""

from __future__ import annotations
import sys
from datetime import datetime
from pathlib import Path

# import the solver you already have
# adjust the path / name if you placed the file elsewhere
from fast_dp_solver import FastCalendarPuzzleSolver


# ─────────────────────────  pretty printer  ──────────────────────────
_SYM = "ABCDEFTHIJ"        # one symbol per piece (10 total)


def _render(board_state: list[list[int]], solver: FastCalendarPuzzleSolver) -> str:
    out_lines: list[str] = []
    for r, row in enumerate(board_state):
        parts: list[str] = []
        for c, code in enumerate(row):
            cell_label = solver.BOARD[r][c]

            if cell_label == "":                 # blank on original calendar
                parts.append("   ")
            elif code == -1:                     # day / month / weekday squares
                parts.append(f"{cell_label:>3}")
            elif code > 0:                       # filled by a piece
                parts.append(f" {_SYM[code-1]} ")
            else:                                # should not happen
                parts.append(" ? ")
        out_lines.append(" ".join(parts))
    return "\n".join(out_lines)


# ────────────────────────  public convenience  ───────────────────────
def print_solution_for_date(date: datetime | str) -> None:
    """
    Solve and pretty-print the puzzle for `date`.

    `date` may be a datetime/date object or a string understood by
    `datetime.fromisoformat()` (e.g. "2024-01-01").
    """
    if isinstance(date, str):
        date = datetime.fromisoformat(date)

    solver = FastCalendarPuzzleSolver()
    sols = solver.solve_for_date(date.day, date.month, date.weekday() + 1)

    if not sols:
        print("❌  No solution for that date.")
        return

    print(_render(sols[0], solver))


# ───────────────────────────  CLI entry  ─────────────────────────────
def _main(argv: list[str]) -> None:
    if len(argv) != 2 or argv[1] in {"-h", "--help"}:
        prog = Path(argv[0]).name
        print(f"Usage: {prog} YYYY-MM-DD\n"
              f"       {prog} 2024-02-29")
        sys.exit(1)

    try:
        date = datetime.fromisoformat(argv[1])
    except ValueError as e:
        sys.exit(f"Invalid date: {e}")

    print_solution_for_date(date)


if __name__ == "__main__":
    _main(sys.argv)
