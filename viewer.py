#!/usr/bin/env python3
"""
viewer.py – pretty-print a calendar-puzzle solution for any date with colorized pieces

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


# ─────────────────────────  ANSI Color Codes  ──────────────────────────
class Colors:
    # Bright colors for better visibility
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Standard colors
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    
    # Background colors for extra distinction
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    
    # Special formatting
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'
    
    # Target cell highlighting
    TARGET = '\033[1m\033[47m\033[30m'  # Bold black text on white background


# Color palette for pieces (10 different colors)
PIECE_COLORS = [
    Colors.BRIGHT_RED,      # Piece 1 - Bright Red
    Colors.BRIGHT_GREEN,    # Piece 2 - Bright Green  
    Colors.BRIGHT_YELLOW,   # Piece 3 - Bright Yellow
    Colors.BRIGHT_BLUE,     # Piece 4 - Bright Blue
    Colors.BRIGHT_MAGENTA,  # Piece 5 - Bright Magenta
    Colors.BRIGHT_CYAN,     # Piece 6 - Bright Cyan
    Colors.RED,             # Piece 7 - Red
    Colors.GREEN,           # Piece 8 - Green
    Colors.YELLOW,          # Piece 9 - Yellow
    Colors.BLUE,            # Piece 10 - Blue
]

# Symbols for pieces (can be customized)
_SYM = "ABCDEFGHIJ"        # one symbol per piece (10 total)


# ─────────────────────────  pretty printer  ──────────────────────────
def _render(board_state: list[list[int]], solver: FastCalendarPuzzleSolver, colorize: bool = True) -> str:
    """Render board with optional colorization"""
    out_lines: list[str] = []
    
    # Add header with legend if colorized
    if colorize:
        out_lines.append("🧩 Calendar Puzzle Solution (Colorized)")
        out_lines.append("=" * 50)
        out_lines.append("Legend:")
        
        # Show piece colors
        legend_line = ""
        for i in range(10):
            color = PIECE_COLORS[i] if colorize else ""
            reset = Colors.RESET if colorize else ""
            symbol = _SYM[i]
            legend_line += f"{color}Piece {i+1}({symbol}){reset}  "
            if (i + 1) % 5 == 0:  # Break into two lines
                out_lines.append(legend_line)
                legend_line = ""
        if legend_line:
            out_lines.append(legend_line)
        
        out_lines.append(f"{Colors.TARGET}Target{Colors.RESET} = Date cells to leave uncovered")
        out_lines.append("")
    
    # Render the board
    for r, row in enumerate(board_state):
        parts: list[str] = []
        for c, code in enumerate(row):
            cell_label = solver.BOARD[r][c]

            if cell_label == "":                 # blank on original calendar
                parts.append("   ")
            elif code == -1:                     # day / month / weekday squares
                if colorize:
                    colored_label = f"{Colors.TARGET}{cell_label:>3}{Colors.RESET}"
                    parts.append(colored_label)
                else:
                    parts.append(f"{cell_label:>3}")
            elif code > 0:                       # filled by a piece
                piece_idx = code - 1
                symbol = _SYM[piece_idx]
                
                if colorize and piece_idx < len(PIECE_COLORS):
                    color = PIECE_COLORS[piece_idx]
                    colored_piece = f"{color}{Colors.BOLD} {symbol} {Colors.RESET}"
                    parts.append(colored_piece)
                else:
                    parts.append(f" {symbol} ")
            else:                                # should not happen
                parts.append(" ? ")
        out_lines.append(" ".join(parts))
    
    return "\n".join(out_lines)


def _render_piece_legend() -> str:
    """Render a separate piece legend with colors"""
    lines = []
    lines.append("\n🎨 Piece Legend:")
    lines.append("=" * 30)
    
    for i in range(10):
        color = PIECE_COLORS[i]
        symbol = _SYM[i]
        piece_name = f"Piece {i+1}"
        colored_entry = f"{color}{Colors.BOLD}{symbol}{Colors.RESET} = {color}{piece_name}{Colors.RESET}"
        lines.append(colored_entry)
    
    return "\n".join(lines)


# ────────────────────────  public convenience  ───────────────────────
def print_solution_for_date(date: datetime | str, colorize: bool = True, show_legend: bool = True) -> None:
    """
    Solve and pretty-print the puzzle for `date`.

    `date` may be a datetime/date object or a string understood by
    `datetime.fromisoformat()` (e.g. "2024-01-01").
    
    Args:
        date: The date to solve for
        colorize: Whether to use colored output (default: True)
        show_legend: Whether to show the piece legend (default: True)
    """
    if isinstance(date, str):
        date = datetime.fromisoformat(date)

    solver = FastCalendarPuzzleSolver()
    sols = solver.solve_for_date(date.day, date.month, date.weekday() + 1)

    if not sols:
        print("❌  No solution for that date.")
        return

    # Print the solution
    print(_render(sols[0], solver, colorize))
    
    # Optionally print separate legend
    if colorize and show_legend:
        print(_render_piece_legend())


def print_multiple_solutions(date: datetime | str, max_solutions: int = 3, colorize: bool = True) -> None:
    """Print multiple solutions for a date if available"""
    if isinstance(date, str):
        date = datetime.fromisoformat(date)

    solver = FastCalendarPuzzleSolver()
    sols = solver.solve_for_date(date.day, date.month, date.weekday() + 1)

    if not sols:
        print("❌  No solution for that date.")
        return

    print(f"🎯 Found {len(sols)} solution(s) for {date.strftime('%Y-%m-%d')}")
    
    # Show up to max_solutions
    for i, solution in enumerate(sols[:max_solutions]):
        print(f"\n📋 Solution {i + 1}:")
        print(_render(solution, solver, colorize))
        
        if i == 0 and colorize:  # Show legend only for first solution
            print(_render_piece_legend())
    
    if len(sols) > max_solutions:
        print(f"\n... and {len(sols) - max_solutions} more solution(s)")


# ───────────────────────────  CLI entry  ─────────────────────────────
def _main(argv: list[str]) -> None:
    if len(argv) < 2 or argv[1] in {"-h", "--help"}:
        prog = Path(argv[0]).name
        print(f"Usage: {prog} YYYY-MM-DD [options]")
        print(f"       {prog} 2024-02-29")
        print(f"")
        print(f"Options:")
        print(f"  --no-color     Disable colored output")
        print(f"  --no-legend    Hide piece legend")
        print(f"  --multiple N   Show up to N solutions (default: 1)")
        print(f"  -h, --help     Show this help message")
        sys.exit(1)

    # Parse arguments
    date_str = argv[1]
    colorize = "--no-color" not in argv
    show_legend = "--no-legend" not in argv
    multiple = False
    max_solutions = 1
    
    # Check for multiple solutions option
    if "--multiple" in argv:
        multiple = True
        try:
            idx = argv.index("--multiple")
            if idx + 1 < len(argv):
                max_solutions = int(argv[idx + 1])
            else:
                max_solutions = 3  # default
        except (ValueError, IndexError):
            max_solutions = 3

    try:
        date = datetime.fromisoformat(date_str)
    except ValueError as e:
        sys.exit(f"Invalid date: {e}")

    # Print solution(s)
    if multiple:
        print_multiple_solutions(date, max_solutions, colorize)
    else:
        print_solution_for_date(date, colorize, show_legend)


if __name__ == "__main__":
    _main(sys.argv)
