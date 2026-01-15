# Database Schema Documentation

**Database Path:** `QCBD\qc_graph.db`
**Generated:** 2026-01-08T22:30:50.396176
**Total Tables:** 4

## Table of Contents

- [nodes](#nodes)
- [relationships](#relationships)
- [embeddings](#embeddings)
- [edges](#edges)

## Tables

### nodes

**Row Count:** 150

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | TEXT | Yes | Yes | - |
| `label` | TEXT | No | No | - |
| `name` | TEXT | Yes | No | - |
| `properties` | TEXT | Yes | No | - |

**Indexes:**

- idx_nodes_label
- sqlite_autoindex_nodes_1

### relationships

**Row Count:** 69

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | INTEGER | Yes | Yes | - |
| `source_id` | TEXT | No | No | - |
| `target_id` | TEXT | No | No | - |
| `rel_type` | TEXT | No | No | - |

**Indexes:**

- idx_rel_type
- idx_rel_target
- idx_rel_source

### embeddings

**Row Count:** 10

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `method_id` | TEXT | Yes | Yes | - |
| `name` | TEXT | Yes | No | - |
| `vector` | TEXT | Yes | No | - |

**Indexes:**

- sqlite_autoindex_embeddings_1

### edges

**Row Count:** 50

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | TEXT | Yes | Yes | - |
| `source_id` | TEXT | Yes | No | - |
| `target_id` | TEXT | Yes | No | - |
| `relationship` | TEXT | Yes | No | - |
| `properties` | TEXT | Yes | No | - |
| `created_at` | TEXT | Yes | No | - |

**Indexes:**

- sqlite_autoindex_edges_1
