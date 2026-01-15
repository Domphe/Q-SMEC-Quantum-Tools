"""Extract text corpus for vectorization/embedding."""
import sqlite3
import json
import sys
from pathlib import Path
from utils import DB_DIR

def extract_text_from_record(record: dict, table: str) -> str:
    """Extract searchable text from a record."""
    parts = []
    
    # Common fields
    if 'title' in record:
        parts.append(f"Title: {record['title']}")
    if 'name' in record:
        parts.append(f"Name: {record['name']}")
    if 'term' in record:
        parts.append(f"Term: {record['term']}")
    
    # Content fields
    if 'summary' in record:
        parts.append(f"Summary: {record['summary']}")
    if 'brief' in record:
        parts.append(f"Brief: {record['brief']}")
    if 'description' in record:
        parts.append(f"Description: {record['description']}")
    if 'definition' in record:
        parts.append(f"Definition: {record['definition']}")
    if 'long_explanation' in record:
        parts.append(f"Explanation: {record['long_explanation']}")
    if 'long_description' in record:
        parts.append(f"Description: {record['long_description']}")
    
    # Keywords/tags
    if 'keywords' in record:
        parts.append(f"Keywords: {', '.join(record['keywords'])}")
    if 'tags' in record:
        parts.append(f"Tags: {', '.join(record['tags'])}")
    
    return ' '.join(parts)

def main():
    """Extract corpus for embedding."""
    db_path = DB_DIR / 'qc_qp_expert.db'
    output_path = DB_DIR / 'embedding_corpus.txt'
    
    if not db_path.exists():
        print(f"ERROR: Database not found at {db_path}", file=sys.stderr)
        return 1
    
    conn = sqlite3.connect(db_path)
    
    try:
        tables = ['concepts', 'methods', 'workflows', 'software_tools', 'glossary']
        
        with open(output_path, 'w', encoding='utf-8') as f:
            total = 0
            
            for table in tables:
                cursor = conn.execute(f"SELECT id, json FROM {table}")
                
                for row in cursor:
                    record_id, json_str = row
                    record = json.loads(json_str)
                    
                    text = extract_text_from_record(record, table)
                    if text:
                        f.write(f"[{table}:{record_id}]\n")
                        f.write(text + '\n\n')
                        total += 1
            
            print(f"Extracted {total} records to {output_path}")
            print("NOTE: This is a stub. Integrate with actual embedding service (OpenAI, HuggingFace, etc.)")
        
        return 0
        
    finally:
        conn.close()

if __name__ == '__main__':
    sys.exit(main())
