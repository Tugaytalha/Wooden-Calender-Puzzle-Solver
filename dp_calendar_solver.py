#!/usr/bin/env python3

import json
import copy
from typing import List, Tuple, Dict, Set, Optional
from datetime import datetime
import functools

class DPCalendarPuzzleSolver:
    def __init__(self):
        # Game board layout
        self.board = [
            ["1",  "2",  "3",  "4",  "OCA", "♥",  "PZT"],   # Row 0
            ["5",  "6",  "7",  "8",  "SUB", "MAR", "SAL"],   # Row 1
            ["9",  "10", "11", "12", "NIS", "MAY", "CAR"],   # Row 2
            ["13", "14", "15", "16", "HAZ", "TEM", "PER"],   # Row 3
            ["17", "18", "19", "20", "AGU", "EYL", "CUM"],   # Row 4
            ["21", "22", "23", "24", "EKI", "KAS", "CMT"],   # Row 5
            ["25", "26", "27", "28", "ARA", "♥",  "PAZ"],   # Row 6
            ["29", "30", "31", "",   "",    "",    ""]       # Row 7
        ]
        
        # Original pieces
        self.pieces = [
            # 1. L shape (4 cells)
            [
                [1, 0],
                [1, 0],
                [1, 0],
                [1, 1]
            ],
            # 2. Z shape (5 cells)
            [
                [1, 1, 0],
                [0, 1, 0],
                [0, 1, 1]
            ],
            # 3. L mirrored (4 cells)
            [
                [0, 1],
                [0, 1],
                [1, 1],
                [1, 0]
            ],
            # 4. Straight line (5 cells)
            [
                [1, 1, 1, 1, 1]
            ],
            # 5. Z tetromino (4 cells)
            [
                [0, 1, 1],
                [1, 1, 0]
            ],
            # 6. L-shaped pentomino (5 cells)
            [
                [0, 0, 1],
                [0, 0, 1],
                [1, 1, 1]
            ],
            # 7. T shape (5 cells)
            [
                [1, 1, 1],
                [0, 1, 0],
                [0, 1, 0]
            ],
            # 8. T mirrored (5 cells)
            [
                [1, 1, 1],
                [1, 0, 1]
            ],
            # 9. T-pentomino (5 cells)
            [
                [1, 1, 1, 1],
                [0, 0, 1, 0]
            ],
            # 10. Skewed block (4 cells)
            [
                [0, 1],
                [1, 1],
                [1, 1]
            ]
        ]
        
        # Turkish month and day mappings
        self.months = {
            "OCA": 1, "SUB": 2, "MAR": 3, "NIS": 4, "MAY": 5, "HAZ": 6,
            "TEM": 7, "AGU": 8, "EYL": 9, "EKI": 10, "KAS": 11, "ARA": 12
        }
        
        self.days = {
            "PZT": 1, "SAL": 2, "CAR": 3, "PER": 4, "CUM": 5, "CMT": 6, "PAZ": 7
        }
        
        self.days_in_month = {
            1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
            7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
        }
        
        self.board_height = len(self.board)
        self.board_width = len(self.board[0])
        
        # Pre-compute piece orientations and bit representations
        self.all_piece_orientations = []
        self.piece_bit_patterns = []
        
        for piece in self.pieces:
            orientations = self.generate_all_orientations(piece)
            self.all_piece_orientations.append(orientations)
            
            # Convert orientations to bit patterns for efficiency
            bit_patterns = []
            for orientation in orientations:
                bit_patterns.append(self.piece_to_positions(orientation))
            self.piece_bit_patterns.append(bit_patterns)
        
        # Create mapping from (row, col) to bit position
        self.pos_to_bit = {}
        self.bit_to_pos = {}
        bit_index = 0
        
        for r in range(self.board_height):
            for c in range(self.board_width):
                if self.board[r][c] != "":  # Only valid board positions
                    self.pos_to_bit[(r, c)] = bit_index
                    self.bit_to_pos[bit_index] = (r, c)
                    bit_index += 1
        
        self.total_bits = bit_index
        
        # Memoization cache
        self.memo = {}
        
        # Statistics
        self.cache_hits = 0
        self.cache_misses = 0
    
    def rotate_90(self, piece: List[List[int]]) -> List[List[int]]:
        """Rotate piece 90 degrees clockwise"""
        if not piece or not piece[0]:
            return piece
        rows, cols = len(piece), len(piece[0])
        rotated = [[0] * rows for _ in range(cols)]
        for i in range(rows):
            for j in range(cols):
                rotated[j][rows - 1 - i] = piece[i][j]
        return rotated
    
    def flip_horizontal(self, piece: List[List[int]]) -> List[List[int]]:
        """Flip piece horizontally"""
        return [row[::-1] for row in piece]
    
    def flip_vertical(self, piece: List[List[int]]) -> List[List[int]]:
        """Flip piece vertically"""
        return piece[::-1]
    
    def normalize_piece(self, piece: List[List[int]]) -> tuple:
        """Convert piece to a normalized tuple for comparison"""
        return tuple(tuple(row) for row in piece)
    
    def generate_all_orientations(self, piece: List[List[int]]) -> List[List[List[int]]]:
        """Generate all unique rotations and reflections of a piece"""
        orientations = set()
        current = copy.deepcopy(piece)
        
        # Generate all combinations of rotations and reflections
        for _ in range(4):  # 4 rotations
            orientations.add(self.normalize_piece(current))
            
            # Add horizontal flip
            flipped_h = self.flip_horizontal(current)
            orientations.add(self.normalize_piece(flipped_h))
            
            # Add vertical flip
            flipped_v = self.flip_vertical(current)
            orientations.add(self.normalize_piece(flipped_v))
            
            # Add both flips
            flipped_both = self.flip_horizontal(self.flip_vertical(current))
            orientations.add(self.normalize_piece(flipped_both))
            
            current = self.rotate_90(current)
        
        # Convert back to list format
        return [list(list(row) for row in orientation) for orientation in orientations]
    
    def piece_to_positions(self, piece: List[List[int]]) -> List[Tuple[int, int]]:
        """Convert piece to list of relative positions"""
        positions = []
        for i, row in enumerate(piece):
            for j, cell in enumerate(row):
                if cell == 1:
                    positions.append((i, j))
        return positions
    
    def can_place_piece_at(self, board_mask: int, piece_positions: List[Tuple[int, int]], 
                          start_row: int, start_col: int) -> Tuple[bool, int]:
        """Check if piece can be placed and return the resulting board mask"""
        new_mask = 0
        
        for dr, dc in piece_positions:
            r, c = start_row + dr, start_col + dc
            
            # Check bounds
            if r < 0 or r >= self.board_height or c < 0 or c >= self.board_width:
                return False, 0
            
            # Check if position is valid on board
            if self.board[r][c] == "":
                return False, 0
            
            # Check if position is available
            bit_pos = self.pos_to_bit.get((r, c))
            if bit_pos is None:
                return False, 0
            
            if board_mask & (1 << bit_pos):
                return False, 0  # Position already occupied
            
            new_mask |= (1 << bit_pos)
        
        return True, new_mask
    
    def board_to_mask(self, board_state: List[List[int]], target_mask: int) -> int:
        """Convert board state to bit mask (excluding targets)"""
        mask = 0
        for r in range(self.board_height):
            for c in range(self.board_width):
                if board_state[r][c] > 0:  # Occupied by piece
                    bit_pos = self.pos_to_bit.get((r, c))
                    if bit_pos is not None:
                        mask |= (1 << bit_pos)
        return mask | target_mask
    
    def create_target_mask(self, day: int, month_abbr: str, day_abbr: str) -> int:
        """Create bit mask for target positions"""
        target_mask = 0
        day_str = str(day)
        
        for r in range(self.board_height):
            for c in range(self.board_width):
                cell_value = self.board[r][c]
                if cell_value == day_str or cell_value == month_abbr or cell_value == day_abbr:
                    bit_pos = self.pos_to_bit.get((r, c))
                    if bit_pos is not None:
                        target_mask |= (1 << bit_pos)
        
        # Also mark empty cells
        for r in range(self.board_height):
            for c in range(self.board_width):
                if self.board[r][c] == "":
                    bit_pos = self.pos_to_bit.get((r, c))
                    if bit_pos is not None:
                        target_mask |= (1 << bit_pos)
        
        return target_mask
    
    def solve_dp(self, board_mask: int, used_pieces: int, target_mask: int) -> List[Dict[str, any]]:
        """Dynamic programming solver with memoization"""
        # Create cache key
        cache_key = (board_mask, used_pieces)
        
        if cache_key in self.memo:
            self.cache_hits += 1
            return self.memo[cache_key]
        
        self.cache_misses += 1
        
        # Check if all pieces are used
        if used_pieces == (1 << len(self.pieces)) - 1:
            # Check if board is complete (all non-target positions covered)
            full_mask = (1 << self.total_bits) - 1
            if board_mask == full_mask:
                result = [{"board_mask": board_mask, "used_pieces": used_pieces}]
            else:
                result = []
            self.memo[cache_key] = result
            return result
        
        solutions = []
        
        # Try each unused piece
        for piece_idx in range(len(self.pieces)):
            if used_pieces & (1 << piece_idx):
                continue  # Piece already used
            
            # Try all orientations of this piece
            for pattern_idx, piece_positions in enumerate(self.piece_bit_patterns[piece_idx]):
                # Try all positions on the board
                for start_row in range(self.board_height):
                    for start_col in range(self.board_width):
                        can_place, piece_mask = self.can_place_piece_at(
                            board_mask, piece_positions, start_row, start_col
                        )
                        
                        if can_place:
                            new_board_mask = board_mask | piece_mask
                            new_used_pieces = used_pieces | (1 << piece_idx)
                            
                            # Recurse
                            sub_solutions = self.solve_dp(new_board_mask, new_used_pieces, target_mask)
                            
                            # Add current placement info to solutions
                            for sol in sub_solutions:
                                enhanced_sol = sol.copy()
                                enhanced_sol[f"piece_{piece_idx}"] = {
                                    "position": (start_row, start_col),
                                    "orientation": pattern_idx,
                                    "mask": piece_mask
                                }
                                solutions.append(enhanced_sol)
        
        # Cache and return results
        self.memo[cache_key] = solutions
        return solutions
    
    def mask_to_board(self, solutions: List[Dict], target_mask: int) -> List[List[List[int]]]:
        """Convert bit mask solutions back to board representation"""
        board_solutions = []
        
        for sol in solutions:
            board = [[-2 if self.board[r][c] == "" else 0 for c in range(self.board_width)] 
                    for r in range(self.board_height)]
            
            # Mark target positions
            for bit_pos in range(self.total_bits):
                if target_mask & (1 << bit_pos):
                    r, c = self.bit_to_pos[bit_pos]
                    if self.board[r][c] != "":  # Not an empty cell
                        board[r][c] = -1
            
            # Place pieces
            for piece_idx in range(len(self.pieces)):
                piece_key = f"piece_{piece_idx}"
                if piece_key in sol:
                    piece_info = sol[piece_key]
                    start_row, start_col = piece_info["position"]
                    orientation_idx = piece_info["orientation"]
                    
                    piece_positions = self.piece_bit_patterns[piece_idx][orientation_idx]
                    
                    for dr, dc in piece_positions:
                        r, c = start_row + dr, start_col + dc
                        if 0 <= r < self.board_height and 0 <= c < self.board_width:
                            board[r][c] = piece_idx + 1
            
            board_solutions.append(board)
        
        return board_solutions
    
    def solve_for_date(self, day: int, month: int, weekday: int) -> List[List[List[int]]]:
        """Solve puzzle for a specific date using dynamic programming"""
        # Convert month and weekday to abbreviations
        month_abbr = None
        day_abbr = None
        
        for abbr, num in self.months.items():
            if num == month:
                month_abbr = abbr
                break
        
        for abbr, num in self.days.items():
            if num == weekday:
                day_abbr = abbr
                break
        
        if not month_abbr or not day_abbr:
            return []
        
        print(f"Solving for {day} {month_abbr} {day_abbr} using Dynamic Programming...")
        
        # Reset cache for each solve
        self.memo.clear()
        self.cache_hits = 0
        self.cache_misses = 0
        
        # Create target mask
        target_mask = self.create_target_mask(day, month_abbr, day_abbr)
        
        # Solve using DP
        solutions = self.solve_dp(target_mask, 0, target_mask)
        
        print(f"Found {len(solutions)} solution(s) for {day} {month_abbr} {day_abbr}")
        print(f"Cache stats: {self.cache_hits} hits, {self.cache_misses} misses")
        print(f"Cache hit ratio: {self.cache_hits/(self.cache_hits + self.cache_misses)*100:.1f}%")
        
        # Convert back to board representation
        board_solutions = self.mask_to_board(solutions, target_mask)
        
        return board_solutions
    
    def generate_valid_dates(self) -> List[Tuple[int, int, int]]:
        """Generate all valid date combinations"""
        valid_dates = []
        
        for month in range(1, 13):
            max_day = self.days_in_month[month]
            for day in range(1, max_day + 1):
                try:
                    current_date = datetime(2024, month, day)
                    weekday = current_date.weekday() + 1  # Convert to 1-7
                    valid_dates.append((day, month, weekday))
                except ValueError:
                    continue
        
        return valid_dates
    
    def solve_all_dates(self) -> Dict[str, List]:
        """Solve puzzle for all valid dates and return results"""
        valid_dates = self.generate_valid_dates()
        all_solutions = {}
        
        total_dates = len(valid_dates)
        print(f"Solving for {total_dates} dates using Dynamic Programming...")
        
        for i, (day, month, weekday) in enumerate(valid_dates):
            # Create date key
            month_abbr = None
            day_abbr = None
            
            for abbr, num in self.months.items():
                if num == month:
                    month_abbr = abbr
                    break
            
            for abbr, num in self.days.items():
                if num == weekday:
                    day_abbr = abbr
                    break
            
            if month_abbr and day_abbr:
                date_key = f"{day} {month_abbr} {day_abbr}"
                solutions = self.solve_for_date(day, month, weekday)
                
                if solutions:
                    # Convert solutions to JSON-friendly format
                    all_solutions[date_key] = [
                        {"solution_id": idx, "board_state": solution}
                        for idx, solution in enumerate(solutions)
                    ]
                
                print(f"Progress: {i+1}/{total_dates} ({((i+1)/total_dates*100):.1f}%)")
        
        return all_solutions
    
    def save_solutions_to_json(self, solutions: Dict, filename: str = "dp_calendar_solutions.json"):
        """Save all solutions to a JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(solutions, f, ensure_ascii=False, indent=2)
        print(f"Solutions saved to {filename}")

def main():
    solver = DPCalendarPuzzleSolver()
    
    print("Starting Dynamic Programming Calendar Puzzle Solver...")
    print("This should be significantly faster than the brute-force approach!")
    
    # Test with a specific date first
    print("\nTesting with January 1st...")
    test_solutions = solver.solve_for_date(1, 1, 1)
    
    if test_solutions:
        print(f"✅ Test successful! Found {len(test_solutions)} solutions.")
        
        # Optionally solve all dates
        response = input("\nSolve for all dates? (y/n): ")
        if response.lower() == 'y':
            all_solutions = solver.solve_all_dates()
            solver.save_solutions_to_json(all_solutions)
            print(f"Complete! Found solutions for {len(all_solutions)} different dates.")
        else:
            print("Test completed. Run with all dates when ready!")
    else:
        print("❌ No solutions found for test date. Please check piece definitions.")

if __name__ == "__main__":
    main() 