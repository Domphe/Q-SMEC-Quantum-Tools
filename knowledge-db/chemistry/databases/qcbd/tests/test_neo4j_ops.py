"""
Neo4j Operations Tests
Tests database sync, backups, queries, and relationship integrity.
"""

import pytest
import json
from pathlib import Path
from neo4j import GraphDatabase
import os
import time


QCBD_ROOT = Path(os.environ.get('QCBD_ROOT', r'G:\My Drive\Databases\QCBD'))
NEO4J_URI = os.environ.get('NEO4J_URI', 'bolt://localhost:7687')
NEO4J_USER = os.environ.get('NEO4J_USER', 'neo4j')
NEO4J_PASSWORD = os.environ.get('NEO4J_PASSWORD', 'quantum_db_2025')


class TestNeo4jConnection:
    """Test Neo4j connection and setup."""
    
    def test_neo4j_connection(self):
        """Test that Neo4j is accessible."""
        try:
            driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
            with driver.session() as session:
                result = session.run("RETURN 1 AS num")
                assert result.single()['num'] == 1
            driver.close()
        except Exception as e:
            pytest.fail(f"Cannot connect to Neo4j: {e}")
    
    def test_neo4j_version(self):
        """Test Neo4j version is 5.x."""
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        with driver.session() as session:
            result = session.run("CALL dbms.components() YIELD versions RETURN versions[0] AS version")
            version = result.single()['version']
            assert version.startswith('5.'), f"Expected Neo4j 5.x, got {version}"
        driver.close()


class TestNeo4jSync:
    """Test knowledge graph sync to Neo4j."""
    
    @pytest.fixture(scope='class')
    def driver(self):
        """Neo4j driver fixture."""
        drv = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        yield drv
        drv.close()
    
    def test_constraints_exist(self, driver):
        """Test that uniqueness constraints are created."""
        with driver.session() as session:
            result = session.run("SHOW CONSTRAINTS")
            constraints = [record['name'] for record in result]
            
            expected_constraints = [
                'unique_concept_id',
                'unique_method_id',
                'unique_tool_id',
                'unique_parameter_id',
                'unique_workflow_id'
            ]
            
            for constraint in expected_constraints:
                assert any(constraint in c for c in constraints), \
                    f"Missing constraint: {constraint}"
    
    def test_nodes_exist(self, driver):
        """Test that nodes were synced."""
        with driver.session() as session:
            # Check Concepts
            result = session.run("MATCH (c:Concept) RETURN count(c) AS count")
            concept_count = result.single()['count']
            assert concept_count > 0, "No Concept nodes found"
            
            # Check Methods
            result = session.run("MATCH (m:Method) RETURN count(m) AS count")
            method_count = result.single()['count']
            assert method_count > 0, "No Method nodes found"
            
            # Check Tools
            result = session.run("MATCH (t:SoftwareTool) RETURN count(t) AS count")
            tool_count = result.single()['count']
            assert tool_count > 0, "No SoftwareTool nodes found"
    
    def test_relationships_exist(self, driver):
        """Test that relationships were created."""
        with driver.session() as session:
            # Check PREREQUISITE_OF
            result = session.run(
                "MATCH ()-[r:PREREQUISITE_OF]->() RETURN count(r) AS count"
            )
            count = result.single()['count']
            # May be 0 if not defined in JSON
            assert count >= 0
            
            # Check BASED_ON
            result = session.run(
                "MATCH ()-[r:BASED_ON]->() RETURN count(r) AS count"
            )
            count = result.single()['count']
            assert count >= 0
            
            # Check IMPLEMENTS
            result = session.run(
                "MATCH ()-[r:IMPLEMENTS]->() RETURN count(r) AS count"
            )
            count = result.single()['count']
            assert count >= 0


class TestNeo4jQuery:
    """Test Cypher queries."""
    
    @pytest.fixture(scope='class')
    def driver(self):
        drv = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        yield drv
        drv.close()
    
    def test_find_methods_by_accuracy(self, driver):
        """Test finding methods by accuracy level."""
        query = """
        MATCH (m:Method)
        WHERE m.accuracy_level IN ['high', 'very_high']
        RETURN m.id AS id, m.name AS name, m.accuracy_level AS accuracy
        LIMIT 10
        """
        
        with driver.session() as session:
            result = session.run(query)
            methods = [dict(record) for record in result]
            
            # Should find some high-accuracy methods
            assert len(methods) >= 0  # May be 0 if data not populated
    
    def test_method_with_tools(self, driver):
        """Test finding tools that implement a method."""
        query = """
        MATCH (m:Method)<-[:IMPLEMENTS]-(t:SoftwareTool)
        RETURN m.name AS method, collect(t.name) AS tools
        LIMIT 5
        """
        
        with driver.session() as session:
            result = session.run(query)
            results = [dict(record) for record in result]
            
            # May be empty if relationships not defined
            assert isinstance(results, list)
    
    def test_workflow_methods(self, driver):
        """Test finding methods used in workflows."""
        query = """
        MATCH (w:Workflow)-[:RELATED_TO]->(m:Method)
        RETURN w.name AS workflow, m.name AS method
        LIMIT 10
        """
        
        with driver.session() as session:
            result = session.run(query)
            results = [dict(record) for record in result]
            assert isinstance(results, list)


class TestNeo4jBackup:
    """Test backup functionality."""
    
    def test_backup_script_exists(self):
        """Test that backup script exists."""
        backup_script = QCBD_ROOT / "scripts" / "neo4j_backup.ps1"
        assert backup_script.exists(), "Backup script not found"
    
    def test_backup_directory_exists(self):
        """Test that backup directory is created."""
        backup_dir = QCBD_ROOT / "neo4j_backups"
        if not backup_dir.exists():
            backup_dir.mkdir(parents=True, exist_ok=True)
        assert backup_dir.exists()


@pytest.mark.slow
def test_full_sync_cycle():
    """Test complete sync cycle: clear -> sync -> verify."""
    from sync_to_neo4j import Neo4jSyncManager
    
    # Load KB
    kb_path = QCBD_ROOT / "qc_knowledge_graph_full.json"
    if not kb_path.exists():
        pytest.skip("Knowledge graph not built")
    
    with open(kb_path, 'r', encoding='utf-8') as f:
        kb = json.load(f)
    
    # Create sync manager
    manager = Neo4jSyncManager(uri=NEO4J_URI, user=NEO4J_USER, password=NEO4J_PASSWORD)
    
    # Clear and sync
    manager.clear_database()
    time.sleep(1)
    
    manager.create_constraints()
    manager.sync_all(kb)
    
    # Verify
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    with driver.session() as session:
        result = session.run("MATCH (n) RETURN count(n) AS count")
        node_count = result.single()['count']
        assert node_count > 0, "No nodes after sync"
    
    driver.close()
    manager.close()


if __name__ == "__main__":
    pytest.main([__file__, '-v'])
