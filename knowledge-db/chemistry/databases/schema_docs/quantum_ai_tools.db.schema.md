# Database Schema Documentation

**Database Path:** `Quantumn AI DB _ Tools\quantum_ai_tools.db`
**Generated:** 2026-01-08T22:30:50.350406
**Total Tables:** 9

## Table of Contents

- [ai_tools_files](#ai_tools_files)
- [ai_frameworks](#ai_frameworks)
- [quantum_capabilities](#quantum_capabilities)
- [technical_specs](#technical_specs)
- [cii_sector_mappings](#cii_sector_mappings)
- [entity_relationships](#entity_relationships)
- [scan_log](#scan_log)
- [use_cases](#use_cases)
- [benchmarks](#benchmarks)

## Tables

### ai_tools_files

**Row Count:** 406

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | INTEGER | Yes | Yes | - |
| `file_path` | TEXT | No | No | - |
| `file_name` | TEXT | Yes | No | - |
| `file_ext` | TEXT | Yes | No | - |
| `file_size` | INTEGER | Yes | No | - |
| `parent_folder` | TEXT | Yes | No | - |
| `ai_relevance_score` | REAL | Yes | No | 0.0 |
| `quantum_relevance_score` | REAL | Yes | No | 0.0 |
| `qsmec_relevance_score` | REAL | Yes | No | 0.0 |
| `cii_relevance_score` | REAL | Yes | No | 0.0 |
| `text_snippet` | TEXT | Yes | No | - |
| `scan_timestamp` | TEXT | Yes | No | - |
| `last_modified` | TEXT | Yes | No | - |

**Indexes:**

- idx_parent_folder
- idx_file_ext
- idx_qsmec_relevance
- idx_quantum_relevance
- idx_ai_relevance
- sqlite_autoindex_ai_tools_files_1

### ai_frameworks

**Row Count:** 320

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | INTEGER | Yes | Yes | - |
| `file_id` | INTEGER | Yes | No | - |
| `framework_name` | TEXT | Yes | No | - |
| `frequency` | INTEGER | Yes | No | 1 |
| `context` | TEXT | Yes | No | - |

### quantum_capabilities

**Row Count:** 745

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | INTEGER | Yes | Yes | - |
| `file_id` | INTEGER | Yes | No | - |
| `capability_type` | TEXT | Yes | No | - |
| `capability_name` | TEXT | Yes | No | - |
| `frequency` | INTEGER | Yes | No | 1 |
| `description` | TEXT | Yes | No | - |

### technical_specs

**Row Count:** 492

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | INTEGER | Yes | Yes | - |
| `file_id` | INTEGER | Yes | No | - |
| `spec_category` | TEXT | Yes | No | - |
| `spec_name` | TEXT | Yes | No | - |
| `spec_value` | TEXT | Yes | No | - |
| `frequency` | INTEGER | Yes | No | 1 |

### cii_sector_mappings

**Row Count:** 1,358

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | INTEGER | Yes | Yes | - |
| `file_id` | INTEGER | Yes | No | - |
| `sector_name` | TEXT | Yes | No | - |
| `frequency` | INTEGER | Yes | No | 1 |
| `relevance_context` | TEXT | Yes | No | - |

### entity_relationships

**Row Count:** 0

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | INTEGER | Yes | Yes | - |
| `source_file_id` | INTEGER | Yes | No | - |
| `target_file_id` | INTEGER | Yes | No | - |
| `relationship_type` | TEXT | Yes | No | - |
| `strength` | REAL | Yes | No | 0.5 |

### scan_log

**Row Count:** 2

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | INTEGER | Yes | Yes | - |
| `scan_start` | TEXT | Yes | No | - |
| `scan_end` | TEXT | Yes | No | - |
| `root_directory` | TEXT | Yes | No | - |
| `total_files_scanned` | INTEGER | Yes | No | - |
| `ai_relevant_files` | INTEGER | Yes | No | - |
| `quantum_relevant_files` | INTEGER | Yes | No | - |
| `qsmec_relevant_files` | INTEGER | Yes | No | - |
| `status` | TEXT | Yes | No | - |

### use_cases

**Row Count:** 42

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | TEXT | Yes | Yes | - |
| `name` | TEXT | No | No | - |
| `sector` | TEXT | Yes | No | - |
| `description` | TEXT | Yes | No | - |
| `tam_billion` | REAL | Yes | No | - |
| `cagr_percent` | REAL | Yes | No | - |
| `trl_target` | TEXT | Yes | No | - |
| `performance_params` | TEXT | Yes | No | - |
| `json` | TEXT | Yes | No | - |
| `updated_at` | TEXT | Yes | No | - |

**Indexes:**

- sqlite_autoindex_use_cases_1

### benchmarks

**Row Count:** 100

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | TEXT | Yes | Yes | - |
| `method` | TEXT | Yes | No | - |
| `use_case_id` | TEXT | Yes | No | - |
| `metric_name` | TEXT | Yes | No | - |
| `metric_value` | REAL | Yes | No | - |
| `metric_unit` | TEXT | Yes | No | - |
| `reference` | TEXT | Yes | No | - |
| `json` | TEXT | Yes | No | - |
| `updated_at` | TEXT | Yes | No | - |

**Indexes:**

- sqlite_autoindex_benchmarks_1
