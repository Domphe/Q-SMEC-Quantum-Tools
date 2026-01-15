# Database Schema Documentation

**Database Path:** `qsmec_knowledge_base.db`
**Generated:** 2026-01-08T22:30:50.088054
**Total Tables:** 5

## Table of Contents

- [files](#files)
- [entities](#entities)
- [relationships](#relationships)
- [file_references](#file_references)
- [scan_log](#scan_log)

## Tables

### files

**Row Count:** 0

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | INTEGER | Yes | Yes | - |
| `path` | TEXT | No | No | - |
| `filename` | TEXT | No | No | - |
| `extension` | TEXT | Yes | No | - |
| `size_bytes` | INTEGER | Yes | No | - |
| `modified_timestamp` | TEXT | Yes | No | - |
| `content_hash` | TEXT | Yes | No | - |
| `qsmec_relevance_score` | REAL | Yes | No | 0.0 |
| `content_summary` | TEXT | Yes | No | - |
| `scan_timestamp` | TEXT | No | No | - |

**Indexes:**

- idx_files_ext
- idx_files_relevance
- sqlite_autoindex_files_1

### entities

**Row Count:** 0

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | INTEGER | Yes | Yes | - |
| `entity_text` | TEXT | No | No | - |
| `entity_type` | TEXT | No | No | - |
| `category` | TEXT | Yes | No | - |
| `frequency` | INTEGER | Yes | No | 1 |

**Indexes:**

- idx_entities_freq
- sqlite_autoindex_entities_1

### relationships

**Row Count:** 0

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | INTEGER | Yes | Yes | - |
| `file_id` | INTEGER | No | No | - |
| `entity_id` | INTEGER | No | No | - |
| `context_snippet` | TEXT | Yes | No | - |
| `relevance_score` | REAL | Yes | No | 0.0 |

**Indexes:**

- idx_rel_entity
- idx_rel_file

### file_references

**Row Count:** 0

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | INTEGER | Yes | Yes | - |
| `source_file_id` | INTEGER | No | No | - |
| `target_file_id` | INTEGER | No | No | - |
| `reference_type` | TEXT | Yes | No | - |

### scan_log

**Row Count:** 0

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | INTEGER | Yes | Yes | - |
| `scan_timestamp` | TEXT | No | No | - |
| `files_scanned` | INTEGER | Yes | No | - |
| `qsmec_files_found` | INTEGER | Yes | No | - |
| `total_entities` | INTEGER | Yes | No | - |
