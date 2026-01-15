# AIRTH Mining Sensor Integration — Quick Start

## Overview
The AIRTH system provides sensor data templates, domain-specific KPIs, and analytics workflows for mining sensor deployments (THz RCS, EM Field, Vibration, Thermal).

## Files
- **Excel Template**: `AIRTH_SENSOR_TEMPLATE.xlsx`
  - `DataSchema`: Column definitions
  - `SampleData`: 400 simulated sensor readings
  - `KPIs`: Basic metrics (counts, averages)
  - `Assumptions`: Domain thresholds (warn/alarm levels)
  - `DomainKPIs`: Uptime, threshold exceedances, signal/battery health

- **Notebook**: `AIRTH_Mining_Sensor_Integration.ipynb`
  - Loads all sheets
  - Preprocesses data (datetime, numeric coercion)
  - Recomputes KPIs using assumptions
  - Generates visualizations (spatial, distributions, battery vs signal)
  - Detects anomalies (z-score per sensor+type)
  - Exports HTML/PNG charts and `AIRTH_ANALYTICS_REPORT.xlsx` to `exports/`

- **Generator Script**: `g:\My Drive\scripts\airth_create_excel_templates.py`

## Quick Usage

### 1. Regenerate Excel Template
Use the VS Code task or run manually:

**Via Task**:
- Press `Ctrl+Shift+P` → `Tasks: Run Task` → `Generate AIRTH Workbook`

**Via Terminal**:
```powershell
& "g:\My Drive\Powershell_Python Scripts\environment\activation\activate-qsmec-env.ps1" -Silent
python "g:\My Drive\scripts\airth_create_excel_templates.py" -n 500
```

Options:
- `-n 500`: Generate 500 rows (default 200)
- `-o custom_name.xlsx`: Custom output filename

### 2. Run Analytics (Headless)
Execute the notebook and generate exports without opening Jupyter:

**Via Task**:
- Press `Ctrl+Shift+P` → `Tasks: Run Task` → `Run AIRTH Analytics (Headless)`

**Via Terminal**:
```powershell
& "g:\My Drive\Powershell_Python Scripts\environment\activation\activate-qsmec-env.ps1" -Silent
jupyter nbconvert --to notebook --execute --inplace "Q-SMEC_Development_Environment/airth_mining/AIRTH_Mining_Sensor_Integration.ipynb"
```

Outputs appear in `Q-SMEC_Development_Environment/airth_mining/exports/`:
- `spatial_distribution.html` (interactive geo plot)
- `value_distributions.html` (per-type histograms)
- `battery_vs_signal.html` (scatter with trendline)
- `AIRTH_ANALYTICS_REPORT.xlsx` (KPIs + domain metrics)

### 3. Interactive Notebook
Open and run cells manually:

**Via JupyterLab**:
```powershell
& "g:\My Drive\Powershell_Python Scripts\environment\activation\activate-qsmec-env.ps1" -AutoStart
```
Then navigate to: `Q-SMEC_Development_Environment/airth_mining/AIRTH_Mining_Sensor_Integration.ipynb`

**Via VS Code**:
- Open `AIRTH_Mining_Sensor_Integration.ipynb`
- Select kernel: `.venv_qsmec`
- Run all cells (`Ctrl+Shift+Enter`)

## Domain KPIs Explained
- **Uptime per sensor**: % of "OK" status readings
- **Threshold exceedances**: Warn/alarm counts per reading type (THz RCS, EM Field, Vibration, Thermal)
- **Low battery count**: Sensors below `battery_warn_pct` (default 40%)
- **Weak signal count**: Readings below `signal_warn_db` (default -85 dB)
- **Depth normalization**: THz RCS adjusted for depth variance

Adjust thresholds by editing the `Assumptions` sheet or modifying `scripts/airth_create_excel_templates.py` → `build_assumptions()`.

## Customization
1. **Add sensors/sites**: Edit `generate_sample_data()` lists (`sensors`, `sites`, `ore_types`)
2. **New reading types**: Add to `reading_types` list and update threshold logic
3. **Custom KPIs**: Extend `compute_domain_kpis()` in script or notebook
4. **Visualizations**: Add Plotly figures in notebook cells; auto-export to `exports/`

## Troubleshooting
- **Missing dependencies**: Activate `.venv_qsmec` first
- **Trendline errors**: Install `statsmodels` (`pip install statsmodels`) or remove `trendline='ols'` from scatter plots
- **PNG export fails**: Install `kaleido` (`pip install kaleido`) for static image export (HTML always works)

## Next Steps
- Integrate with real sensor APIs/data pipelines
- Map to NIKET proposal milestones (deployment phases, site-specific KPIs)
- Connect to AI+Quantum workflows (anomaly detection via VQE, optimization via QAOA)
