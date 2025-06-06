#!/usr/bin/env python3
"""
Fast calendar-puzzle solver — drop-in replacement for the original
"""

from __future__ import annotations
import json
from functools import lru_cache
from datetime import datetime
from typing import List, Tuple, Dict


class FastCalendarPuzzleSolver:
    # ─────────────────────────  STATIC BOARD DATA  ──────────────────────────
    BOARD: List[List[str]] = [
        ["1",  "2",  "3",  "4",  "OCA", "♥",  "PZT"],   # 0
        ["5",  "6",  "7",  "8",  "SUB", "MAR", "SAL"],   # 1
        ["9",  "10", "11", "12", "NIS", "MAY", "CAR"],   # 2
        ["13", "14", "15", "16", "HAZ", "TEM", "PER"],   # 3
        ["17", "18", "19", "20", "AGU", "EYL", "CUM"],   # 4
        ["21", "22", "23", "24", "EKI", "KAS", "CMT"],   # 5
        ["25", "26", "27", "28", "ARA", "♥",  "PAZ"],   # 6
        ["29", "30", "31", "",   "",    "",    ""],      # 7
    ]

    MONTHS = {"OCA": 1, "SUB": 2, "MAR": 3, "NIS": 4, "MAY": 5, "HAZ": 6,
              "TEM": 7, "AGU": 8, "EYL": 9, "EKI": 10, "KAS": 11, "ARA": 12}

    DAYS = {"PZT": 1, "SAL": 2, "CAR": 3, "PER": 4, "CUM": 5, "CMT": 6, "PAZ": 7}

    DAYS_IN_MONTH = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
                     7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}

    # Original 10 pieces (1 = filled)
    PIECES: List[List[List[int]]] = [
        # 1. L-tetromino
        [[1, 0],
         [1, 0],
         [1, 0],
         [1, 1]],
        # 2. Z-pentomino
        [[1, 1, 0],
         [0, 1, 0],
         [0, 1, 1]],
        # 3. mirrored L-tetromino
        [[0, 1],
         [0, 1],
         [1, 1],
         [1, 0]],
        # 4. straight 5-cell
        [[1, 1, 1, 1, 1]],
        # 5. Z-tetromino
        [[0, 1, 1],
         [1, 1, 0]],
        # 6. L-pentomino
        [[0, 0, 1],
         [0, 0, 1],
         [1, 1, 1]],
        # 7. T-pentomino
        [[1, 1, 1],
         [0, 1, 0],
         [0, 1, 0]],
        # 8. mirrored wide-T
        [[1, 1, 1],
         [1, 0, 1]],
        # 9. long T-pentomino
        [[1, 1, 1, 1],
         [0, 0, 1, 0]],
        # 10. “skewed block” tetromino
        [[0, 1],
         [1, 1],
         [1, 1]],
    ]

    # ────────────────────────────────────────────────────────────────────────

    def __init__(self) -> None:
        # board geometry → bit positions
        self.pos_to_bit: Dict[Tuple[int, int], int] = {}
        self.bit_to_pos: Dict[int, Tuple[int, int]] = {}
        bit = 0
        for r, row in enumerate(self.BOARD):
            for c, cell in enumerate(row):
                if cell:                       # skip blanks (“”)
                    self.pos_to_bit[(r, c)] = bit
                    self.bit_to_pos[bit] = (r, c)
                    bit += 1

        self.total_bits: int = bit
        self.valid_mask: int = (1 << self.total_bits) - 1
        self.all_used_mask: int = (1 << len(self.PIECES)) - 1

        # generate piece placements
        self.placements_by_piece: List[Tuple[int, ...]] = []
        # for each cell, which (piece, mask) pairs can cover it?
        self.cell_to_options: List[List[Tuple[int, int]]] = [
            [] for _ in range(self.total_bits)
        ]

        self._precompute_placements()

    # ───────────────────────────  GEOMETRY HELPERS  ────────────────────────
    @staticmethod
    def _rot90(mat: List[List[int]]) -> List[List[int]]:
        return [list(reversed(col)) for col in zip(*mat)]

    @staticmethod
    def _flip_h(mat: List[List[int]]) -> List[List[int]]:
        return [row[::-1] for row in mat]

    @staticmethod
    def _flip_v(mat: List[List[int]]) -> List[List[int]]:
        return list(reversed(mat))

    @staticmethod
    def _normalise(mat: List[List[int]]) -> Tuple[Tuple[int, ...], ...]:
        return tuple(tuple(row) for row in mat)

    # ─────────────────────────  PLACEMENT PRE-COMPUTE  ─────────────────────
    def _gen_orientations(self, piece: List[List[int]]) -> List[List[Tuple[int, int]]]:
        """Return list of orientations; each orientation is list[(dr, dc)]."""
        seen = set()
        outs: List[List[Tuple[int, int]]] = []

        cur = piece
        for _ in range(4):
            for variant in (
                    cur,
                    self._flip_h(cur),
                    self._flip_v(cur),
                    self._flip_h(self._flip_v(cur)),
            ):
                key = self._normalise(variant)
                if key in seen:
                    continue
                seen.add(key)
                cells = [(r, c)
                         for r, row in enumerate(variant)
                         for c, v in enumerate(row) if v]
                # shift to top-left origin
                min_r = min(r for r, _ in cells)
                min_c = min(c for _, c in cells)
                outs.append([(r - min_r, c - min_c) for r, c in cells])
            cur = self._rot90(cur)
        return outs

    def _precompute_placements(self) -> None:
        """Fill placements_by_piece and cell_to_options tables."""
        board_h = len(self.BOARD)
        board_w = len(self.BOARD[0])

        for p_idx, raw_piece in enumerate(self.PIECES):
            placements: List[int] = []

            for orient in self._gen_orientations(raw_piece):
                max_r = max(r for r, _ in orient)
                max_c = max(c for _, c in orient)

                for sr in range(board_h - max_r):
                    for sc in range(board_w - max_c):
                        mask = 0
                        ok = True
                        for dr, dc in orient:
                            rr, cc = sr + dr, sc + dc
                            cell = self.BOARD[rr][cc]
                            if not cell:           # blank square on calendar
                                ok = False
                                break
                            mask |= 1 << self.pos_to_bit[(rr, cc)]
                        if ok:
                            placements.append(mask)
                            # register for every cell it covers
                            for bit in range(self.total_bits):
                                if mask & (1 << bit):
                                    self.cell_to_options[bit].append((p_idx, mask))

            self.placements_by_piece.append(tuple(placements))

    # ─────────────────────────────  SOLVER CORE  ───────────────────────────
    def _solve_mask(self, initial_mask: int) -> List[Tuple[int, int]] | None:
        """Return list[(piece_idx, placement_mask)] or None."""
        solution: List[Tuple[int, int]] = []

        @lru_cache(maxsize=None)
        def dfs(board_mask: int, used_mask: int) -> bool:
            if board_mask == self.valid_mask:
                return True        # everything covered (target + pieces)

            # first empty cell (LSB zero in board_mask)
            empty_bits = self.valid_mask ^ board_mask
            first_empty_bit = (empty_bits & -empty_bits).bit_length() - 1

            for p_idx, placement in self.cell_to_options[first_empty_bit]:
                if used_mask & (1 << p_idx):
                    continue
                if placement & board_mask:
                    continue
                if dfs(board_mask | placement, used_mask | (1 << p_idx)):
                    solution.append((p_idx, placement))
                    return True
            return False

        return solution[::-1] if dfs(initial_mask, 0) else None

    # ────────────────────────────  PUBLIC API  ─────────────────────────────
    def _target_mask(self, day: int, month_abbr: str, day_abbr: str) -> int:
        """Bit-mask of squares reserved for date (and blanks)."""
        target = 0
        day_str = str(day)
        for (r, c), bit in self.pos_to_bit.items():
            cell = self.BOARD[r][c]
            if cell in ("", day_str, month_abbr, day_abbr):
                target |= 1 << bit
        return target

    def _mask_to_board(self, moves: List[Tuple[int, int]], target: int) -> List[List[int]]:
        board = [[-2 if not cell else 0] for cell in []]  # dummy for editor lint
        # build fresh board each call
        board = [[-2 if not self.BOARD[r][c] else 0
                  for c in range(len(self.BOARD[0]))]
                 for r in range(len(self.BOARD))]

        # mark target squares
        for bit in range(self.total_bits):
            if target & (1 << bit):
                r, c = self.bit_to_pos[bit]
                if self.BOARD[r][c]:
                    board[r][c] = -1

        # lay pieces
        for p_idx, placement in moves:
            for bit in range(self.total_bits):
                if placement & (1 << bit):
                    r, c = self.bit_to_pos[bit]
                    board[r][c] = p_idx + 1
        return board

    # ─────────────────────────────  USER FACING  ───────────────────────────
    def solve_for_date(self, day: int, month: int, weekday: int) -> List[List[List[int]]]:
        month_abbr = next(k for k, v in self.MONTHS.items() if v == month)
        day_abbr = next(k for k, v in self.DAYS.items() if v == weekday)

        target = self._target_mask(day, month_abbr, day_abbr)
        moves = self._solve_mask(target)
        if moves is None:
            return []
        return [self._mask_to_board(moves, target)]

    # exhaustively solve 2024
    def _valid_dates(self) -> List[Tuple[int, int, int]]:
        out = []
        for m in range(1, 13):
            for d in range(1, self.DAYS_IN_MONTH[m] + 1):
                wd = datetime(2024, m, d).weekday() + 1  # 1-7
                out.append((d, m, wd))
        return out

    def solve_all_dates(self) -> Dict[str, List]:
        res: Dict[str, List] = {}
        for day, month, wd in self._valid_dates():
            month_abbr = next(k for k, v in self.MONTHS.items() if v == month)
            day_abbr = next(k for k, v in self.DAYS.items() if v == wd)
            key = f"{day} {month_abbr} {day_abbr}"
            sols = self.solve_for_date(day, month, wd)
            if sols:
                res[key] = [{"solution_id": 0, "board_state": sols[0]}]
        return res

    def save_solutions_to_json(self, solutions: Dict, filename: str = "dp_calendar_solutions.json") -> None:
        with open(filename, "w", encoding="utf-8") as fh:
            json.dump(solutions, fh, ensure_ascii=False, indent=2)


# ────────────────────────────  CLI HARNESS  ───────────────────────────────
def main() -> None:
    solver = FastCalendarPuzzleSolver()

    print("Fast Calendar Puzzle Solver")
    print("Testing 1 January 2024 …")
    sols = solver.solve_for_date(1, 1, 1)
    if not sols:
        print("❌  No solution found — check piece definitions.")
        return
    print(f"✅  Found {len(sols)} solution(s).")

    if input("Solve the whole year? (y/n): ").strip().lower() == "y":
        all_solutions = solver.solve_all_dates()
        solver.save_solutions_to_json(all_solutions)
        print(f"Done!  Solutions for {len(all_solutions)} distinct dates written to JSON.")


if __name__ == "__main__":
    main()
