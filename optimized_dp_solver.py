#!/usr/bin/env python3

import json
import copy
from typing import List, Tuple, Dict, Set
from datetime import datetime
import time

class OptimizedDPSolver:
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
        
        # Piece definitions (same as original)
        self.pieces = [
            [[1, 0], [1, 0], [1, 0], [1, 1]],  # L shape (4 cells)
            [[1, 1, 0], [0, 1, 0], [0, 1, 1]],  # Z shape (5 cells)
            [[0, 1], [0, 1], [1, 1], [1, 0]],  # L mirrored (4 cells)
            [[1, 1, 1, 1, 1]],  # Straight line (5 cells)
            [[0, 1, 1], [1, 1, 0]],  # Z tetromino (4 cells)
            [[0, 0, 1], [0, 0, 1], [1, 1, 1]],  # L-shaped pentomino (5 cells)
            [[1, 1, 1], [0, 1, 0], [0, 1, 0]],  # T shape (5 cells)
            [[1, 1, 1], [1, 0, 1]],  # T mirrored (5 cells)
            [[1, 1, 1, 1], [0, 0, 1, 0]],  # T-pentomino (5 cells)
            [[0, 1], [1, 1], [1, 1]]  # Skewed block (4 cells)
        ]
        
        # Turkish mappings
        self.months = {
            "OCA": 1, "SUB": 2, "MAR": 3, "NIS": 4, "MAY": 5, "HAZ": 6,
            "TEM": 7, "AGU": 8, "EYL": 9, "EKI": 10, "KAS": 11, "ARA": 12
        }
        
        self.days = {
            "PZT": 1, "SAL": 2, "CAR": 3, "PER": 4, "CUM": 5, "CMT": 6, "PAZ": 7
        }
        
        self.board_height = len(self.board)
        self.board_width = len(self.board[0])
        
        # Create position mapping for valid cells only
        self.valid_positions = []
        self.pos_to_index = {}
        
        for r in range(self.board_height):
            for c in range(self.board_width):
                if self.board[r][c] != "":  # Valid position
                    index = len(self.valid_positions)
                    self.valid_positions.append((r, c))
                    self.pos_to_index[(r, c)] = index
        
        self.total_positions = len(self.valid_positions)
        print(f"Total valid positions: {self.total_positions}")
        
        # Pre-compute piece placements
        self.piece_placements = []
        for piece_idx, piece in enumerate(self.pieces):
            placements = self.compute_piece_placements(piece)
            self.piece_placements.append(placements)
            print(f"Piece {piece_idx + 1}: {len(placements)} possible placements")
        
        # Memoization
        self.memo = {}
        self.cache_hits = 0
        self.cache_misses = 0
    
    def rotate_90(self, piece):
        """Rotate piece 90 degrees clockwise"""
        if not piece or not piece[0]:
            return piece
        rows, cols = len(piece), len(piece[0])
        return [[piece[rows - 1 - j][i] for j in range(rows)] for i in range(cols)]
    
    def flip_horizontal(self, piece):
        """Flip piece horizontally"""
        return [row[::-1] for row in piece]
    
    def generate_orientations(self, piece):
        """Generate all unique orientations of a piece"""
        orientations = set()
        current = copy.deepcopy(piece)
        
        for _ in range(4):  # 4 rotations
            # Add current orientation
            normalized = tuple(tuple(row) for row in current)
            orientations.add(normalized)
            
            # Add horizontal flip
            flipped = self.flip_horizontal(current)
            normalized_flip = tuple(tuple(row) for row in flipped)
            orientations.add(normalized_flip)
            
            current = self.rotate_90(current)
        
        return [list(list(row) for row in orientation) for orientation in orientations]
    
    def piece_to_positions(self, piece):
        """Convert piece to relative position list"""
        positions = []
        for i, row in enumerate(piece):
            for j, cell in enumerate(row):
                if cell == 1:
                    positions.append((i, j))
        return positions
    
    def compute_piece_placements(self, piece):
        """Compute all valid placements for a piece"""
        placements = []
        orientations = self.generate_orientations(piece)
        
        for orientation in orientations:
            piece_positions = self.piece_to_positions(orientation)
            
            # Try all starting positions
            for start_r in range(self.board_height):
                for start_c in range(self.board_width):
                    # Check if piece fits at this position
                    valid_positions = []
                    valid = True
                    
                    for dr, dc in piece_positions:
                        r, c = start_r + dr, start_c + dc
                        
                        # Check bounds
                        if r < 0 or r >= self.board_height or c < 0 or c >= self.board_width:
                            valid = False
                            break
                        
                        # Check if position is valid on board
                        if self.board[r][c] == "":
                            valid = False
                            break
                        
                        # Get position index
                        if (r, c) not in self.pos_to_index:
                            valid = False
                            break
                        
                        valid_positions.append(self.pos_to_index[(r, c)])
                    
                    if valid and valid_positions:
                        # Create bitmask for this placement
                        mask = 0
                        for pos_idx in valid_positions:
                            mask |= (1 << pos_idx)
                        
                        placements.append({
                            'mask': mask,
                            'positions': valid_positions,
                            'start': (start_r, start_c),
                            'piece_positions': piece_positions
                        })
        
        return placements
    
    def create_target_mask(self, day, month_abbr, day_abbr):
        """Create mask for target positions that must remain uncovered"""
        target_mask = 0
        day_str = str(day)
        
        for r in range(self.board_height):
            for c in range(self.board_width):
                cell_value = self.board[r][c]
                if cell_value == day_str or cell_value == month_abbr or cell_value == day_abbr:
                    if (r, c) in self.pos_to_index:
                        pos_idx = self.pos_to_index[(r, c)]
                        target_mask |= (1 << pos_idx)
        
        return target_mask
    
    def solve_recursive(self, covered_mask, used_pieces, target_mask, piece_idx=0):
        """Recursive solver with memoization"""
        # Create cache key
        cache_key = (covered_mask, used_pieces)
        
        if cache_key in self.memo:
            self.cache_hits += 1
            return self.memo[cache_key]
        
        self.cache_misses += 1
        
        # Check if we've used all pieces
        if used_pieces == (1 << len(self.pieces)) - 1:
            # Check if all non-target positions are covered
            required_mask = (1 << self.total_positions) - 1  # All positions
            covered_required = covered_mask | target_mask
            
            if covered_required == required_mask:
                result = [{'covered_mask': covered_mask, 'used_pieces': used_pieces}]
            else:
                result = []
            
            self.memo[cache_key] = result
            return result
        
        # Early termination: if we have covered positions that should be targets
        if covered_mask & target_mask:
            self.memo[cache_key] = []
            return []
        
        solutions = []
        
        # Try each unused piece
        for piece_idx in range(len(self.pieces)):
            if used_pieces & (1 << piece_idx):
                continue  # Piece already used
            
            # Try all placements for this piece
            for placement in self.piece_placements[piece_idx]:
                piece_mask = placement['mask']
                
                # Check if placement conflicts with already covered positions
                if covered_mask & piece_mask:
                    continue  # Overlap with existing pieces
                
                # Check if placement covers target positions
                if piece_mask & target_mask:
                    continue  # Would cover target positions
                
                # Place piece and recurse
                new_covered = covered_mask | piece_mask
                new_used = used_pieces | (1 << piece_idx)
                
                sub_solutions = self.solve_recursive(new_covered, new_used, target_mask, piece_idx + 1)
                
                # Add placement info to solutions
                for sol in sub_solutions:
                    enhanced_sol = sol.copy()
                    enhanced_sol[f'piece_{piece_idx}'] = placement
                    solutions.append(enhanced_sol)
        
        self.memo[cache_key] = solutions
        return solutions
    
    def solve_for_date(self, day, month, weekday):
        """Solve for a specific date"""
        # Convert to abbreviations
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
        
        print(f"Solving for {day} {month_abbr} {day_abbr}...")
        
        # Reset memoization
        self.memo.clear()
        self.cache_hits = 0
        self.cache_misses = 0
        
        # Create target mask
        target_mask = self.create_target_mask(day, month_abbr, day_abbr)
        print(f"Target positions: {bin(target_mask).count('1')}")
        
        start_time = time.time()
        solutions = self.solve_recursive(0, 0, target_mask)
        end_time = time.time()
        
        print(f"Found {len(solutions)} solutions in {end_time - start_time:.3f}s")
        print(f"Cache: {self.cache_hits} hits, {self.cache_misses} misses")
        
        return self.convert_solutions_to_board(solutions, target_mask)
    
    def convert_solutions_to_board(self, solutions, target_mask):
        """Convert solutions back to board format"""
        board_solutions = []
        
        for sol in solutions:
            # Initialize board
            board = [[-2 if self.board[r][c] == "" else 0 for c in range(self.board_width)] 
                    for r in range(self.board_height)]
            
            # Mark targets
            for pos_idx in range(self.total_positions):
                if target_mask & (1 << pos_idx):
                    r, c = self.valid_positions[pos_idx]
                    board[r][c] = -1
            
            # Place pieces
            for piece_idx in range(len(self.pieces)):
                piece_key = f'piece_{piece_idx}'
                if piece_key in sol:
                    placement = sol[piece_key]
                    start_r, start_c = placement['start']
                    
                    for dr, dc in placement['piece_positions']:
                        r, c = start_r + dr, start_c + dc
                        if 0 <= r < self.board_height and 0 <= c < self.board_width:
                            board[r][c] = piece_idx + 1
            
            board_solutions.append(board)
        
        return board_solutions

def main():
    print("🚀 Optimized Dynamic Programming Calendar Puzzle Solver")
    print("=" * 60)
    
    solver = OptimizedDPSolver()
    
    # Test with January 1st, 2024 (Monday)
    print("\n📅 Testing with January 1st, 2024 (Monday)...")
    
    solutions = solver.solve_for_date(1, 1, 1)
    
    if solutions:
        print(f"✅ Success! Found {len(solutions)} solutions")
        
        # Display first solution
        print("\nFirst solution:")
        for row in solutions[0]:
            print(" ".join(f"{cell:>3}" for cell in row))
    else:
        print("❌ No solutions found")
    
    print("\n" + "=" * 60)
    print("Test completed!")

if __name__ == "__main__":
    main() 