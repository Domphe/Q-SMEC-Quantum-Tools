"""
QCDB Client Extension Validator
Validates client extension JSON files against schema and security requirements.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import jsonschema


class ExtensionValidator:
    """Validate client extension files."""
    
    def __init__(self, schema_path: Path):
        with open(schema_path, 'r') as f:
            self.schema = json.load(f)
        self.errors = []
        self.warnings = []
    
    def validate_schema(self, extension_data: Dict) -> bool:
        """Validate against JSON schema."""
        try:
            jsonschema.validate(instance=extension_data, schema=self.schema)
            return True
        except jsonschema.ValidationError as e:
            self.errors.append(f"Schema validation failed: {e.message}")
            return False
        except Exception as e:
            self.errors.append(f"Validation error: {str(e)}")
            return False
    
    def validate_id_namespace(self, extension_data: Dict) -> bool:
        """Validate that all IDs follow client namespace pattern."""
        client_id = extension_data.get('client_id', '')
        valid = True
        
        for entity_type, entities in extension_data.get('entities', {}).items():
            for entity in entities:
                entity_id = entity.get('id', '')
                
                # Check namespace prefix
                expected_prefix = f"client_{client_id}_"
                if not entity_id.startswith(expected_prefix):
                    self.errors.append(
                        f"{entity_type} ID '{entity_id}' must start with '{expected_prefix}'"
                    )
                    valid = False
                
                # Check for invalid characters
                if not re.match(r'^[a-z0-9_]+$', entity_id):
                    self.errors.append(
                        f"{entity_type} ID '{entity_id}' contains invalid characters"
                    )
                    valid = False
        
        return valid
    
    def check_id_collisions(self, extension_data: Dict, existing_ids: set) -> bool:
        """Check for ID collisions with existing entities."""
        valid = True
        
        for entity_type, entities in extension_data.get('entities', {}).items():
            for entity in entities:
                entity_id = entity.get('id', '')
                if entity_id in existing_ids:
                    self.errors.append(
                        f"{entity_type} ID '{entity_id}' already exists in knowledge base"
                    )
                    valid = False
        
        return valid
    
    def validate_references(self, extension_data: Dict, core_kb_ids: set, extension_ids: set) -> bool:
        """Validate that all referenced IDs exist in core KB or extension."""
        valid = True
        all_valid_ids = core_kb_ids | extension_ids
        
        reference_fields = {
            'Concepts': ['prerequisites', 'related_methods', 'related_tools'],
            'Methods': ['theoretical_basis', 'implemented_in'],
            'Workflows': ['related_methods', 'example_problems']
        }
        
        for entity_type, entities in extension_data.get('entities', {}).items():
            if entity_type not in reference_fields:
                continue
            
            for entity in entities:
                for field in reference_fields[entity_type]:
                    if field in entity:
                        refs = entity[field]
                        if isinstance(refs, str):
                            refs = [refs]
                        
                        for ref_id in refs:
                            if ref_id not in all_valid_ids:
                                self.warnings.append(
                                    f"{entity_type}.{entity['id']}.{field} references unknown ID: {ref_id}"
                                )
        
        return valid
    
    def validate_security(self, extension_data: Dict) -> bool:
        """Validate security constraints."""
        valid = True
        
        # Check encryption requirements for confidential data
        visibility = extension_data.get('visibility', 'client_specific')
        encryption = extension_data.get('encryption_level', 'none')
        
        if visibility == 'confidential' and encryption == 'none':
            self.errors.append(
                "Confidential extensions must have encryption enabled"
            )
            valid = False
        
        # Check authorized users
        if visibility in ['client_specific', 'confidential']:
            if not extension_data.get('authorized_users'):
                self.warnings.append(
                    "No authorized users specified for restricted extension"
                )
        
        return valid
    
    def validate_extension(
        self,
        extension_path: Path,
        core_kb_ids: Optional[set] = None,
        existing_extension_ids: Optional[set] = None
    ) -> Tuple[bool, List[str], List[str]]:
        """
        Validate a client extension file.
        
        Returns:
            (is_valid, errors, warnings)
        """
        self.errors = []
        self.warnings = []
        
        # Load extension file
        try:
            with open(extension_path, 'r', encoding='utf-8') as f:
                extension_data = json.load(f)
        except Exception as e:
            self.errors.append(f"Failed to load extension file: {str(e)}")
            return False, self.errors, self.warnings
        
        # Run validations
        valid = True
        
        # Schema validation
        if not self.validate_schema(extension_data):
            valid = False
        
        # ID namespace validation
        if not self.validate_id_namespace(extension_data):
            valid = False
        
        # ID collision check
        if core_kb_ids is not None:
            all_existing = core_kb_ids | (existing_extension_ids or set())
            if not self.check_id_collisions(extension_data, all_existing):
                valid = False
        
        # Reference validation
        if core_kb_ids is not None:
            # Collect extension IDs
            ext_ids = set()
            for entities in extension_data.get('entities', {}).values():
                for entity in entities:
                    ext_ids.add(entity.get('id', ''))
            
            self.validate_references(extension_data, core_kb_ids, ext_ids)
        
        # Security validation
        if not self.validate_security(extension_data):
            valid = False
        
        return valid, self.errors, self.warnings


def main():
    """Test validator."""
    import os
    qcbd_root = Path(os.environ.get('QCBD_ROOT', r'G:\My Drive\Databases\QCBD'))
    schema_path = qcbd_root / "schemas" / "client_extension_schema.json"
    
    if not schema_path.exists():
        print(f"✗ Schema file not found: {schema_path}")
        return 1
    
    validator = ExtensionValidator(schema_path)
    
    # Create test extension
    test_extension = {
        "client_id": "test_client",
        "extension_version": "1.0.0",
        "visibility": "client_specific",
        "encryption_level": "none",
        "authorized_users": ["user1", "user2"],
        "entities": {
            "Methods": [
                {
                    "id": "client_test_client_method_custom_dft",
                    "name": "Custom DFT Functional",
                    "class": "DFT",
                    "visibility": "client_specific",
                    "proprietary": True
                }
            ]
        },
        "metadata": {
            "created_by": "test_user",
            "description": "Test extension"
        }
    }
    
    # Save test extension
    test_path = qcbd_root / "QCBD_client_extensions" / "template" / "extension.json"
    test_path.parent.mkdir(parents=True, exist_ok=True)
    with open(test_path, 'w') as f:
        json.dump(test_extension, f, indent=2)
    
    # Validate
    valid, errors, warnings = validator.validate_extension(test_path)
    
    print(f"\nValidation result: {'✓ Valid' if valid else '✗ Invalid'}")
    if errors:
        print(f"\nErrors ({len(errors)}):")
        for error in errors:
            print(f"  - {error}")
    if warnings:
        print(f"\nWarnings ({len(warnings)}):")
        for warning in warnings:
            print(f"  - {warning}")
    
    return 0 if valid else 1


if __name__ == "__main__":
    exit(main())
