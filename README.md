# 🧩 Wooden Calendar Puzzle Solver

> **High-performance algorithms for solving wooden calendar puzzles with dynamic programming optimization**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Algorithm](https://img.shields.io/badge/Algorithm-Dynamic%20Programming-green.svg)](https://en.wikipedia.org/wiki/Dynamic_programming)
[![Solutions](https://img.shields.io/badge/Solutions-28K%2B%20Found-red.svg)](./dp_calendar_solutions.json)

## Overview

This project implements multiple algorithms for solving wooden calendar puzzles, progressing from brute-force approaches to optimized dynamic programming solutions. The puzzle involves placing 10 wooden pieces on a 7×8 board to cover all squares except for a specific date (day + month + weekday in Turkish).

## The Puzzle

- **Board**: 7×8 grid with numbers 1-31, Turkish month abbreviations, and Turkish day abbreviations
- **Pieces**: 10 wooden pieces of varying shapes (tetrominos and pentominos)
- **Objective**: Cover all squares except the target date
- **Constraints**: No overlaps, no gaps, all pieces must be used

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

## Implementation Approaches

### 1. Brute-Force Solver (`calendar_puzzle_solver.py`)
A straightforward backtracking implementation featuring:
- Complete piece transformation handling (rotations and reflections)
- Systematic search through all possibilities
- Clear, readable code structure suitable for understanding the problem

### 2. Dynamic Programming Solver (`dp_calendar_solver.py`)
An optimized version using memoization:
- Bit manipulation for efficient board state representation
- Memoization with `(board_mask, used_pieces)` cache keys
- Significant performance improvement over brute-force

### 3. Fast Solver (`fast_dp_solver.py`)
A highly optimized implementation with:
- LRU caching using Python's `@lru_cache` decorator
- First-empty-cell heuristic for improved search ordering
- Precomputed piece placement tables
- Minimal state representation

### 4. Solution Viewer (`viewer.py`)
A utility for visualizing solutions:
- ASCII art rendering of board states
- Command-line interface for easy date queries
- Clear piece identification with symbols

## Performance Comparison

| Approach | Time Complexity | Space Usage | Cache Strategy |
|----------|----------------|-------------|----------------|
| Brute-Force | O(10! × orientations) | 2D arrays | None |
| Dynamic Programming | O(states × pieces) | Bit masks | Manual memoization |
| Fast Solver | O(states) | Compressed states | LRU automatic |

Results show significant speedup from brute-force to optimized DP, with the fast solver achieving sub-second solving times for individual dates.

## Usage

### Quick Start
```bash
# Solve and visualize a specific date
python viewer.py 2024-03-15

# Run performance comparison
python compare_solvers.py

# Solve all dates with fast solver
python fast_dp_solver.py
```

### Programmatic Usage
```python
from fast_dp_solver import FastCalendarPuzzleSolver

solver = FastCalendarPuzzleSolver()
solutions = solver.solve_for_date(15, 3, 5)  # March 15th, Friday

# Visualization
from viewer import print_solution_for_date
print_solution_for_date("2024-03-15")
```

## Technical Features

### Optimization Techniques
- **Bit manipulation**: Board states represented as 64-bit integers
- **Memoization**: Caching of intermediate results to avoid redundant computation
- **Heuristics**: First-empty-cell search ordering for better pruning
- **Precomputation**: Valid piece placements calculated once at startup

### Data Structures
- Position-to-bit mapping for efficient board operations
- Precomputed orientation tables for all pieces
- Cache-friendly state representations

### Code Organization
- Modular design with clear separation of concerns
- Comprehensive documentation and type hints
- Performance measurement and comparison tools
- JSON output format for solution storage

## Project Structure

| File | Purpose |
|------|---------|
| `fast_dp_solver.py` | Optimized solver with LRU caching |
| `dp_calendar_solver.py` | DP implementation with manual memoization |
| `calendar_puzzle_solver.py` | Brute-force baseline implementation |
| `viewer.py` | Solution visualization tool |
| `compare_solvers.py` | Performance benchmarking |
| `dp_calendar_solutions.json` | Complete solution database (28K+ solutions) |

## Results

The project successfully finds solutions for valid calendar dates, with over 28,000 solutions stored in the complete database. The fast solver can process individual dates in sub-second time, making it practical for interactive use.

## Installation

No external dependencies required - uses only Python standard library.

```bash
git clone https://github.com/your-username/Wooden-Calendar-Puzzle-Solver.git
cd Wooden-Calendar-Puzzle-Solver
```

## Contributing

Contributions welcome! Potential areas for improvement:
- Algorithm research (constraint satisfaction, SAT solvers)
- Web-based visualization interface
- Support for other calendar systems
- Additional optimization techniques
- Extended testing and validation

## License

See [LICENSE](LICENSE) file for details.
