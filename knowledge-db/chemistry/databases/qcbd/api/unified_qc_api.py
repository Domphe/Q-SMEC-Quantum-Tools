"""
Unified Query API for QCDB
Connects Neo4j, SQLite, ChromaDB, and Redis to provide seamless access.
"""

import os
from typing import List, Dict, Optional, Any, Tuple
from neo4j import GraphDatabase
import sqlite3
import chromadb
import redis
import json
from pathlib import Path
import hashlib


class UnifiedQCAPI:
    """Unified API for quantum chemistry knowledge base."""
    
    def __init__(self, qcbd_root: str = None):
        """Initialize connections to all databases."""
        self.qcbd_root = Path(qcbd_root or os.environ.get('QCBD_ROOT', 
                                                           r'G:\My Drive\Databases\QCBD'))
        
        # Neo4j connection
        self.neo4j_uri = os.environ.get('NEO4J_URI', 'bolt://localhost:7687')
        self.neo4j_user = os.environ.get('NEO4J_USER', 'neo4j')
        self.neo4j_password = os.environ.get('NEO4J_PASSWORD', 'quantum_db_2025')
        self.neo4j_driver = GraphDatabase.driver(
            self.neo4j_uri,
            auth=(self.neo4j_user, self.neo4j_password)
        )
        
        # Redis connection
        self.redis_uri = os.environ.get('REDIS_URI', 'redis://localhost:6379')
        self.redis_client = redis.from_url(self.redis_uri, decode_responses=True)
        self.cache_ttl = 3600  # 1 hour
        
        # ChromaDB connection
        self.chroma_client = chromadb.PersistentClient(
            path=str(self.qcbd_root / "chroma_db")
        )
        self.embedding_collection = self.chroma_client.get_or_create_collection(
            name="qc_entities",
            metadata={"description": "QC knowledge base embeddings"}
        )
        
        # SQLite connection (if quantum_ai_tools.db exists)
        self.tools_db_path = Path(r'G:\My Drive\Databases\quantum_ai_tools.db')
        self.tools_db = None
        if self.tools_db_path.exists():
            self.tools_db = sqlite3.connect(str(self.tools_db_path))
            self.tools_db.row_factory = sqlite3.Row
    
    def __del__(self):
        """Close connections."""
        if hasattr(self, 'neo4j_driver'):
            self.neo4j_driver.close()
        if hasattr(self, 'redis_client'):
            self.redis_client.close()
        if self.tools_db:
            self.tools_db.close()
    
    # ==================== Cache Management ====================
    
    def _cache_key(self, method: str, **kwargs) -> str:
        """Generate cache key from method name and params."""
        params_str = json.dumps(kwargs, sort_keys=True)
        hash_obj = hashlib.sha256(params_str.encode())
        return f"qcdb:{method}:{hash_obj.hexdigest()[:16]}"
    
    def _get_cached(self, method: str, **kwargs) -> Optional[Any]:
        """Get cached result if available."""
        key = self._cache_key(method, **kwargs)
        cached = self.redis_client.get(key)
        if cached:
            return json.loads(cached)
        return None
    
    def _set_cached(self, result: Any, method: str, **kwargs):
        """Cache query result."""
        key = self._cache_key(method, **kwargs)
        self.redis_client.setex(key, self.cache_ttl, json.dumps(result))
    
    # ==================== Method Queries ====================
    
    def find_methods_by_accuracy(
        self,
        min_accuracy: str = "medium",
        max_cost: str = None,
        system_type: str = None
    ) -> List[Dict]:
        """Find methods meeting accuracy/cost criteria.
        
        Args:
            min_accuracy: "low", "medium", "high", "very_high"
            max_cost: "low", "medium", "high", "very_high"
            system_type: Optional filter (e.g., "organic", "transition_metal")
        
        Returns:
            List of method dictionaries with properties
        """
        # Check cache
        cached = self._get_cached('find_methods_by_accuracy', 
                                 min_accuracy=min_accuracy, 
                                 max_cost=max_cost,
                                 system_type=system_type)
        if cached:
            return cached
        
        # Build Cypher query
        accuracy_order = ["low", "medium", "high", "very_high"]
        min_idx = accuracy_order.index(min_accuracy)
        acceptable_accuracies = accuracy_order[min_idx:]
        
        query = """
        MATCH (m:Method)
        WHERE m.accuracy_level IN $accuracies
        """
        
        params = {"accuracies": acceptable_accuracies}
        
        if max_cost:
            query += " AND m.computational_cost <= $max_cost"
            params["max_cost"] = max_cost
        
        query += """
        OPTIONAL MATCH (m)-[:VALIDATED_ON]->(b:BenchmarkSet)
        RETURN m.id AS id, m.name AS name, m.accuracy_level AS accuracy,
               m.computational_cost AS cost, m.description AS description,
               collect(DISTINCT b.name) AS benchmarks
        ORDER BY m.accuracy_level DESC, m.computational_cost ASC
        """
        
        with self.neo4j_driver.session() as session:
            result = session.run(query, params)
            methods = [dict(record) for record in result]
        
        # Filter by system type if specified (from description text)
        if system_type:
            methods = [m for m in methods if system_type.lower() in m['description'].lower()]
        
        # Cache and return
        self._set_cached(methods, 'find_methods_by_accuracy',
                        min_accuracy=min_accuracy, max_cost=max_cost,
                        system_type=system_type)
        return methods
    
    def get_method_details(self, method_id: str) -> Optional[Dict]:
        """Get full details for a method."""
        cached = self._get_cached('get_method_details', method_id=method_id)
        if cached:
            return cached
        
        query = """
        MATCH (m:Method {id: $method_id})
        OPTIONAL MATCH (m)-[:BASED_ON]->(c:Concept)
        OPTIONAL MATCH (m)<-[:IMPLEMENTS]-(t:SoftwareTool)
        OPTIONAL MATCH (m)-[:VALIDATED_ON]->(b:BenchmarkSet)
        OPTIONAL MATCH (m)-[:USED_IN]->(w:Workflow)
        RETURN m, collect(DISTINCT c) AS concepts,
               collect(DISTINCT t) AS tools,
               collect(DISTINCT b) AS benchmarks,
               collect(DISTINCT w) AS workflows
        """
        
        with self.neo4j_driver.session() as session:
            result = session.run(query, method_id=method_id)
            record = result.single()
            
            if not record:
                return None
            
            method = dict(record['m'])
            method['theoretical_basis'] = [dict(c) for c in record['concepts']]
            method['implemented_in'] = [dict(t) for t in record['tools']]
            method['validated_on'] = [dict(b) for b in record['benchmarks']]
            method['used_in_workflows'] = [dict(w) for w in record['workflows']]
        
        self._set_cached(method, 'get_method_details', method_id=method_id)
        return method
    
    # ==================== Tool Queries ====================
    
    def get_workflows_for_tool(self, tool_id: str) -> List[Dict]:
        """Get all workflows that use a specific tool."""
        cached = self._get_cached('get_workflows_for_tool', tool_id=tool_id)
        if cached:
            return cached
        
        query = """
        MATCH (t:SoftwareTool {id: $tool_id})<-[:SUPPORTS]-(w:Workflow)
        OPTIONAL MATCH (w)-[:RELATED_TO]->(m:Method)
        RETURN w, collect(DISTINCT m) AS methods
        ORDER BY w.difficulty_level
        """
        
        with self.neo4j_driver.session() as session:
            result = session.run(query, tool_id=tool_id)
            workflows = []
            for record in result:
                workflow = dict(record['w'])
                workflow['methods'] = [dict(m) for m in record['methods']]
                workflows.append(workflow)
        
        self._set_cached(workflows, 'get_workflows_for_tool', tool_id=tool_id)
        return workflows
    
    def find_tools_with_capability(self, capability: str) -> List[Dict]:
        """Find tools that support a specific capability."""
        query = """
        MATCH (t:SoftwareTool)
        WHERE $capability IN t.capabilities OR 
              t.description CONTAINS $capability
        RETURN t.id AS id, t.name AS name, t.version AS version,
               t.capabilities AS capabilities, t.license AS license
        ORDER BY t.name
        """
        
        with self.neo4j_driver.session() as session:
            result = session.run(query, capability=capability)
            return [dict(record) for record in result]
    
    # ==================== Semantic Search ====================
    
    def semantic_search(
        self,
        query: str,
        entity_types: List[str] = None,
        top_k: int = 10
    ) -> List[Dict]:
        """Semantic search across knowledge base.
        
        Args:
            query: Natural language query
            entity_types: Filter by types (e.g., ['Method', 'Workflow'])
            top_k: Number of results to return
        
        Returns:
            List of matching entities with similarity scores
        """
        # Import embedding manager
        from qcdb_embeddings import EmbeddingManager
        embedding_mgr = EmbeddingManager(qcbd_root=str(self.qcbd_root))
        
        # Get query embedding
        query_embedding = embedding_mgr.embed(query)
        
        # Query ChromaDB
        where_filter = None
        if entity_types:
            where_filter = {"entity_type": {"$in": entity_types}}
        
        results = self.embedding_collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_filter
        )
        
        # Format results
        matches = []
        for i, doc_id in enumerate(results['ids'][0]):
            matches.append({
                'id': doc_id,
                'metadata': results['metadatas'][0][i],
                'text': results['documents'][0][i],
                'similarity': 1 - results['distances'][0][i]  # Convert distance to similarity
            })
        
        return matches
    
    # ==================== Benchmark Queries ====================
    
    def get_benchmark_performance(
        self,
        benchmark_id: str,
        methods: List[str] = None
    ) -> Dict:
        """Get method performance on a benchmark.
        
        Args:
            benchmark_id: Benchmark set ID (e.g., 's22', 's66')
            methods: Optional list of method names to filter
        
        Returns:
            Dictionary with benchmark data and method statistics
        """
        # Load from CSV
        csv_path = self.qcbd_root / "benchmarks" / benchmark_id / "binding_energies.csv"
        
        if not csv_path.exists():
            return {"error": f"Benchmark data not found: {benchmark_id}"}
        
        import pandas as pd
        df = pd.read_csv(csv_path)
        
        # Calculate statistics
        stats = {}
        error_cols = [col for col in df.columns if col.endswith('_error')]
        
        for col in error_cols:
            method_name = col.replace('_error', '')
            if methods and method_name not in methods:
                continue
            
            errors = df[col].dropna()
            if len(errors) > 0:
                import numpy as np
                stats[method_name] = {
                    'mae': float(np.mean(np.abs(errors))),
                    'rmse': float(np.sqrt(np.mean(errors**2))),
                    'max_error': float(np.max(np.abs(errors))),
                    'n_systems': len(errors)
                }
        
        return {
            'benchmark_id': benchmark_id,
            'statistics': stats,
            'systems': df.to_dict('records')
        }
    
    # ==================== AI Tool Integration ====================
    
    def find_ai_tools_for_qc_method(self, method_id: str) -> List[Dict]:
        """Find AI tools from quantum_ai_tools.db related to QC method.
        
        Bridges QCDB and existing quantum_ai_tools database.
        """
        if not self.tools_db:
            return []
        
        # Get method details from QCDB
        method = self.get_method_details(method_id)
        if not method:
            return []
        
        # Search quantum_ai_tools.db for related tools
        cursor = self.tools_db.cursor()
        
        # Search by method name and keywords
        search_terms = [method['name']]
        if 'keywords' in method:
            search_terms.extend(method['keywords'])
        
        query = """
        SELECT * FROM ai_tools
        WHERE category = 'quantum_chemistry'
        AND (description LIKE ? OR capabilities LIKE ?)
        """
        
        tools = []
        for term in search_terms:
            search_pattern = f"%{term}%"
            cursor.execute(query, (search_pattern, search_pattern))
            tools.extend([dict(row) for row in cursor.fetchall()])
        
        return tools
    
    # ==================== Graph Queries ====================
    
    def get_method_prerequisites(self, method_id: str) -> List[Dict]:
        """Get prerequisite concepts/methods for understanding a method."""
        query = """
        MATCH path = (m:Method {id: $method_id})-[:BASED_ON*]->(c:Concept)
        RETURN c.id AS id, c.name AS name, c.difficulty_level AS difficulty,
               length(path) AS depth
        ORDER BY depth
        """
        
        with self.neo4j_driver.session() as session:
            result = session.run(query, method_id=method_id)
            return [dict(record) for record in result]
    
    def find_similar_workflows(self, workflow_id: str, top_k: int = 5) -> List[Dict]:
        """Find workflows similar to a given workflow."""
        query = """
        MATCH (w1:Workflow {id: $workflow_id})-[:RELATED_TO]->(m:Method)
        MATCH (w2:Workflow)-[:RELATED_TO]->(m)
        WHERE w1 <> w2
        WITH w2, count(DISTINCT m) AS shared_methods
        RETURN w2.id AS id, w2.name AS name, shared_methods
        ORDER BY shared_methods DESC
        LIMIT $top_k
        """
        
        with self.neo4j_driver.session() as session:
            result = session.run(query, workflow_id=workflow_id, top_k=top_k)
            return [dict(record) for record in result]


# ==================== Convenience Functions ====================

def quick_method_search(query: str) -> List[Dict]:
    """Quick semantic search for methods."""
    api = UnifiedQCAPI()
    return api.semantic_search(query, entity_types=['Method'], top_k=5)


def get_recommended_workflow(task: str, tool: str = None) -> Optional[Dict]:
    """Get recommended workflow for a task."""
    api = UnifiedQCAPI()
    results = api.semantic_search(task, entity_types=['Workflow'], top_k=1)
    if results:
        workflow_id = results[0]['id']
        # Get full workflow details from Neo4j
        with api.neo4j_driver.session() as session:
            result = session.run(
                "MATCH (w:Workflow {id: $id}) RETURN w",
                id=workflow_id
            )
            record = result.single()
            if record:
                return dict(record['w'])
    return None


if __name__ == "__main__":
    # Test API
    api = UnifiedQCAPI()
    
    print("Testing method search...")
    methods = api.find_methods_by_accuracy(min_accuracy="high", max_cost="medium")
    print(f"Found {len(methods)} methods")
    
    print("\nTesting semantic search...")
    results = api.semantic_search("optimize transition state geometry")
    print(f"Found {len(results)} results")
