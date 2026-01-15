"""Enhanced harvester for local database folders discovered by deep scan."""
import sys
import sqlite3
import json
import csv
from pathlib import Path
from datetime import date
from typing import List, Dict, Any
from utils import write_jsonl, read_jsonl, DATA_PROCESSED, write_json

# Base path for discovered databases
DATABASES_ROOT = Path("G:/My Drive/Databases")

def harvest_strategic_partners_db() -> List[Dict]:
    """Harvest strategic_partners.db SQLite database."""
    db_path = DATABASES_ROOT / "strategic_partners.db"
    if not db_path.exists():
        print(f"  [SKIP] strategic_partners.db not found")
        return []
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor]
        
        datasets = []
        for table in tables:
            cursor = conn.execute(f"SELECT * FROM {table} LIMIT 1")
            columns = [desc[0] for desc in cursor.description]
            
            datasets.append({
                "id": f"ds.strategic_partners.{table}",
                "name": f"Strategic Partners: {table}",
                "domain": "market_analysis",
                "category": "strategic_partnerships",
                "description": f"Strategic partner data from {table} table",
                "source_id": "src.local.strategic_partners_db",
                "url": str(db_path),
                "metadata": {
                    "table": table,
                    "columns": columns
                },
                "last_reviewed": str(date.today())
            })
        
        conn.close()
        return datasets
    except Exception as e:
        print(f"  [ERROR] strategic_partners.db: {e}")
        return []

def harvest_csv_exports() -> List[Dict]:
    """Harvest CSV export folders."""
    datasets = []
    
    for folder in ["CSV_Exports", "Enhanced_CSV_Exports"]:
        folder_path = DATABASES_ROOT / folder
        if not folder_path.exists():
            continue
        
        for csv_file in folder_path.glob("**/*.csv"):
            try:
                with open(csv_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    columns = reader.fieldnames or []
                
                datasets.append({
                    "id": f"ds.csv_exports.{csv_file.stem}",
                    "name": f"CSV Export: {csv_file.stem}",
                    "domain": "market_analysis",
                    "category": "csv_data",
                    "description": f"CSV data export from {folder}",
                    "source_id": "src.local.csv_exports",
                    "url": str(csv_file),
                    "metadata": {
                        "filename": csv_file.name,
                        "columns": columns,
                        "folder": folder
                    },
                    "last_reviewed": str(date.today())
                })
            except Exception as e:
                print(f"  [ERROR] {csv_file}: {e}")
    
    return datasets

def harvest_ai_tools() -> List[Dict]:
    """Harvest AI Tools databases."""
    tools = []
    
    for folder in ["AI Tools", "AI_Tools_Database"]:
        folder_path = DATABASES_ROOT / folder
        if not folder_path.exists():
            continue
        
        # Look for JSON/JSONL files describing AI tools
        for json_file in folder_path.glob("**/*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Assume structure with tool records
                if isinstance(data, list):
                    for item in data:
                        if 'name' in item or 'tool_name' in item:
                            tool_name = item.get('name') or item.get('tool_name', 'unknown')
                            tools.append({
                                "id": f"tool.ai_tools.{tool_name.lower().replace(' ', '_')}",
                                "name": tool_name,
                                "domain": "market_analysis",
                                "categories": ["ai_tools"],
                                "capabilities": item.get('capabilities', ''),
                                "license": item.get('license', 'unknown'),
                                "official_url": item.get('url', ''),
                                "docs_url": item.get('docs_url', ''),
                                "standard_refs": [f"src.local.ai_tools"],
                                "last_reviewed": str(date.today())
                            })
            except Exception as e:
                print(f"  [ERROR] {json_file}: {e}")
    
    return tools

def harvest_dhs_sectors() -> List[Dict]:
    """Harvest DHS Critical Infrastructure Sectors data."""
    concepts = []
    sectors_path = DATABASES_ROOT / "16 DHS Critical Infrastructure Sectors"
    
    if not sectors_path.exists():
        return []
    
    # List known sectors
    sectors = [
        "Chemical", "Commercial Facilities", "Communications",
        "Critical Manufacturing", "Dams", "Defense Industrial Base",
        "Emergency Services", "Energy", "Financial Services",
        "Food and Agriculture", "Government Facilities",
        "Healthcare and Public Health", "Information Technology",
        "Nuclear Reactors", "Transportation Systems", "Water and Wastewater"
    ]
    
    for sector in sectors:
        concepts.append({
            "id": f"concept.dhs.{sector.lower().replace(' ', '_')}",
            "domain": "critical_infrastructure",
            "title": f"DHS Sector: {sector}",
            "level": "strategic",
            "tags": ["critical_infrastructure", "dhs", "security"],
            "summary": f"DHS-designated critical infrastructure sector: {sector}",
            "prerequisites": [],
            "standard_refs": ["src.local.dhs_sectors"],
            "last_reviewed": str(date.today())
        })
    
    return concepts

def main():
    """Run enhanced local harvester."""
    print("Harvesting local database folders...\n")
    
    # Harvest datasets
    print("[1/4] Strategic partners database...")
    strategic_datasets = harvest_strategic_partners_db()
    print(f"  Found {len(strategic_datasets)} datasets")
    
    print("[2/4] CSV exports...")
    csv_datasets = harvest_csv_exports()
    print(f"  Found {len(csv_datasets)} CSV datasets")
    
    print("[3/4] AI Tools...")
    ai_tools = harvest_ai_tools()
    print(f"  Found {len(ai_tools)} AI tools")
    
    print("[4/4] DHS Critical Infrastructure Sectors...")
    dhs_concepts = harvest_dhs_sectors()
    print(f"  Found {len(dhs_concepts)} DHS sector concepts")
    
    # Write outputs
    if strategic_datasets or csv_datasets:
        all_datasets = strategic_datasets + csv_datasets
        output_path = DATA_PROCESSED / "local_datasets.jsonl"
        write_jsonl(output_path, all_datasets)
        print(f"\n[OUTPUT] {output_path} ({len(all_datasets)} datasets)")
    
    if ai_tools:
        output_path = DATA_PROCESSED / "local_ai_tools.jsonl"
        write_jsonl(output_path, ai_tools)
        print(f"[OUTPUT] {output_path} ({len(ai_tools)} tools)")
    
    if dhs_concepts:
        output_path = DATA_PROCESSED / "local_dhs_concepts.jsonl"
        write_jsonl(output_path, dhs_concepts)
        print(f"[OUTPUT] {output_path} ({len(dhs_concepts)} concepts)")
    
    # Create source records for local folders
    local_sources = [
        {
            "id": "src.local.strategic_partners_db",
            "type": "database",
            "title": "Strategic Partners Database",
            "authors": ["Internal"],
            "year": 2025,
            "publisher": "Q-SMEC",
            "provenance": "local_filesystem",
            "url": str(DATABASES_ROOT / "strategic_partners.db"),
            "domains": ["market_analysis"],
            "trust_tier": "C",
            "allowed_content": "full_open_content",
            "open_access": False,
            "keywords": ["strategic", "partners", "business"],
            "notes": "Local SQLite database of strategic partnerships.",
            "last_verified": str(date.today())
        },
        {
            "id": "src.local.csv_exports",
            "type": "database",
            "title": "CSV Exports Collection",
            "authors": ["Internal"],
            "year": 2025,
            "publisher": "Q-SMEC",
            "provenance": "local_filesystem",
            "url": str(DATABASES_ROOT),
            "domains": ["market_analysis"],
            "trust_tier": "C",
            "allowed_content": "full_open_content",
            "open_access": False,
            "keywords": ["csv", "exports", "data"],
            "notes": "Collection of CSV data exports from various analyses.",
            "last_verified": str(date.today())
        },
        {
            "id": "src.local.ai_tools",
            "type": "database",
            "title": "AI Tools Database",
            "authors": ["Internal"],
            "year": 2025,
            "publisher": "Q-SMEC",
            "provenance": "local_filesystem",
            "url": str(DATABASES_ROOT / "AI Tools"),
            "domains": ["market_analysis"],
            "trust_tier": "C",
            "allowed_content": "full_open_content",
            "open_access": False,
            "keywords": ["ai", "tools", "technology"],
            "notes": "Database of AI tools and technologies for market analysis.",
            "last_verified": str(date.today())
        },
        {
            "id": "src.local.dhs_sectors",
            "type": "database",
            "title": "DHS Critical Infrastructure Sectors",
            "authors": ["Department of Homeland Security"],
            "year": 2025,
            "publisher": "DHS",
            "provenance": "gov_us_dhs",
            "url": str(DATABASES_ROOT / "16 DHS Critical Infrastructure Sectors"),
            "domains": ["critical_infrastructure"],
            "trust_tier": "A",
            "allowed_content": "full_open_content",
            "open_access": True,
            "keywords": ["critical infrastructure", "dhs", "security"],
            "notes": "16 DHS-designated critical infrastructure sectors.",
            "last_verified": str(date.today())
        }
    ]
    
    sources_output = DATA_PROCESSED / "local_sources.jsonl"
    write_jsonl(sources_output, local_sources)
    print(f"[OUTPUT] {sources_output} ({len(local_sources)} sources)")
    
    print("\n[COMPLETE] Enhanced local harvester finished.")
    return 0

if __name__ == '__main__':
    sys.exit(main())
