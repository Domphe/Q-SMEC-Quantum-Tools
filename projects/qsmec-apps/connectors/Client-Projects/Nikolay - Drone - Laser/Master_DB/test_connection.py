import os
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
except Exception:
    pass

print("Neo4j Configuration:")
print(f"  URI: {os.getenv('NEO4J_URI', 'NOT SET')}")
print(f"  USER: {os.getenv('NEO4J_USER', 'NOT SET')}")
print(f"  PASSWORD: {'***' + os.getenv('NEO4J_PASSWORD', 'NOT SET')[-4:] if os.getenv('NEO4J_PASSWORD') else 'NOT SET'}")

try:
    from neo4j import GraphDatabase
    uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    user = os.getenv('NEO4J_USER', 'neo4j')
    password = os.getenv('NEO4J_PASSWORD', 'password')
    
    print("\nTesting connection...")
    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session() as session:
        result = session.run("RETURN 1 as test")
        print("✓ Connection successful!")
        driver.close()
except Exception as e:
    print(f"✗ Connection failed: {e}")
    print("\nTroubleshooting:")
    print("1. Check if the database is running at https://console.neo4j.io")
    print("2. Verify the instance status is 'Running'")
    print("3. Wait 60-120 seconds after creation for full startup")
    print("4. Check if your IP needs to be whitelisted (Aura settings)")
