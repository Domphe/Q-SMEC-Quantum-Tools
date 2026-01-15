import csv
import os
from datetime import datetime
from neo4j import GraphDatabase
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

# Env variables with sane defaults
NEO4J_URI = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
NEO4J_USER = os.getenv('NEO4J_USER', 'neo4j')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'password')


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
            'created_at': row.get('created_at') or datetime.utcnow().isoformat() + 'Z',
            'updated_at': row.get('updated_at') or datetime.utcnow().isoformat() + 'Z',
        }
        session.run(
            "MERGE (n:Node {node_id:$node_id}) SET n += $props",
            node_id=props['node_id'], props=props
        )
        # Add labels by node_type and domain for easier queries
        session.run(
            "MATCH (n:Node {node_id:$node_id}) SET n:`%s` SET n:`%s`" % (props['node_type'], props['domain']),
            node_id=props['node_id']
        )


def load_edges(session, edges):
    for row in edges:
        props = {
            'edge_id': row['edge_id'],
            'relation_type': row['relation_type'],
            'description': row.get('description') or None,
            'primary_source': row.get('primary_source') or None,
            'confidence': row.get('confidence') or 'medium',
            'created_by': row.get('created_by') or 'system',
            'created_at': row.get('created_at') or datetime.utcnow().isoformat() + 'Z',
            'updated_at': row.get('updated_at') or datetime.utcnow().isoformat() + 'Z',
        }
        session.run(
            """
            MATCH (a:Node {node_id:$from_id})
            MATCH (b:Node {node_id:$to_id})
            MERGE (a)-[r:REL {edge_id:$edge_id}]->(b)
            SET r += $props
            SET r:`%s`
            """ % props['relation_type'],
            from_id=row['from_node_id'], to_id=row['to_node_id'], edge_id=props['edge_id'], props=props
        )


def main():
    nodes = read_csv(os.path.normpath(NODE_FILE))
    edges = read_csv(os.path.normpath(EDGE_FILE))
    try:
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        with driver.session() as session:
            ensure_constraints(session)
            load_nodes(session, nodes)
            load_edges(session, edges)
        driver.close()
    except Exception as e:
        print("Neo4j connection/ingestion error: %s" % e)
        print("Check NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD and that Neo4j is running and reachable.")
        return
    print("Ingestion complete: %d nodes, %d edges" % (len(nodes), len(edges)))


if __name__ == '__main__':
    main()
