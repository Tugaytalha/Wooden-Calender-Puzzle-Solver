#!/usr/bin/env python3

from calendar_puzzle_solver import CalendarPuzzleSolver
import time

def debug_board_and_pieces():
    """Debug the board layout and piece orientations"""
    solver = CalendarPuzzleSolver()
    
    print("=== BOARD LAYOUT ===")
    for i, row in enumerate(solver.board):
        print(f"Row {i}: {row}")
    
    print(f"\nBoard dimensions: {solver.board_height}x{solver.board_width}")
    
    print("\n=== PIECE INFORMATION ===")
    for i, piece in enumerate(solver.pieces):
        print(f"\nPiece {i+1}:")
        for row in piece:
            print("  " + " ".join("█" if cell else "." for cell in row))
        
        orientations = solver.all_piece_orientations[i]
        print(f"  Total orientations: {len(orientations)}")
    
    print("\n=== MONTH MAPPINGS ===")
    for abbr, num in solver.months.items():
        print(f"{abbr} -> {num}")
    
    print("\n=== DAY MAPPINGS ===")
    for abbr, num in solver.days.items():
        print(f"{abbr} -> {num}")

def debug_date_setup(day, month, weekday):
    """Debug the setup for a specific date"""
    solver = CalendarPuzzleSolver()
    
    # Convert to abbreviations
    month_abbr = None
    day_abbr = None
    
    for abbr, num in solver.months.items():
        if num == month:
            month_abbr = abbr
            break
    
    for abbr, num in solver.days.items():
        if num == weekday:
            day_abbr = abbr
            break
    
    print(f"\n=== DATE SETUP DEBUG ===")
    print(f"Input: Day {day}, Month {month}, Weekday {weekday}")
    print(f"Converted: {day} {month_abbr} {day_abbr}")
    
    # Find target positions
    targets = solver.find_target_positions(day, month_abbr, day_abbr)
    print(f"Target positions: {targets}")
    
    # Show initial board state
    board_state = solver.create_initial_board_state(day, month_abbr, day_abbr)
    print(f"\nInitial board state:")
    for i, row in enumerate(board_state):
        row_display = []
        for j, cell in enumerate(row):
            if cell == -1:
                row_display.append(f"{solver.board[i][j]:>3}")  # Target
            elif cell == -2:
                row_display.append("  .")  # Empty
            else:
                row_display.append(f"{cell:>3}")  # Normal
        print(" ".join(row_display))
    
    return solver, board_state, month_abbr, day_abbr

def test_piece_placement():
    """Test basic piece placement functionality"""
    solver = CalendarPuzzleSolver()
    
    print("\n=== PIECE PLACEMENT TEST ===")
    
    # Create empty board
    board_state = [[0 for _ in range(solver.board_width)] for _ in range(solver.board_height)]
    
    # Try to place first piece in first orientation at position (0,0)
    piece = solver.all_piece_orientations[0][0]  # First orientation of first piece
    
    print("Testing piece:")
    for row in piece:
        print("  " + " ".join("█" if cell else "." for cell in row))
    
    can_place = solver.can_place_piece(board_state, piece, 0, 0)
    print(f"Can place at (0,0): {can_place}")
    
    if can_place:
        solver.place_piece(board_state, piece, 0, 0, 1)
        print("Board after placement:")
        for row in board_state:
            print("  " + " ".join(f"{cell:2}" for cell in row))
        
        solver.remove_piece(board_state, piece, 0, 0)
        print("Board after removal:")
        for row in board_state:
            print("  " + " ".join(f"{cell:2}" for cell in row))

def quick_solve_test():
    """Try a very quick solve with limited search"""
    solver = CalendarPuzzleSolver()
    
    print("\n=== QUICK SOLVE TEST ===")
    
    # Test with a simple date - January 1st
    day, month, weekday = 1, 1, 1  # Assuming Monday
    
    solver_obj, board_state, month_abbr, day_abbr = debug_date_setup(day, month, weekday)
    
    print(f"\nAttempting to solve {day} {month_abbr} {day_abbr}...")
    
    # Try just the first few pieces to see if placement works
    solutions = []
    
    def limited_backtrack(board_state, piece_index, max_pieces=3):
        """Limited backtracking for testing"""
        if piece_index >= max_pieces:
            return [board_state.copy()]
        
        if piece_index >= len(solver.pieces):
            return []
        
        solutions = []
        
        # Try first few orientations only
        orientations_to_try = solver.all_piece_orientations[piece_index][:2]
        
        for orientation in orientations_to_try:
            # Try just a few positions
            for row in range(min(3, solver.board_height)):
                for col in range(min(3, solver.board_width)):
                    if solver.can_place_piece(board_state, orientation, row, col):
                        # Place piece
                        solver.place_piece(board_state, orientation, row, col, piece_index + 1)
                        
                        # Recurse
                        sub_solutions = limited_backtrack([row[:] for row in board_state], piece_index + 1, max_pieces)
                        solutions.extend(sub_solutions)
                        
                        # Remove piece
                        solver.remove_piece(board_state, orientation, row, col)
                        
                        # Limit solutions to avoid too much output
                        if len(solutions) > 2:
                            return solutions
        
        return solutions
    
    start_time = time.time()
    test_solutions = limited_backtrack([row[:] for row in board_state], 0, 3)
    end_time = time.time()
    
    print(f"Limited test found {len(test_solutions)} partial solutions in {end_time - start_time:.3f} seconds")
    
    if test_solutions:
        print("First partial solution:")
        for row in test_solutions[0]:
            print("  " + " ".join(f"{cell:2}" for cell in row))

if __name__ == "__main__":
    print("Calendar Puzzle Solver - Debug Script")
    print("=" * 50)
    
    # Debug basic setup
    debug_board_and_pieces()
    
    # Debug date setup
    debug_date_setup(1, 1, 1)
    
    # Test piece placement
    test_piece_placement()
    
    # Quick solve test
    quick_solve_test()
    
    print("\n" + "=" * 50)
    print("Debug completed!") 