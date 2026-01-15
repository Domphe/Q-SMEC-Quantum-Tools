import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import csv
import os
import time
from datetime import datetime, timezone

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
except Exception:
    pass

# Disable SSL warnings for self-signed certs if needed
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
NODE_FILE = os.path.join(BASE_DIR, 'master_nodes.csv')
EDGE_FILE = os.path.join(BASE_DIR, 'master_edges.csv')

NEO4J_URI = os.getenv('NEO4J_URI', '')
NEO4J_USER = os.getenv('NEO4J_USER', 'neo4j')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', '')

# Extract host from URI for HTTP API
if 'neo4j+s://' in NEO4J_URI or 'bolt+s://' in NEO4J_URI:
    host = NEO4J_URI.split('://')[1]
    API_URL = f"https://{host}/db/neo4j/query/v2"
else:
    print("Error: Expected neo4j+s:// or bolt+s:// URI")
    exit(1)

print(f"Using HTTP Query API: {API_URL}")
print(f"Username: {NEO4J_USER}")

def run_cypher(query, parameters=None, retry_count=3):
    """Execute Cypher query via HTTP API with retries"""
    payload = {
        "statement": query
    }
    if parameters:
        payload["parameters"] = parameters
    
    for attempt in range(retry_count):
        try:
            response = requests.post(
                API_URL,
                auth=(NEO4J_USER, NEO4J_PASSWORD),
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=30,
                verify=True  # Try with SSL verification first
            )
            response.raise_for_status()
            return response.json()
        except (requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
            if attempt < retry_count - 1:
                import time
                time.sleep(1)
                continue
            else:
                raise

def read_csv(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

try:
    # Test connection
    print("\nTesting connection...")
    result = run_cypher("RETURN 1 as test")
    print("✓ Connection successful!")
    
    # Load CSVs
    nodes = read_csv(NODE_FILE)
    edges = read_csv(EDGE_FILE)
    
    # Create constraint
    print("\nCreating constraints...")
    run_cypher("CREATE CONSTRAINT IF NOT EXISTS FOR (n:Node) REQUIRE n.node_id IS UNIQUE")
    
    # Load nodes
    print(f"\nLoading {len(nodes)} nodes...")
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
        run_cypher(
            "MERGE (n:Node {node_id:$node_id}) SET n += $props",
            {"node_id": props['node_id'], "props": props}
        )
        run_cypher(
            f"MATCH (n:Node {{node_id:$node_id}}) SET n:`{props['node_type']}` SET n:`{props['domain']}`",
            {"node_id": props['node_id']}
        )
        print(f"  ✓ {props['node_id']}")
    
    # Load edges
    print(f"\nLoading {len(edges)} edges...")
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
        run_cypher(
            """
            MATCH (a:Node {node_id:$from_id})
            MATCH (b:Node {node_id:$to_id})
            MERGE (a)-[r:REL {edge_id:$edge_id}]->(b)
            SET r += $props
            """,
            {
                "from_id": row['from_node_id'],
                "to_id": row['to_node_id'],
                "edge_id": props['edge_id'],
                "props": props
            }
        )
        print(f"  ✓ {props['edge_id']}")
    
    print(f"\n✓ Ingestion complete: {len(nodes)} nodes, {len(edges)} edges")
    print("\nNext steps:")
    print("1. Go to: https://console.neo4j.io")
    print("2. Click 'Query' on your database")
    print("3. Run: MATCH (n) RETURN n LIMIT 25")

except requests.exceptions.HTTPError as e:
    print(f"\n✗ HTTP Error: {e}")
    print(f"Response: {e.response.text if hasattr(e, 'response') else 'N/A'}")
except Exception as e:
    print(f"\n✗ Error: {e}")
    print("\nThis fallback uses the HTTP Query API instead of Bolt protocol.")
    print("If this also fails, check:")
    print("1. Firewall/antivirus blocking HTTPS to *.neo4j.io")
    print("2. Corporate proxy/VPN interfering")
    print("3. Try from a different network")
