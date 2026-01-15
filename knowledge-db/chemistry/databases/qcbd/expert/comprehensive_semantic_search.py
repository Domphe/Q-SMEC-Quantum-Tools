"""Enhanced semantic search across ALL knowledge graph entities.

Extends the original semantic_search.py to index:
- Methods, Concepts, SoftwareTools, Workflows
- BenchmarkSets, UseCases, Equations
- Any other list-type entities in the knowledge graph

Uses the same deterministic hash embedding approach but applies to all content.
"""

import hashlib
import math
import json
import sqlite3
from pathlib import Path
from typing import List, Dict, Any, Tuple
import os

DIM = 64
QCBD_ROOT = Path(os.environ.get('QCBD_ROOT', r'G:\My Drive\Databases\QCBD'))
KG_PATH = QCBD_ROOT / 'qc_knowledge_graph_full.json'
EMBEDDINGS_DB = QCBD_ROOT / 'expert' / 'embeddings.db'
EMBEDDINGS_DB.parent.mkdir(parents=True, exist_ok=True)

def _tokenize(text: str) -> List[str]:
    """Convert text to tokens."""
    if not text: return []
    for ch in ',;:\n\r\t()[]{}<>/\\':
        text = text.replace(ch, ' ')
    return [t for t in text.lower().split(' ') if t]

def _embed(text: str) -> List[float]:
    """Create deterministic hash-based embedding vector."""
    tokens = _tokenize(text)
    vec = [0.0] * DIM
    for i, tok in enumerate(tokens):
        h = hashlib.sha256(tok.encode()).hexdigest()
        bucket = int(h, 16) % DIM
        vec[bucket] += 1.0 / (i + 1)
    # L2 normalize
    norm = math.sqrt(sum(v*v for v in vec)) or 1.0
    return [v / norm for v in vec]

def _cosine(a: List[float], b: List[float]) -> float:
    """Cosine similarity."""
    return sum(x*y for x,y in zip(a,b))

def _extract_text(entity: Dict[str, Any], entity_type: str) -> str:
    """Extract searchable text from entity based on type."""
    text_parts = []
    
    # Common fields
    for field in ['name', 'title', 'short_definition', 'definition', 'description', 
                  'long_explanation', 'equation']:
        if field in entity:
            text_parts.append(str(entity[field]))
    
    # Type-specific fields
    if entity_type == 'UseCases':
        text_parts.extend([
            str(entity.get('sector', '')),
            ' '.join(entity.get('key_technologies', []))
        ])
    elif entity_type == 'BenchmarkSets':
        text_parts.extend([
            str(entity.get('category', '')),
            str(entity.get('methodology', ''))
        ])
    elif entity_type == 'SoftwareTools':
        text_parts.extend(entity.get('capabilities', []))
    
    # Tags
    if 'tags' in entity:
        text_parts.extend(entity.get('tags', []))
    
    return ' '.join(text_parts)

def load_all_entities() -> List[Tuple[str, str, str, Dict[str, Any]]]:
    """Load all entities from knowledge graph.
    
    Returns: List of (entity_id, entity_type, searchable_text, full_entity_data)
    """
    if not KG_PATH.exists():
        print(f"Warning: Knowledge graph not found at {KG_PATH}")
        return []
    
    with open(KG_PATH, 'r', encoding='utf-8') as f:
        kg = json.load(f)
    
    entities = []
    
    # Process all list-type categories
    for category, items in kg.items():
        if not isinstance(items, list):
            continue
        if category == 'metadata' or category.startswith('metadata_'):
            continue
        
        for item in items:
            if not isinstance(item, dict):
                continue
            
            entity_id = item.get('id', f"{category.lower()}_{len(entities)}")
            searchable_text = _extract_text(item, category)
            entities.append((entity_id, category, searchable_text, item))
    
    return entities

def build_comprehensive_embeddings(persist: bool = True) -> Dict[str, Tuple[str, List[float], Dict[str, Any]]]:
    """Build embeddings for all entities in knowledge graph.
    
    Returns: Dict[entity_id, (entity_type, embedding_vector, full_data)]
    """
    print("Loading entities from knowledge graph...")
    entities = load_all_entities()
    print(f"Found {len(entities)} entities across knowledge graph")
    
    embeddings = {}
    type_counts = {}
    
    for entity_id, entity_type, text, data in entities:
        vec = _embed(text)
        embeddings[entity_id] = (entity_type, vec, data)
        type_counts[entity_type] = type_counts.get(entity_type, 0) + 1
    
    print("\nEmbedding counts by type:")
    for etype, count in sorted(type_counts.items()):
        print(f"  {etype}: {count}")
    
    if persist:
        print(f"\nPersisting to {EMBEDDINGS_DB}...")
        conn = sqlite3.connect(str(EMBEDDINGS_DB))
        cur = conn.cursor()
        
        # Create table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS embeddings (
                entity_id TEXT PRIMARY KEY,
                entity_type TEXT,
                name TEXT,
                searchable_text TEXT,
                vector TEXT,
                data TEXT
            )
        """)
        
        # Create index for type-based filtering
        cur.execute("CREATE INDEX IF NOT EXISTS idx_entity_type ON embeddings(entity_type)")
        
        # Insert embeddings
        for entity_id, (entity_type, vec, data) in embeddings.items():
            name = data.get('name', data.get('title', ''))
            searchable_text = _extract_text(data, entity_type)
            
            cur.execute("""
                INSERT OR REPLACE INTO embeddings 
                (entity_id, entity_type, name, searchable_text, vector, data)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                entity_id,
                entity_type,
                name,
                searchable_text[:500],  # Truncate for storage
                json.dumps(vec),
                json.dumps(data)
            ))
        
        conn.commit()
        conn.close()
        print(f"✓ Saved {len(embeddings)} embeddings to database")
    
    return embeddings

def search_all(query: str, top_k: int = 10, entity_types: List[str] = None) -> List[Dict[str, Any]]:
    """Search across all entity types.
    
    Args:
        query: Search query string
        top_k: Number of results to return
        entity_types: Optional list of entity types to filter by (e.g., ['Methods', 'UseCases'])
    
    Returns: List of matching entities with scores
    """
    query_vec = _embed(query)
    
    # Load embeddings from database if available
    if EMBEDDINGS_DB.exists():
        conn = sqlite3.connect(str(EMBEDDINGS_DB))
        cur = conn.cursor()
        
        if entity_types:
            placeholders = ','.join('?' * len(entity_types))
            cur.execute(f"SELECT entity_id, entity_type, name, vector, data FROM embeddings WHERE entity_type IN ({placeholders})", entity_types)
        else:
            cur.execute("SELECT entity_id, entity_type, name, vector, data FROM embeddings")
        
        rows = cur.fetchall()
        conn.close()
        
        if not rows:
            print("No embeddings found in database. Run build_comprehensive_embeddings() first.")
            return []
        
        # Score each entity
        scored = []
        for entity_id, entity_type, name, vec_json, data_json in rows:
            vec = json.loads(vec_json)
            data = json.loads(data_json)
            score = _cosine(query_vec, vec)
            scored.append({
                'entity_id': entity_id,
                'entity_type': entity_type,
                'name': name,
                'score': round(score, 4),
                'data': data
            })
        
        # Sort by score and return top_k
        scored.sort(key=lambda x: x['score'], reverse=True)
        return scored[:top_k]
    
    else:
        print(f"Embeddings database not found at {EMBEDDINGS_DB}")
        print("Run build_comprehensive_embeddings() first.")
        return []

def search_by_type(query: str, entity_type: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """Search within a specific entity type."""
    return search_all(query, top_k=top_k, entity_types=[entity_type])

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'build':
        # Build embeddings
        build_comprehensive_embeddings(persist=True)
    elif len(sys.argv) > 1 and sys.argv[1] == 'search':
        # Test search
        query = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else 'quantum computing'
        print(f"\nSearching for: {query}\n")
        results = search_all(query, top_k=5)
        for r in results:
            print(f"[{r['entity_type']}] {r['name']} (score: {r['score']})")
            if 'description' in r['data']:
                desc = r['data']['description'][:100]
                print(f"  {desc}...")
            print()
    else:
        print("Usage:")
        print("  python comprehensive_semantic_search.py build          # Build embeddings")
        print("  python comprehensive_semantic_search.py search <query> # Test search")
