#!/usr/bin/env python3

import time
import traceback
from calendar_puzzle_solver import CalendarPuzzleSolver
from dp_calendar_solver import DPCalendarPuzzleSolver
from fast_dp_solver import FastCalendarPuzzleSolver
from optimized_dp_solver import OptimizedDPSolver

def compare_all_solvers():
    """Compare performance between all available solver implementations"""
    print("🔬 Comprehensive Performance Comparison: All Solver Implementations")
    print("=" * 80)
    
    # Test dates
    test_dates = [
        (1, 1, 1),   # January 1st, Monday
        (15, 3, 5),  # March 15th, Friday
        (25, 12, 3), # December 25th, Wednesday
    ]
    
    # Initialize all solvers
    solvers = {
        "Brute-Force": CalendarPuzzleSolver(),
        "Dynamic Programming": DPCalendarPuzzleSolver(),
        "Fast DP": FastCalendarPuzzleSolver(),
        "Optimized DP": OptimizedDPSolver()
    }
    
    all_results = []
    
    for day, month, weekday in test_dates:
        print(f"\n📅 Testing date: Day {day}, Month {month}, Weekday {weekday}")
        print("-" * 60)
        
        # Get date abbreviations (using first solver for reference)
        month_abbr = None
        day_abbr = None
        
        reference_solver = list(solvers.values())[0]
        for abbr, num in reference_solver.months.items():
            if num == month:
                month_abbr = abbr
                break
        
        for abbr, num in reference_solver.days.items():
            if num == weekday:
                day_abbr = abbr
                break
        
        date_str = f"{day} {month_abbr} {day_abbr}"
        date_results = {"date": date_str}
        
        # Test each solver
        for solver_name, solver in solvers.items():
            print(f"\n🧮 Testing {solver_name}...")
            
            start_time = time.time()
            try:
                solutions = solver.solve_for_date(day, month, weekday)
                end_time = time.time()
                
                elapsed_time = end_time - start_time
                num_solutions = len(solutions) if solutions else 0
                
                date_results[solver_name] = {
                    'success': True,
                    'time': elapsed_time,
                    'solutions': num_solutions,
                    'cache_stats': get_cache_stats(solver)
                }
                
                print(f"   ✅ Found {num_solutions} solution(s) in {elapsed_time:.4f}s")
                
                # Show cache statistics if available
                cache_stats = get_cache_stats(solver)
                if cache_stats:
                    print(f"   📊 {cache_stats}")
                    
            except Exception as e:
                end_time = time.time()
                elapsed_time = end_time - start_time
                
                date_results[solver_name] = {
                    'success': False,
                    'time': elapsed_time,
                    'solutions': 0,
                    'error': str(e),
                    'cache_stats': None
                }
                
                print(f"   ❌ Failed after {elapsed_time:.4f}s: {str(e)[:100]}...")
        
        # Compare results for this date
        print(f"\n📊 Results Summary for {date_str}:")
        successful_solvers = {name: data for name, data in date_results.items() 
                            if name != "date" and data['success']}
        
        if len(successful_solvers) > 1:
            # Find fastest solver
            fastest = min(successful_solvers.items(), key=lambda x: x[1]['time'])
            print(f"   🏆 Fastest: {fastest[0]} ({fastest[1]['time']:.4f}s)")
            
            # Calculate speedups relative to brute-force
            if "Brute-Force" in successful_solvers:
                bf_time = successful_solvers["Brute-Force"]['time']
                print(f"   ⚡ Speedups vs Brute-Force:")
                for name, data in successful_solvers.items():
                    if name != "Brute-Force" and data['time'] > 0:
                        speedup = bf_time / data['time']
                        print(f"      {name}: {speedup:.2f}x faster")
            
            # Verify solution consistency
            solution_counts = [data['solutions'] for data in successful_solvers.values()]
            if len(set(solution_counts)) == 1:
                print(f"   ✅ All solvers found {solution_counts[0]} solution(s)")
            else:
                print(f"   ⚠️  Solution count mismatch: {dict(zip(successful_solvers.keys(), solution_counts))}")
        
        all_results.append(date_results)
    
    # Overall summary
    print_overall_summary(all_results)
    
    return all_results

def get_cache_stats(solver):
    """Extract cache statistics from solver if available"""
    if hasattr(solver, 'cache_hits') and hasattr(solver, 'cache_misses'):
        total = solver.cache_hits + solver.cache_misses
        if total > 0:
            hit_ratio = (solver.cache_hits / total) * 100
            return f"Cache: {solver.cache_hits} hits, {solver.cache_misses} misses ({hit_ratio:.1f}% hit rate)"
    return None

def print_overall_summary(all_results):
    """Print comprehensive summary of all test results"""
    print(f"\n🏁 Overall Performance Summary")
    print("=" * 50)
    
    # Collect solver names
    solver_names = []
    for result in all_results:
        for key in result.keys():
            if key != "date" and key not in solver_names:
                solver_names.append(key)
    
    # Calculate average times and success rates
    summary_stats = {}
    for solver_name in solver_names:
        times = []
        successes = 0
        total_solutions = 0
        
        for result in all_results:
            if solver_name in result:
                data = result[solver_name]
                if data['success']:
                    times.append(data['time'])
                    successes += 1
                    total_solutions += data['solutions']
        
        if times:
            summary_stats[solver_name] = {
                'avg_time': sum(times) / len(times),
                'success_rate': successes / len(all_results),
                'total_solutions': total_solutions,
                'fastest_time': min(times),
                'slowest_time': max(times)
            }
    
    # Print summary table
    print("\nSolver Performance Summary:")
    print(f"{'Solver':<20} {'Avg Time':<12} {'Success Rate':<12} {'Total Solutions':<15}")
    print("-" * 65)
    
    for solver_name, stats in summary_stats.items():
        avg_time = f"{stats['avg_time']:.4f}s"
        success_rate = f"{stats['success_rate']*100:.0f}%"
        solutions = str(stats['total_solutions'])
        print(f"{solver_name:<20} {avg_time:<12} {success_rate:<12} {solutions:<15}")
    
    # Speedup analysis
    if "Brute-Force" in summary_stats and summary_stats["Brute-Force"]['success_rate'] > 0:
        print(f"\nSpeedup Analysis (vs Brute-Force):")
        bf_avg = summary_stats["Brute-Force"]['avg_time']
        
        for solver_name, stats in summary_stats.items():
            if solver_name != "Brute-Force" and stats['success_rate'] > 0:
                speedup = bf_avg / stats['avg_time']
                print(f"  {solver_name}: {speedup:.2f}x faster on average")
    
    # Time estimates for full solve
    print(f"\nEstimated time for all 365 dates:")
    for solver_name, stats in summary_stats.items():
        if stats['success_rate'] > 0:
            total_estimated = stats['avg_time'] * 365
            if total_estimated < 60:
                time_str = f"{total_estimated:.1f} seconds"
            elif total_estimated < 3600:
                time_str = f"{total_estimated/60:.1f} minutes"
            else:
                time_str = f"{total_estimated/3600:.1f} hours"
            print(f"  {solver_name}: {time_str}")

def test_cache_effectiveness():
    """Test cache effectiveness by running same date multiple times"""
    print("\n🧪 Cache Effectiveness Test")
    print("=" * 40)
    
    # Test solvers with caching capabilities
    cache_solvers = {
        "Dynamic Programming": DPCalendarPuzzleSolver(),
        "Fast DP": FastCalendarPuzzleSolver(),
        "Optimized DP": OptimizedDPSolver()
    }
    
    test_date = (1, 1, 1)  # January 1st, Monday
    
    for solver_name, solver in cache_solvers.items():
        print(f"\n🔄 Testing {solver_name} cache effectiveness...")
        
        times = []
        for run in range(3):
            start = time.time()
            try:
                solutions = solver.solve_for_date(*test_date)
                end = time.time()
                elapsed = end - start
                times.append(elapsed)
                
                cache_stats = get_cache_stats(solver)
                print(f"  Run {run + 1}: {elapsed:.4f}s" + 
                      (f" - {cache_stats}" if cache_stats else ""))
                
            except Exception as e:
                print(f"  Run {run + 1}: Failed - {str(e)[:50]}...")
                break
        
        if len(times) >= 2:
            improvement = times[0] / times[1] if times[1] > 0 else float('inf')
            print(f"  Cache improvement: {improvement:.2f}x faster on second run")

def main():
    """Main comparison function"""
    print("🎯 Comprehensive Calendar Puzzle Solver Comparison")
    print("=" * 60)
    
    # Compare all solvers
    results = compare_all_solvers()
    
    # Test cache effectiveness
    test_cache_effectiveness()
    
    print(f"\n🎉 Comparison completed!")
    print("📈 Review the results to see performance differences between approaches.")

if __name__ == "__main__":
    main() 