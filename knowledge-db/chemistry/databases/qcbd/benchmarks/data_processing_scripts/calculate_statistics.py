"""
Calculate benchmark statistics (MAE, RMSE, MaxError) from CSV data.

Usage:
    python calculate_statistics.py benchmarks/s22/binding_energies.csv
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys


def calculate_stats(errors):
    """Calculate MAE, RMSE, MaxError."""
    mae = np.mean(np.abs(errors))
    rmse = np.sqrt(np.mean(errors**2))
    max_error = np.max(np.abs(errors))
    return mae, rmse, max_error


def analyze_benchmark_file(csv_path):
    """Analyze a benchmark CSV file."""
    df = pd.read_csv(csv_path)
    
    print(f"\n{'='*80}")
    print(f"Benchmark Statistics: {csv_path.name}")
    print(f"{'='*80}\n")
    
    # Find error columns (end with _error)
    error_cols = [col for col in df.columns if col.endswith('_error')]
    
    if not error_cols:
        print("No error columns found in CSV")
        return
    
    # Calculate stats for each method
    results = []
    for col in error_cols:
        method = col.replace('_error', '').upper().replace('_', '-')
        errors = df[col].dropna()
        
        if len(errors) == 0:
            continue
        
        mae, rmse, max_err = calculate_stats(errors.values)
        
        results.append({
            'Method': method,
            'MAE (kcal/mol)': mae,
            'RMSE (kcal/mol)': rmse,
            'MaxError (kcal/mol)': max_err,
            'N': len(errors)
        })
    
    # Display results
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values('MAE (kcal/mol)')
    
    print(results_df.to_string(index=False))
    print()
    
    # Category breakdown if available
    if 'category' in df.columns:
        print(f"\n{'='*80}")
        print("Category Breakdown")
        print(f"{'='*80}\n")
        
        categories = df['category'].unique()
        for cat in categories:
            cat_df = df[df['category'] == cat]
            print(f"\n{cat.upper().replace('_', ' ')} ({len(cat_df)} systems):")
            print("-" * 60)
            
            cat_results = []
            for col in error_cols:
                method = col.replace('_error', '').upper().replace('_', '-')
                errors = cat_df[col].dropna()
                
                if len(errors) == 0:
                    continue
                
                mae, rmse, max_err = calculate_stats(errors.values)
                cat_results.append({
                    'Method': method,
                    'MAE': f"{mae:.2f}",
                    'RMSE': f"{rmse:.2f}",
                    'MaxError': f"{max_err:.2f}"
                })
            
            cat_results_df = pd.DataFrame(cat_results)
            print(cat_results_df.to_string(index=False))
    
    # Method ranking
    print(f"\n{'='*80}")
    print("Method Ranking (by MAE)")
    print(f"{'='*80}\n")
    
    for i, row in results_df.iterrows():
        print(f"{i+1}. {row['Method']:20s} MAE={row['MAE (kcal/mol)']:.3f} kcal/mol")


def compare_benchmarks(benchmark_dir):
    """Compare multiple benchmark files."""
    benchmark_dir = Path(benchmark_dir)
    csv_files = list(benchmark_dir.rglob('binding_energies.csv'))
    
    if len(csv_files) == 0:
        print(f"No binding_energies.csv files found in {benchmark_dir}")
        return
    
    print(f"\n{'='*80}")
    print(f"Found {len(csv_files)} benchmark datasets")
    print(f"{'='*80}\n")
    
    for csv_file in csv_files:
        analyze_benchmark_file(csv_file)
        print("\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python calculate_statistics.py <csv_file_or_directory>")
        sys.exit(1)
    
    path = Path(sys.argv[1])
    
    if path.is_file():
        analyze_benchmark_file(path)
    elif path.is_dir():
        compare_benchmarks(path)
    else:
        print(f"Error: {path} not found")
        sys.exit(1)
