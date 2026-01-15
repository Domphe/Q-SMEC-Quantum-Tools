# Database Schema Documentation

**Database Path:** `niket_factual_database.db`
**Generated:** 2026-01-08T22:30:49.961767
**Total Tables:** 6

## Table of Contents

- [technical_specs](#technical_specs)
- [market_data](#market_data)
- [technical_terms](#technical_terms)
- [competitive_advantages](#competitive_advantages)
- [development_timeline](#development_timeline)
- [source_documents](#source_documents)

## Tables

### technical_specs

**Row Count:** 722

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | INTEGER | Yes | Yes | - |
| `spec_type` | TEXT | No | No | - |
| `value` | TEXT | No | No | - |
| `unit` | TEXT | Yes | No | - |
| `context` | TEXT | Yes | No | - |
| `source_document` | TEXT | Yes | No | - |
| `extraction_date` | TEXT | Yes | No | - |
| `confidence_level` | TEXT | Yes | No | 'medium' |

### market_data

**Row Count:** 0

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | INTEGER | Yes | Yes | - |
| `market_segment` | TEXT | No | No | - |
| `market_size_value` | REAL | Yes | No | - |
| `market_size_unit` | TEXT | Yes | No | - |
| `cagr_percentage` | REAL | Yes | No | - |
| `context` | TEXT | Yes | No | - |
| `source_document` | TEXT | Yes | No | - |
| `year_reference` | INTEGER | Yes | No | - |
| `extraction_date` | TEXT | Yes | No | - |

### technical_terms

**Row Count:** 31

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | INTEGER | Yes | Yes | - |
| `term` | TEXT | No | No | - |
| `category` | TEXT | No | No | - |
| `frequency` | INTEGER | Yes | No | - |
| `context` | TEXT | Yes | No | - |
| `definition` | TEXT | Yes | No | - |
| `extraction_date` | TEXT | Yes | No | - |

### competitive_advantages

**Row Count:** 20

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | INTEGER | Yes | Yes | - |
| `claim` | TEXT | No | No | - |
| `advantage_type` | TEXT | Yes | No | - |
| `confidence_level` | TEXT | Yes | No | - |
| `supporting_data` | TEXT | Yes | No | - |
| `source_document` | TEXT | Yes | No | - |
| `extraction_date` | TEXT | Yes | No | - |

### development_timeline

**Row Count:** 40

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | INTEGER | Yes | Yes | - |
| `phase_type` | TEXT | No | No | - |
| `phase_identifier` | TEXT | Yes | No | - |
| `description` | TEXT | Yes | No | - |
| `timeline_reference` | TEXT | Yes | No | - |
| `context` | TEXT | Yes | No | - |
| `extraction_date` | TEXT | Yes | No | - |

### source_documents

**Row Count:** 12

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | INTEGER | Yes | Yes | - |
| `filename` | TEXT | No | No | - |
| `file_size` | INTEGER | Yes | No | - |
| `word_count` | INTEGER | Yes | No | - |
| `modified_date` | TEXT | Yes | No | - |
| `extraction_date` | TEXT | Yes | No | - |
| `document_type` | TEXT | Yes | No | - |

**Indexes:**

- sqlite_autoindex_source_documents_1
