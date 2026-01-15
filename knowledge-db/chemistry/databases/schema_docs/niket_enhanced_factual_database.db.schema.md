# Database Schema Documentation

**Database Path:** `niket_enhanced_factual_database.db`
**Generated:** 2026-01-08T22:30:50.025341
**Total Tables:** 5

## Table of Contents

- [enhanced_technical_specs](#enhanced_technical_specs)
- [market_analysis](#market_analysis)
- [enhanced_technical_terms](#enhanced_technical_terms)
- [performance_metrics](#performance_metrics)
- [application_domains](#application_domains)

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
