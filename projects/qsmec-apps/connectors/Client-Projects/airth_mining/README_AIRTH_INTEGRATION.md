# AIRTH Mining Sensor Integration — Quick Start

This guide shows how to use the AIRTH sensor template generator, integration notebook, and VS Code tasks.

---

## Overview

**AIRTH** (Arizona Integrated Real-Time High-resolution monitoring) is the Q-SMEC mining sensor platform integration:

- **Generator script**: `scripts/airth_create_excel_templates.py` produces `AIRTH_SENSOR_TEMPLATE.xlsx` with:
  - `DataSchema`: Column definitions (timestamp, sensor_id, reading_type, value, etc.)
  - `SampleData`: Synthetic sensor readings (THz RCS, EM Field, Vibration, Thermal)
  - `KPIs`: Basic metrics (avg signal, uptime, type counts)
  - `Assumptions`: Domain thresholds (warn/alarm levels, coefficients)
  - `DomainKPIs`: Advanced metrics (per-sensor uptime, threshold exceedances, low battery/signal counts)

- **Integration notebook**: `AIRTH_Mining_Sensor_Integration.ipynb` loads the template, performs preprocessing, recomputes KPIs, visualizes data, and exports analytics (HTML charts + Excel report).

---

## Quick Start (VS Code Tasks)

### 1. Generate AIRTH Workbook
**Task**: `Generate AIRTH Workbook` (Terminal → Run Task…)

What it does:
- Activates `.venv_qsmec`
- Runs `airth_create_excel_templates.py -n 400` (400 sample rows)
- Output: `Q-SMEC_Development_Environment/airth_mining/AIRTH_SENSOR_TEMPLATE.xlsx`

**Manual command** (PowerShell):
```powershell
& "g:\My Drive\Powershell_Python Scripts\environment\activation\activate-qsmec-env.ps1" -Silent
python "g:\My Drive\scripts\airth_create_excel_templates.py" -n 400
```

### 2. Run AIRTH Analytics (Headless Notebook Execution)
**Task**: `Run AIRTH Analytics (nbconvert)` (Terminal → Run Task…)

What it does:
- Activates `.venv_qsmec`
- Executes the notebook via `jupyter nbconvert --execute`
- Outputs:
  - Executed notebook: `exports/AIRTH_Mining_Sensor_Integration.out.ipynb`
  - HTML charts: `exports/*.html` (spatial_distribution, value_distributions, battery_vs_signal)
  - Analytics report: `exports/AIRTH_ANALYTICS_REPORT.xlsx`

**Manual command** (PowerShell):
```powershell
& "g:\My Drive\Powershell_Python Scripts\environment\activation\activate-qsmec-env.ps1" -Silent
python -m jupyter nbconvert --to notebook --execute `
  "g:\My Drive\Q-SMEC_Development_Environment\airth_mining\AIRTH_Mining_Sensor_Integration.ipynb" `
  --output "AIRTH_Mining_Sensor_Integration.out.ipynb" `
  --output-dir "g:\My Drive\Q-SMEC_Development_Environment\airth_mining\exports" `
  --ExecutePreprocessor.timeout=600
```

---

## Manual Workflow (Interactive Notebook)

### 1. Generate the Excel template
```powershell
& "g:\My Drive\Powershell_Python Scripts\environment\activation\activate-qsmec-env.ps1" -Silent
python "g:\My Drive\scripts\airth_create_excel_templates.py" -n 300
```

### 2. Open the notebook in Jupyter
```powershell
& "g:\My Drive\Powershell_Python Scripts\environment\activation\activate-qsmec-env.ps1" -Silent
jupyter lab "g:\My Drive\Q-SMEC_Development_Environment\airth_mining\AIRTH_Mining_Sensor_Integration.ipynb"
```

Or use VS Code's Jupyter extension:
- Open `AIRTH_Mining_Sensor_Integration.ipynb`
- Select kernel: `.venv_qsmec` (Python 3.12)
- Run all cells (Ctrl+Shift+Alt+Enter)

### 3. View outputs
- Charts: `Q-SMEC_Development_Environment/airth_mining/exports/*.html`
- Report: `Q-SMEC_Development_Environment/airth_mining/exports/AIRTH_ANALYTICS_REPORT.xlsx`

---

## Generator Options

```powershell
python scripts/airth_create_excel_templates.py --help
```

Options:
- `--output` / `-o`: Custom output path or filename (default: `airth_mining/AIRTH_SENSOR_TEMPLATE.xlsx`)
- `--rows` / `-n`: Number of sample rows (default: 200)

Examples:
```powershell
# Generate 1000 rows
python scripts/airth_create_excel_templates.py -n 1000

# Custom output
python scripts/airth_create_excel_templates.py -o "my_custom_template.xlsx" -n 500
```

---

## What's in the Notebook?

### Cells:
1. **Setup**: Load paths, imports
2. **Load Excel**: Read all sheets (`DataSchema`, `SampleData`, `KPIs`, `Assumptions`, `DomainKPIs`)
3. **Preprocessing**: Convert timestamps, coerce numerics, drop null values
4. **KPI Recompute**: Basic metrics (records, avg signal, uptime, etc.)
5. **Load Assumptions**: Load domain thresholds and coefficients
6. **Domain KPIs**: Compute per-sensor uptime, threshold exceedances, battery/signal health
7. **Visualizations**: Time series, distributions, battery vs signal scatter
8. **Anomaly Detection**: Z-score per sensor+type (outliers flagged)
9. **Enhanced Visuals + Export**: Geo scatter (lat/lon), per-type distributions, battery vs signal with trendline → HTML/PNG exports
10. **Export Analytics Report**: Save KPIs and domain KPIs to `AIRTH_ANALYTICS_REPORT.xlsx`

---

## Outputs

### Generated Files
- `AIRTH_SENSOR_TEMPLATE.xlsx`: Input template with 5 sheets (schema, data, KPIs, assumptions, domain KPIs)
- `exports/AIRTH_Mining_Sensor_Integration.out.ipynb`: Executed notebook (when using nbconvert)
- `exports/AIRTH_ANALYTICS_REPORT.xlsx`: KPI summary (recomputed + domain)
- `exports/*.html`: Interactive Plotly charts (spatial, distributions, battery vs signal)
- `exports/*.png`: Static images (requires `kaleido` package; optional)

### Install `kaleido` for PNG exports (optional)
```powershell
& "g:\My Drive\.venv_qsmec\Scripts\Activate.ps1"
pip install -U kaleido
```

---

## Domain Assumptions (Default Thresholds)

| Parameter                | Value | Description                        |
|--------------------------|-------|------------------------------------|
| `thz_rcs_warn_dbsm`      | -15   | THz RCS warning (dBsm)             |
| `thz_rcs_alarm_dbsm`     | -10   | THz RCS alarm (dBsm)               |
| `em_field_warn_mVpm`     | 80    | EM field warning (mV/m)            |
| `em_field_alarm_mVpm`    | 100   | EM field alarm (mV/m)              |
| `vibration_warn_mms`     | 4.0   | Vibration warning (mm/s)           |
| `vibration_alarm_mms`    | 6.0   | Vibration alarm (mm/s)             |
| `thermal_warn_c`         | 40.0  | Thermal warning (°C)               |
| `thermal_alarm_c`        | 45.0  | Thermal alarm (°C)                 |
| `battery_warn_pct`       | 40.0  | Battery warning (%)                |
| `signal_warn_db`         | -85.0 | Signal strength warning (dB)       |
| `depth_norm_ref_m`       | 50.0  | Reference depth for normalization  |
| `thz_temp_coeff_db_per_c`| -0.02 | Temp compensation coeff (dB/°C)    |

These are loaded from the `Assumptions` sheet and used to compute `DomainKPIs`.

---

## Next Steps

- **Customize thresholds**: Edit `Assumptions` sheet in the Excel template or update the `build_assumptions()` function in `airth_create_excel_templates.py`.
- **Add real data**: Replace `SampleData` with actual sensor readings (preserve schema).
- **Integrate with Q-SMEC workflows**: Import AIRTH data into AI+Quantum pipelines (feature extraction, optimization, anomaly detection via VQE/QAOA).
- **Automate**: Schedule the `Generate AIRTH Workbook` and `Run AIRTH Analytics` tasks via Windows Task Scheduler or Prefect flows.

---

## Troubleshooting

### "Module not found" errors
Ensure `.venv_qsmec` is activated and packages installed:
```powershell
& "g:\My Drive\.venv_qsmec\Scripts\Activate.ps1"
pip install -r requirements_qsmec.txt
```

### Notebook execution timeout
Increase timeout in the task command or manual invocation:
```powershell
--ExecutePreprocessor.timeout=1200
```

### Charts not displaying in VS Code
- HTML charts open best in a browser: `exports/*.html`
- Or use Jupyter Lab: `jupyter lab` (better interactive support)

### "No such file" errors
Verify paths in the notebook setup cell:
```python
WORKSPACE_ROOT = os.getenv('WORKSPACE_ROOT') or str(Path.cwd())
AIRTH_DIR = Path(WORKSPACE_ROOT) / 'Q-SMEC_Development_Environment' / 'airth_mining'
```

---

## Summary

**Quick workflow**:
1. Run task: `Generate AIRTH Workbook` → creates `AIRTH_SENSOR_TEMPLATE.xlsx`
2. Run task: `Run AIRTH Analytics (nbconvert)` → executes notebook, produces charts + report
3. View outputs: `Q-SMEC_Development_Environment/airth_mining/exports/`

**Interactive workflow**:
1. Generate template (command or task)
2. Open notebook in Jupyter or VS Code
3. Run cells; explore visualizations; tweak analyses

**Customization**:
- Edit `build_assumptions()` or Excel `Assumptions` sheet for domain rules
- Modify notebook cells to add features (ML models, quantum optimization, real-time dashboards)

---

Happy mining! 🚀
