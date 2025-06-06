import json
import copy
from typing import List, Tuple, Dict, Set
from datetime import datetime, timedelta
import itertools

class CalendarPuzzleSolver:
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
            # 1. Top left (L shape)
            [
                [1, 0],
                [1, 0],
                [1, 0],
                [1, 1]
            ],

            # 2. Second down, left column (Z shape)
            [
                [1, 1, 0],
                [0, 1, 0],
                [0, 1, 1]
            ],

            # 3. Third down, left column (L mirrored)
            [
                [0, 1],
                [0, 1],
                [1, 1],
                [1, 0]
            ],

            # 4. Straight line (I pentomino)
            [
                [1, 1, 1, 1, 1]
            ],

            # 5. Z tetromino
            [
                [0, 1, 1],
                [1, 1, 0]
            ],

            # 6. L-shaped pentomino (shorter version)
            [
                [0, 0, 1],
                [0, 0, 1],
                [1, 1, 1]
            ],

            # 7. T shape
            [
                [1, 1, 1],
                [0, 1, 0],
                [0, 1, 0]
            ],

            # 8. T mirrored
            [
                [1, 1, 1],
                [1, 0, 1]
            ],

            # 9. T-pentomino (flat-top)
            [
                [1, 1, 1, 1],
                [0, 0, 1, 0]
            ],

            # 10. Skewed block (fat L shape)
            [
                [0, 1],
                [1, 1],
                [1, 1]
            ]
        ]
        
        # Turkish month abbreviations mapping
        self.months = {
            "OCA": 1, "SUB": 2, "MAR": 3, "NIS": 4, "MAY": 5, "HAZ": 6,
            "TEM": 7, "AGU": 8, "EYL": 9, "EKI": 10, "KAS": 11, "ARA": 12
        }
        
        # Turkish day abbreviations mapping  
        self.days = {
            "PZT": 1, "SAL": 2, "CAR": 3, "PER": 4, "CUM": 5, "CMT": 6, "PAZ": 7
        }
        
        # Days in each month (non-leap year)
        self.days_in_month = {
            1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
            7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
        }
        
        self.board_height = len(self.board)
        self.board_width = len(self.board[0])
        
        # Pre-generate all piece orientations
        self.all_piece_orientations = []
        for piece in self.pieces:
            orientations = self.generate_all_orientations(piece)
            self.all_piece_orientations.append(orientations)
    
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
    
    def can_place_piece(self, board_state: List[List[int]], piece: List[List[int]], 
                       start_row: int, start_col: int) -> bool:
        """Check if a piece can be placed at the given position"""
        piece_height = len(piece)
        piece_width = len(piece[0]) if piece else 0
        
        if start_row + piece_height > self.board_height or start_col + piece_width > self.board_width:
            return False
        
        for i in range(piece_height):
            for j in range(piece_width):
                if piece[i][j] == 1:
                    if board_state[start_row + i][start_col + j] != 0:
                        return False
        
        return True
    
    def place_piece(self, board_state: List[List[int]], piece: List[List[int]], 
                   start_row: int, start_col: int, piece_id: int) -> None:
        """Place a piece on the board"""
        piece_height = len(piece)
        piece_width = len(piece[0]) if piece else 0
        
        for i in range(piece_height):
            for j in range(piece_width):
                if piece[i][j] == 1:
                    board_state[start_row + i][start_col + j] = piece_id
    
    def remove_piece(self, board_state: List[List[int]], piece: List[List[int]], 
                    start_row: int, start_col: int) -> None:
        """Remove a piece from the board"""
        piece_height = len(piece)
        piece_width = len(piece[0]) if piece else 0
        
        for i in range(piece_height):
            for j in range(piece_width):
                if piece[i][j] == 1:
                    board_state[start_row + i][start_col + j] = 0
    
    def find_target_positions(self, day: int, month_abbr: str, day_abbr: str) -> List[Tuple[int, int]]:
        """Find positions of target day, month, and day of week on the board"""
        targets = []
        day_str = str(day)
        
        for i in range(self.board_height):
            for j in range(self.board_width):
                cell_value = self.board[i][j]
                if cell_value == day_str or cell_value == month_abbr or cell_value == day_abbr:
                    targets.append((i, j))
        
        return targets
    
    def create_initial_board_state(self, day: int, month_abbr: str, day_abbr: str) -> List[List[int]]:
        """Create initial board state with target positions marked as uncoverable"""
        board_state = [[0 for _ in range(self.board_width)] for _ in range(self.board_height)]
        target_positions = self.find_target_positions(day, month_abbr, day_abbr)
        
        # Mark target positions as -1 (uncoverable)
        for row, col in target_positions:
            board_state[row][col] = -1
        
        # Mark empty cells as already covered
        for i in range(self.board_height):
            for j in range(self.board_width):
                if self.board[i][j] == "":
                    board_state[i][j] = -2  # Empty cell marker
        
        return board_state
    
    def is_board_complete(self, board_state: List[List[int]]) -> bool:
        """Check if all cells are covered except targets"""
        for i in range(self.board_height):
            for j in range(self.board_width):
                if board_state[i][j] == 0:  # Uncovered non-target cell
                    return False
        return True
    
    def solve_backtrack(self, board_state: List[List[int]], piece_index: int, 
                       used_pieces: Set[int]) -> List[Dict]:
        """Backtracking solver that returns all solutions"""
        if piece_index == len(self.pieces):
            if self.is_board_complete(board_state):
                return [copy.deepcopy(board_state)]
            else:
                return []
        
        if piece_index in used_pieces:
            return self.solve_backtrack(board_state, piece_index + 1, used_pieces)
        
        solutions = []
        
        # Try all orientations of the current piece
        for orientation in self.all_piece_orientations[piece_index]:
            # Try all positions on the board
            for row in range(self.board_height):
                for col in range(self.board_width):
                    if self.can_place_piece(board_state, orientation, row, col):
                        # Place the piece
                        self.place_piece(board_state, orientation, row, col, piece_index + 1)
                        used_pieces.add(piece_index)
                        
                        # Recurse
                        sub_solutions = self.solve_backtrack(board_state, piece_index + 1, used_pieces)
                        solutions.extend(sub_solutions)
                        
                        # Backtrack
                        used_pieces.remove(piece_index)
                        self.remove_piece(board_state, orientation, row, col)
        
        return solutions
    
    def solve_for_date(self, day: int, month: int, weekday: int) -> List[List[List[int]]]:
        """Solve puzzle for a specific date"""
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
        
        print(f"Solving for {day} {month_abbr} {day_abbr}...")
        
        board_state = self.create_initial_board_state(day, month_abbr, day_abbr)
        solutions = self.solve_backtrack(board_state, 0, set())
        
        print(f"Found {len(solutions)} solution(s) for {day} {month_abbr} {day_abbr}")
        return solutions
    
    def generate_valid_dates(self) -> List[Tuple[int, int, int]]:
        """Generate all valid date combinations (day, month, weekday)"""
        valid_dates = []
        
        # For simplicity, we'll generate dates for a specific year (2024)
        # and extract the weekday for each date
        for month in range(1, 13):
            max_day = self.days_in_month[month]
            for day in range(1, max_day + 1):
                try:
                    current_date = datetime(2024, month, day)
                    # Fix weekday calculation: Python's weekday() returns 0-6 (Mon-Sun)
                    # We need 1-7 (Mon=1, Tue=2, ..., Sun=7)
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
        print(f"Solving for {total_dates} dates...")
        
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
                    # Convert solutions to a more JSON-friendly format
                    all_solutions[date_key] = [
                        {"solution_id": idx, "board_state": solution}
                        for idx, solution in enumerate(solutions)
                    ]
                
                print(f"Progress: {i+1}/{total_dates} ({((i+1)/total_dates*100):.1f}%)")
        
        return all_solutions
    
    def save_solutions_to_json(self, solutions: Dict, filename: str = "calendar_puzzle_solutions.json"):
        """Save all solutions to a JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(solutions, f, ensure_ascii=False, indent=2)
        print(f"Solutions saved to {filename}")

def main():
    solver = CalendarPuzzleSolver()
    
    print("Starting Calendar Puzzle Solver...")
    print("This may take a very long time due to the brute-force nature of the algorithm.")
    print("Consider running this on a subset of dates first for testing.")
    
    # For testing, you might want to solve just a few specific dates first
    # test_solutions = solver.solve_for_date(15, 3, 5)  # March 15th, Friday
    
    # Solve for all dates (this will take a very long time!)
    all_solutions = solver.solve_all_dates()
    
    # Save to JSON
    solver.save_solutions_to_json(all_solutions)
    
    print(f"Complete! Found solutions for {len(all_solutions)} different dates.")

if __name__ == "__main__":
    main() 