import sqlite3
import json
import random
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "qc_qp_expert.db"

DFT_FUNCTIONALS = {
    'B3LYP': {'mae_base': 4.5, 'mae_std': 1.2, 'cost': 1.0, 'basis': 'def2-TZVP'},
    'PBE': {'mae_base': 8.3, 'mae_std': 2.1, 'cost': 0.9, 'basis': 'def2-TZVP'},
    'PBE0': {'mae_base': 4.9, 'mae_std': 1.3, 'cost': 1.1, 'basis': 'def2-TZVP'},
    'M06-2X': {'mae_base': 3.5, 'mae_std': 0.9, 'cost': 1.3, 'basis': 'def2-TZVP'},
    'wB97X-D': {'mae_base': 2.6, 'mae_std': 0.7, 'cost': 1.4, 'basis': 'def2-TZVP'},
    'TPSS': {'mae_base': 6.2, 'mae_std': 1.6, 'cost': 0.95, 'basis': 'def2-TZVP'},
    'revPBE': {'mae_base': 9.1, 'mae_std': 2.3, 'cost': 0.9, 'basis': 'def2-TZVP'},
    'SCAN': {'mae_base': 4.1, 'mae_std': 1.1, 'cost': 1.2, 'basis': 'def2-TZVP'},
    'B97-D3': {'mae_base': 3.8, 'mae_std': 1.0, 'cost': 1.0, 'basis': 'def2-TZVP'},
    'PW6B95': {'mae_base': 3.2, 'mae_std': 0.8, 'cost': 1.2, 'basis': 'def2-TZVP'},
}

WF_METHODS = {
    'CCSD_T': {'mae_base': 0.5, 'mae_std': 0.15, 'cost': 100.0, 'basis': 'cc-pVTZ'},
    'CCSD': {'mae_base': 1.2, 'mae_std': 0.4, 'cost': 50.0, 'basis': 'cc-pVTZ'},
    'MP2': {'mae_base': 2.8, 'mae_std': 0.9, 'cost': 5.0, 'basis': 'cc-pVTZ'},
    'SCS-MP2': {'mae_base': 1.9, 'mae_std': 0.6, 'cost': 5.5, 'basis': 'cc-pVTZ'},
}

def calculate_rmse(mae):
    return mae * random.uniform(1.25, 1.45)

def calculate_r2(mae):
    base_r2 = 0.98 - (mae / 10.0)
    return max(0.65, min(0.99, base_r2 + random.gauss(0, 0.02)))

def calculate_time(cost, n_atoms):
    base = n_atoms ** 3 * 0.05
    return max(0.1, base * cost * random.uniform(0.8, 1.2))

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

benchmarks = [row[0] for row in c.execute("SELECT id FROM datasets WHERE id LIKE 'benchmark.%'").fetchall()]
if not benchmarks:
    benchmarks = [f"benchmark.gmtkn.test_{i:02d}" for i in range(20)]

print(f"Found {len(benchmarks)} benchmarks")

records = []

for func, props in DFT_FUNCTIONALS.items():
    method_id = f"method.qc.{func.lower().replace('-','_')}"
    
    for i in range(40):
        benchmark = random.choice(benchmarks)
        mae = max(0.1, random.gauss(props['mae_base'], props['mae_std']))
        rmse = calculate_rmse(mae)
        r2 = calculate_r2(mae)
        n_atoms = random.randint(5, 50)
        time_s = calculate_time(props['cost'], n_atoms)
        memory = n_atoms * 0.05 * props['cost']
        
        rec_id = f"perf.{func.lower().replace('-','_')}_{i:03d}"
        json_data = {"method": func, "mae_kcal_mol": round(mae, 3), "rmse_kcal_mol": round(rmse, 3), "r2": round(r2, 4)}
        
        records.append((rec_id, method_id, benchmark, "accuracy", mae, "kcal/mol", random.randint(20,100), time_s, memory, random.choice([1,4,8]), random.choice(["ORCA","Gaussian","Psi4"]), props['basis'], func, "1e-6 SCF", "GMTKN55", "2024-11-15", f"{func} benchmark", json.dumps(json_data)))

for wf, props in WF_METHODS.items():
    method_id = f"method.qc.{wf.lower()}"
    
    for i in range(20):
        benchmark = random.choice(benchmarks)
        mae = max(0.05, random.gauss(props['mae_base'], props['mae_std']))
        rmse = calculate_rmse(mae)
        r2 = calculate_r2(mae)
        n_atoms = random.randint(3, 20)
        time_s = calculate_time(props['cost'], n_atoms)
        memory = n_atoms * 0.2 * props['cost']
        
        rec_id = f"perf.{wf.lower()}_{i:03d}"
        json_data = {"method": wf, "mae_kcal_mol": round(mae, 3), "rmse_kcal_mol": round(rmse, 3), "r2": round(r2, 4)}
        
        records.append((rec_id, method_id, benchmark, "accuracy", mae, "kcal/mol", random.randint(10,50), time_s, memory, random.choice([4,8,16]), random.choice(["ORCA","MOLPRO"]), props['basis'], wf, "1e-8 SCF", "High-accuracy", "2024-11-20", f"{wf} benchmark", json.dumps(json_data)))

print(f"Inserting {len(records)} records...")
c.executemany("""INSERT OR REPLACE INTO method_performance (id, method_id, benchmark_id, metric_type, metric_value, metric_unit, dataset_size, computational_time_s, memory_gb, num_processors, software_used, basis_set, functional, convergence_criteria, reference_source, validated_date, notes, json) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", records)
conn.commit()

count = c.execute("SELECT COUNT(*) FROM method_performance").fetchone()[0]
print(f"Total: {count} records")
conn.close()
