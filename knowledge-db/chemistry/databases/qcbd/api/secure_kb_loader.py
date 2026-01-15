"""
QCDB Secure Knowledge Base Loader
Loads knowledge base with client extensions, RBAC, and encryption.
"""

import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Set
from datetime import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
import base64


class AccessControl:
    """Role-based access control manager."""
    
    def __init__(self, roles_config_path: Path):
        with open(roles_config_path, 'r') as f:
            self.config = json.load(f)
        self.roles = self.config['roles']
        self.users = self.config['users']
    
    def get_user_role(self, user_id: str) -> Optional[str]:
        """Get role for a user."""
        user = self.users.get(user_id)
        return user['role'] if user else None
    
    def can_access_visibility(self, user_id: str, visibility: str) -> bool:
        """Check if user can access content with given visibility level."""
        role_name = self.get_user_role(user_id)
        if not role_name:
            return False
        
        role = self.roles[role_name]
        return visibility in role.get('can_access_visibility', [])
    
    def can_access_client(self, user_id: str, client_id: str) -> bool:
        """Check if user can access a specific client's extensions."""
        user = self.users.get(user_id)
        if not user:
            return False
        
        # Admin has access to all
        if user['role'] == 'admin':
            return True
        
        # Check explicit authorization
        authorized_clients = user.get('authorized_clients', [])
        return '*' in authorized_clients or client_id in authorized_clients
    
    def has_permission(self, user_id: str, permission: str) -> bool:
        """Check if user has a specific permission."""
        role_name = self.get_user_role(user_id)
        if not role_name:
            return False
        
        role = self.roles[role_name]
        permissions = role.get('permissions', [])
        
        # Check exact match or wildcard
        return permission in permissions or 'read:all' in permissions


class EncryptionManager:
    """Manage encryption/decryption of client extension data."""
    
    def __init__(self, keys_file: Path):
        self.keys_file = keys_file
        self.keys = self._load_keys()
    
    def _load_keys(self) -> Dict[str, bytes]:
        """Load encryption keys from secure storage."""
        if self.keys_file.exists():
            with open(self.keys_file, 'r') as f:
                keys_data = json.load(f)
            
            # Convert base64 keys to bytes
            return {
                client_id: base64.b64decode(key)
                for client_id, key in keys_data.items()
            }
        return {}
    
    def _save_keys(self):
        """Save encryption keys."""
        keys_data = {
            client_id: base64.b64encode(key).decode()
            for client_id, key in self.keys.items()
        }
        with open(self.keys_file, 'w') as f:
            json.dump(keys_data, f, indent=2)
    
    def generate_key_for_client(self, client_id: str, password: str) -> bytes:
        """Generate encryption key for a client."""
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=client_id.encode(),
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        self.keys[client_id] = key
        self._save_keys()
        return key
    
    def decrypt_extension(self, client_id: str, encrypted_data: bytes) -> Dict:
        """Decrypt client extension data."""
        if client_id not in self.keys:
            raise ValueError(f"No encryption key for client: {client_id}")
        
        fernet = Fernet(self.keys[client_id])
        decrypted = fernet.decrypt(encrypted_data)
        return json.loads(decrypted)
    
    def encrypt_extension(self, client_id: str, extension_data: Dict) -> bytes:
        """Encrypt client extension data."""
        if client_id not in self.keys:
            raise ValueError(f"No encryption key for client: {client_id}")
        
        fernet = Fernet(self.keys[client_id])
        json_data = json.dumps(extension_data).encode()
        return fernet.encrypt(json_data)


class AuditLogger:
    """Log access to knowledge base for security auditing."""
    
    def __init__(self, log_db_path: Path):
        self.db_path = log_db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize audit log database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS access_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                user_id TEXT NOT NULL,
                action TEXT NOT NULL,
                entity_type TEXT,
                entity_id TEXT,
                client_id TEXT,
                success INTEGER NOT NULL,
                details TEXT
            )
        """)
        conn.commit()
        conn.close()
    
    def log_access(
        self,
        user_id: str,
        action: str,
        success: bool,
        entity_type: Optional[str] = None,
        entity_id: Optional[str] = None,
        client_id: Optional[str] = None,
        details: Optional[str] = None
    ):
        """Log an access event."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO access_logs 
            (timestamp, user_id, action, entity_type, entity_id, client_id, success, details)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            user_id,
            action,
            entity_type,
            entity_id,
            client_id,
            1 if success else 0,
            details
        ))
        conn.commit()
        conn.close()


class SecureKBLoader:
    """Securely load knowledge base with extensions and access control."""
    
    def __init__(
        self,
        qcbd_root: Path,
        user_id: str,
        keys_file: Optional[Path] = None
    ):
        self.qcbd_root = qcbd_root
        self.user_id = user_id
        
        # Initialize components
        self.access_control = AccessControl(qcbd_root / "access_control" / "roles.json")
        self.audit_logger = AuditLogger(qcbd_root / "client_access_logs.db")
        
        if keys_file:
            self.encryption_manager = EncryptionManager(keys_file)
        else:
            self.encryption_manager = None
        
        self.core_kb = None
        self.loaded_extensions = {}
    
    def load_core_kb(self) -> Dict:
        """Load core knowledge base."""
        kb_path = self.qcbd_root / "qc_knowledge_graph_full.json"
        
        if not kb_path.exists():
            raise FileNotFoundError(f"Core KB not found: {kb_path}")
        
        with open(kb_path, 'r', encoding='utf-8') as f:
            self.core_kb = json.load(f)
        
        self.audit_logger.log_access(
            self.user_id,
            "load_core_kb",
            True,
            details="Loaded core knowledge base"
        )
        
        return self.core_kb
    
    def _filter_entities_by_visibility(self, entities: List[Dict]) -> List[Dict]:
        """Filter entities based on user's visibility permissions."""
        filtered = []
        for entity in entities:
            visibility = entity.get('visibility', 'public')
            if self.access_control.can_access_visibility(self.user_id, visibility):
                filtered.append(entity)
        return filtered
    
    def load_client_extension(self, client_id: str) -> Optional[Dict]:
        """Load a client extension if user is authorized."""
        # Check authorization
        if not self.access_control.can_access_client(self.user_id, client_id):
            self.audit_logger.log_access(
                self.user_id,
                "load_extension",
                False,
                client_id=client_id,
                details="Unauthorized access attempt"
            )
            return None
        
        # Load extension file
        extension_path = self.qcbd_root / "QCBD_client_extensions" / client_id / "extension.json"
        encrypted_path = self.qcbd_root / "QCBD_client_extensions" / client_id / "extension.enc"
        
        try:
            if encrypted_path.exists() and self.encryption_manager:
                # Load and decrypt
                with open(encrypted_path, 'rb') as f:
                    encrypted_data = f.read()
                extension = self.encryption_manager.decrypt_extension(client_id, encrypted_data)
            elif extension_path.exists():
                # Load plain JSON
                with open(extension_path, 'r', encoding='utf-8') as f:
                    extension = json.load(f)
            else:
                return None
            
            # Filter by visibility
            filtered_extension = extension.copy()
            for entity_type in filtered_extension.get('entities', {}):
                filtered_extension['entities'][entity_type] = self._filter_entities_by_visibility(
                    filtered_extension['entities'][entity_type]
                )
            
            self.loaded_extensions[client_id] = filtered_extension
            
            self.audit_logger.log_access(
                self.user_id,
                "load_extension",
                True,
                client_id=client_id,
                details=f"Loaded extension for {client_id}"
            )
            
            return filtered_extension
        
        except Exception as e:
            self.audit_logger.log_access(
                self.user_id,
                "load_extension",
                False,
                client_id=client_id,
                details=f"Error: {str(e)}"
            )
            return None
    
    def get_merged_kb(self, client_ids: Optional[List[str]] = None) -> Dict:
        """Get knowledge base merged with authorized client extensions."""
        if not self.core_kb:
            self.load_core_kb()
        
        # Start with filtered core KB
        merged = {
            entity_type: self._filter_entities_by_visibility(entities)
            for entity_type, entities in self.core_kb.items()
            if entity_type != 'metadata'
        }
        merged['metadata'] = self.core_kb.get('metadata', {}).copy()
        
        # Merge client extensions
        if client_ids:
            for client_id in client_ids:
                extension = self.load_client_extension(client_id)
                if extension:
                    for entity_type, entities in extension.get('entities', {}).items():
                        if entity_type in merged:
                            merged[entity_type].extend(entities)
                        else:
                            merged[entity_type] = entities
        
        # Update metadata
        merged['metadata']['loaded_extensions'] = list(self.loaded_extensions.keys())
        merged['metadata']['loaded_by'] = self.user_id
        merged['metadata']['loaded_at'] = datetime.now().isoformat()
        
        return merged


def main():
    """Test secure KB loader."""
    import os
    qcbd_root = Path(os.environ.get('QCBD_ROOT', r'G:\My Drive\Databases\QCBD'))
    
    # Test with example admin user
    loader = SecureKBLoader(qcbd_root, user_id="example_admin")
    
    # Load core KB
    print("Loading core knowledge base...")
    kb = loader.load_core_kb()
    print(f"✓ Loaded {kb['metadata']['total_entities']} entities")
    
    # Get merged KB (no extensions)
    merged = loader.get_merged_kb()
    print(f"✓ Merged KB ready")
    print(f"  User: {merged['metadata']['loaded_by']}")
    print(f"  Extensions: {merged['metadata']['loaded_extensions']}")


if __name__ == "__main__":
    main()
