"""Command-line interface for searching the QCDB database."""
import sqlite3
import json
import argparse
import sys
from pathlib import Path
from utils import DB_DIR

def search_table(conn: sqlite3.Connection, table: str, query: str, domain: str = None, field: str = None) -> list:
    """Search a table for text matches."""
    results = []
    
    # For sources table with field-specific search
    if table == 'sources' and field:
        valid_fields = ['title', 'abstract', 'doi', 'container_title', 'subject']
        if field not in valid_fields:
            raise ValueError(f"Invalid field '{field}'. Valid fields for sources: {valid_fields}")
        sql = f"SELECT id, json FROM sources WHERE {field} LIKE ?"
        params = [f'%{query}%']
    else:
        # Default JSON search
        sql = f"SELECT id, json FROM {table} WHERE json LIKE ?"
        params = [f'%{query}%']
        
        if domain and table != 'sources':
            sql += " AND domain = ?"
            params.append(domain)
    
    cursor = conn.execute(sql, params)
    
    for row in cursor:
        record_id, json_str = row
        record = json.loads(json_str)
        results.append(record)
    
    return results

def main():
    parser = argparse.ArgumentParser(description="Search QCDB expert database")
    parser.add_argument('query', help='Search query text')
    parser.add_argument('--table', choices=[
        'sources', 'concepts', 'methods', 'equations', 
        'workflows', 'software_tools', 'datasets', 'glossary', 'all'
    ], default='all', help='Table to search')
    parser.add_argument('--domain', help='Filter by domain')
    parser.add_argument('--field', help='Field to search in sources table (title, abstract, doi, container_title, subject)')
    parser.add_argument('--limit', type=int, default=10, help='Max results to show')
    args = parser.parse_args()
    
    db_path = DB_DIR / 'qc_qp_expert.db'
    if not db_path.exists():
        print(f"ERROR: Database not found at {db_path}", file=sys.stderr)
        return 1
    
    conn = sqlite3.connect(db_path)
    
    try:
        tables_to_search = [
            'sources', 'concepts', 'methods', 'equations',
            'workflows', 'software_tools', 'datasets', 'glossary'
        ] if args.table == 'all' else [args.table]
        
        all_results = []
        
        for table in tables_to_search:
            results = search_table(conn, table, args.query, args.domain, args.field)
            for result in results:
                result['_table'] = table
                all_results.append(result)
        
        # Display results
        print(f"Found {len(all_results)} results for '{args.query}':\n")
        
        for idx, result in enumerate(all_results[:args.limit], 1):
            table = result.pop('_table')
            record_id = result.get('id', 'unknown')
            title = result.get('title') or result.get('name') or result.get('term', '')
            
            print(f"{idx}. [{table}] {record_id}")
            if title:
                print(f"   {title}")
            
            # Show brief excerpt
            if 'summary' in result:
                print(f"   {result['summary'][:100]}...")
            elif 'brief' in result:
                print(f"   {result['brief'][:100]}...")
            elif 'description' in result:
                print(f"   {result['description'][:100]}...")
            elif 'definition' in result:
                print(f"   {result['definition'][:100]}...")
            
            print()
        
        if len(all_results) > args.limit:
            print(f"... and {len(all_results) - args.limit} more results")
        
        return 0
        
    finally:
        conn.close()

if __name__ == '__main__':
    sys.exit(main())
