#!/usr/bin/env python3

import time
from calendar_puzzle_solver import CalendarPuzzleSolver
from dp_calendar_solver import DPCalendarPuzzleSolver

def compare_solvers():
    """Compare performance between brute-force and DP solvers"""
    print("🔬 Performance Comparison: Brute-Force vs Dynamic Programming")
    print("=" * 70)
    
    # Test dates
    test_dates = [
        (1, 1, 1),   # January 1st, Monday
        (15, 3, 5),  # March 15th, Friday
        (25, 12, 3), # December 25th, Wednesday
    ]
    
    # Initialize solvers
    bf_solver = CalendarPuzzleSolver()
    dp_solver = DPCalendarPuzzleSolver()
    
    results = []
    
    for day, month, weekday in test_dates:
        print(f"\n📅 Testing date: Day {day}, Month {month}, Weekday {weekday}")
        print("-" * 50)
        
        # Get date abbreviations
        month_abbr = None
        day_abbr = None
        
        for abbr, num in bf_solver.months.items():
            if num == month:
                month_abbr = abbr
                break
        
        for abbr, num in bf_solver.days.items():
            if num == weekday:
                day_abbr = abbr
                break
        
        date_str = f"{day} {month_abbr} {day_abbr}"
        
        # Test Brute-Force solver
        print("🐢 Testing Brute-Force solver...")
        bf_start = time.time()
        try:
            bf_solutions = bf_solver.solve_for_date(day, month, weekday)
            bf_end = time.time()
            bf_time = bf_end - bf_start
            bf_success = True
        except Exception as e:
            print(f"❌ Brute-Force solver failed: {e}")
            bf_solutions = []
            bf_time = float('inf')
            bf_success = False
        
        # Test Dynamic Programming solver
        print("🚀 Testing Dynamic Programming solver...")
        dp_start = time.time()
        try:
            dp_solutions = dp_solver.solve_for_date(day, month, weekday)
            dp_end = time.time()
            dp_time = dp_end - dp_start
            dp_success = True
        except Exception as e:
            print(f"❌ DP solver failed: {e}")
            dp_solutions = []
            dp_time = float('inf')
            dp_success = False
        
        # Compare results
        print(f"\n📊 Results for {date_str}:")
        print(f"   Brute-Force: {len(bf_solutions) if bf_success else 0} solutions in {bf_time:.3f}s")
        print(f"   Dynamic Prog: {len(dp_solutions) if dp_success else 0} solutions in {dp_time:.3f}s")
        
        if bf_success and dp_success:
            if bf_time > 0:
                speedup = bf_time / dp_time
                print(f"   🎯 Speedup: {speedup:.2f}x faster with DP")
            else:
                print("   ⚡ Both too fast to measure accurately")
            
            # Verify same number of solutions
            if len(bf_solutions) == len(dp_solutions):
                print("   ✅ Both solvers found the same number of solutions")
            else:
                print("   ⚠️  Different number of solutions found!")
        
        results.append({
            'date': date_str,
            'bf_time': bf_time if bf_success else None,
            'dp_time': dp_time if dp_success else None,
            'bf_solutions': len(bf_solutions) if bf_success else 0,
            'dp_solutions': len(dp_solutions) if dp_success else 0,
            'speedup': bf_time / dp_time if (bf_success and dp_success and dp_time > 0) else None
        })
    
    # Summary
    print(f"\n🏁 Summary")
    print("=" * 30)
    
    valid_results = [r for r in results if r['speedup'] is not None]
    
    if valid_results:
        avg_speedup = sum(r['speedup'] for r in valid_results) / len(valid_results)
        max_speedup = max(r['speedup'] for r in valid_results)
        min_speedup = min(r['speedup'] for r in valid_results)
        
        print(f"Average speedup: {avg_speedup:.2f}x")
        print(f"Maximum speedup: {max_speedup:.2f}x")
        print(f"Minimum speedup: {min_speedup:.2f}x")
        
        total_bf_time = sum(r['bf_time'] for r in valid_results)
        total_dp_time = sum(r['dp_time'] for r in valid_results)
        
        print(f"\nTotal time comparison:")
        print(f"Brute-Force: {total_bf_time:.3f}s")
        print(f"Dynamic Prog: {total_dp_time:.3f}s")
        print(f"Overall speedup: {total_bf_time / total_dp_time:.2f}x")
        
        # Estimate time for all dates
        avg_dp_time = total_dp_time / len(valid_results)
        estimated_total_dp = avg_dp_time * 365
        estimated_total_bf = total_bf_time / len(valid_results) * 365
        
        print(f"\n📈 Estimated time for all 365 dates:")
        print(f"Brute-Force: {estimated_total_bf / 3600:.1f} hours")
        print(f"Dynamic Prog: {estimated_total_dp / 3600:.1f} hours")
    else:
        print("No valid comparison data available")
    
    return results

def test_dp_features():
    """Test specific DP features like caching"""
    print("\n🧪 Testing Dynamic Programming Features")
    print("=" * 50)
    
    solver = DPCalendarPuzzleSolver()
    
    # Test same date multiple times to see caching effect
    print("Testing cache effectiveness...")
    
    times = []
    for i in range(3):
        start = time.time()
        solutions = solver.solve_for_date(1, 1, 1)
        end = time.time()
        times.append(end - start)
        print(f"Run {i+1}: {end - start:.3f}s, Cache hit ratio: {solver.cache_hits/(solver.cache_hits + solver.cache_misses)*100:.1f}%")
    
    print(f"\nCache effectiveness:")
    print(f"First run: {times[0]:.3f}s (cold cache)")
    if len(times) > 1:
        print(f"Second run: {times[1]:.3f}s (warm cache)")
        if times[1] > 0:
            print(f"Cache speedup: {times[0]/times[1]:.2f}x")

def main():
    """Main comparison function"""
    print("🎯 Calendar Puzzle Solver Performance Comparison")
    print("=" * 60)
    
    # Compare basic performance
    results = compare_solvers()
    
    # Test DP-specific features
    test_dp_features()
    
    print(f"\n🎉 Comparison completed!")
    print("🚀 The Dynamic Programming approach should show significant improvements!")

if __name__ == "__main__":
    main() 