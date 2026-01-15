# Validation Checklist — EEG & ECG Sensor Baselines

Purpose: Provide a detailed, actionable validation plan and acceptance criteria for both EEG and ECG baseline sensor stacks. Use this as a pre-compliance verification prior to formal IEC 60601 certification.

## 1. Bench Electrical Tests

- Noise Floor (EEG):
  - Setup: Short input; shielded environment
  - Metric: ≤ 1 µV RMS (0.5–100 Hz), preferred ≤ 0.5 µV
  - Procedure: 60 s recording; RMS over band; repeat ×3; report mean ± SD
  - Acceptance: PASS if mean ≤ 1 µV

- Noise Floor (ECG):
  - Setup: Short input; shielded environment
  - Metric: ≤ 5 µV RMS (0.05–150 Hz)
  - Procedure: 60 s recording; RMS over band; repeat ×3
  - Acceptance: PASS if mean ≤ 5 µV

- CMRR (EEG/ECG):
  - Setup: Inject 50/60 Hz common-mode; DRL active
  - Metric: ≥ 100 dB (≥ 110 dB preferred)
  - Procedure: Sweep ±50–200 mV common-mode; compute attenuation
  - Acceptance: PASS if ≥ 100 dB

- Gain Linearity:
  - EEG: ±50 µV sine at 10 Hz; error ≤ ±2%
  - ECG: ±1 mV sine at 10 Hz; error ≤ ±1%
  - Procedure: 10 cycles; compare measured amplitude to input
  - Acceptance: PASS if errors within limits

- Notch Filter Efficacy:
  - Metric: Residual 50/60 Hz ≤ −30 dB vs. baseline
  - Procedure: Apply 50/60 Hz interference; measure post-filter amplitude
  - Acceptance: PASS

## 2. Electrode Impedance & Lead-Off

- Impedance Estimation:
  - EEG dry: 10–100 kΩ; wet: 1–5 kΩ
  - ECG dry: 10–50 kΩ; wet: 1–5 kΩ
  - Procedure: AC probe (e.g., 31.25 Hz, 10 nA); compute Z
  - Acceptance: PASS if within expected ranges and reported consistently

- Lead-Off Detection:
  - Procedure: Lift electrode contact deliberately; verify firmware flag within 2 s
  - Acceptance: PASS if detected reliably across channels

## 3. Protocol-Based Physiological Validation (EEG)

- Alpha Reactivity (Eyes-Open/Closed):
  - Electrode sites: O1/O2/Pz
  - Protocol: 3×(eyes-open 60 s → eyes-closed 60 s)
  - Metric: α power rise ≥ 20% during eyes-closed vs. open
  - Analysis: Welch PSD, 8–13 Hz band power; subject-level statistics
  - Acceptance: PASS if ≥ 20% increase for ≥ 8/10 subjects

- Theta Meditation Response:
  - Sites: Fz/Pz
  - Protocol: 10-min guided meditation vs. 10-min quiet rest
  - Metric: θ power increase ≥ 10%
  - Acceptance: PASS if subject median ≥ 10%

- Beta Stress Indicator (Cognitive Load):
  - Sites: F3/F4/Cz
  - Protocol: 10-min baseline vs. 10-min N-back task
  - Metric: β power increase ≥ 15%
  - Acceptance: PASS if group mean ≥ 15%

## 4. Protocol-Based Physiological Validation (ECG)

- Rest HR Accuracy:
  - Protocol: 10-min seated rest vs. clinical reference ECG
  - Metric: Beat detection sensitivity ≥ 99%
  - Acceptance: PASS

- Sleep HR Tracking:
  - Protocol: Overnight study with polysomnography reference
  - Metric: Mean HR error ≤ ±1 BPM; REM band fidelity (0.6–0.85 Hz)
  - Acceptance: PASS

- HRV Metrics Repeatability:
  - Metrics: SDNN, RMSSD, pNN50
  - Protocol: 3×5-min recordings/day × 3 days
  - Acceptance: CoV ≤ 5% intra-subject

- VLF Preservation:
  - Protocol: 10-min controlled breathing/rest
  - Metric: PSD error ≤ ±10% in 0.04–0.15 Hz band vs. DC-coupled reference
  - Acceptance: PASS

- HF QRS Feature Capture:
  - Protocol: Curated datasets (ventricular late potentials)
  - Metric: Sensitivity ≥ 85%, specificity ≥ 90%
  - Acceptance: PASS

## 5. Artifact Robustness

- Motion:
  - EEG: Head movement < 30°/s; maintain α detection; false EMG classification < 5%
  - ECG: Walking at 3 km/h; maintain HR tracking; dropouts < 1%

- EMG (Muscle):
  - EEG: Jaw clench; classifier should isolate EMG vs. β; maintain SNR thresholds
  - ECG: Arm movement; filter should limit false beats

- Power-Line & EMI:
  - 50/60 Hz rejection validated; radiated immunity spot-check

## 6. Wireless & Power

- BLE Throughput:
  - EEG/ECG: ≥ 8 kbps/channel sustained; packet loss < 0.1%

- Battery Life:
  - ECG patch: 7–14 days target (duty-cycled BLE)
  - EEG headband: 8–12 hours continuous

- Thermal:
  - Skin-contact temperature rise ≤ 2 °C over ambient

## 7. Data Integrity & Schema

- File Formats:
  - EDF+/CSV/JSON clearly documented; include sampling rate, gains, filter profiles, impedance, timestamps

- Time Sync:
  - Monotonic clock drift ≤ 50 ppm; optional PTP/GPS sync validated to ≤ 1 ms alignment

## 8. Reporting & Acceptance

- Validation Report must include:
  - Test setups (photos, schematics), parameters, raw data snippets
  - Metrics tables (mean, SD, CoV, confidence intervals)
  - PASS/FAIL per criterion with justifications

- Acceptance Decision:
  - Baseline is "ACCEPTED" when all mandatory criteria pass; exceptions documented with mitigations

---

This checklist is designed to be executed iteratively during engineering sprints to ensure sensor stack quality prior to formal certification steps.
