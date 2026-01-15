# Database Schema Documentation

**Database Path:** `QCBD\db\qc_qp_expert_v2.db`
**Generated:** 2026-01-08T22:30:50.501451
**Total Tables:** 8

## Table of Contents

- [method_performance](#method_performance)
- [use_case_requirements](#use_case_requirements)
- [material_properties](#material_properties)
- [performance_metrics](#performance_metrics)
- [benchmark_metadata](#benchmark_metadata)
- [method_applicability](#method_applicability)
- [cross_references](#cross_references)
- [validation_results](#validation_results)

## Tables

### method_performance

**Row Count:** 0

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | TEXT | Yes | Yes | - |
| `method_id` | TEXT | No | No | - |
| `benchmark_id` | TEXT | No | No | - |
| `metric_type` | TEXT | No | No | - |
| `metric_value` | REAL | Yes | No | - |
| `metric_unit` | TEXT | Yes | No | - |
| `dataset_size` | INTEGER | Yes | No | - |
| `computational_time_s` | REAL | Yes | No | - |
| `memory_gb` | REAL | Yes | No | - |
| `num_processors` | INTEGER | Yes | No | - |
| `software_used` | TEXT | Yes | No | - |
| `basis_set` | TEXT | Yes | No | - |
| `functional` | TEXT | Yes | No | - |
| `convergence_criteria` | TEXT | Yes | No | - |
| `reference_source` | TEXT | Yes | No | - |
| `validated_date` | TEXT | Yes | No | - |
| `notes` | TEXT | Yes | No | - |
| `json` | TEXT | No | No | - |

**Indexes:**

- idx_method_perf_benchmark
- idx_method_perf_method
- sqlite_autoindex_method_performance_1

### use_case_requirements

**Row Count:** 0

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | TEXT | Yes | Yes | - |
| `use_case_id` | TEXT | No | No | - |
| `requirement_type` | TEXT | No | No | - |
| `requirement_name` | TEXT | No | No | - |
| `target_value` | TEXT | Yes | No | - |
| `min_value` | REAL | Yes | No | - |
| `max_value` | REAL | Yes | No | - |
| `unit` | TEXT | Yes | No | - |
| `priority` | TEXT | Yes | No | - |
| `validation_method` | TEXT | Yes | No | - |
| `current_status` | TEXT | Yes | No | - |
| `trl_milestone` | INTEGER | Yes | No | - |
| `notes` | TEXT | Yes | No | - |
| `json` | TEXT | No | No | - |

**Indexes:**

- idx_use_case_req
- sqlite_autoindex_use_case_requirements_1

### material_properties

**Row Count:** 0

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | TEXT | Yes | Yes | - |
| `material_id` | TEXT | No | No | - |
| `property_type` | TEXT | No | No | - |
| `property_name` | TEXT | No | No | - |
| `property_value` | REAL | Yes | No | - |
| `property_unit` | TEXT | Yes | No | - |
| `temperature_k` | REAL | Yes | No | - |
| `pressure_gpa` | REAL | Yes | No | - |
| `measurement_method` | TEXT | Yes | No | - |
| `computational_method` | TEXT | Yes | No | - |
| `uncertainty` | REAL | Yes | No | - |
| `reference_source` | TEXT | Yes | No | - |
| `validated_experimental` | BOOLEAN | Yes | No | - |
| `quality_score` | REAL | Yes | No | - |
| `json` | TEXT | No | No | - |

**Indexes:**

- idx_material_prop_type
- sqlite_autoindex_material_properties_1

### performance_metrics

**Row Count:** 0

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | TEXT | Yes | Yes | - |
| `entity_id` | TEXT | No | No | - |
| `entity_type` | TEXT | No | No | - |
| `metric_name` | TEXT | No | No | - |
| `metric_value` | REAL | Yes | No | - |
| `metric_unit` | TEXT | Yes | No | - |
| `timestamp` | TEXT | Yes | No | - |
| `measurement_conditions` | TEXT | Yes | No | - |
| `operator` | TEXT | Yes | No | - |
| `instrument` | TEXT | Yes | No | - |
| `calibration_date` | TEXT | Yes | No | - |
| `environmental_conditions` | TEXT | Yes | No | - |
| `json` | TEXT | No | No | - |

**Indexes:**

- idx_perf_metrics_entity
- sqlite_autoindex_performance_metrics_1

### benchmark_metadata

**Row Count:** 0

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | TEXT | Yes | Yes | - |
| `benchmark_id` | TEXT | No | No | - |
| `data_source` | TEXT | Yes | No | - |
| `num_entries` | INTEGER | Yes | No | - |
| `property_range_min` | REAL | Yes | No | - |
| `property_range_max` | REAL | Yes | No | - |
| `chemical_space` | TEXT | Yes | No | - |
| `system_size_range` | TEXT | Yes | No | - |
| `accuracy_targets` | TEXT | Yes | No | - |
| `reference_level` | TEXT | Yes | No | - |
| `validation_protocol` | TEXT | Yes | No | - |
| `last_updated` | TEXT | Yes | No | - |
| `curator` | TEXT | Yes | No | - |
| `doi` | TEXT | Yes | No | - |
| `notes` | TEXT | Yes | No | - |
| `json` | TEXT | No | No | - |

**Indexes:**

- sqlite_autoindex_benchmark_metadata_1

### method_applicability

**Row Count:** 0

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | TEXT | Yes | Yes | - |
| `method_id` | TEXT | No | No | - |
| `problem_type` | TEXT | No | No | - |
| `system_size_min` | INTEGER | Yes | No | - |
| `system_size_max` | INTEGER | Yes | No | - |
| `accuracy_expected` | TEXT | Yes | No | - |
| `computational_scaling` | TEXT | Yes | No | - |
| `memory_scaling` | TEXT | Yes | No | - |
| `recommended` | BOOLEAN | Yes | No | - |
| `limitations` | TEXT | Yes | No | - |
| `best_practices` | TEXT | Yes | No | - |
| `json` | TEXT | No | No | - |

**Indexes:**

- sqlite_autoindex_method_applicability_1

### cross_references

**Row Count:** 0

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | TEXT | Yes | Yes | - |
| `source_id` | TEXT | No | No | - |
| `source_type` | TEXT | No | No | - |
| `target_id` | TEXT | No | No | - |
| `target_type` | TEXT | No | No | - |
| `relationship_type` | TEXT | No | No | - |
| `strength` | REAL | Yes | No | - |
| `bidirectional` | BOOLEAN | Yes | No | - |
| `notes` | TEXT | Yes | No | - |
| `json` | TEXT | No | No | - |

**Indexes:**

- idx_cross_ref_target
- idx_cross_ref_source
- sqlite_autoindex_cross_references_1

### validation_results

**Row Count:** 0

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | TEXT | Yes | Yes | - |
| `method_id` | TEXT | No | No | - |
| `benchmark_id` | TEXT | No | No | - |
| `validation_date` | TEXT | Yes | No | - |
| `mae` | REAL | Yes | No | - |
| `rmse` | REAL | Yes | No | - |
| `max_error` | REAL | Yes | No | - |
| `r2_score` | REAL | Yes | No | - |
| `num_outliers` | INTEGER | Yes | No | - |
| `pass_rate` | REAL | Yes | No | - |
| `validator` | TEXT | Yes | No | - |
| `validation_notes` | TEXT | Yes | No | - |
| `json` | TEXT | No | No | - |

**Indexes:**

- idx_validation_method
- sqlite_autoindex_validation_results_1
