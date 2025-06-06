#!/usr/bin/env python3

from calendar_puzzle_solver import CalendarPuzzleSolver
import time

def test_specific_dates():
    """Test the solver on a few specific dates"""
    solver = CalendarPuzzleSolver()
    
    # Test dates: (day, month, weekday)
    test_dates = [
        (1, 1, 1),   # January 1st, Monday (1 OCA PZT)
        (15, 3, 5),  # March 15th, Friday (15 MAR CUM) 
        (25, 12, 3), # December 25th, Wednesday (25 ARA CAR)
    ]
    
    all_test_solutions = {}
    
    for day, month, weekday in test_dates:
        print(f"\n{'='*50}")
        print(f"Testing date: Day {day}, Month {month}, Weekday {weekday}")
        print(f"{'='*50}")
        
        start_time = time.time()
        solutions = solver.solve_for_date(day, month, weekday)
        end_time = time.time()
        
        # Create date key for JSON
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
        
        if month_abbr and day_abbr:
            date_key = f"{day} {month_abbr} {day_abbr}"
            
            if solutions:
                all_test_solutions[date_key] = [
                    {"solution_id": idx, "board_state": solution}
                    for idx, solution in enumerate(solutions)
                ]
                print(f"✅ Found {len(solutions)} solution(s) for {date_key}")
            else:
                print(f"❌ No solutions found for {date_key}")
            
            print(f"⏱️  Time taken: {end_time - start_time:.2f} seconds")
            
            # Display first solution if available
            if solutions:
                print(f"\nFirst solution board state:")
                display_solution(solver, solutions[0], day, month_abbr, day_abbr)
    
    # Save test results
    if all_test_solutions:
        solver.save_solutions_to_json(all_test_solutions, "test_solutions.json")
        print(f"\n✅ Test solutions saved to test_solutions.json")
    
    return all_test_solutions

def display_solution(solver, solution, day, month_abbr, day_abbr):
    """Display a solution in a readable format"""
    print("\nBoard layout with piece placements:")
    print("Legend: -1=target, -2=empty, 0=uncovered, 1-10=piece IDs")
    
    for i, row in enumerate(solution):
        row_display = []
        for j, cell in enumerate(row):
            if cell == -1:
                row_display.append(f"{solver.board[i][j]:>3}")  # Target cells
            elif cell == -2:
                row_display.append("   ")  # Empty cells
            elif cell == 0:
                row_display.append(" ? ")  # Uncovered (shouldn't happen in valid solution)
            else:
                row_display.append(f"P{cell:>2}")  # Piece IDs
        print(" ".join(row_display))
    
    print(f"\nTarget date: {day} {month_abbr} {day_abbr}")

def run_performance_test():
    """Run a simple performance test to estimate time for full solve"""
    solver = CalendarPuzzleSolver()
    
    print("Running performance test on a single date...")
    start_time = time.time()
    
    # Test on January 1st
    solutions = solver.solve_for_date(1, 1, 1)
    
    end_time = time.time()
    elapsed = end_time - start_time
    
    print(f"Time for one date: {elapsed:.2f} seconds")
    print(f"Estimated time for all ~365 dates: {elapsed * 365 / 3600:.1f} hours")
    
    return elapsed

if __name__ == "__main__":
    print("Calendar Puzzle Solver - Test Script")
    print("=" * 50)
    
    # Run performance test first
    run_performance_test()
    
    print("\n" + "=" * 50)
    print("Testing specific dates...")
    
    # Test specific dates
    test_results = test_specific_dates()
    
    print("\n" + "=" * 50)
    print("Test completed!")
    
    if test_results:
        print(f"Found solutions for {len(test_results)} test dates")
    else:
        print("No solutions found for any test dates")
        print("This might indicate an issue with the solver logic or piece definitions.") 