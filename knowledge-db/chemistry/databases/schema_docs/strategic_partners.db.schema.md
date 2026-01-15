# Database Schema Documentation

**Database Path:** `strategic_partners.db`
**Generated:** 2026-01-08T22:30:49.883735
**Total Tables:** 6

## Table of Contents

- [companies](#companies)
- [technologies](#technologies)
- [cordis_grants](#cordis_grants)
- [us_grants](#us_grants)
- [export_classifications](#export_classifications)
- [partners](#partners)

## Tables

### companies

**Row Count:** 3

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | INTEGER | Yes | Yes | - |
| `name` | TEXT | No | No | - |
| `website` | TEXT | Yes | No | - |
| `location` | TEXT | Yes | No | - |
| `expertise` | TEXT | Yes | No | - |
| `relevance` | TEXT | Yes | No | - |

### technologies

**Row Count:** 2

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | INTEGER | Yes | Yes | - |
| `name` | TEXT | No | No | - |
| `description` | TEXT | Yes | No | - |
| `applications` | TEXT | Yes | No | - |
| `challenges_and_market` | TEXT | Yes | No | - |
| `synergy_and_players` | TEXT | Yes | No | - |

### cordis_grants

**Row Count:** 1

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | INTEGER | Yes | Yes | - |
| `program_id` | INTEGER | Yes | No | - |
| `query` | TEXT | Yes | No | - |
| `url` | TEXT | Yes | No | - |
| `notes` | TEXT | Yes | No | - |

### us_grants

**Row Count:** 1

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | INTEGER | Yes | Yes | - |
| `program_id` | INTEGER | Yes | No | - |
| `keyword` | TEXT | Yes | No | - |
| `url` | TEXT | Yes | No | - |
| `notes` | TEXT | Yes | No | - |

### export_classifications

**Row Count:** 3

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | INTEGER | Yes | Yes | - |
| `tech_id` | INTEGER | Yes | No | - |
| `regime` | TEXT | Yes | No | - |
| `category_code` | TEXT | Yes | No | - |
| `status` | TEXT | Yes | No | - |
| `notes` | TEXT | Yes | No | - |

### partners

**Row Count:** 10

**Columns:**

| Column | Type | Nullable | Primary Key | Default |
|--------|------|----------|-------------|---------|
| `id` | TEXT | Yes | Yes | - |
| `name` | TEXT | No | No | - |
| `sector` | TEXT | Yes | No | - |
| `partnership_type` | TEXT | Yes | No | - |
| `use_cases` | TEXT | Yes | No | - |
| `tam_billion` | REAL | Yes | No | - |
| `cagr_percent` | REAL | Yes | No | - |
| `nre_cost_k` | REAL | Yes | No | - |
| `trl_target` | TEXT | Yes | No | - |
| `status` | TEXT | Yes | No | - |
| `contact_info` | TEXT | Yes | No | - |
| `notes` | TEXT | Yes | No | - |
| `json` | TEXT | Yes | No | - |
| `created_at` | TEXT | Yes | No | - |
| `updated_at` | TEXT | Yes | No | - |

**Indexes:**

- sqlite_autoindex_partners_1
