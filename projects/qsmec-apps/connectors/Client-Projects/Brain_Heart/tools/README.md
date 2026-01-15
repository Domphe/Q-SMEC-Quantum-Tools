# Brain_Heart Tools: Validation & Analysis Harnesses

## Overview

Python harnesses for synthetic EEG/ECG signal generation, peak detection, and HRV/band-power analysis. Designed for baseline validation and detector tuning.

## Tools

### 1. HRV Test Harness (`hrv_test.py`)

**Purpose:** Generate synthetic ECG, detect R-peaks, and compute heart rate variability (HRV) metrics.

**Key features:**
- Synthetic ECG generation with configurable heart rate and noise.
- Pan-Tompkins-like R-peak detection with tunable sensitivity.
- Time-domain HRV: SDNN (standard deviation NN), RMSSD, pNN50.
- Frequency-domain HRV: LF (0.04–0.15 Hz), HF (0.15–0.40 Hz), LF/HF ratio.
- CSV input support (real ECG data).
- CSV output for RR intervals and validation metrics.

**Usage:**

```bash
# Synthetic ECG (default: 60 sec, HR=60 bpm, Fs=500 Hz)
python hrv_test.py --mode synthetic

# Synthetic with custom parameters
python hrv_test.py --mode synthetic --duration 120 --hr 75 --threshold 0.25 --output results_hrv.csv

# CSV input (e.g., real ECG data)
python hrv_test.py --mode csv --csv path/to/ecg.csv --fs 500 --output results_hrv.csv

# Peak detection tuning (lower threshold = more peaks)
python hrv_test.py --mode synthetic --threshold 0.2  # Sensitive
python hrv_test.py --mode synthetic --threshold 0.4  # Specific
```

**Parameters:**
- `--mode`: 'synthetic' or 'csv'
- `--duration`: Recording duration (seconds)
- `--fs`: Sampling rate (Hz)
- `--hr`: Target heart rate for synthetic (bpm)
- `--threshold`: Peak detection threshold (0.1–0.5; default 0.3)
- `--refractory`: Refractory period (ms; default 200)
- `--csv`: Path to CSV input (required for CSV mode)
- `--output`: Output CSV filename for validation

**Output:** JSON to stdout (synthetic mode) or CSV results (if `--output` provided).

**Baseline criteria:**
- **HR:** 40–180 bpm (wide normal range for testing)
- **SDNN:** 50–400 ms (HRV magnitude)
- **RMSSD:** 20–200 ms (short-term variability)
- **pNN50:** 0–100% (proportion of RR > 50 ms)
- **LF/HF:** 1–3 (sympathovagal balance; stress state)

---

### 2. EEG Band-Power Harness (`eeg_band_power_test.py`)

**Purpose:** Generate synthetic multi-channel EEG, compute spectral power in canonical bands, and assess inter-channel coherence.

**Key features:**
- Synthetic multi-channel EEG with band emphasis (Delta, Theta, Alpha, Beta, Gamma).
- Welch power spectral density (PSD) analysis.
- Relative (normalized) band power per channel.
- Inter-channel coherence (spatial connectivity) analysis.
- Baseline validation against EEG specs.
- CSV output for per-channel band power.

**Usage:**

```bash
# Default: 60 sec, 8 channels, Alpha emphasis, 256 Hz sampling
python eeg_band_power_test.py --mode synthetic

# Theta emphasis, 16 channels, 120 seconds
python eeg_band_power_test.py --mode synthetic --duration 120 --channels 16 --emphasis theta

# Mixed bands, high SNR
python eeg_band_power_test.py --mode synthetic --emphasis mixed --snr 30

# Output CSV for per-channel band power
python eeg_band_power_test.py --mode synthetic --emphasis alpha --output band_power.csv
```

**Parameters:**
- `--mode`: 'synthetic' (only mode currently)
- `--duration`: Recording duration (seconds; default 60)
- `--channels`: Number of EEG channels (default 8)
- `--fs`: Sampling rate (Hz; default 256)
- `--emphasis`: Emphasized band ('delta', 'theta', 'alpha', 'beta', 'gamma', 'mixed')
- `--snr`: Signal-to-noise ratio (dB; default 20)
- `--output`: Output CSV filename for per-channel band power

**Output:** JSON to stdout with band power summaries, coherence, and baseline validation results.

**Baseline criteria (relative power, normalized):**
- **Band total:** 0.95–1.05 (normalized to 1.0)
- **Typical distribution (at rest, eyes closed):**
  - Delta: 0.05–0.15
  - Theta: 0.05–0.10
  - Alpha: 0.20–0.35 (highest at rest)
  - Beta: 0.10–0.25
  - Gamma: 0.02–0.10
- **Coherence (alpha, inter-channel):** 0.3–0.7 (spatial organization)

---

## Requirements

- Python 3.7+
- `numpy` (signal generation, analysis)
- `scipy` (Welch PSD, filtering)

**Installation:**

```bash
pip install -r requirements.txt
```

Contents of `requirements.txt`:
```
numpy>=1.26.0
scipy>=1.11.0
```

---

## Validation Workflow

1. **Generate synthetic data** with known parameters (HR, band emphasis).
2. **Run detector** (peak detection, band power).
3. **Compare output** to ground truth (expected HR, expected band power).
4. **Tune parameters** (threshold, refractory, SNR) for robustness.
5. **Validate against baseline** specs (EEG/ECG technical specifications documents).
6. **Export CSV** for downstream analysis or clinical integration.

---

## Examples

### Example 1: HR validation (target 75 bpm)

```bash
python hrv_test.py --mode synthetic --duration 60 --hr 75 --output hrv_75bpm.csv
```

Expected output:
- `beats_detected`: ~75 (may vary; refractory period affects count)
- `mean_hr_bpm`: ~75 ± 10%
- `SDNN`: 50–150 ms (synthetic may be lower)

### Example 2: Alpha band validation

```bash
python eeg_band_power_test.py --mode synthetic --duration 120 --channels 16 --emphasis alpha --output eeg_alpha.csv
```

Expected output:
- `alpha_mean`: ~0.30–0.40 (relative power)
- `total_power_valid`: True (sum of bands ≈ 1.0)
- `mean_coherence_alpha`: 0.4–0.6 (inter-channel synchrony)

### Example 3: CSV ECG validation (real data)

```bash
python hrv_test.py --mode csv --csv patient_ecg.csv --fs 500 --threshold 0.25 --output patient_hrv.csv
```

Output CSV (`patient_hrv.csv`):
```
rr_interval_ms,beat_number
800,1
810,2
795,3
...
metric,value
mean_hr_bpm,75.3
SDNN_ms,120.5
...
```

---

## Notes & Constraints

- **Synthetic signals:** Simplified; real ECG/EEG more complex (motion, artifacts, non-stationarity).
- **Peak detection:** Tuning threshold/refractory is essential for real data; consider external validation (gold standard).
- **Band power:** Welch PSD assumes quasi-stationary signals; use shorter windows for non-stationary data.
- **Coherence:** Simplified correlation-based; advanced metrics (imaginary coherence, phase-locking value) available in MNE-Python or other toolkits.

---

## Future Extensions

- Support for real ECG/EEG files (WFDB, BDF, EDF formats).
- Advanced peak detection algorithms (e.g., template matching, machine learning).
- Adaptive band definitions (personalized frequency ranges).
- Advanced connectivity metrics (phase-amplitude coupling, directed coherence).
- Integration with cloud FHIR servers for real-time validation.
