"""Export QCBD database content to qc_knowledge_graph_full.json for expert layer indexing.

This script:
1. Loads all content from qc_qp_expert.db (methods, concepts, datasets, use cases, etc.)
2. Merges with existing qc_knowledge_graph_full.json (preserving structure)
3. Adds new entries from database while avoiding duplicates
4. Saves updated knowledge graph for semantic search indexing

After running this, run semantic_search.build_embeddings() to create search index.
"""

import sqlite3
import json
from pathlib import Path
from typing import Dict, Any, List

# Paths
SCRIPT_DIR = Path(__file__).parent
DB_PATH = SCRIPT_DIR.parent / "db" / "qc_qp_expert.db"
KG_PATH = SCRIPT_DIR.parent / "qc_knowledge_graph_full.json"
BACKUP_PATH = SCRIPT_DIR.parent / f"qc_knowledge_graph_full_backup_{Path(__file__).stem}.json"

def load_database_content() -> Dict[str, List[Dict[str, Any]]]:
    """Load all relevant content from database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    result = {}
    
    # Load methods
    methods = []
    for row in c.execute("SELECT id, domain, json FROM methods"):
        data = json.loads(row[2])
        methods.append({
            "id": row[0],
            "name": data.get("name", ""),
            "short_definition": data.get("description", "")[:200],
            "long_explanation": data.get("description", ""),
            "domain": row[1],
            "tags": [row[1]] if row[1] else [],
            "source": "qcbd_database"
        })
    result["Methods"] = methods
    print(f"Loaded {len(methods)} methods from database")
    
    # Load concepts
    concepts = []
    for row in c.execute("SELECT id, domain, json FROM concepts"):
        data = json.loads(row[2])
        concepts.append({
            "id": row[0],
            "name": data.get("name", ""),
            "definition": data.get("definition", ""),
            "description": data.get("description", ""),
            "domain": row[1],
            "tags": [row[1]] if row[1] else [],
            "source": "qcbd_database"
        })
    result["Concepts"] = concepts
    print(f"Loaded {len(concepts)} concepts from database")
    
    # Load software tools
    tools = []
    for row in c.execute("SELECT id, domain, json FROM software_tools"):
        data = json.loads(row[2])
        tools.append({
            "id": row[0],
            "name": data.get("name", ""),
            "description": data.get("description", ""),
            "domain": row[1],
            "capabilities": data.get("capabilities", []),
            "tags": [row[1]] if row[1] else [],
            "source": "qcbd_database"
        })
    result["SoftwareTools"] = tools
    print(f"Loaded {len(tools)} software tools from database")
    
    # Load benchmarks (from datasets table)
    benchmarks = []
    for row in c.execute("SELECT id, domain, json FROM datasets WHERE id LIKE 'benchmark.%'"):
        data = json.loads(row[2])
        benchmarks.append({
            "id": row[0],
            "name": data.get("name", ""),
            "description": data.get("description", ""),
            "domain": row[1] or data.get("domain", ""),
            "category": data.get("category", ""),
            "num_entries": data.get("num_entries", 0),
            "methodology": data.get("methodology", ""),
            "sources": data.get("sources", []),
            "tags": [row[1] or "benchmark", data.get("category", "")],
            "source": "qcbd_database"
        })
    result["BenchmarkSets"] = benchmarks
    print(f"Loaded {len(benchmarks)} benchmarks from database")
    
    # Load use cases
    use_cases = []
    for row in c.execute("SELECT id, json FROM use_cases"):
        data = json.loads(row[1])
        use_cases.append({
            "id": row[0],
            "name": data.get("name", ""),
            "description": data.get("description", ""),
            "sector": data.get("sector", ""),
            "market_size_billion": data.get("market_size_billion", 0),
            "cagr_percent": data.get("cagr_percent", 0),
            "trl_target": data.get("trl_target", 0),
            "key_technologies": data.get("key_technologies", []),
            "performance_targets": data.get("performance_targets", {}),
            "tags": [data.get("sector", ""), "use_case"],
            "source": "qcbd_database"
        })
    result["UseCases"] = use_cases
    print(f"Loaded {len(use_cases)} use cases from database")
    
    # Load equations
    equations = []
    for row in c.execute("SELECT id, domain, json FROM equations"):
        data = json.loads(row[2])
        equations.append({
            "id": row[0],
            "name": data.get("name", ""),
            "equation": data.get("equation", ""),
            "description": data.get("description", ""),
            "domain": row[1],
            "tags": [row[1]] if row[1] else [],
            "source": "qcbd_database"
        })
    result["Equations"] = equations
    print(f"Loaded {len(equations)} equations from database")
    
    # Load workflows
    workflows = []
    for row in c.execute("SELECT id, domain, json FROM workflows"):
        data = json.loads(row[2])
        workflows.append({
            "id": row[0],
            "name": data.get("name", ""),
            "description": data.get("description", ""),
            "steps": data.get("steps", []),
            "domain": row[1],
            "tags": [row[1]] if row[1] else [],
            "source": "qcbd_database"
        })
    result["Workflows"] = workflows
    print(f"Loaded {len(workflows)} workflows from database")
    
    conn.close()
    return result

def merge_knowledge_graphs(existing: Dict[str, Any], database: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
    """Merge database content with existing knowledge graph, avoiding duplicates."""
    merged = dict(existing)
    
    for key, db_items in database.items():
        if key not in merged:
            # New category from database
            merged[key] = db_items
            print(f"Added new category: {key} ({len(db_items)} items)")
        else:
            # Merge items, avoiding duplicates by ID
            existing_items = merged[key] if isinstance(merged[key], list) else []
            existing_ids = {item.get("id") for item in existing_items if isinstance(item, dict)}
            
            added_count = 0
            for db_item in db_items:
                item_id = db_item.get("id")
                if item_id not in existing_ids:
                    existing_items.append(db_item)
                    existing_ids.add(item_id)
                    added_count += 1
            
            merged[key] = existing_items
            print(f"Merged {key}: added {added_count} new items (total: {len(existing_items)})")
    
    # Update metadata
    if "metadata" not in merged:
        merged["metadata"] = {}
    merged["metadata"]["last_database_sync"] = "2025-12-03"
    merged["metadata"]["database_source"] = str(DB_PATH)
    merged["metadata"]["database_records"] = sum(len(items) if isinstance(items, list) else 0 for items in database.values())
    
    return merged

def main():
    print("=" * 70)
    print("QCBD Database → Knowledge Graph Export")
    print("=" * 70)
    
    # 1. Load database content
    print("\n[1/4] Loading content from database...")
    database_content = load_database_content()
    
    # 2. Load existing knowledge graph
    print("\n[2/4] Loading existing knowledge graph...")
    if KG_PATH.exists():
        with open(KG_PATH, 'r', encoding='utf-8') as f:
            existing_kg = json.load(f)
        print(f"Loaded existing knowledge graph from {KG_PATH}")
        
        # Create backup
        with open(BACKUP_PATH, 'w', encoding='utf-8') as f:
            json.dump(existing_kg, f, indent=2)
        print(f"Created backup at {BACKUP_PATH}")
    else:
        existing_kg = {
            "metadata": {
                "version": "1.0",
                "description": "Q-SMEC Quantum Chemistry & Physics Knowledge Graph"
            }
        }
        print("No existing knowledge graph found, creating new one")
    
    # 3. Merge content
    print("\n[3/4] Merging database content with knowledge graph...")
    merged_kg = merge_knowledge_graphs(existing_kg, database_content)
    
    # 4. Save updated knowledge graph
    print("\n[4/4] Saving updated knowledge graph...")
    with open(KG_PATH, 'w', encoding='utf-8') as f:
        json.dump(merged_kg, f, indent=2)
    
    print(f"\n✓ Successfully exported to {KG_PATH}")
    print("\nKnowledge Graph Summary:")
    print("-" * 70)
    for key, value in merged_kg.items():
        if isinstance(value, list):
            print(f"  {key}: {len(value)} items")
    
    print("\n" + "=" * 70)
    print("Next Steps:")
    print("  1. Run: python -c \"from expert.semantic_search import build_embeddings; build_embeddings()\"")
    print("  2. Test search: python -m expert.expert_cli semantic \"your query\"")
    print("=" * 70)

if __name__ == "__main__":
    main()
