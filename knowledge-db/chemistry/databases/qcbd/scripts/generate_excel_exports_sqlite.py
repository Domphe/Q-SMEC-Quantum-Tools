"""
Generate Excel exports from SQLite knowledge base.
Creates sortable method comparison tables and software capability matrices.
"""

import pandas as pd
import sqlite3
import os
from pathlib import Path
from datetime import datetime
import json


QCBD_ROOT = Path(os.environ.get('QCBD_ROOT', r'G:\My Drive\Databases\QCBD'))
DB_PATH = QCBD_ROOT / 'qc_graph.db'


def export_methods_reference():
    """Generate QC_Methods_Reference.xlsx with sortable columns."""
    
    print("Connecting to SQLite...")
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    
    # Query all methods with related information
    query = """
    SELECT 
        n.id AS method_id,
        n.name AS method_name,
        n.properties AS props
    FROM nodes n
    WHERE n.label = 'Method'
    ORDER BY n.name
    """
    
    cursor = conn.cursor()
    cursor.execute(query)
    
    data = []
    for row in cursor.fetchall():
        props = json.loads(row['props'])
        method_id = row['method_id']
        
        # Get benchmarks (VALIDATED_ON relationships)
        cursor2 = conn.cursor()
        cursor2.execute("""
            SELECT n.name 
            FROM relationships r
            JOIN nodes n ON r.target_id = n.id
            WHERE r.source_id = ? AND r.rel_type = 'VALIDATED_ON'
        """, (method_id,))
        benchmarks = [r[0] for r in cursor2.fetchall()]
        
        # Get software tools (IMPLEMENTS relationships pointing to this method)
        cursor2.execute("""
            SELECT n.name 
            FROM relationships r
            JOIN nodes n ON r.source_id = n.id
            WHERE r.target_id = ? AND r.rel_type = 'IMPLEMENTS'
        """, (method_id,))
        software_tools = [r[0] for r in cursor2.fetchall()]
        
        data.append({
            'Method ID': method_id,
            'Method Name': row['method_name'],
            'Accuracy Level': props.get('accuracy_level', 'N/A'),
            'Computational Cost': props.get('computational_cost', 'N/A'),
            'Scaling': props.get('scaling', 'N/A'),
            'Description': props.get('description', ''),
            'Validated on Benchmarks': ', '.join(benchmarks) if benchmarks else 'None',
            'Available in Software': ', '.join(software_tools) if software_tools else 'None'
        })
    
    conn.close()
    
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
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get all software tools
    cursor.execute("SELECT name FROM nodes WHERE label = 'SoftwareTool' ORDER BY name")
    tools = [row[0] for row in cursor.fetchall()]
    
    # Get all methods
    cursor.execute("SELECT name, id FROM nodes WHERE label = 'Method' ORDER BY name")
    methods = [(row[0], row[1]) for row in cursor.fetchall()]
    
    # Build matrix
    matrix_data = []
    for tool_name in tools:
        # Get tool ID
        cursor.execute("SELECT id FROM nodes WHERE name = ? AND label = 'SoftwareTool'", (tool_name,))
        tool_id = cursor.fetchone()[0]
        
        row_data = {'Software Tool': tool_name}
        
        for method_name, method_id in methods:
            # Check if IMPLEMENTS relationship exists
            cursor.execute("""
                SELECT COUNT(*) 
                FROM relationships 
                WHERE source_id = ? AND target_id = ? AND rel_type = 'IMPLEMENTS'
            """, (tool_id, method_id))
            
            has_impl = cursor.fetchone()[0] > 0
            row_data[method_name] = '✓' if has_impl else ''
        
        matrix_data.append(row_data)
    
    conn.close()
    
    # Create DataFrame
    df = pd.DataFrame(matrix_data)
    
    # Export to Excel
    output_path = QCBD_ROOT / "exports" / "excel" / "QC_Software_Capability_Matrix.xlsx"
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Capabilities')
        
        # Auto-adjust column widths
        worksheet = writer.sheets['Capabilities']
        for idx, col in enumerate(df.columns):
            max_length = max(
                df[col].astype(str).map(len).max(),
                len(col)
            )
            worksheet.column_dimensions[chr(65 + idx)].width = min(max_length + 2, 20)
    
    print(f"✓ Exported capability matrix to: {output_path}")
    print(f"  Software tools: {len(tools)}")
    print(f"  Methods: {len(methods)}")
    return output_path


def main():
    """Generate all Excel exports."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"=== Generating Excel Exports ({timestamp}) ===\n")
    
    if not DB_PATH.exists():
        print(f"✗ SQLite database not found: {DB_PATH}")
        print("  Run sync_to_sqlite.py first")
        return 1
    
    try:
        methods_path = export_methods_reference()
        matrix_path = export_software_capability_matrix()
        
        print("\n=== Export Complete ===")
        print(f"Methods reference: {methods_path}")
        print(f"Capability matrix: {matrix_path}")
        return 0
        
    except Exception as e:
        print(f"\n✗ Export failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
