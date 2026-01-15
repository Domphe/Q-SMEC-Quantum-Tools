import sqlite3
import json

conn = sqlite3.connect('db/qc_qp_expert.db')
cur = conn.cursor()

# Get all datasets and filter for benchmark molecules
cur.execute("SELECT id, json FROM datasets")
all_datasets = cur.fetchall()

benchmark_molecules = []
for row in all_datasets:
    ds_id, json_data = row
    data = json.loads(json_data)
    if data.get('category') == 'benchmark_molecule':
        benchmark_molecules.append(data)

print(f"Total benchmark molecules: {len(benchmark_molecules)}")

# Show first 10 with SMILES
print("\nFirst 10 benchmark molecules with SMILES:")
print("-" * 80)
for mol in benchmark_molecules[:10]:
    name = mol.get('name', 'N/A')
    smiles = mol.get('smiles', 'N/A')
    formula = mol.get('formula', 'N/A')
    print(f"  {name:25} | Formula: {formula:10} | SMILES: {smiles}")

# Get charged species
charged = [m for m in benchmark_molecules if m.get('metadata', {}).get('charge')]
print(f"\n\nCharged species ({len(charged)}):")
print("-" * 80)
for mol in charged:
    name = mol.get('name', 'N/A')
    charge = mol.get('metadata', {}).get('charge', 0)
    smiles = mol.get('smiles', 'N/A')
    print(f"  {name:25} | Charge: {charge:+2} | SMILES: {smiles}")

# Get radicals
radicals = [m for m in benchmark_molecules if m.get('metadata', {}).get('multiplicity', 1) > 1]
print(f"\n\nRadical species ({len(radicals)}):")
print("-" * 80)
for mol in radicals:
    name = mol.get('name', 'N/A')
    mult = mol.get('metadata', {}).get('multiplicity', 1)
    smiles = mol.get('smiles', 'N/A')
    print(f"  {name:25} | Multiplicity: {mult} | SMILES: {smiles}")

# Summary by property
print("\n\nSummary:")
print("-" * 80)
print(f"  Neutral molecules:    {len([m for m in benchmark_molecules if not m.get('metadata', {}).get('charge')])}")
print(f"  Charged species:      {len(charged)}")
print(f"  Radicals:            {len(radicals)}")
print(f"  Closed-shell:        {len([m for m in benchmark_molecules if m.get('metadata', {}).get('multiplicity', 1) == 1])}")

conn.close()
