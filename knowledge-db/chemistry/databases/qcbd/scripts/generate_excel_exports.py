"""
Generate Excel exports from Neo4j knowledge base.
Creates sortable method comparison tables and software capability matrices.
"""

import pandas as pd
from neo4j import GraphDatabase
import os
from pathlib import Path
from datetime import datetime


QCBD_ROOT = Path(os.environ.get('QCBD_ROOT', r'G:\My Drive\Databases\QCBD'))
NEO4J_URI = os.environ.get('NEO4J_URI', 'bolt://localhost:7687')
NEO4J_USER = os.environ.get('NEO4J_USER', 'neo4j')
NEO4J_PASSWORD = os.environ.get('NEO4J_PASSWORD', 'quantum_db_2025')


def export_methods_reference():
    """Generate QC_Methods_Reference.xlsx with sortable columns."""
    
    print("Connecting to Neo4j...")
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    # Query all methods with related information
    query = """
    MATCH (m:Method)
    OPTIONAL MATCH (m)-[:VALIDATED_ON]->(b:BenchmarkSet)
    OPTIONAL MATCH (m)<-[:IMPLEMENTS]-(t:SoftwareTool)
    RETURN m.id AS method_id,
           m.name AS method_name,
           m.accuracy_level AS accuracy,
           m.computational_cost AS cost,
           m.description AS description,
           m.scaling AS scaling,
           collect(DISTINCT b.name) AS benchmarks,
           collect(DISTINCT t.name) AS software_tools
    ORDER BY m.accuracy_level DESC, m.computational_cost ASC
    """
    
    with driver.session() as session:
        result = session.run(query)
        data = []
        
        for record in result:
            data.append({
                'Method ID': record['method_id'],
                'Method Name': record['method_name'],
                'Accuracy Level': record['accuracy'] or 'N/A',
                'Computational Cost': record['cost'] or 'N/A',
                'Scaling': record['scaling'] or 'N/A',
                'Description': record['description'] or '',
                'Validated on Benchmarks': ', '.join(record['benchmarks']) if record['benchmarks'] else 'None',
                'Available in Software': ', '.join(record['software_tools']) if record['software_tools'] else 'None'
            })
    
    driver.close()
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Export to Excel
    output_path = QCBD_ROOT / "exports" / "excel" / "QC_Methods_Reference.xlsx"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Methods')
        
        # Auto-adjust column widths
        worksheet = writer.sheets['Methods']
        for idx, col in enumerate(df.columns):
            max_length = max(
                df[col].astype(str).map(len).max(),
                len(col)
            )
            worksheet.column_dimensions[chr(65 + idx)].width = min(max_length + 2, 50)
    
    print(f"✓ Exported methods reference to: {output_path}")
    print(f"  Total methods: {len(df)}")
    return output_path


def export_software_capability_matrix():
    """Generate QC_Software_Capability_Matrix.xlsx (tools × methods)."""
    
    print("\nGenerating software capability matrix...")
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    # Get all software tools
    with driver.session() as session:
        result = session.run("MATCH (t:SoftwareTool) RETURN t.name AS name ORDER BY t.name")
        tools = [record['name'] for record in result]
    
    # Get all methods
    with driver.session() as session:
        result = session.run("MATCH (m:Method) RETURN m.name AS name ORDER BY m.name")
        methods = [record['name'] for record in result]
    
    # Build matrix
    matrix_data = []
    
    for method in methods:
        row = {'Method': method}
        
        for tool in tools:
            # Check if tool implements method
            with driver.session() as session:
                query = """
                MATCH (t:SoftwareTool {name: $tool})
                MATCH (m:Method {name: $method})
                RETURN EXISTS((t)-[:IMPLEMENTS]->(m)) AS implements
                """
                result = session.run(query, tool=tool, method=method)
                record = result.single()
                row[tool] = '✓' if record and record['implements'] else ''
        
        matrix_data.append(row)
    
    driver.close()
    
    # Create DataFrame
    df = pd.DataFrame(matrix_data)
    
    # Export to Excel
    output_path = QCBD_ROOT / "exports" / "excel" / "QC_Software_Capability_Matrix.xlsx"
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Capabilities')
        
        # Format
        worksheet = writer.sheets['Capabilities']
        
        # Method column width
        worksheet.column_dimensions['A'].width = 30
        
        # Tool columns width
        for idx, col in enumerate(df.columns[1:], start=2):
            worksheet.column_dimensions[chr(64 + idx)].width = 15
    
    print(f"✓ Exported capability matrix to: {output_path}")
    print(f"  Tools: {len(tools)}, Methods: {len(methods)}")
    return output_path


def export_benchmark_summary():
    """Generate benchmark summary sheet."""
    
    print("\nGenerating benchmark summary...")
    
    benchmark_dir = QCBD_ROOT / "benchmarks"
    data = []
    
    for csv_file in benchmark_dir.rglob("binding_energies.csv"):
        benchmark_name = csv_file.parent.name
        df = pd.read_csv(csv_file)
        
        error_cols = [col for col in df.columns if col.endswith('_error')]
        
        for col in error_cols:
            method_name = col.replace('_error', '').replace('_', '-').upper()
            errors = df[col].dropna()
            
            if len(errors) > 0:
                import numpy as np
                data.append({
                    'Benchmark': benchmark_name.upper(),
                    'Method': method_name,
                    'N Systems': len(errors),
                    'MAE (kcal/mol)': f"{np.mean(np.abs(errors)):.3f}",
                    'RMSE (kcal/mol)': f"{np.sqrt(np.mean(errors**2)):.3f}",
                    'Max Error (kcal/mol)': f"{np.max(np.abs(errors)):.3f}"
                })
    
    df_summary = pd.DataFrame(data)
    
    # Export
    output_path = QCBD_ROOT / "exports" / "excel" / "Benchmark_Performance_Summary.xlsx"
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        df_summary.to_excel(writer, index=False, sheet_name='Benchmarks')
        
        worksheet = writer.sheets['Benchmarks']
        for idx, col in enumerate(df_summary.columns):
            worksheet.column_dimensions[chr(65 + idx)].width = 20
    
    print(f"✓ Exported benchmark summary to: {output_path}")
    return output_path


def main():
    """Generate all Excel exports."""
    print("="*60)
    print("QCDB Excel Export Generator")
    print("="*60)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    try:
        # Generate exports
        methods_file = export_methods_reference()
        matrix_file = export_software_capability_matrix()
        benchmark_file = export_benchmark_summary()
        
        print("\n" + "="*60)
        print("✓ All exports completed successfully!")
        print("="*60)
        print("\nGenerated files:")
        print(f"  1. {methods_file.name}")
        print(f"  2. {matrix_file.name}")
        print(f"  3. {benchmark_file.name}")
        print("\nLocation:", QCBD_ROOT / "exports" / "excel")
        
    except Exception as e:
        print(f"\n✗ Error during export: {e}")
        raise


if __name__ == "__main__":
    main()
