"""
QCDB Knowledge Base Integrity Tests
Tests JSON schema, cross-references, and data consistency.
"""

import json
import pytest
from pathlib import Path
import os


QCBD_ROOT = Path(os.environ.get('QCBD_ROOT', r'G:\My Drive\Databases\QCBD'))


class TestKBIntegrity:
    """Test knowledge base integrity."""
    
    @pytest.fixture(scope='class')
    def kb(self):
        """Load unified knowledge graph."""
        kb_path = QCBD_ROOT / "qc_knowledge_graph_full.json"
        if not kb_path.exists():
            pytest.skip("Knowledge graph not built yet")
        
        with open(kb_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @pytest.fixture(scope='class')
    def all_ids(self, kb):
        """Collect all entity IDs."""
        ids = set()
        for entity_type in ['Concepts', 'Methods', 'SoftwareTools', 'Parameters', 
                           'Workflows', 'ExampleProblems', 'BenchmarkSets', 'Resources']:
            if entity_type in kb:
                for entity in kb[entity_type]:
                    ids.add(entity.get('id'))
        return ids
    
    def test_kb_file_exists(self):
        """Test that unified KB file exists."""
        kb_path = QCBD_ROOT / "qc_knowledge_graph_full.json"
        assert kb_path.exists(), f"Knowledge graph not found at {kb_path}"
    
    def test_kb_loads(self, kb):
        """Test that KB loads as valid JSON."""
        assert isinstance(kb, dict)
        assert 'metadata' in kb
    
    def test_metadata_complete(self, kb):
        """Test that metadata contains required fields."""
        metadata = kb['metadata']
        required_fields = ['version', 'build_date', 'entity_counts', 'total_entities']
        for field in required_fields:
            assert field in metadata, f"Missing metadata field: {field}"
    
    def test_all_entity_types_present(self, kb):
        """Test that all entity types are present."""
        entity_types = ['Concepts', 'Methods', 'SoftwareTools', 'Parameters',
                       'Workflows', 'ExampleProblems', 'BenchmarkSets', 'Resources']
        for entity_type in entity_types:
            assert entity_type in kb, f"Missing entity type: {entity_type}"
            assert isinstance(kb[entity_type], list)
    
    @pytest.mark.parametrize('entity_type', ['Concepts', 'Methods', 'SoftwareTools', 
                                             'Workflows', 'BenchmarkSets'])
    def test_entities_have_required_fields(self, kb, entity_type):
        """Test that entities have required fields."""
        required_fields = ['id', 'name']
        entities = kb.get(entity_type, [])
        
        for entity in entities:
            for field in required_fields:
                assert field in entity, \
                    f"{entity_type} entity missing '{field}': {entity.get('id', 'unknown')}"
    
    def test_no_duplicate_ids(self, kb, all_ids):
        """Test that all IDs are unique."""
        seen_ids = {}
        for entity_type in ['Concepts', 'Methods', 'SoftwareTools', 'Parameters',
                           'Workflows', 'ExampleProblems', 'BenchmarkSets', 'Resources']:
            if entity_type in kb:
                for entity in kb[entity_type]:
                    entity_id = entity.get('id')
                    if entity_id in seen_ids:
                        pytest.fail(
                            f"Duplicate ID '{entity_id}' in {entity_type} "
                            f"(also in {seen_ids[entity_id]})"
                        )
                    seen_ids[entity_id] = entity_type
    
    def test_id_naming_convention(self, kb):
        """Test that IDs follow naming convention."""
        import re
        pattern = re.compile(r'^[a-z0-9_]+$')
        
        for entity_type in ['Concepts', 'Methods', 'SoftwareTools']:
            entities = kb.get(entity_type, [])
            for entity in entities:
                entity_id = entity.get('id', '')
                assert pattern.match(entity_id), \
                    f"Invalid ID format: {entity_id} (must be lowercase alphanumeric with underscores)"
    
    def test_cross_references_valid(self, kb, all_ids):
        """Test that all cross-references point to existing IDs."""
        reference_fields = {
            'Concepts': ['prerequisites', 'related_methods', 'related_tools'],
            'Methods': ['theoretical_basis', 'implemented_in', 'validated_on_benchmarks'],
            'Workflows': ['related_methods', 'example_problems']
        }
        
        broken_refs = []
        
        for entity_type, fields in reference_fields.items():
            entities = kb.get(entity_type, [])
            for entity in entities:
                entity_id = entity.get('id')
                for field in fields:
                    if field in entity:
                        refs = entity[field]
                        if isinstance(refs, str):
                            refs = [refs]
                        for ref in refs:
                            if ref not in all_ids:
                                broken_refs.append(
                                    f"{entity_type}.{entity_id}.{field} -> {ref}"
                                )
        
        if broken_refs:
            pytest.fail(f"Broken cross-references found:\n" + "\n".join(broken_refs[:10]))
    
    def test_doi_format(self, kb):
        """Test that DOI fields have valid format."""
        import re
        doi_pattern = re.compile(r'^10\.\d{4,}/\S+$')
        
        for resource in kb.get('Resources', []):
            if 'doi' in resource:
                doi = resource['doi']
                assert doi_pattern.match(doi), f"Invalid DOI format: {doi}"
    
    def test_benchmark_attribution(self):
        """Test that benchmark attribution file exists and is complete."""
        attr_file = QCBD_ROOT / "benchmarks" / "BENCHMARK_ATTRIBUTION.md"
        assert attr_file.exists(), "Benchmark attribution file missing"
        
        content = attr_file.read_text(encoding='utf-8')
        assert '##' in content, "Attribution file appears empty"
        assert 'DOI:' in content, "Missing DOI citations"
        assert 'License:' in content, "Missing license information"


class TestEntityCounts:
    """Test entity counts and coverage."""
    
    @pytest.fixture(scope='class')
    def kb(self):
        kb_path = QCBD_ROOT / "qc_knowledge_graph_full.json"
        if not kb_path.exists():
            pytest.skip("Knowledge graph not built yet")
        with open(kb_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def test_minimum_concepts(self, kb):
        """Test that KB has minimum number of concepts."""
        concepts = kb.get('Concepts', [])
        assert len(concepts) >= 5, f"Expected at least 5 concepts, got {len(concepts)}"
    
    def test_minimum_methods(self, kb):
        """Test that KB has minimum number of methods."""
        methods = kb.get('Methods', [])
        assert len(methods) >= 10, f"Expected at least 10 methods, got {len(methods)}"
    
    def test_minimum_tools(self, kb):
        """Test that KB has minimum number of tools."""
        tools = kb.get('SoftwareTools', [])
        assert len(tools) >= 10, f"Expected at least 10 tools, got {len(tools)}"
    
    def test_benchmarks_present(self, kb):
        """Test that key benchmarks are present."""
        benchmarks = kb.get('BenchmarkSets', [])
        benchmark_names = {b['name'] for b in benchmarks}
        
        expected = {'S22 Set', 'S66 Set', 'WATER27'}
        missing = expected - benchmark_names
        assert not missing, f"Missing key benchmarks: {missing}"


def test_file_structure():
    """Test that required directory structure exists."""
    required_dirs = [
        'api',
        'scripts',
        'benchmarks',
        'tests',
        'docs',
        'QCBD_client_extensions'
    ]
    
    for dir_name in required_dirs:
        dir_path = QCBD_ROOT / dir_name
        assert dir_path.exists(), f"Missing required directory: {dir_name}"


if __name__ == "__main__":
    pytest.main([__file__, '-v'])
