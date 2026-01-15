# ECG Heart Signal Sensors — BASELINE Technical Specifications

Purpose: Define a concise, implementation-ready baseline for ECG heart signal sensing hardware, firmware, and validation. This specification excludes market, business, and quantum-sensing topics and focuses strictly on technical requirements for a classical electrical sensor stack.

## 1. Scope & Target Signals

- Resting heart rate: 1.0–1.7 Hz (60–102 BPM)
- Sleep (deep/REM) heart rate: 0.6–0.85 Hz (36–51 BPM)
- Valve/mayer-wave VLF components: 0.04–0.15 Hz
- QRS complex high-frequency content: 20–250 Hz (extendable to 500 Hz in research modes)
- Full diagnostic ECG bandwidth: 0.05–150 Hz (clinical standard), optional 0.05–250 Hz (HF QRS analysis)

## 2. Performance Requirements (Per Channel)

- Input-referred noise: ≤ 5 µV RMS over 0.05–150 Hz
- CMRR: ≥ 100 dB at 50/60 Hz
- Input impedance: ≥ 100 MΩ (dry electrode compatibility; ≥ 1 GΩ preferred)
- Gain: Programmable, total 40–60 dB (100–1000×)
- ADC resolution: ≥ 16 bits (preferred 24 bits for research)
- Sampling rate: 500 Hz standard; 1000 Hz for HF QRS mode
- Dynamic range: ≥ 90 dB
- Anti-alias margin: Low-pass cutoff ≤ 150 Hz (standard) / ≤ 250 Hz (HF mode) with ≥ 3× oversampling
- Amplitude capture: 0.1–5 mVpp (limb leads) and up to 10 mVpp (precordial leads)
- Electrode impedance tolerance: ≤ 50 kΩ (dry) with stable capture; ≤ 5 kΩ (wet)
- Power per channel (AFE+ADC): ≤ 2 mW; full node (MCU+BLE average): ≤ 15 mW

## 3. Analog Front-End (AFE)

- Input protection: ±300 mV continuous; defibrillation survivability via series resistors/TVS (system-level)
- Bias current: ≤ 100 pA
- High-pass filter: 0.05 Hz (diagnostic) / 0.5 Hz (monitoring)
- Low-pass filter: 150 Hz (diagnostic) / 250 Hz (HF mode)
- Notch filter: 50/60 Hz selectable ±1 Hz tolerance
- Driven-right-leg (DRL) circuit for common-mode suppression
- Lead-off detection: AC or DC method, threshold configurable (e.g., > 100 kΩ)

## 4. Digital Signal Processing (On-Device)

- R-peak detection: Pan–Tompkins or wavelet-based, latency < 50 ms
- Heart rate computation: 3–10 s rolling window, outlier rejection
- HRV metrics (short-term): RMSSD, pNN50, LF/HF via Welch PSD on RR intervals
- Baseline wander correction: Adaptive high-pass or cubic spline
- Motion artifact mitigation: Accelerometer-assisted adaptive filter (LMS/RLS)
- Event flags: Asystole, bradycardia, tachycardia, irregular rhythm (AFib pre-screen via RR irregularity)

## 5. Frequency-Domain Requirements

- VLF band (0.04–0.15 Hz): Preserve low-frequency content (HPF ≤ 0.05 Hz; DC drift management)
- Sleep HR band (0.6–0.85 Hz): Maintain passband flatness ±0.5 dB
- Rest HR band (1.0–1.7 Hz): Maintain passband flatness ±0.5 dB
- HF QRS band (20–250 Hz): SNR ≥ 20 dB; EMG discrimination via wavelet/thresholding

## 6. Leads & Electrode Systems

- Lead configurations: Single-lead (Lead I equivalent), 3-lead Holter, 5-lead ICU compatible
- Electrode types:
  - Wet (Ag/AgCl): impedance 1–5 kΩ; short-term diagnostics
  - Dry (polymer/carbon/metalized fabric): impedance 10–100 kΩ; long-term wear
  - Capacitive (through clothing): impedance MΩ range; experimental, increased noise
- Contact area: 50–200 mm² (dry); 20–50 mm² (wet)
- Attachment: Patch adhesive, strap, garment integration

## 7. Wireless & Data

- BLE 5.x preferred; throughput ≥ 8 kbps per channel
- Latency: ≤ 200 ms for real-time HR/event flags
- Buffering: ≥ 30 s circular buffer for connection drops
- Timestamping: Monotonic clock; optional PTP/GPS sync for multi-node setups
- File format: EDF+, MIT-BIH compatible CSV JSON line-delimited, or custom protobuf

## 8. Firmware Interfaces

- Command set:
  - Start/stop stream; set sampling rate (250/500/1000 Hz)
  - Filter profiles: Diagnostic (0.05–150 Hz), HF (0.05–250 Hz)
  - Notch: 50/60 Hz toggle
  - Gain profiles: Low/Med/High
  - Event query: Last N events JSON
- Diagnostics:
  - Lead-off status, electrode impedance estimate
  - Battery level, temperature
  - Self-test: Noise floor, CMRR quick check

## 9. Calibration & Self-Test

- Noise floor test: Shorted input; ≤ 5 µV RMS requirement
- CMRR test: Inject 50/60 Hz common-mode; verify ≥ 100 dB
- Gain/linearization: Apply known ±1 mV signal; error ≤ ±1%
- Impedance check: AC probe (e.g., 31.25 Hz, 10 nA); infer 5 kΩ–100 kΩ
- Notch efficacy: Residual 50/60 Hz ≤ −30 dB vs. baseline

## 10. Validation & Acceptance Criteria

- Rest HR detection accuracy: ≥ 99% beats detected vs. annotated ground truth (MIT-BIH subset)
- RR interval precision: ≤ ±1 ms at 500–1000 Hz sampling
- HRV short-term metrics repeatability: SDNN/RMSSD within ±5% across repeats
- Sleep HR tracking error: ≤ ±1 BPM vs. reference polysomnography ECG
- VLF preservation: PSD error ≤ ±10% vs. DC-coupled clinical reference
- HF QRS feature capture: Detect ventricular late potentials in curated datasets with sensitivity ≥ 85%, specificity ≥ 90%

## 11. Environmental & Safety

- Operating temp: 0–45 °C; humidity: 10–95% non-condensing
- Skin contact materials: ISO 10993 biocompatible, cytotoxicity/sensitization/irritation passed
- EMC: IEC 60601-1-2 pre-compliance guidance for design (no formal certification scope here)
- Electrical safety: Leakage currents within IEC 60601-1 limits (system-level)

## 12. Reference ICs (Examples)

- AFE: AD8232, MAX30003, ADS1293/ADS1299 (multi-channel)
- MCU: nRF52 (BLE SoC), STM32L4 (low-power), RP2040 (cost-effective)
- Power: Buck/LDO with low ripple; battery monitoring IC

## 13. Test Datasets & Benchmarks

- MIT-BIH Arrhythmia Database (PhysioNet)
- MIT-BIH Noise Stress Test Database
- QT Database (waveform annotations)
- Fantasia Database (young/elderly RR intervals)
- Polysomnography datasets (sleep HR reference)

## 14. Deliverables (Engineering)

- Schematics + PCB layout (Gerbers, BoM)
- Firmware binaries + source (AFE config, DSP, BLE)
- Validation report (noise, CMRR, HR/RR/HRV accuracy)
- User guide (electrode placement, troubleshooting)
- Data interface spec (payloads, protocol versioning)

## 15. Change Control

- Versioning: MAJOR.MINOR.PATCH (e.g., 1.0.0)
- Baseline freeze upon passing acceptance; changes via ECO with regression tests

---

This baseline aligns strictly with the specified heart frequencies and establishes measurable acceptance criteria to qualify an ECG sensor stack for production and clinical evaluation readiness (pre-compliance level).
