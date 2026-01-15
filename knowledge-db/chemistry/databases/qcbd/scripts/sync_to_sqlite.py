"""
SQLite Alternative Graph Database
Fallback storage when Neo4j unavailable - stores graph in SQLite with simple schema.
"""

import sqlite3
import json
from pathlib import Path
from typing import Dict, List, Any
import os


class SQLiteGraphDB:
    """Simple graph database using SQLite for fallback."""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            qcbd_root = os.environ.get('QCBD_ROOT', r'G:\My Drive\Databases\QCBD')
            db_path = Path(qcbd_root) / 'qc_graph.db'
        
        self.db_path = Path(db_path)
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        self._initialize_schema()
    
    def _initialize_schema(self):
        """Create tables for graph storage."""
        cursor = self.conn.cursor()
        
        # Nodes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS nodes (
                id TEXT PRIMARY KEY,
                label TEXT NOT NULL,
                name TEXT,
                properties TEXT
            )
        """)
        
        # Relationships table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS relationships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_id TEXT NOT NULL,
                target_id TEXT NOT NULL,
                rel_type TEXT NOT NULL,
                FOREIGN KEY (source_id) REFERENCES nodes(id),
                FOREIGN KEY (target_id) REFERENCES nodes(id)
            )
        """)
        
        # Indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_nodes_label ON nodes(label)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_rel_source ON relationships(source_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_rel_target ON relationships(target_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_rel_type ON relationships(rel_type)")
        
        self.conn.commit()
    
    def clear_database(self):
        """Clear all data."""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM relationships")
        cursor.execute("DELETE FROM nodes")
        self.conn.commit()
        print("✓ Database cleared")
    
    def add_node(self, node_id: str, label: str, properties: Dict):
        """Add a node."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO nodes (id, label, name, properties)
            VALUES (?, ?, ?, ?)
        """, (node_id, label, properties.get('name', ''), json.dumps(properties)))
        self.conn.commit()
    
    def add_relationship(self, source_id: str, target_id: str, rel_type: str):
        """Add a relationship."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO relationships (source_id, target_id, rel_type)
            VALUES (?, ?, ?)
        """, (source_id, target_id, rel_type))
        self.conn.commit()
    
    def get_node(self, node_id: str) -> Dict:
        """Get node by ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM nodes WHERE id = ?", (node_id,))
        row = cursor.fetchone()
        if row:
            return {
                'id': row['id'],
                'label': row['label'],
                'properties': json.loads(row['properties'])
            }
        return None
    
    def get_stats(self) -> Dict:
        """Get database statistics."""
        cursor = self.conn.cursor()
        
        # Node counts by label
        cursor.execute("SELECT label, COUNT(*) as count FROM nodes GROUP BY label")
        node_counts = {row['label']: row['count'] for row in cursor.fetchall()}
        
        # Total nodes
        cursor.execute("SELECT COUNT(*) as count FROM nodes")
        total_nodes = cursor.fetchone()['count']
        
        # Relationship counts by type
        cursor.execute("SELECT rel_type, COUNT(*) as count FROM relationships GROUP BY rel_type")
        rel_counts = {row['rel_type']: row['count'] for row in cursor.fetchall()}
        
        # Total relationships
        cursor.execute("SELECT COUNT(*) as count FROM relationships")
        total_rels = cursor.fetchone()['count']
        
        return {
            'total_nodes': total_nodes,
            'nodes_by_label': node_counts,
            'total_relationships': total_rels,
            'relationships_by_type': rel_counts
        }
    
    def close(self):
        """Close connection."""
        self.conn.close()
    
    def sync_from_json(self, kb: Dict):
        """Sync knowledge graph from JSON."""
        print("\n=== Syncing to SQLite ===")
        
        # Clear existing data
        self.clear_database()
        
        stats = {'nodes': 0, 'relationships': 0}
        
        # Sync nodes
        label_map = {
            'Concepts': 'Concept',
            'Methods': 'Method',
            'SoftwareTools': 'SoftwareTool',
            'Parameters': 'Parameter',
            'Workflows': 'Workflow',
            'ExampleProblems': 'ExampleProblem',
            'BenchmarkSets': 'BenchmarkSet',
            'Resources': 'Resource'
        }
        
        for collection, label in label_map.items():
            for entity in kb.get(collection, []):
                self.add_node(entity['id'], label, entity)
                stats['nodes'] += 1
        
        print(f"✓ Synced {stats['nodes']} nodes")
        
        # Sync relationships
        # Load enrichment data from base files
        qcbd_root = os.environ.get('QCBD_ROOT', r'G:\My Drive\Databases\QCBD')
        methods_path = Path(qcbd_root) / 'qc_methods.json'
        tools_path = Path(qcbd_root) / 'qc_software_tools.json'
        
        base_methods = []
        base_tools = []
        
        if methods_path.exists():
            with open(methods_path, 'r', encoding='utf-8') as f:
                base_methods = json.load(f)
            print(f"✓ Loaded {len(base_methods)} base methods")
        
        if tools_path.exists():
            with open(tools_path, 'r', encoding='utf-8') as f:
                base_tools = json.load(f)
            print(f"✓ Loaded {len(base_tools)} base tools")
        
        # Build lookup for base data
        base_methods_lookup = {m['id']: m for m in base_methods}
        base_tools_lookup = {t['id']: t for t in base_tools}
        
        # Sync relationships with enrichment
        rel_mappings = [
            ('Methods', 'implemented_in', 'IMPLEMENTED_IN'),
            ('SoftwareTools', 'implemented_methods', 'IMPLEMENTS'),
            ('Methods', 'theoretical_basis', 'BASED_ON'),
            ('Methods', 'validated_on_benchmarks', 'VALIDATED_ON'),
        ]
        
        for collection, field, rel_type in rel_mappings:
            for entity in kb.get(collection, []):
                source_id = entity.get('id')
                
                # Use enriched data if available
                if collection == 'Methods' and source_id in base_methods_lookup:
                    targets = base_methods_lookup[source_id].get(field, entity.get(field, []))
                elif collection == 'SoftwareTools' and source_id in base_tools_lookup:
                    targets = base_tools_lookup[source_id].get(field, entity.get(field, []))
                else:
                    targets = entity.get(field, [])
                
                if isinstance(targets, str):
                    targets = [targets]
                
                for target_id in targets:
                    try:
                        self.add_relationship(source_id, target_id, rel_type)
                        stats['relationships'] += 1
                    except:
                        pass
        
        print(f"✓ Created {stats['relationships']} relationships")
        
        return stats


def main():
    """Sync KB to SQLite."""
    qcbd_root = os.environ.get('QCBD_ROOT', r'G:\My Drive\Databases\QCBD')
    kb_path = Path(qcbd_root) / "qc_knowledge_graph_full.json"
    
    if not kb_path.exists():
        print(f"✗ Knowledge graph not found: {kb_path}")
        return 1
    
    print(f"Loading knowledge graph from: {kb_path}")
    with open(kb_path, 'r', encoding='utf-8') as f:
        kb = json.load(f)
    
    print(f"✓ Loaded {kb['metadata']['total_entities']} entities\n")
    
    # Create SQLite database
    db = SQLiteGraphDB()
    stats = db.sync_from_json(kb)
    
    # Print final stats
    print("\n=== Sync Complete ===")
    final_stats = db.get_stats()
    print(f"Total nodes: {final_stats['total_nodes']}")
    print(f"Total relationships: {final_stats['total_relationships']}")
    print("\nNodes by type:")
    for label, count in final_stats['nodes_by_label'].items():
        print(f"  {label}: {count}")
    print("\nRelationships by type:")
    for rel_type, count in final_stats['relationships_by_type'].items():
        print(f"  {rel_type}: {count}")
    
    db.close()
    print(f"\n✓ Database saved to: {db.db_path}")
    return 0


if __name__ == "__main__":
    exit(main())
