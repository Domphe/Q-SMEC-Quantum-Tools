#!/usr/bin/env python3
"""
Benchmark Analysis Module for QCBD
===================================

Provides tools for analyzing quantum chemistry method performance against benchmark data:
- MAE/RMSE calculation
- Method comparison and ranking
- Performance visualization (stub)
- Error distribution analysis

Requires benchmark_results table with schema:
  (method_id, benchmark_id, computed_energy_kcal, error_kcal, timestamp)
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
from collections import defaultdict
import math

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
DB_DIR = PROJECT_ROOT / 'db'

def calculate_mae(errors: List[float]) -> float:
    """Calculate Mean Absolute Error."""
    if not errors:
        return 0.0
    return sum(abs(e) for e in errors) / len(errors)

def calculate_rmse(errors: List[float]) -> float:
    """Calculate Root Mean Square Error."""
    if not errors:
        return 0.0
    return math.sqrt(sum(e**2 for e in errors) / len(errors))

def calculate_max_error(errors: List[float]) -> float:
    """Calculate maximum absolute error."""
    if not errors:
        return 0.0
    return max(abs(e) for e in errors)

def get_benchmark_statistics(conn: sqlite3.Connection, benchmark_set: str) -> Dict:
    """
    Get reference statistics for a benchmark set.
    
    Args:
        conn: Database connection
        benchmark_set: Name of benchmark set (e.g., "S22", "S66x8", "BandGap30")
    
    Returns:
        Dict with keys: system_count, property statistics, property_type
    """
    cursor = conn.cursor()
    
    # Query all benchmark records for this set
    cursor.execute("""
        SELECT json FROM datasets 
        WHERE json_extract(json, '$.benchmark_set') = ?
    """, (benchmark_set,))
    
    records = [json.loads(row[0]) for row in cursor.fetchall()]
    
    if not records:
        return {"system_count": 0, "error": f"No records found for {benchmark_set}"}
    
    stats = {
        "benchmark_set": benchmark_set,
        "system_count": len(records),
        "property_type": records[0].get("property_type", "unknown"),
        "reference_level": records[0].get("reference_level", "unknown")
    }
    
    # Identify primary property and compute statistics
    if "reference_energy_kcal" in records[0]:
        energies = [r.get("reference_energy_kcal", 0) for r in records]
        stats["avg_reference_energy_kcal"] = sum(energies) / len(energies)
        stats["energy_range_kcal"] = (min(energies), max(energies))
    elif "band_gap_eV" in records[0]:
        gaps = [r.get("band_gap_eV", 0) for r in records]
        stats["avg_band_gap_eV"] = sum(gaps) / len(gaps)
        stats["gap_range_eV"] = (min(gaps), max(gaps))
    elif "critical_temperature_K" in records[0]:
        Tcs = [r.get("critical_temperature_K", 0) for r in records]
        stats["avg_Tc_K"] = sum(Tcs) / len(Tcs)
        stats["Tc_range_K"] = (min(Tcs), max(Tcs))
    elif "voltage_V" in records[0]:
        voltages = [r.get("voltage_V", 0) for r in records]
        stats["avg_voltage_V"] = sum(voltages) / len(voltages)
        stats["voltage_range_V"] = (min(voltages), max(voltages))
    elif "magnetic_moment_muB" in records[0]:
        moments = [r.get("magnetic_moment_muB", 0) for r in records]
        stats["avg_magnetic_moment_muB"] = sum(moments) / len(moments)
        stats["moment_range_muB"] = (min(moments), max(moments))
    elif "binding_energy_kcal" in records[0]:
        be_values = [r.get("binding_energy_kcal", 0) for r in records]
        stats["avg_binding_energy_kcal"] = sum(be_values) / len(be_values)
        stats["binding_energy_range_kcal"] = (min(be_values), max(be_values))
    elif "relative_energy_kcal" in records[0]:
        rel_e = [r.get("relative_energy_kcal", 0) for r in records]
        stats["avg_relative_energy_kcal"] = sum(rel_e) / len(rel_e)
        stats["relative_energy_range_kcal"] = (min(rel_e), max(rel_e))
    elif "refractive_index" in records[0]:
        n_values = [r.get("refractive_index", 0) for r in records]
        stats["avg_refractive_index"] = sum(n_values) / len(n_values)
        stats["refractive_index_range"] = (min(n_values), max(n_values))
        # Also include absorption coefficient if present
        if "absorption_coeff_cm" in records[0]:
            alpha_values = [r.get("absorption_coeff_cm", 0) for r in records]
            stats["avg_absorption_coeff_cm"] = sum(alpha_values) / len(alpha_values)
            stats["absorption_range_cm"] = (min(alpha_values), max(alpha_values))
    elif "cohesive_energy_eV" in records[0]:
        coh_e = [r.get("cohesive_energy_eV", 0) for r in records]
        stats["avg_cohesive_energy_eV"] = sum(coh_e) / len(coh_e)
        stats["cohesive_energy_range_eV"] = (min(coh_e), max(coh_e))
    elif "adsorption_energy_eV" in records[0]:
        ads_e = [r.get("adsorption_energy_eV", 0) for r in records]
        stats["avg_adsorption_energy_eV"] = sum(ads_e) / len(ads_e)
        stats["adsorption_energy_range_eV"] = (min(ads_e), max(ads_e))
    elif "formation_energy_eV" in records[0]:
        form_e = [r.get("formation_energy_eV", 0) for r in records]
        stats["avg_formation_energy_eV"] = sum(form_e) / len(form_e)
        stats["formation_energy_range_eV"] = (min(form_e), max(form_e))
    
    return stats

def compare_typical_errors(conn: sqlite3.Connection, benchmark_set: str, methods: List[str] = None) -> Dict:
    """
    Compare typical errors stored in benchmark records for different methods.
    
    Args:
        conn: Database connection
        benchmark_set: Benchmark set name
        methods: List of method names to compare (e.g., ["HF", "MP2", "CCSD"])
    
    Returns:
        Dict with MAE, RMSE, Max Error for each method
    """
    if methods is None:
        methods = ["HF", "MP2", "CCSD", "B3LYP"]
    
    cursor = conn.cursor()
    cursor.execute("""
        SELECT json FROM datasets 
        WHERE json_extract(json, '$.benchmark_set') = ?
        AND json_extract(json, '$.typical_errors') IS NOT NULL
    """, (benchmark_set,))
    
    records = [json.loads(row[0]) for row in cursor.fetchall()]
    
    if not records:
        return {"error": f"No records with typical_errors for {benchmark_set}"}
    
    results = {}
    
    for method in methods:
        errors = []
        for record in records:
            typical_errors = record.get("typical_errors", {})
            if method in typical_errors:
                errors.append(typical_errors[method])
        
        if errors:
            results[method] = {
                "system_count": len(errors),
                "MAE": round(calculate_mae(errors), 4),
                "RMSE": round(calculate_rmse(errors), 4),
                "Max_Error": round(calculate_max_error(errors), 4),
                "Min_Error": round(min(abs(e) for e in errors), 4)
            }
        else:
            results[method] = {"error": f"No {method} data available"}
    
    return {
        "benchmark_set": benchmark_set,
        "method_comparison": results,
        "system_count": len(records)
    }

def rank_methods_by_mae(conn: sqlite3.Connection, benchmark_set: str, methods: List[str] = None) -> List[Tuple[str, float]]:
    """
    Rank methods by MAE on a benchmark set.
    
    Returns:
        List of (method_name, mae) tuples sorted by MAE (ascending)
    """
    comparison = compare_typical_errors(conn, benchmark_set, methods)
    
    if "error" in comparison:
        return []
    
    rankings = []
    for method, stats in comparison["method_comparison"].items():
        if "MAE" in stats:
            rankings.append((method, stats["MAE"]))
    
    return sorted(rankings, key=lambda x: x[1])

def get_all_benchmark_sets(conn: sqlite3.Connection) -> List[str]:
    """
    Retrieve list of all benchmark sets in database.
    
    Returns:
        List of unique benchmark set names
    """
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT json_extract(json, '$.benchmark_set') 
        FROM datasets 
        WHERE json LIKE '%"benchmark_set"%'
    """)
    
    sets = [row[0] for row in cursor.fetchall() if row[0]]
    return sorted(sets)

def export_benchmark_performance_report(conn: sqlite3.Connection, output_file: Path = None) -> Dict:
    """
    Generate comprehensive performance report for all benchmark sets.
    
    Args:
        conn: Database connection
        output_file: Optional path to save JSON report
    
    Returns:
        Dict with performance statistics for all benchmarks
    """
    benchmark_sets = get_all_benchmark_sets(conn)
    
    report = {
        "generated": datetime.now().isoformat(),
        "benchmark_count": len(benchmark_sets),
        "benchmarks": {}
    }
    
    for bset in benchmark_sets:
        stats = get_benchmark_statistics(conn, bset)
        comparison = compare_typical_errors(conn, bset)
        rankings = rank_methods_by_mae(conn, bset)
        
        report["benchmarks"][bset] = {
            "statistics": stats,
            "method_comparison": comparison.get("method_comparison", {}),
            "method_ranking": [{"method": m, "mae": mae} for m, mae in rankings]
        }
    
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"Report saved to {output_file}")
    
    return report

# ========================================
# VISUALIZATION STUBS (future enhancement)
# ========================================

def plot_error_distribution(benchmark_set: str, method: str):
    """
    [STUB] Plot error distribution histogram for a method on a benchmark.
    
    Future implementation: matplotlib histogram of errors with MAE/RMSE lines
    """
    print(f"[VISUALIZATION STUB] plot_error_distribution({benchmark_set}, {method})")
    print("  To implement: Use matplotlib to create histogram of errors")
    return None

def plot_method_comparison(benchmark_set: str):
    """
    [STUB] Bar chart comparing MAE/RMSE across methods.
    
    Future implementation: matplotlib grouped bar chart
    """
    print(f"[VISUALIZATION STUB] plot_method_comparison({benchmark_set})")
    print("  To implement: Use matplotlib to create grouped bar chart")
    return None

def plot_benchmark_heatmap():
    """
    [STUB] Heatmap of method performance across all benchmarks.
    
    Future implementation: seaborn heatmap with benchmarks x methods
    """
    print("[VISUALIZATION STUB] plot_benchmark_heatmap()")
    print("  To implement: Use seaborn to create heatmap of MAEs")
    return None

# ========================================
# CLI INTERFACE
# ========================================

def main():
    """Benchmark analysis CLI."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Analyze quantum chemistry benchmark performance")
    parser.add_argument("--db", type=str, default=str(DB_DIR / "qc_qp_expert.db"), help="Database path")
    parser.add_argument("--list", action="store_true", help="List all benchmark sets")
    parser.add_argument("--stats", type=str, metavar="SET", help="Show statistics for benchmark set")
    parser.add_argument("--compare", type=str, metavar="SET", help="Compare methods on benchmark set")
    parser.add_argument("--methods", type=str, nargs="+", default=["HF", "MP2", "CCSD"], help="Methods to compare")
    parser.add_argument("--rank", type=str, metavar="SET", help="Rank methods by MAE on benchmark set")
    parser.add_argument("--report", type=str, metavar="FILE", help="Generate full performance report (JSON)")
    
    args = parser.parse_args()
    
    conn = sqlite3.connect(args.db)
    
    try:
        if args.list:
            sets = get_all_benchmark_sets(conn)
            print(f"\nFound {len(sets)} benchmark sets:")
            for s in sets:
                print(f"  - {s}")
        
        elif args.stats:
            stats = get_benchmark_statistics(conn, args.stats)
            print(f"\n=== {args.stats} Statistics ===")
            for key, val in stats.items():
                print(f"  {key}: {val}")
        
        elif args.compare:
            comparison = compare_typical_errors(conn, args.compare, args.methods)
            print(f"\n=== {args.compare} Method Comparison ===")
            if "error" in comparison:
                print(f"  Error: {comparison['error']}")
            else:
                for method, stats in comparison["method_comparison"].items():
                    print(f"\n  {method}:")
                    for metric, value in stats.items():
                        print(f"    {metric}: {value}")
        
        elif args.rank:
            rankings = rank_methods_by_mae(conn, args.rank, args.methods)
            print(f"\n=== {args.rank} Method Ranking (by MAE) ===")
            for i, (method, mae) in enumerate(rankings, 1):
                print(f"  {i}. {method:10s} MAE = {mae:.4f} kcal/mol")
        
        elif args.report:
            report = export_benchmark_performance_report(conn, Path(args.report))
            print(f"\nGenerated report with {report['benchmark_count']} benchmark sets")
        
        else:
            parser.print_help()
    
    finally:
        conn.close()

if __name__ == '__main__':
    main()
