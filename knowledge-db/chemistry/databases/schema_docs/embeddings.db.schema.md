# Database Schema Documentation

**Database Path:** `QCBD\expert\embeddings.db`
**Generated:** 2026-01-08T22:30:50.421709
**Total Tables:** 2

## Table of Contents

- [embeddings](#embeddings)
- [documents](#documents)

## Tables

### embeddings

**Row Count:** 526

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `entity_id` | TEXT | Yes | Yes | - |
| `entity_type` | TEXT | Yes | No | - |
| `name` | TEXT | Yes | No | - |
| `searchable_text` | TEXT | Yes | No | - |
| `vector` | TEXT | Yes | No | - |
| `data` | TEXT | Yes | No | - |

**Indexes:**

- idx_entity_type
- sqlite_autoindex_embeddings_1

### documents

**Row Count:** 42

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | TEXT | Yes | Yes | - |
| `doc_type` | TEXT | Yes | No | - |
| `title` | TEXT | Yes | No | - |
| `content` | TEXT | Yes | No | - |
| `metadata` | TEXT | Yes | No | - |
| `embedding` | BLOB | Yes | No | - |
| `updated_at` | TEXT | Yes | No | - |

**Indexes:**

- sqlite_autoindex_documents_1
