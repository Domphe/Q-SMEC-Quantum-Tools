"""
QCDB Neo4j Sync Script
Synchronizes the JSON knowledge graph to Neo4j graph database.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
from neo4j import GraphDatabase
import time


class Neo4jSyncManager:
    """Manage synchronization between JSON KB and Neo4j."""
    
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.stats = {
            'nodes_created': 0,
            'relationships_created': 0,
            'nodes_updated': 0,
            'errors': []
        }
    
    def close(self):
        """Close the Neo4j driver."""
        self.driver.close()
    
    def clear_database(self):
        """Clear all existing nodes and relationships."""
        with self.driver.session() as session:
            print("Clearing existing database...")
            session.run("MATCH (n) DETACH DELETE n")
            print("✓ Database cleared")
    
    def create_constraints(self):
        """Create uniqueness constraints for entity IDs."""
        constraints = [
            # Use explicit names expected by test suite
            "CREATE CONSTRAINT unique_concept_id IF NOT EXISTS FOR (c:Concept) REQUIRE c.id IS UNIQUE",
            "CREATE CONSTRAINT unique_method_id IF NOT EXISTS FOR (m:Method) REQUIRE m.id IS UNIQUE",
            "CREATE CONSTRAINT unique_tool_id IF NOT EXISTS FOR (t:SoftwareTool) REQUIRE t.id IS UNIQUE",
            "CREATE CONSTRAINT unique_parameter_id IF NOT EXISTS FOR (p:Parameter) REQUIRE p.id IS UNIQUE",
            "CREATE CONSTRAINT unique_workflow_id IF NOT EXISTS FOR (w:Workflow) REQUIRE w.id IS UNIQUE",
            "CREATE CONSTRAINT unique_problem_id IF NOT EXISTS FOR (e:ExampleProblem) REQUIRE e.id IS UNIQUE",
            "CREATE CONSTRAINT unique_benchmark_id IF NOT EXISTS FOR (b:BenchmarkSet) REQUIRE b.id IS UNIQUE",
            "CREATE CONSTRAINT unique_resource_id IF NOT EXISTS FOR (r:Resource) REQUIRE r.id IS UNIQUE"
        ]
        
        with self.driver.session() as session:
            for constraint in constraints:
                try:
                    session.run(constraint)
                except Exception as e:
                    # Constraint may already exist
                    pass
        
        print("✓ Constraints created")
    
    def sync_concepts(self, concepts: List[Dict]):
        """Sync Concept nodes."""
        print(f"Syncing {len(concepts)} Concepts...")
        
        with self.driver.session() as session:
            for concept in concepts:
                try:
                    # Create node with properties
                    session.run("""
                        CREATE (c:Concept {
                            id: $id,
                            name: $name,
                            short_definition: $short_definition,
                            long_explanation: $long_explanation,
                            tags: $tags,
                            difficulty_level: $difficulty_level
                        })
                    """, 
                        id=concept['id'],
                        name=concept['name'],
                        short_definition=concept.get('short_definition', ''),
                        long_explanation=concept.get('long_explanation', ''),
                        tags=concept.get('tags', []),
                        difficulty_level=concept.get('difficulty_level', 'intermediate')
                    )
                    self.stats['nodes_created'] += 1
                except Exception as e:
                    self.stats['errors'].append(f"Concept {concept['id']}: {str(e)}")
    
    def sync_methods(self, methods: List[Dict]):
        """Sync Method nodes."""
        print(f"Syncing {len(methods)} Methods...")
        
        with self.driver.session() as session:
            for method in methods:
                try:
                    session.run("""
                        CREATE (m:Method {
                            id: $id,
                            name: $name,
                            method_class: $method_class,
                            scaling: $scaling,
                            accuracy_level: $accuracy_level,
                            computational_cost: $computational_cost,
                            tags: $tags
                        })
                    """,
                        id=method['id'],
                        name=method['name'],
                        method_class=method.get('class', ''),
                        scaling=method.get('scaling', ''),
                        accuracy_level=method.get('accuracy_level', ''),
                        computational_cost=method.get('computational_cost', ''),
                        tags=method.get('tags', [])
                    )
                    self.stats['nodes_created'] += 1
                except Exception as e:
                    self.stats['errors'].append(f"Method {method['id']}: {str(e)}")
    
    def sync_tools(self, tools: List[Dict]):
        """Sync SoftwareTool nodes."""
        print(f"Syncing {len(tools)} Software Tools...")
        
        with self.driver.session() as session:
            for tool in tools:
                try:
                    session.run("""
                        CREATE (t:SoftwareTool {
                            id: $id,
                            name: $name,
                            short_description: $short_description,
                            capabilities: $capabilities,
                            tags: $tags
                        })
                    """,
                        id=tool['id'],
                        name=tool['name'],
                        short_description=tool.get('short_description', ''),
                        capabilities=tool.get('capabilities', []),
                        tags=tool.get('tags', [])
                    )
                    self.stats['nodes_created'] += 1
                except Exception as e:
                    self.stats['errors'].append(f"Tool {tool['id']}: {str(e)}")
    
    def sync_workflows(self, workflows: List[Dict]):
        """Sync Workflow nodes."""
        print(f"Syncing {len(workflows)} Workflows...")
        
        with self.driver.session() as session:
            for workflow in workflows:
                try:
                    session.run("""
                        CREATE (w:Workflow {
                            id: $id,
                            name: $name,
                            workflow_type: $workflow_type,
                            difficulty: $difficulty,
                            steps: $steps,
                            tags: $tags
                        })
                    """,
                        id=workflow['id'],
                        name=workflow['name'],
                        workflow_type=workflow.get('workflow_type', ''),
                        difficulty=workflow.get('difficulty_level', 'intermediate'),
                        steps=workflow.get('steps', []),
                        tags=workflow.get('tags', [])
                    )
                    self.stats['nodes_created'] += 1
                except Exception as e:
                    self.stats['errors'].append(f"Workflow {workflow['id']}: {str(e)}")
    
    def sync_benchmarks(self, benchmarks: List[Dict]):
        """Sync BenchmarkSet nodes."""
        print(f"Syncing {len(benchmarks)} Benchmark Sets...")
        
        with self.driver.session() as session:
            for benchmark in benchmarks:
                try:
                    session.run("""
                        CREATE (b:BenchmarkSet {
                            id: $id,
                            name: $name,
                            benchmark_type: $benchmark_type,
                            num_systems: $num_systems,
                            reference_method: $reference_method,
                            description: $description,
                            tags: $tags
                        })
                    """,
                        id=benchmark['id'],
                        name=benchmark['name'],
                        benchmark_type=benchmark.get('benchmark_type', ''),
                        num_systems=benchmark.get('num_systems', 0),
                        reference_method=benchmark.get('reference_method',''),
                        description=benchmark.get('description', ''),
                        tags=benchmark.get('tags', [])
                    )
                    self.stats['nodes_created'] += 1
                except Exception as e:
                    self.stats['errors'].append(f"Benchmark {benchmark['id']}: {str(e)}")

    def sync_parameters(self, parameters: List[Dict]):
        """Sync Parameter (basis set) nodes."""
        print(f"Syncing {len(parameters)} Parameters...")
        with self.driver.session() as session:
            for param in parameters:
                try:
                    session.run("""
                        CREATE (p:Parameter {
                            id: $id,
                            name: $name,
                            parameter_type: $parameter_type,
                            quality: $quality,
                            computational_cost: $computational_cost
                        })
                    """,
                        id=param['id'],
                        name=param['name'],
                        parameter_type=param.get('parameter_type',''),
                        quality=param.get('quality',''),
                        computational_cost=param.get('computational_cost','')
                    )
                    self.stats['nodes_created'] += 1
                except Exception as e:
                    self.stats['errors'].append(f"Parameter {param['id']}: {str(e)}")

    def sync_example_problems(self, problems: List[Dict]):
        """Sync ExampleProblem nodes."""
        print(f"Syncing {len(problems)} Example Problems...")
        with self.driver.session() as session:
            for prob in problems:
                try:
                    session.run("""
                        CREATE (e:ExampleProblem {
                            id: $id,
                            title: $title,
                            difficulty: $difficulty,
                            category: $category
                        })
                    """,
                        id=prob['id'],
                        title=prob.get('title',''),
                        difficulty=prob.get('difficulty',''),
                        category=prob.get('category','')
                    )
                    self.stats['nodes_created'] += 1
                except Exception as e:
                    self.stats['errors'].append(f"ExampleProblem {prob['id']}: {str(e)}")

    def sync_resources(self, resources: List[Dict]):
        """Sync Resource nodes."""
        print(f"Syncing {len(resources)} Resources...")
        with self.driver.session() as session:
            for res in resources:
                try:
                    session.run("""
                        CREATE (r:Resource {
                            id: $id,
                            title: $title,
                            resource_type: $resource_type,
                            difficulty_level: $difficulty_level
                        })
                    """,
                        id=res['id'],
                        title=res.get('title',''),
                        resource_type=res.get('resource_type',''),
                        difficulty_level=res.get('difficulty_level','')
                    )
                    self.stats['nodes_created'] += 1
                except Exception as e:
                    self.stats['errors'].append(f"Resource {res['id']}: {str(e)}")
    
    def create_relationships(self, kb: Dict):
        """Create relationships between nodes."""
        print("\nCreating relationships...")

        # Hardcoded relationship seed data (fallback when enrichment files unavailable)
        method_to_tools = {
            'method_hf': ['tool_gaussian', 'tool_orca', 'tool_psi4', 'tool_pyscf'],
            'method_b3lyp': ['tool_gaussian', 'tool_orca', 'tool_psi4', 'tool_qchem'],
            'method_mp2': ['tool_gaussian', 'tool_orca', 'tool_psi4', 'tool_qchem'],
            'method_ccsd_t': ['tool_gaussian', 'tool_orca', 'tool_molpro', 'tool_cfour']
        }
        tool_to_methods = {
            'tool_gaussian': ['method_hf', 'method_b3lyp', 'method_mp2', 'method_ccsd_t'],
            'tool_orca': ['method_hf', 'method_b3lyp', 'method_mp2', 'method_ccsd_t'],
            'tool_psi4': ['method_hf', 'method_b3lyp', 'method_mp2', 'method_ccsd_t'],
            'tool_pyscf': ['method_hf', 'method_b3lyp', 'method_mp2'],
            'tool_qchem': ['method_hf', 'method_b3lyp', 'method_mp2'],
            'tool_molpro': ['method_ccsd_t'],
            'tool_cfour': ['method_ccsd_t']
        }

        # Inject fallback relationship fields if missing
        for m in kb.get('Methods', []):
            mid = m.get('id')
            if mid in method_to_tools and 'implemented_in' not in m:
                m['implemented_in'] = method_to_tools[mid]
        for t in kb.get('SoftwareTools', []):
            tid = t.get('id')
            if tid in tool_to_methods and 'implemented_methods' not in t:
                t['implemented_methods'] = tool_to_methods[tid]

        # Each tuple: (SourceCollectionKey, SourceLabel, SourceField, RelationshipType, TargetLabel)
        relationship_maps = [
            ('Concepts', 'Concept', 'prerequisites', 'PREREQUISITE_OF', 'Concept'),
            ('Methods', 'Method', 'theoretical_basis', 'BASED_ON', 'Concept'),
            ('Methods', 'Method', 'implemented_in', 'IMPLEMENTED_IN', 'SoftwareTool'),
            ('Methods', 'Method', 'validated_on_benchmarks', 'VALIDATED_ON', 'BenchmarkSet'),
            ('Methods', 'Method', 'recommended_basis_sets', 'RECOMMENDS_PARAMETER', 'Parameter'),
            ('SoftwareTools', 'SoftwareTool', 'implemented_methods', 'IMPLEMENTS', 'Method'),
            ('Workflows', 'Workflow', 'related_methods', 'USES_METHOD', 'Method'),
            ('Workflows', 'Workflow', 'supported_tools', 'SUPPORTED_BY', 'SoftwareTool'),
            ('Parameters', 'Parameter', 'used_with_methods', 'USED_WITH', 'Method'),
            ('ExampleProblems', 'ExampleProblem', 'recommended_method', 'USES_METHOD', 'Method'),
            ('ExampleProblems', 'ExampleProblem', 'recommended_tool', 'USES_TOOL', 'SoftwareTool'),
            ('ExampleProblems', 'ExampleProblem', 'related_workflow', 'USES_WORKFLOW', 'Workflow'),
        ]

        with self.driver.session() as session:
            for collection_key, source_label, field_name, rel_type, target_label in relationship_maps:
                entities = kb.get(collection_key, [])
                for entity in entities:
                    source_id = entity.get('id')
                    if not source_id:
                        continue
                    raw_targets = entity.get(field_name, [])
                    # Normalize target list
                    if isinstance(raw_targets, str):
                        target_ids = [raw_targets]
                    elif isinstance(raw_targets, list):
                        target_ids = raw_targets
                    else:
                        target_ids = []
                    for target_id in target_ids:
                        try:
                            session.run(
                                """
                                MATCH (source:%s {id: $source_id})
                                MATCH (target:%s {id: $target_id})
                                MERGE (source)-[:%s]->(target)
                                """ % (source_label, target_label, rel_type),
                                source_id=source_id,
                                target_id=target_id
                            )
                            self.stats['relationships_created'] += 1
                        except Exception:
                            continue
        
        print(f"✓ Created {self.stats['relationships_created']} relationships")
    
    def sync_knowledge_graph(self, kb: Dict, incremental: bool = False):
        """Sync the entire knowledge graph to Neo4j."""
        print("=== Syncing Knowledge Graph to Neo4j ===\n")
        start_time = time.time()
        
        # Clear database if full sync
        if not incremental:
            self.clear_database()
        
        # Create constraints
        self.create_constraints()
        
        # Sync all entity types
        self.sync_concepts(kb.get('Concepts', []))
        self.sync_methods(kb.get('Methods', []))
        self.sync_tools(kb.get('SoftwareTools', []))
        self.sync_workflows(kb.get('Workflows', []))
        self.sync_benchmarks(kb.get('BenchmarkSets', []))
        self.sync_parameters(kb.get('Parameters', []))
        self.sync_example_problems(kb.get('ExampleProblems', []))
        self.sync_resources(kb.get('Resources', []))
        
        # Create relationships
        self.create_relationships(kb)
        
        elapsed = time.time() - start_time
        
        print(f"\n=== Sync Complete ===")
        print(f"Time: {elapsed:.2f} seconds")
        print(f"Nodes created: {self.stats['nodes_created']}")
        print(f"Relationships created: {self.stats['relationships_created']}")
        
        if self.stats['errors']:
            print(f"\n⚠ Errors ({len(self.stats['errors'])}):")
            for error in self.stats['errors'][:10]:
                print(f"  - {error}")


def main():
    """Main entry point."""
    # Get configuration from environment
    neo4j_uri = os.environ.get('NEO4J_URI', 'bolt://localhost:7687')
    neo4j_user = os.environ.get('NEO4J_USER', 'neo4j')
    neo4j_password = os.environ.get('NEO4J_PASSWORD', 'qcdb_password_2025')
    qcbd_root = os.environ.get('QCBD_ROOT', r'G:\My Drive\Databases\QCBD')
    
    # Load knowledge graph
    kb_path = Path(qcbd_root) / "qc_knowledge_graph_full.json"
    
    if not kb_path.exists():
        print(f"✗ Knowledge graph not found: {kb_path}")
        print("  Run build_knowledge_graph.py first")
        return 1
    
    print(f"Loading knowledge graph from: {kb_path}")
    with open(kb_path, 'r', encoding='utf-8') as f:
        kb = json.load(f)
    
    print(f"✓ Loaded {kb['metadata']['total_entities']} entities\n")

    # === Relationship/Data Enrichment ===
    # The expanded knowledge graph JSON currently lacks explicit relationship
    # fields (e.g. implemented_in, implemented_methods). We enrich the in-memory
    # KB with these by loading the base (non-expanded) source JSON files that
    # contain them, performing ID normalization where necessary.
    def enrich_relationship_data(kb: Dict, root: str):
        root_path = Path(root)
        try:
            base_methods_path = root_path / 'qc_methods.json'
            base_tools_path = root_path / 'qc_software_tools.json'
            if not base_methods_path.exists() or not base_tools_path.exists():
                print('⚠ Base relationship seed files missing; skipping enrichment')
                return
            print(f"Loading base method file: {base_methods_path}")
            with open(base_methods_path, 'r', encoding='utf-8') as fm:
                raw_methods = fm.read()
            print(f"Base methods file size: {len(raw_methods)} bytes")
            base_methods = json.loads(raw_methods)
            print(f"Loaded {len(base_methods)} base methods")
            print(f"Loading base tools file: {base_tools_path}")
            with open(base_tools_path, 'r', encoding='utf-8') as ft:
                raw_tools = ft.read()
            print(f"Base tools file size: {len(raw_tools)} bytes")
            base_tools = json.loads(raw_tools)
            print(f"Loaded {len(base_tools)} base tools")

            # Build quick index of existing method IDs in expanded KB
            existing_method_ids = {m.get('id') for m in kb.get('Methods', [])}
            id_mapping = {
                # Map verbose base IDs to expanded IDs where they represent same concept
                'method_hartree_fock': 'method_hf'
            }

            # Enrich / merge methods
            added_count = 0
            for bm in base_methods:
                original_id = bm.get('id')
                mapped_id = id_mapping.get(original_id, original_id)
                # Prepare relationship-bearing fields
                rel_fields = {
                    'implemented_in': bm.get('implemented_in', []),
                    'theoretical_basis': bm.get('theoretical_basis', []),
                    'validated_on_benchmarks': bm.get('validated_on_benchmarks', []),
                    'recommended_basis_sets': bm.get('recommended_basis_sets', [])
                }
                if mapped_id in existing_method_ids:
                    # Update existing expanded method with relationship fields if absent
                    for m in kb['Methods']:
                        if m.get('id') == mapped_id:
                            for k, v in rel_fields.items():
                                if v and k not in m:
                                    m[k] = v
                    continue
                # Create a minimal method node for IDs not present in expanded set
                new_method = {
                    'id': mapped_id,
                    'name': bm.get('name', mapped_id),
                    'method_class': bm.get('method_type', ''),
                    'accuracy_level': bm.get('accuracy_level', ''),
                    'computational_cost': bm.get('computational_cost', ''),
                    'tags': ['QC', 'method']
                }
                # Attach relationship fields
                new_method.update(rel_fields)
                kb['Methods'].append(new_method)
                existing_method_ids.add(mapped_id)
                added_count += 1

            # Enrich tools with implemented_methods (mapping IDs where needed)
            existing_tool_index = {t.get('id'): t for t in kb.get('SoftwareTools', [])}
            for bt in base_tools:
                tid = bt.get('id')
                if tid not in existing_tool_index:
                    continue
                impl = bt.get('implemented_methods', [])
                # Apply ID mapping
                impl_mapped = [id_mapping.get(mid, mid) for mid in impl]
                tool_obj = existing_tool_index[tid]
                if impl_mapped:
                    # Preserve any existing field name expectations (implemented_methods used by relationship logic)
                    if 'implemented_methods' not in tool_obj:
                        tool_obj['implemented_methods'] = impl_mapped
                    else:
                        # Merge without duplicates
                        merged = set(tool_obj['implemented_methods']) | set(impl_mapped)
                        tool_obj['implemented_methods'] = sorted(list(merged))
            if added_count:
                print(f"✓ Enriched KB with {added_count} additional method nodes carrying relationship data")
            else:
                print("✓ Relationship fields merged into existing method nodes (no new nodes needed)")
        except Exception as e:
            print(f"⚠ Relationship enrichment failed: {e}")

    # Sanitize workflow steps (convert list of objects to list of strings)
    for wf in kb.get('Workflows', []):
        steps = wf.get('steps', [])
        if steps and isinstance(steps, list) and all(isinstance(s, dict) for s in steps):
            sanitized = []
            for s in steps:
                # Prefer description field; fallback to name/step number
                if 'description' in s:
                    sanitized.append(s['description'])
                elif 'name' in s:
                    sanitized.append(s['name'])
                else:
                    sanitized.append(str(s))
            wf['steps'] = sanitized
            # Tag that workflow was sanitized
            wf.setdefault('tags', []).append('sanitized')
    enrich_relationship_data(kb, qcbd_root)

    enrich_relationship_data(kb, qcbd_root)
    
    # Connect to Neo4j and sync
    try:
        sync_manager = Neo4jSyncManager(neo4j_uri, neo4j_user, neo4j_password)
        sync_manager.sync_knowledge_graph(kb, incremental=False)
        sync_manager.close()
        print("\n✓ Sync successful!")
        return 0
    except Exception as e:
        print(f"\n✗ Sync failed: {e}")
        print("\nTroubleshooting:")
        print("  1. Ensure Neo4j is running: docker-compose up -d")
        print("  2. Check connection: http://localhost:7474")
        print("  3. Verify credentials in environment variables")
        return 1


if __name__ == "__main__":
    exit(main())
