import csv
import os
from datetime import datetime, timezone
try:
    from dotenv import load_dotenv
    _DOTENV_AVAILABLE = True
except Exception:
    _DOTENV_AVAILABLE = False

# Resolve paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
NODE_FILE = os.path.join(BASE_DIR, 'master_nodes.csv')
EDGE_FILE = os.path.join(BASE_DIR, 'master_edges.csv')

# Load .env if available
if _DOTENV_AVAILABLE:
    load_dotenv(os.path.join(BASE_DIR, '.env'))

# Env variables
NEO4J_URI = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
NEO4J_USER = os.getenv('NEO4J_USER', 'neo4j')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'password')

print(f"Connecting to: {NEO4J_URI}")
print(f"Username: {NEO4J_USER}")

try:
    from neo4j import GraphDatabase
    
    # Create driver - bolt+s:// handles encryption automatically
    driver = GraphDatabase.driver(
        NEO4J_URI, 
        auth=(NEO4J_USER, NEO4J_PASSWORD)
    )
    
    # Verify connectivity
    driver.verify_connectivity()
    print("✓ Connection verified!")
    
    def read_csv(path):
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    
    def ensure_constraints(session):
        session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (n:Node) REQUIRE n.node_id IS UNIQUE")
    
    def load_nodes(session, nodes):
        for row in nodes:
            props = {
                'node_id': row['node_id'],
                'node_type': row['node_type'],
                'domain': row['domain'],
                'name': row['name'],
                'subtype': row.get('subtype') or None,
                'description': row.get('description') or None,
                'spec_json': row.get('spec_json') or '{}',
                'primary_source': row.get('primary_source') or None,
                'status': row.get('status') or 'draft',
                'created_by': row.get('created_by') or 'system',
                'created_at': row.get('created_at') or datetime.now(timezone.utc).isoformat(),
                'updated_at': row.get('updated_at') or datetime.now(timezone.utc).isoformat(),
            }
            session.run(
                "MERGE (n:Node {node_id:$node_id}) SET n += $props",
                node_id=props['node_id'], props=props
            )
            # Add labels by node_type and domain
            session.run(
                f"MATCH (n:Node {{node_id:$node_id}}) SET n:`{props['node_type']}` SET n:`{props['domain']}`",
                node_id=props['node_id']
            )
            print(f"  Loaded node: {props['node_id']}")
    
    def load_edges(session, edges):
        for row in edges:
            props = {
                'edge_id': row['edge_id'],
                'relation_type': row['relation_type'],
                'description': row.get('description') or None,
                'primary_source': row.get('primary_source') or None,
                'confidence': row.get('confidence') or 'medium',
                'created_by': row.get('created_by') or 'system',
                'created_at': row.get('created_at') or datetime.now(timezone.utc).isoformat(),
                'updated_at': row.get('updated_at') or datetime.now(timezone.utc).isoformat(),
            }
            session.run(
                f"""
                MATCH (a:Node {{node_id:$from_id}})
                MATCH (b:Node {{node_id:$to_id}})
                MERGE (a)-[r:REL {{edge_id:$edge_id}}]->(b)
                SET r += $props
                SET r:`{props['relation_type']}`
                """,
                from_id=row['from_node_id'], to_id=row['to_node_id'], 
                edge_id=props['edge_id'], props=props
            )
            print(f"  Loaded edge: {props['edge_id']}")
    
    # Load data
    nodes = read_csv(os.path.normpath(NODE_FILE))
    edges = read_csv(os.path.normpath(EDGE_FILE))
    
    print(f"\nLoading {len(nodes)} nodes...")
    with driver.session() as session:
        ensure_constraints(session)
        load_nodes(session, nodes)
    
    print(f"\nLoading {len(edges)} edges...")
    with driver.session() as session:
        load_edges(session, edges)
    
    driver.close()
    print(f"\n✓ Ingestion complete: {len(nodes)} nodes, {len(edges)} edges")
    print("\nNext steps:")
    print("1. Go to: https://console.neo4j.io")
    print("2. Click 'Query' on your database")
    print("3. Run: MATCH (n) RETURN n LIMIT 25")

except Exception as e:
    print(f"\n✗ Error: {e}")
    print("\nTroubleshooting:")
    print("1. Verify database is Running at https://console.neo4j.io")
    print("2. Check if a firewall/VPN is blocking the connection")
    print("3. Try from a different network if possible")
