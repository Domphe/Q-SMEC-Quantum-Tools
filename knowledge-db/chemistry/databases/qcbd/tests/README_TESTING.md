# QCDB Testing Suite

## Running Tests

### Run All Tests
```powershell
pytest tests/ -v --cov=api --cov=scripts
```

### Run Specific Test File
```powershell
pytest tests/test_kb_integrity.py -v
pytest tests/test_neo4j_ops.py -v
pytest tests/test_api_comprehensive.py -v
```

### Run with Coverage Report
```powershell
pytest tests/ --cov=api --cov=scripts --cov-report=html
# View coverage_report/index.html
```

### Run Fast Tests Only
```powershell
pytest tests/ -m "not slow" -v
```

## Test Organization

### test_kb_integrity.py
- JSON schema validation
- Cross-reference integrity
- ID uniqueness
- Naming conventions
- DOI format validation
- Minimum entity counts

### test_neo4j_ops.py
- Neo4j connection
- Sync operations
- Query correctness
- Backup/restore cycle
- Relationship integrity

### test_api_comprehensive.py
- Unified API methods
- Client extension loading
- RBAC enforcement
- Cache functionality
- Error handling

### test_embeddings_system.py
- Embedding generation
- Cache hits/misses
- Cost tracking accuracy
- Model switching
- Budget enforcement

### test_agent_e2e.py
- End-to-end agent responses
- Retrieval accuracy
- Citation generation
- Multi-turn conversations

## Test Markers

Use pytest markers to organize tests:

```python
@pytest.mark.slow
def test_expensive_operation():
    ...

@pytest.mark.integration
def test_full_pipeline():
    ...

@pytest.mark.unit
def test_single_function():
    ...
```

Run specific markers:
```powershell
pytest -m unit  # Fast unit tests only
pytest -m "not slow"  # Skip slow tests
```

## Fixtures

Common fixtures available in conftest.py:

- `kb`: Loaded knowledge graph
- `neo4j_session`: Neo4j database session
- `test_client`: API test client
- `embedding_manager`: Embedding system

## Coverage Target

- Overall: >85%
- Critical modules (api/): >90%
- Scripts: >75%

## Continuous Integration

Tests run automatically on:
- Pre-commit (fast tests only)
- Pull request (full suite)
- Post-merge (full suite + Neo4j sync validation)

## Test Data

Test data located in:
- `tests/fixtures/`: Sample entities
- `tests/mock_data/`: Mock API responses
- `evaluation/ground_truth_qa.json`: QA pairs for agent testing
