#!/usr/bin/env python3

import datetime

def test_weekday_calculation():
    """Test if our weekday calculation is correct"""
    print("=== WEEKDAY CALCULATION TEST ===")
    
    # Test a few known dates
    test_dates = [
        (2024, 1, 1),   # January 1, 2024 - Monday
        (2024, 3, 15),  # March 15, 2024 - Friday
        (2024, 12, 25), # December 25, 2024 - Wednesday
    ]
    
    for year, month, day in test_dates:
        date = datetime.datetime(year, month, day)
        weekday_python = date.weekday()  # 0=Monday, 6=Sunday
        weekday_corrected = weekday_python + 1  # 1=Monday, 7=Sunday
        
        weekday_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        weekday_name = weekday_names[weekday_python]
        
        print(f"{year}-{month:02d}-{day:02d}: {weekday_name} (weekday={weekday_corrected})")

def test_board_setup():
    """Test basic board setup"""
    print("\n=== BOARD SETUP TEST ===")
    
    board = [
        ["1",  "2",  "3",  "4",  "OCA", "♥",  "PZT"],   # Row 0
        ["5",  "6",  "7",  "8",  "SUB", "MAR", "SAL"],   # Row 1
        ["9",  "10", "11", "12", "NIS", "MAY", "CAR"],   # Row 2
        ["13", "14", "15", "16", "HAZ", "TEM", "PER"],   # Row 3
        ["17", "18", "19", "20", "AGU", "EYL", "CUM"],   # Row 4
        ["21", "22", "23", "24", "EKI", "KAS", "CMT"],   # Row 5
        ["25", "26", "27", "28", "ARA", "♥",  "PAZ"],   # Row 6
        ["29", "30", "31", "",   "",    "",    ""]       # Row 7
    ]
    
    print("Board layout:")
    for i, row in enumerate(board):
        print(f"Row {i}: {row}")
    
    # Test finding specific values
    test_values = ["1", "15", "OCA", "MAR", "PZT", "CUM"]
    
    for value in test_values:
        positions = []
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == value:
                    positions.append((i, j))
        print(f"'{value}' found at: {positions}")

def test_mappings():
    """Test month and day mappings"""
    print("\n=== MAPPING TEST ===")
    
    months = {
        "OCA": 1, "SUB": 2, "MAR": 3, "NIS": 4, "MAY": 5, "HAZ": 6,
        "TEM": 7, "AGU": 8, "EYL": 9, "EKI": 10, "KAS": 11, "ARA": 12
    }
    
    days = {
        "PZT": 1, "SAL": 2, "CAR": 3, "PER": 4, "CUM": 5, "CMT": 6, "PAZ": 7
    }
    
    print("Month mappings:")
    for abbr, num in months.items():
        print(f"  {abbr} -> {num}")
    
    print("\nDay mappings:")
    for abbr, num in days.items():
        print(f"  {abbr} -> {num}")
    
    # Test a specific date conversion
    day = 15
    month = 3  # March
    weekday = 5  # Friday
    
    month_abbr = None
    day_abbr = None
    
    for abbr, num in months.items():
        if num == month:
            month_abbr = abbr
            break
    
    for abbr, num in days.items():
        if num == weekday:
            day_abbr = abbr
            break
    
    print(f"\nExample conversion:")
    print(f"Day {day}, Month {month}, Weekday {weekday}")
    print(f"Converts to: {day} {month_abbr} {day_abbr}")

def test_piece_shapes():
    """Test piece definitions"""
    print("\n=== PIECE SHAPES TEST ===")
    
    pieces = [
        # 1. L shape
        [
            [1, 0],
            [1, 0],
            [1, 0],
            [1, 1]
        ],
        
        # 2. Z shape
        [
            [1, 1, 0],
            [0, 1, 0],
            [0, 1, 1]
        ],
    ]
    
    for i, piece in enumerate(pieces):
        print(f"\nPiece {i+1}:")
        for row in piece:
            print("  " + " ".join("█" if cell else "." for cell in row))
        
        # Count cells
        cell_count = sum(sum(row) for row in piece)
        print(f"  Total cells: {cell_count}")

if __name__ == "__main__":
    print("Simple Validation Tests")
    print("=" * 40)
    
    test_weekday_calculation()
    test_board_setup()
    test_mappings()
    test_piece_shapes()
    
    print("\n" + "=" * 40)
    print("Validation completed!") 