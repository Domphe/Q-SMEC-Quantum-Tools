# EEG Brain Signal Sensors — BASELINE Technical Specifications

Purpose: Define an implementation-ready baseline for EEG brain signal sensing hardware, firmware, and validation. This specification focuses strictly on classical electrical sensing requirements (no market, business, or quantum topics) and aligns with the bands: Delta (0.5–4 Hz), Theta (4–8 Hz), Alpha (8–13 Hz), Beta (13–30 Hz), Gamma (30–100 Hz).

## 1. Scope & Target Signals

- Delta (δ): 0.5–4 Hz (deep sleep, healing)
- Theta (θ): 4–8 Hz (light sleep, meditation)
- Alpha (α): 8–13 Hz (relaxation, eyes-closed)
- Beta (β): 13–30 Hz (active cognition, stress elevation)
- Gamma (γ): 30–100 Hz (peak cognition; up to 100 Hz for baseline; optional research to 150 Hz)
- Typical scalp amplitude: 0.5–100 µV (EEG ~100× smaller than ECG)

## 2. Performance Requirements (Per Channel)

- Input-referred noise: ≤ 1 µV RMS (0.5–100 Hz), preferred ≤ 0.5 µV RMS
- CMRR: ≥ 100 dB at 50/60 Hz (≥ 110 dB preferred)
- Input impedance: ≥ 1 GΩ (dry electrodes), ≥ 100 MΩ minimum
- Gain: Programmable, total 40–60 dB (100–1000×), low-noise
- ADC resolution: ≥ 16 bits (preferred 24 bits for research/alpha/gamma fidelity)
- Sampling rate: 500 Hz standard; 1000 Hz optional for precise gamma/EMG discrimination
- Dynamic range: ≥ 90 dB
- Anti-alias margin: Low-pass cutoff ≤ 100 Hz (baseline) / ≤ 150 Hz (research) with ≥ 3× oversampling
- Electrode impedance tolerance: ≤ 50 kΩ (dry) stable capture; ≤ 5 kΩ (wet)
- Power per channel (AFE+ADC): ≤ 2 mW; full node (MCU+BLE avg.): ≤ 15 mW

## 3. Analog Front-End (AFE)

- Input protection: ±300 mV continuous; ESD/EMC protection per IEC 60601-1-2 guidance
- Bias current: ≤ 100 pA
- High-pass filter: 0.5 Hz (baseline EEG); optional 0.1 Hz for slow-drift studies
- Low-pass filter: 100 Hz (baseline); optional 150 Hz (research)
- Notch filter: 50/60 Hz selectable ±1 Hz tolerance
- Reference: Driven-right-leg or equivalent active reference for common-mode suppression
- Lead-off detection: AC or DC method, threshold configurable (e.g., > 100 kΩ)
- Channel coupling: Differential inputs per electrode pair; shielded leads

## 4. Digital Signal Processing (On-Device)

- Artifact rejection primitives: Blink (EOG), jaw/forehead EMG, motion; accelerometer-assisted adaptive filtering (LMS/RLS)
- Bandpass profiles: Delta, Theta, Alpha, Beta, Gamma bandpass sets with stable passband ripple (≤ ±0.5 dB)
- Alpha detection routine: Eyes-closed alpha power rise ≥ 20% vs. eyes-open baseline
- Beta stress indicator: Beta power elevation ≥ 15% vs. relaxed baseline
- Epoching: 1–2 s epochs with 50% overlap; windowing (Hann/Hamming)
- Power spectral density (PSD): Welch method with ≥ 4 segments; frequency resolution ≤ 0.5 Hz
- Event flags: Drowsiness (theta↑), stress (beta↑, alpha↓), engagement (gamma↑) — configurable thresholds

## 5. Frequency-Domain Requirements

- Delta (0.5–4 Hz): Preserve low-frequency content; HPF ≤ 0.5 Hz (optional 0.1 Hz studies)
- Theta (4–8 Hz): Passband flatness ±0.5 dB; sufficient resolution to track meditation changes
- Alpha (8–13 Hz): Maintain passband flatness ±0.5 dB; detect alpha blocking (eyes-open α↓ ≥ 20%)
- Beta (13–30 Hz): SNR ≥ 10 dB; EMG discrimination via spectral slope/wavelet features
- Gamma (30–100 Hz): SNR ≥ 6 dB (baseline wearable); avoid false EMG classification using coherence and spatial features

## 6. Electrode Systems & Placement

- Systems: 10–20 standard (Fp1/Fp2, F3/F4, C3/C4, P3/P4, O1/O2, T3/T4, Cz, Pz, Oz); reduced set headband (Fpz, Fz, Cz, Pz, Oz)
- Electrode types:
  - Wet (Ag/AgCl): impedance 1–5 kΩ; clinical baselines and short sessions
  - Dry (polymer/carbon/metalized fabric/microneedle): impedance 10–100 kΩ; long-term wear
  - Capacitive (through hair/band): impedance MΩ range; experimental
- Contact area: 50–200 mm² (dry); 20–50 mm² (wet)
- Mechanical: Spring-loaded pins or flexible substrate to maintain contact under movement

## 7. Wireless & Data

- BLE 5.x preferred; throughput ≥ 8 kbps per channel (500 Hz×16 bits)
- Latency: ≤ 200 ms for real-time alpha/beta/engagement flags
- Buffering: ≥ 30 s circular buffer for dropouts
- Timestamping: Monotonic clock; optional PTP/GPS sync for multi-node studies
- File formats: EDF+, BrainVision, or JSON/CSV with clear schema; include calibration metadata

## 8. Firmware Interfaces

- Command set:
  - Start/stop stream; set sampling rate (250/500/1000 Hz)
  - Filter profiles: Delta/Theta/Alpha/Beta/Gamma; Notch 50/60 Hz toggle
  - Gain profiles: Low/Med/High
  - Epoch duration/window type
  - Event/query: Last N events JSON
- Diagnostics:
  - Lead-off status, impedance estimate
  - Battery level, temperature
  - Self-test: Noise floor and CMRR quick check

## 9. Calibration & Self-Test

- Noise floor test: Shorted input; ≤ 1 µV RMS
- CMRR test: Inject 50/60 Hz common-mode; verify ≥ 100 dB
- Gain linearity: ±50 µV sine at 10 Hz/α band; error ≤ ±2%
- Impedance check: AC probe (e.g., 31.25 Hz, 10 nA); infer 5 kΩ–100 kΩ
- Notch efficacy: Residual 50/60 Hz ≤ −30 dB vs. baseline

## 10. Validation & Acceptance Criteria

- Alpha reactivity (eyes-closed vs. eyes-open at O1/O2/Pz): α power increase ≥ 20% (p < 0.05 across 10 subjects)
- Beta stress response (cognitive load task at F3/F4/Cz): β power increase ≥ 15% vs. relaxed baseline
- Theta meditation response (guided meditation at Fz/Pz): θ power increase ≥ 10%
- Band power reproducibility: CoV ≤ 10% across repeated sessions (same subject, same protocol)
- Motion robustness: Maintain α detection with head movements < 30°/s; false EMG classification rate < 5%
- Spectral accuracy: PSD peak frequency error ≤ ±0.5 Hz in α/β bands with synthetic test signals

## 11. Environmental & Safety

- Operating temp: 0–45 °C; humidity: 10–95% non-condensing
- Skin contact materials: ISO 10993 biocompatibility passed
- EMC: IEC 60601-1-2 pre-compliance design targets
- Electrical safety: Leakage currents per IEC 60601-1 (system-level)

## 12. Reference ICs (Examples)

- AFE: ADS1299 (EEG-grade), ADAS1000, INA-based low-noise front-ends
- MCU: nRF52 (BLE SoC), STM32L4 (low-power), RP2040 (cost-effective)
- Power: Low-noise LDOs; battery monitor

## 13. Test Datasets & Benchmarks

- PhysioNet EEG Databases (alpha, sleep datasets)
- Individual alpha frequency tests (eyes-open/closed)
- Synthetic EEG signals (band-limited noise + sinusoids) for PSD accuracy

## 14. Deliverables (Engineering)

- Schematics + PCB layout (Gerbers, BoM)
- Firmware (AFE config, DSP, BLE)
- Validation report (α/β/θ reactivity, spectral accuracy)
- User guide (electrode placement, protocols)
- Data interface spec (payloads, metadata)

## 15. Change Control

- Versioning: MAJOR.MINOR.PATCH (e.g., 1.0.0)
- Baseline freeze upon passing acceptance; changes via ECO with regression tests

---

This baseline aligns strictly with the specified EEG bands and sets measurable acceptance criteria to qualify an EEG sensor stack for production and clinical evaluation readiness (pre-compliance level).
