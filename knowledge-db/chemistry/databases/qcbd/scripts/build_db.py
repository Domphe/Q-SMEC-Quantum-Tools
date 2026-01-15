"""Build SQLite database from validated JSONL files."""
import sqlite3
import sys
from pathlib import Path
from utils import read_jsonl, DATA_PROCESSED, DB_DIR

def create_tables(conn: sqlite3.Connection) -> None:
    """Create tables for each data type."""
    tables = [
        ('sources', '''CREATE TABLE IF NOT EXISTS sources (
            id TEXT PRIMARY KEY,
            title TEXT,
            abstract TEXT,
            doi TEXT,
            container_title TEXT,
            subject TEXT,
            json TEXT NOT NULL
        )'''),
        ('concepts', 'CREATE TABLE IF NOT EXISTS concepts (id TEXT PRIMARY KEY, domain TEXT, json TEXT NOT NULL)'),
        ('methods', 'CREATE TABLE IF NOT EXISTS methods (id TEXT PRIMARY KEY, domain TEXT, json TEXT NOT NULL)'),
        ('equations', 'CREATE TABLE IF NOT EXISTS equations (id TEXT PRIMARY KEY, domain TEXT, json TEXT NOT NULL)'),
        ('workflows', 'CREATE TABLE IF NOT EXISTS workflows (id TEXT PRIMARY KEY, domain TEXT, json TEXT NOT NULL)'),
        ('software_tools', 'CREATE TABLE IF NOT EXISTS software_tools (id TEXT PRIMARY KEY, domain TEXT, json TEXT NOT NULL)'),
        ('datasets', 'CREATE TABLE IF NOT EXISTS datasets (id TEXT PRIMARY KEY, domain TEXT, json TEXT NOT NULL)'),
        ('use_cases', 'CREATE TABLE IF NOT EXISTS use_cases (id TEXT PRIMARY KEY, domain TEXT, sector TEXT, name TEXT, json TEXT NOT NULL)'),
        ('glossary', 'CREATE TABLE IF NOT EXISTS glossary (id TEXT PRIMARY KEY, domain TEXT, term TEXT, json TEXT NOT NULL)'),
        ('benchmark_results', '''CREATE TABLE IF NOT EXISTS benchmark_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            method_id TEXT NOT NULL,
            benchmark_id TEXT NOT NULL,
            computed_energy_kcal REAL NOT NULL,
            error_kcal REAL NOT NULL,
            timestamp TEXT NOT NULL,
            metadata TEXT,
            FOREIGN KEY (benchmark_id) REFERENCES datasets(id)
        )''')
    ]
    
    for name, sql in tables:
        conn.execute(sql)
        # Create indexes for common queries
        if name == 'sources':
            conn.execute('CREATE INDEX IF NOT EXISTS idx_sources_title ON sources(title)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_sources_doi ON sources(doi)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_sources_container_title ON sources(container_title)')
        elif name == 'benchmark_results':
            conn.execute('CREATE INDEX IF NOT EXISTS idx_benchmark_results_method ON benchmark_results(method_id)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_benchmark_results_benchmark ON benchmark_results(benchmark_id)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_benchmark_results_timestamp ON benchmark_results(timestamp)')
        elif name == 'use_cases':
            conn.execute(f'CREATE INDEX IF NOT EXISTS idx_use_cases_domain ON use_cases(domain)')
            conn.execute(f'CREATE INDEX IF NOT EXISTS idx_use_cases_sector ON use_cases(sector)')
            conn.execute(f'CREATE INDEX IF NOT EXISTS idx_use_cases_name ON use_cases(name)')
        elif name != 'glossary':
            conn.execute(f'CREATE INDEX IF NOT EXISTS idx_{name}_domain ON {name}(domain)')
        if name == 'glossary':
            conn.execute(f'CREATE INDEX IF NOT EXISTS idx_glossary_term ON glossary(term)')

def load_jsonl_to_table(conn: sqlite3.Connection, jsonl_path: Path, table: str, domain_field: str = None) -> int:
    """Load JSONL file into table."""
    import json
    count = 0
    
    for record in read_jsonl(jsonl_path):
        record_id = record.get('id')
        if not record_id:
            continue
        
        json_str = json.dumps(record, ensure_ascii=False)
        
        if table == 'sources':
            # Extract indexed fields for sources
            title = record.get('title', '')
            abstract = record.get('abstract', '')
            doi = record.get('doi', '')
            container_title = record.get('container_title', '')
            subject_list = record.get('subject', []) or []
            subject = json.dumps(subject_list) if subject_list else ''
            conn.execute(
                'INSERT OR REPLACE INTO sources (id, title, abstract, doi, container_title, subject, json) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (record_id, title, abstract, doi, container_title, subject, json_str)
            )
        elif domain_field and domain_field in record:
            domain = record[domain_field]
            if table == 'glossary':
                term = record.get('term', '')
                conn.execute(
                    f'INSERT OR REPLACE INTO {table} (id, domain, term, json) VALUES (?, ?, ?, ?)',
                    (record_id, domain, term, json_str)
                )
            elif table == 'use_cases':
                sector = record.get('sector', '')
                name = record.get('name', '')
                conn.execute(
                    f'INSERT OR REPLACE INTO {table} (id, domain, sector, name, json) VALUES (?, ?, ?, ?, ?)',
                    (record_id, domain, sector, name, json_str)
                )
            else:
                conn.execute(
                    f'INSERT OR REPLACE INTO {table} (id, domain, json) VALUES (?, ?, ?)',
                    (record_id, domain, json_str)
                )
        else:
            conn.execute(
                f'INSERT OR REPLACE INTO {table} (id, json) VALUES (?, ?)',
                (record_id, json_str)
            )
        
        count += 1
    
    return count

def main():
    """Build the QCBD database."""
    db_path = DB_DIR / 'qc_qp_expert.db'
    
    print(f"Building database at {db_path}...")
    conn = sqlite3.connect(db_path)
    
    try:
        create_tables(conn)
        print("  Tables created.")
        
        # Load data files
        data_files = [
            ('sources.jsonl', 'sources', None),
            ('concepts.qc.jsonl', 'concepts', 'domain'),
            ('concepts.qp.jsonl', 'concepts', 'domain'),
            ('concepts_qsmec.jsonl', 'concepts', 'domain'),
            ('methods.qc.jsonl', 'methods', 'domain'),
            ('methods.qp.jsonl', 'methods', 'domain'),
            ('methods_qsmec.jsonl', 'methods', 'domain'),
            ('equations.jsonl', 'equations', 'domain'),
            ('equations_qsmec.jsonl', 'equations', 'domain'),
            ('workflows.jsonl', 'workflows', 'domain'),
            ('software_tools.jsonl', 'software_tools', 'domain'),
            ('datasets.jsonl', 'datasets', 'domain'),
            ('benchmarks_qsmec.jsonl', 'datasets', 'domain'),
            ('benchmarks_qc_qp_advanced.jsonl', 'datasets', 'domain'),
            ('glossary.jsonl', 'glossary', 'domain')
        ]
        
        total_count = 0
        for filename, table, domain_field in data_files:
            filepath = DATA_PROCESSED / filename
            if not filepath.exists():
                print(f"  [SKIP] {filename} (not found)")
                continue
            
            count = load_jsonl_to_table(conn, filepath, table, domain_field)
            total_count += count
            print(f"  [LOADED] {filename} -> {table} ({count} records)")
        
        # Also load Crossref journals and arXiv preprints into sources to maximize coverage
        from utils import DATA_RAW
        crossref_path = DATA_RAW / 'journals' / 'crossref_qcqp.jsonl'
        if crossref_path.exists():
            count = load_jsonl_to_table(conn, crossref_path, 'sources', None)
            total_count += count
            print(f"  [LOADED] crossref_qcqp.jsonl -> sources ({count} records)")
        else:
            print("  [SKIP] crossref_qcqp.jsonl (not found)")
        
        arxiv_path = DATA_RAW / 'preprints' / 'arxiv_qcqp.jsonl'
        if arxiv_path.exists():
            count = load_jsonl_to_table(conn, arxiv_path, 'sources', None)
            total_count += count
            print(f"  [LOADED] arxiv_qcqp.jsonl -> sources ({count} records)")
        else:
            print("  [SKIP] arxiv_qcqp.jsonl (not found)")
        
        # Load benchmark datasets (expanded to 35 sets including thermochem/excited/molecules)
        benchmark_files = [
            'benchmarks/s22_benchmarks.jsonl',
            'benchmarks/s66_benchmarks.jsonl',
            'benchmarks/gmtkn55_subsets.jsonl',
            'benchmarks/water27_benchmarks.jsonl',
            'benchmarks/s66x8_benchmarks.jsonl',
            'benchmarks/x40_benchmarks.jsonl',
            'benchmarks/aconf_benchmarks.jsonl',
            'benchmarks/conformers_benchmarks.jsonl',
            'benchmarks/hbonding_benchmarks.jsonl',
            'benchmarks/ionic_chalcogen_benchmarks.jsonl',
            'benchmarks/thermochem_benchmarks.jsonl',
            'benchmarks/bandgap30_benchmarks.jsonl',
            'benchmarks/supercond_benchmarks.jsonl',
            'benchmarks/nitrides_benchmarks.jsonl',
            'benchmarks/2dmater_benchmarks.jsonl',
            'benchmarks/battery24_benchmarks.jsonl',
            'benchmarks/magnetic_benchmarks.jsonl',
            'benchmarks/tmqb_benchmarks.jsonl',
            'benchmarks/sconf21_benchmarks.jsonl',
            'benchmarks/thz_response_benchmarks.jsonl',
            'benchmarks/qmcrystal_benchmarks.jsonl',
            'benchmarks/adsorption_benchmarks.jsonl',
            'benchmarks/defects_benchmarks.jsonl',
            'benchmarks/thermochem_extended_benchmarks.jsonl',
            'benchmarks/excited_state_benchmarks.jsonl',
            'benchmarks/benchmark_molecules_smiles.jsonl'
        ]
        for bench_file in benchmark_files:
            bench_path = DATA_RAW / bench_file
            if bench_path.exists():
                count = load_jsonl_to_table(conn, bench_path, 'datasets', 'domain')
                total_count += count
                print(f"  [LOADED] {bench_file} -> datasets ({count} records)")
            else:
                print(f"  [SKIP] {bench_file} (not found)")
        
        # Load use cases from raw directory
        use_cases_raw = Path(DATA_PROCESSED.parent / 'raw' / 'use_cases')
        if use_cases_raw.exists():
            for uc_file in use_cases_raw.glob('*.jsonl'):
                count = load_jsonl_to_table(conn, uc_file, 'use_cases', 'domain')
                total_count += count
                print(f"  [LOADED] {uc_file.name} -> use_cases ({count} records)")
        
        conn.commit()
        print(f"\nDatabase built successfully: {total_count} total records.")
        return 0
        
    except Exception as e:
        conn.rollback()
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    finally:
        conn.close()

if __name__ == '__main__':
    sys.exit(main())
