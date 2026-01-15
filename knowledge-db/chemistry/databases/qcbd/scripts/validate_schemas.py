"""Validate JSONL files against JSON schemas."""
import sys
import argparse
from pathlib import Path
from jsonschema import Draft7Validator, ValidationError
from utils import read_jsonl, read_json, SCHEMAS, DATA_PROCESSED

def validate_file(jsonl_path: Path, schema_path: Path) -> tuple[int, int]:
    """Validate JSONL file against schema. Returns (valid_count, error_count)."""
    schema = read_json(schema_path)
    validator = Draft7Validator(schema)
    
    valid_count = 0
    error_count = 0
    
    for idx, record in enumerate(read_jsonl(jsonl_path), 1):
        errors = list(validator.iter_errors(record))
        if errors:
            error_count += 1
            print(f"  [ERROR] Record {idx} (id={record.get('id', 'unknown')}):")
            for error in errors:
                print(f"    - {error.message} at {'.'.join(str(p) for p in error.path)}")
        else:
            valid_count += 1
    
    return valid_count, error_count

def main():
    parser = argparse.ArgumentParser(description="Validate JSONL files against schemas")
    parser.add_argument('--file', help='Specific JSONL file to validate')
    parser.add_argument('--schema', help='Specific schema file to use')
    args = parser.parse_args()
    
    if args.file and args.schema:
        # Validate single file
        jsonl_path = Path(args.file)
        schema_path = Path(args.schema)
        print(f"Validating {jsonl_path.name} against {schema_path.name}...")
        valid, errors = validate_file(jsonl_path, schema_path)
        print(f"  Valid: {valid}, Errors: {errors}")
        return 0 if errors == 0 else 1
    
    # Validate all processed files
    schema_map = {
        'sources.jsonl': 'source.schema.json',
        'concepts.qc.jsonl': 'concept.schema.json',
        'concepts.qp.jsonl': 'concept.schema.json',
        'methods.qc.jsonl': 'method.schema.json',
        'methods.qp.jsonl': 'method.schema.json',
        'equations.jsonl': 'equation.schema.json',
        'workflows.jsonl': 'workflow.schema.json',
        'software_tools.jsonl': 'software_tool.schema.json',
        'datasets.jsonl': 'dataset.schema.json',
        'glossary.jsonl': 'glossary.schema.json'
    }
    
    total_valid = 0
    total_errors = 0
    
    print("Validating all processed data files...\n")
    for jsonl_file, schema_file in schema_map.items():
        jsonl_path = DATA_PROCESSED / jsonl_file
        schema_path = SCHEMAS / schema_file
        
        if not jsonl_path.exists():
            print(f"[SKIP] {jsonl_file} (not found)")
            continue
        
        if not schema_path.exists():
            print(f"[SKIP] {jsonl_file} (schema not found: {schema_file})")
            continue
        
        print(f"Validating {jsonl_file}...")
        valid, errors = validate_file(jsonl_path, schema_path)
        total_valid += valid
        total_errors += errors
        print(f"  Valid: {valid}, Errors: {errors}\n")
    
    print(f"Total valid records: {total_valid}")
    print(f"Total errors: {total_errors}")
    
    return 0 if total_errors == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
