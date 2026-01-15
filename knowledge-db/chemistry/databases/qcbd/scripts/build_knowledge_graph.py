"""
QCDB Knowledge Graph Builder
Merges individual JSON entity files into a unified, cross-linked knowledge graph.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Set, Any
from datetime import datetime
from collections import defaultdict
import hashlib


class KnowledgeGraphBuilder:
    """Build and validate the unified quantum chemistry knowledge graph."""
    
    def __init__(self, qcbd_root: str):
        self.qcbd_root = Path(qcbd_root)
        self.entities = {
            "Concepts": [],
            "Methods": [],
            "SoftwareTools": [],
            "Parameters": [],
            "Workflows": [],
            "ExampleProblems": [],
            "BenchmarkSets": [],
            "Resources": []
        }
        self.id_index = {}  # entity_id -> (entity_type, entity)
        self.errors = []
        self.warnings = []
        
    def load_entity_files(self):
        """Load all individual JSON entity files."""
        file_map = {
            "Concepts": "qc_concepts_expanded.json",
            "Methods": "qc_methods_expanded.json",
            "SoftwareTools": "qc_tools_expanded.json",
            "Parameters": "qc_parameters_expanded.json",
            "Workflows": "qc_workflows_expanded.json",
            "ExampleProblems": "qc_example_problems_expanded.json",
            "BenchmarkSets": "qc_benchmarks_expanded.json",
            "Resources": "qc_resources_expanded.json"
        }
        
        for entity_type, filename in file_map.items():
            filepath = self.qcbd_root / filename
            if filepath.exists():
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self.entities[entity_type] = data
                        print(f"✓ Loaded {len(data)} {entity_type}")
                    else:
                        self.errors.append(f"Invalid format in {filename}: expected list")
            else:
                self.warnings.append(f"Missing file: {filename}")
        
        return len(self.errors) == 0
    
    def build_id_index(self):
        """Create index of all entity IDs for fast lookup."""
        for entity_type, entities in self.entities.items():
            for entity in entities:
                entity_id = entity.get('id')
                if entity_id:
                    if entity_id in self.id_index:
                        self.errors.append(
                            f"Duplicate ID '{entity_id}' in {entity_type} "
                            f"(already exists in {self.id_index[entity_id][0]})"
                        )
                    else:
                        self.id_index[entity_id] = (entity_type, entity)
                else:
                    self.errors.append(f"Missing 'id' field in {entity_type}: {entity.get('name', 'unknown')}")
    
    def add_cross_references(self):
        """Add bidirectional cross-references between entities."""
        print("\nAdding cross-references...")
        
        # Add related_methods to Concepts
        for concept in self.entities["Concepts"]:
            concept_id = concept['id']
            related_methods = set()
            
            # Find methods that reference this concept
            for method in self.entities["Methods"]:
                theoretical_basis = method.get('theoretical_basis', [])
                if concept_id in theoretical_basis:
                    related_methods.add(method['id'])
            
            if related_methods and 'related_methods' not in concept:
                concept['related_methods'] = sorted(list(related_methods))
        
        # Add implemented_in_tools to Methods
        for method in self.entities["Methods"]:
            method_id = method['id']
            implemented_in = set(method.get('implemented_in', []))
            
            # Find tools that support this method
            for tool in self.entities["SoftwareTools"]:
                supported_methods = tool.get('supported_methods', [])
                if method_id in supported_methods:
                    implemented_in.add(tool['id'])
            
            if implemented_in:
                method['implemented_in'] = sorted(list(implemented_in))
        
        # Add related_tools to Concepts
        for concept in self.entities["Concepts"]:
            concept_id = concept['id']
            related_tools = set()
            
            # Find tools through methods
            for method_id in concept.get('related_methods', []):
                if method_id in self.id_index:
                    method = self.id_index[method_id][1]
                    related_tools.update(method.get('implemented_in', []))
            
            if related_tools and 'related_tools' not in concept:
                concept['related_tools'] = sorted(list(related_tools))
        
        # Add recommended_workflows to Methods and Tools
        for workflow in self.entities["Workflows"]:
            workflow_id = workflow['id']
            
            # Extract methods and tools used in workflow
            methods_used = set()
            tools_used = set()
            
            for step in workflow.get('steps', []):
                if 'method' in step:
                    methods_used.add(step['method'])
                if 'tool' in step:
                    tools_used.add(step['tool'])
            
            # Add to methods
            for method_id in methods_used:
                if method_id in self.id_index:
                    method = self.id_index[method_id][1]
                    if 'recommended_workflows' not in method:
                        method['recommended_workflows'] = []
                    if workflow_id not in method['recommended_workflows']:
                        method['recommended_workflows'].append(workflow_id)
            
            # Add to tools
            for tool_id in tools_used:
                if tool_id in self.id_index:
                    tool = self.id_index[tool_id][1]
                    if 'recommended_workflows' not in tool:
                        tool['recommended_workflows'] = []
                    if workflow_id not in tool['recommended_workflows']:
                        tool['recommended_workflows'].append(workflow_id)
        
        print("✓ Cross-references added")
    
    def validate_references(self):
        """Validate that all ID references point to existing entities."""
        print("\nValidating cross-references...")
        
        reference_fields = {
            'Concepts': ['prerequisites', 'related_methods', 'related_tools'],
            'Methods': ['theoretical_basis', 'implemented_in', 'validated_on_benchmarks', 'recommended_workflows'],
            'SoftwareTools': ['supported_methods', 'recommended_workflows'],
            'Workflows': ['related_concepts', 'related_methods', 'example_problems'],
            'ExampleProblems': ['recommended_workflow'],
        }
        
        for entity_type, field_names in reference_fields.items():
            for entity in self.entities[entity_type]:
                entity_id = entity.get('id', 'unknown')
                
                for field_name in field_names:
                    if field_name in entity:
                        ref_value = entity[field_name]
                        
                        # Handle both single values and lists
                        refs = [ref_value] if isinstance(ref_value, str) else ref_value
                        
                        for ref in refs:
                            if ref not in self.id_index:
                                self.warnings.append(
                                    f"Broken reference in {entity_type}.{entity_id}.{field_name}: "
                                    f"'{ref}' does not exist"
                                )
        
        print(f"✓ Validation complete ({len(self.warnings)} warnings)")
    
    def add_metadata(self, kb: Dict):
        """Add metadata to the knowledge graph."""
        kb['metadata'] = {
            'version': '1.0.0',
            'build_date': datetime.now().isoformat(),
            'entity_counts': {
                entity_type: len(entities)
                for entity_type, entities in self.entities.items()
            },
            'total_entities': sum(len(entities) for entities in self.entities.values()),
            'schema_version': '2025.1',
            'maintainer': 'Q-SMEC Development Team',
            'last_updated': datetime.now().isoformat(),
        }
        
        # Calculate content hash for caching
        content = json.dumps(self.entities, sort_keys=True)
        kb['metadata']['content_hash'] = hashlib.sha256(content.encode()).hexdigest()
    
    def build(self) -> Dict:
        """Build the complete knowledge graph."""
        print("=== Building QCDB Knowledge Graph ===\n")
        
        # Load all entity files
        if not self.load_entity_files():
            return None
        
        # Build ID index
        self.build_id_index()
        if self.errors:
            return None
        
        # Add cross-references
        self.add_cross_references()
        
        # Validate references
        self.validate_references()
        
        # Build final knowledge graph
        kb = self.entities.copy()
        self.add_metadata(kb)
        
        return kb
    
    def save(self, kb: Dict, output_path: Path):
        """Save the knowledge graph to file."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(kb, f, indent=2, ensure_ascii=False)
        
        file_size_mb = output_path.stat().st_size / (1024 * 1024)
        print(f"\n✓ Knowledge graph saved to: {output_path}")
        print(f"  Size: {file_size_mb:.2f} MB")
    
    def print_summary(self, kb: Dict):
        """Print build summary."""
        print("\n=== Build Summary ===")
        print(f"Total Entities: {kb['metadata']['total_entities']}")
        for entity_type, count in kb['metadata']['entity_counts'].items():
            print(f"  {entity_type}: {count}")
        
        if self.warnings:
            print(f"\n⚠ Warnings ({len(self.warnings)}):")
            for warning in self.warnings[:10]:  # Show first 10
                print(f"  - {warning}")
            if len(self.warnings) > 10:
                print(f"  ... and {len(self.warnings) - 10} more")
        
        if self.errors:
            print(f"\n✗ Errors ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - {error}")
            return False
        
        print("\n✓ Build successful!")
        return True


def main():
    """Main entry point."""
    qcbd_root = os.environ.get('QCBD_ROOT', r'G:\My Drive\Databases\QCBD')
    qcbd_path = Path(qcbd_root)
    
    if not qcbd_path.exists():
        print(f"✗ QCBD root not found: {qcbd_root}")
        print("  Set QCBD_ROOT environment variable or run setup script")
        return 1
    
    # Build knowledge graph
    builder = KnowledgeGraphBuilder(qcbd_path)
    kb = builder.build()
    
    if kb is None:
        print("\n✗ Build failed due to errors")
        return 1
    
    # Save unified knowledge graph
    output_path = qcbd_path / "qc_knowledge_graph_full.json"
    builder.save(kb, output_path)
    
    # Print summary
    success = builder.print_summary(kb)
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
