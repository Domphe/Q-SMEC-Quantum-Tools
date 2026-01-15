# Database Schema Documentation

**Database Path:** `niket_consolidated_database.db`
**Generated:** 2026-01-08T22:30:50.255235
**Total Tables:** 12

## Table of Contents

- [enhanced_technical_specs](#enhanced_technical_specs)
- [market_analysis](#market_analysis)
- [enhanced_technical_terms](#enhanced_technical_terms)
- [performance_metrics](#performance_metrics)
- [application_domains](#application_domains)
- [competitive_advantages](#competitive_advantages)
- [development_timeline](#development_timeline)
- [market_data](#market_data)
- [source_documents](#source_documents)
- [technical_specs](#technical_specs)
- [technical_terms](#technical_terms)
- [data_refresh_log](#data_refresh_log)

## Tables

### enhanced_technical_specs

**Row Count:** 51

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | INTEGER | Yes | Yes | - |
| `spec_type` | TEXT | No | No | - |
| `value` | TEXT | No | No | - |
| `unit` | TEXT | Yes | No | - |
| `context` | TEXT | Yes | No | - |
| `source_folder` | TEXT | Yes | No | - |
| `confidence_level` | TEXT | Yes | No | 'documented' |
| `extraction_timestamp` | TEXT | Yes | No | - |

**Indexes:**

- sqlite_autoindex_enhanced_technical_specs_1

### market_analysis

**Row Count:** 5

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | INTEGER | Yes | Yes | - |
| `market_segment` | TEXT | No | No | - |
| `value` | TEXT | No | No | - |
| `value_type` | TEXT | No | No | - |
| `currency` | TEXT | Yes | No | 'USD' |
| `timeframe` | TEXT | Yes | No | - |
| `source_folder` | TEXT | Yes | No | - |
| `extraction_timestamp` | TEXT | Yes | No | - |

**Indexes:**

- sqlite_autoindex_market_analysis_1

### enhanced_technical_terms

**Row Count:** 30

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | INTEGER | Yes | Yes | - |
| `term` | TEXT | No | No | - |
| `category` | TEXT | No | No | - |
| `frequency` | INTEGER | Yes | No | 1 |
| `source_folders` | TEXT | Yes | No | - |
| `definition` | TEXT | Yes | No | - |
| `related_terms` | TEXT | Yes | No | - |
| `importance_score` | REAL | Yes | No | - |

**Indexes:**

- sqlite_autoindex_enhanced_technical_terms_1

### performance_metrics

**Row Count:** 12

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | INTEGER | Yes | Yes | - |
| `metric_type` | TEXT | No | No | - |
| `value` | REAL | No | No | - |
| `unit` | TEXT | Yes | No | - |
| `context` | TEXT | Yes | No | - |
| `benchmark_comparison` | TEXT | Yes | No | - |
| `source_folder` | TEXT | Yes | No | - |
| `validation_status` | TEXT | Yes | No | 'documented' |

**Indexes:**

- sqlite_autoindex_performance_metrics_1

### application_domains

**Row Count:** 10

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | INTEGER | Yes | Yes | - |
| `domain_name` | TEXT | No | No | - |
| `sector` | TEXT | Yes | No | - |
| `use_cases` | TEXT | Yes | No | - |
| `trl_level` | TEXT | Yes | No | - |
| `market_potential` | TEXT | Yes | No | - |
| `technical_requirements` | TEXT | Yes | No | - |
| `competitive_landscape` | TEXT | Yes | No | - |

**Indexes:**

- sqlite_autoindex_application_domains_1

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

**Indexes:**

- idx_technical_specs_context
- idx_technical_specs_value

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

### data_refresh_log

**Row Count:** 1

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | INTEGER | Yes | Yes | - |
| `run_timestamp` | TEXT | No | No | - |
| `source_catalog_path` | TEXT | No | No | - |
| `total_directories` | INTEGER | Yes | No | - |
| `total_files` | INTEGER | Yes | No | - |
| `total_size_mb` | REAL | Yes | No | - |
