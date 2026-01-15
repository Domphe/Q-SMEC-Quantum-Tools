#!/usr/bin/env python3
"""
Expanded database schema for QCBD with comprehensive tracking of:
- Benchmark results and method performance
- Use case technical requirements
- Material properties
- Performance metrics and validation data
"""

import sqlite3

def create_expanded_schema(db_path='db/qc_qp_expert.db'):
    """Create expanded database schema with new tables for performance tracking."""
    
    import os
    from pathlib import Path
    
    # Resolve path relative to script location
    script_dir = Path(__file__).parent
    db_path = script_dir.parent / db_path
    
    print(f"Adding expanded schema to: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Existing tables (preserved)
    existing_tables = [
        'sources', 'concepts', 'methods', 'equations', 'workflows',
        'software_tools', 'datasets', 'use_cases', 'glossary', 'benchmark_results'
    ]
    
    # New tables for expanded functionality
    
    # 1. Method Performance Tracking
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS method_performance (
        id TEXT PRIMARY KEY,
        method_id TEXT NOT NULL,
        benchmark_id TEXT NOT NULL,
        metric_type TEXT NOT NULL,  -- 'accuracy', 'computational_cost', 'scalability'
        metric_value REAL,
        metric_unit TEXT,
        dataset_size INTEGER,
        computational_time_s REAL,
        memory_gb REAL,
        num_processors INTEGER,
        software_used TEXT,
        basis_set TEXT,
        functional TEXT,
        convergence_criteria TEXT,
        reference_source TEXT,
        validated_date TEXT,
        notes TEXT,
        json TEXT NOT NULL,
        FOREIGN KEY (method_id) REFERENCES methods(id),
        FOREIGN KEY (benchmark_id) REFERENCES datasets(id)
    )
    ''')
    
    # 2. Use Case Technical Requirements
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS use_case_requirements (
        id TEXT PRIMARY KEY,
        use_case_id TEXT NOT NULL,
        requirement_type TEXT NOT NULL,  -- 'performance', 'environmental', 'cost', 'regulatory'
        requirement_name TEXT NOT NULL,
        target_value TEXT,
        min_value REAL,
        max_value REAL,
        unit TEXT,
        priority TEXT,  -- 'critical', 'high', 'medium', 'low'
        validation_method TEXT,
        current_status TEXT,  -- 'met', 'in_progress', 'at_risk', 'not_met'
        trl_milestone INTEGER,
        notes TEXT,
        json TEXT NOT NULL,
        FOREIGN KEY (use_case_id) REFERENCES use_cases(id)
    )
    ''')
    
    # 3. Material Properties Database
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS material_properties (
        id TEXT PRIMARY KEY,
        material_id TEXT NOT NULL,
        property_type TEXT NOT NULL,  -- 'electronic', 'thermal', 'mechanical', 'optical', 'magnetic'
        property_name TEXT NOT NULL,
        property_value REAL,
        property_unit TEXT,
        temperature_k REAL,
        pressure_gpa REAL,
        measurement_method TEXT,
        computational_method TEXT,
        uncertainty REAL,
        reference_source TEXT,
        validated_experimental BOOLEAN,
        quality_score REAL,  -- 0-1 confidence score
        json TEXT NOT NULL
    )
    ''')
    
    # 4. Performance Metrics Time Series
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS performance_metrics (
        id TEXT PRIMARY KEY,
        entity_id TEXT NOT NULL,  -- Can reference methods, use_cases, materials
        entity_type TEXT NOT NULL,
        metric_name TEXT NOT NULL,
        metric_value REAL,
        metric_unit TEXT,
        timestamp TEXT,
        measurement_conditions TEXT,
        operator TEXT,
        instrument TEXT,
        calibration_date TEXT,
        environmental_conditions TEXT,
        json TEXT NOT NULL
    )
    ''')
    
    # 5. Benchmark Metadata Extended
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS benchmark_metadata (
        id TEXT PRIMARY KEY,
        benchmark_id TEXT NOT NULL,
        data_source TEXT,
        num_entries INTEGER,
        property_range_min REAL,
        property_range_max REAL,
        chemical_space TEXT,  -- e.g., 'organic', 'inorganic', 'organometallic'
        system_size_range TEXT,
        accuracy_targets TEXT,  -- JSON with multiple accuracy metrics
        reference_level TEXT,  -- e.g., 'CCSD(T)/CBS', 'Experimental'
        validation_protocol TEXT,
        last_updated TEXT,
        curator TEXT,
        doi TEXT,
        notes TEXT,
        json TEXT NOT NULL,
        FOREIGN KEY (benchmark_id) REFERENCES datasets(id)
    )
    ''')
    
    # 6. Method Applicability Matrix
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS method_applicability (
        id TEXT PRIMARY KEY,
        method_id TEXT NOT NULL,
        problem_type TEXT NOT NULL,
        system_size_min INTEGER,
        system_size_max INTEGER,
        accuracy_expected TEXT,
        computational_scaling TEXT,  -- e.g., 'O(N^3)', 'O(N^5)'
        memory_scaling TEXT,
        recommended BOOLEAN,
        limitations TEXT,
        best_practices TEXT,
        json TEXT NOT NULL,
        FOREIGN KEY (method_id) REFERENCES methods(id)
    )
    ''')
    
    # 7. Cross-Reference Links
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cross_references (
        id TEXT PRIMARY KEY,
        source_id TEXT NOT NULL,
        source_type TEXT NOT NULL,  -- 'concept', 'method', 'equation', etc.
        target_id TEXT NOT NULL,
        target_type TEXT NOT NULL,
        relationship_type TEXT NOT NULL,  -- 'uses', 'implements', 'validates', 'extends'
        strength REAL,  -- 0-1 relationship strength
        bidirectional BOOLEAN,
        notes TEXT,
        json TEXT NOT NULL
    )
    ''')
    
    # 8. Validation Results
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS validation_results (
        id TEXT PRIMARY KEY,
        method_id TEXT NOT NULL,
        benchmark_id TEXT NOT NULL,
        validation_date TEXT,
        mae REAL,
        rmse REAL,
        max_error REAL,
        r2_score REAL,
        num_outliers INTEGER,
        pass_rate REAL,
        validator TEXT,
        validation_notes TEXT,
        json TEXT NOT NULL,
        FOREIGN KEY (method_id) REFERENCES methods(id),
        FOREIGN KEY (benchmark_id) REFERENCES datasets(id)
    )
    ''')
    
    # Create indexes for performance
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_method_perf_method ON method_performance(method_id)",
        "CREATE INDEX IF NOT EXISTS idx_method_perf_benchmark ON method_performance(benchmark_id)",
        "CREATE INDEX IF NOT EXISTS idx_use_case_req ON use_case_requirements(use_case_id)",
        "CREATE INDEX IF NOT EXISTS idx_material_prop_type ON material_properties(property_type)",
        "CREATE INDEX IF NOT EXISTS idx_perf_metrics_entity ON performance_metrics(entity_id, entity_type)",
        "CREATE INDEX IF NOT EXISTS idx_cross_ref_source ON cross_references(source_id, source_type)",
        "CREATE INDEX IF NOT EXISTS idx_cross_ref_target ON cross_references(target_id, target_type)",
        "CREATE INDEX IF NOT EXISTS idx_validation_method ON validation_results(method_id)"
    ]
    
    for index_sql in indexes:
        cursor.execute(index_sql)
    
    conn.commit()
    
    # Print schema summary
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()
    
    print("=" * 80)
    print("EXPANDED DATABASE SCHEMA CREATED")
    print("=" * 80)
    print(f"\nTotal Tables: {len(tables)}\n")
    
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table[0]})")
        columns = cursor.fetchall()
        print(f"{table[0]} ({len(columns)} columns):")
        for col in columns[:5]:  # Show first 5 columns
            print(f"  • {col[1]} ({col[2]})")
        if len(columns) > 5:
            print(f"  ... and {len(columns) - 5} more columns")
        print()
    
    conn.close()
    print("Schema creation complete!")
    return db_path

if __name__ == '__main__':
    create_expanded_schema()
