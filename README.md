# Wooden Calendar Puzzle Solver

A comprehensive brute-force solver for the wooden calendar puzzle game, implemented in Python.

## What is the Wooden Calendar Puzzle?

This is a wooden calendar puzzle game with:
- A 7×8 wooden board with numbered squares (1-31), Turkish month abbreviations, and Turkish day abbreviations
- 10 wooden pieces of different shapes (similar to Tetris pieces)
- The goal is to place all pieces to cover the board except for today's date (day number + month + day of week)

## Board Layout

```
   C0   C1   C2   C3   C4    C5   C6
R0  1    2    3    4   OCA   ♥   PZT    
R1  5    6    7    8   SUB  MAR  SAL    
R2  9   10   11   12   NIS  MAY  CAR    
R3 13   14   15   16   HAZ  TEM  PER    
R4 17   18   19   20   AGU  EYL  CUM    
R5 21   22   23   24   EKI  KAS  CMT    
R6 25   26   27   28   ARA   ♥   PAZ    
R7 29   30   31   --    --   --   --    
```

### Turkish Abbreviations

**Months (Aylar):**
- OCA = Ocak (January)
- SUB = Şubat (February) 
- MAR = Mart (March)
- NIS = Nisan (April)
- MAY = Mayıs (May)
- HAZ = Haziran (June)
- TEM = Temmuz (July)
- AGU = Ağustos (August)
- EYL = Eylül (September)
- EKI = Ekim (October)
- KAS = Kasım (November)
- ARA = Aralık (December)

**Days of Week (Haftanın Günleri):**
- PZT = Pazartesi (Monday)
- SAL = Salı (Tuesday)
- CAR = Çarşamba (Wednesday)
- PER = Perşembe (Thursday)
- CUM = Cuma (Friday)
- CMT = Cumartesi (Saturday)
- PAZ = Pazar (Sunday)

## Puzzle Pieces

The solver includes 10 different shaped pieces:

1. **L-shape** (4 cells)
2. **Z-shape** (5 cells)
3. **Mirrored L** (4 cells)  
4. **Straight line** (5 cells)
5. **Z tetromino** (4 cells)
6. **L-shaped pentomino** (5 cells)
7. **T-shape** (5 cells)
8. **T mirrored** (5 cells)
9. **T-pentomino** (5 cells)
10. **Skewed block** (4 cells)

All pieces can be rotated (0°, 90°, 180°, 270°) and flipped horizontally/vertically.

## Features

- **Brute-force solver**: Finds all possible solutions for any given date
- **Piece transformations**: Handles all rotations and reflections of pieces
- **Date validation**: Works with real calendar dates and calculates correct weekdays
- **JSON output**: Saves all solutions in a structured JSON format
- **Progress tracking**: Shows solving progress and estimated completion time
- **Multiple solutions**: Finds and stores all possible solutions for each date

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/Wooden-Calendar-Puzzle-Solver.git
cd Wooden-Calendar-Puzzle-Solver
```

2. No external dependencies required! Uses only Python standard library.

## Usage

### Quick Test (Recommended First)

Test the solver on a few specific dates:

```bash
python test_solver.py
```

This will:
- Run a performance test on January 1st
- Test 3 specific dates and show solutions
- Estimate time needed for full solve
- Save test results to `test_solutions.json`

### Full Solve (Warning: Very Time Intensive!)

To solve for all possible dates (365+ combinations):

```bash
python calendar_puzzle_solver.py
```

**⚠️ Warning**: This can take many hours or even days to complete due to the brute-force nature of the algorithm!

### Custom Date Solving

You can also solve for specific dates programmatically:

```python
from calendar_puzzle_solver import CalendarPuzzleSolver

solver = CalendarPuzzleSolver()

# Solve for March 15th (assuming it's a Friday)
# Parameters: (day, month, weekday)
solutions = solver.solve_for_date(15, 3, 5)

print(f"Found {len(solutions)} solutions")
```

## Output Format

Solutions are saved in JSON format with the structure:

```json
{
  "1 OCA PZT": [
    {
      "solution_id": 0,
      "board_state": [
        [1, 1, 2, 2, -1, 3, -1],
        [-1, 4, 4, 2, 5, 5, 5],
        ...
      ]
    }
  ]
}
```

Where:
- Key: `"day month_abbr day_abbr"` (e.g., "15 MAR CUM")
- `solution_id`: Unique identifier for each solution
- `board_state`: 8×7 matrix showing piece placement
  - `-1`: Target cells (uncovered)
  - `-2`: Empty board cells
  - `1-10`: Piece IDs

## Algorithm Details

The solver uses a backtracking algorithm:

1. **Piece Generation**: Pre-generates all unique orientations (rotations + reflections) for each piece
2. **Date Processing**: Converts dates to board positions that must remain uncovered
3. **Backtracking**: Recursively tries placing each piece in all possible positions
4. **Validation**: Ensures no overlaps and all non-target cells are covered
5. **Solution Storage**: Saves all valid solutions for each date

## Performance Considerations

- **Time Complexity**: Exponential due to brute-force approach
- **Space Complexity**: Linear in number of solutions found
- **Optimization Opportunities**:
  - Constraint propagation
  - Symmetry breaking
  - Early pruning of impossible states
  - Parallel processing for different dates

## Files

- `calendar_puzzle_solver.py`: Main solver implementation
- `test_solver.py`: Test script for specific dates
- `requirements.txt`: Dependencies (empty - uses standard library)
- `README.md`: This documentation

## Contributing

Contributions welcome! Areas for improvement:

1. **Algorithm Optimization**: Implement more efficient solving algorithms
2. **Parallel Processing**: Solve multiple dates simultaneously  
3. **Visualization**: Add visual representation of solutions
4. **Validation**: Add more robust input validation
5. **Performance**: Profile and optimize bottlenecks

## License

See LICENSE file for details.

## Troubleshooting

**No solutions found**: 
- Verify piece definitions match your physical puzzle
- Check that board layout matches your puzzle
- Ensure date mappings are correct

**Very slow performance**:
- Start with test script first
- Consider solving only specific dates of interest
- Run on a powerful computer for full solve

**Memory issues**:
- The solver stores all solutions in memory
- For dates with many solutions, this could use significant RAM
