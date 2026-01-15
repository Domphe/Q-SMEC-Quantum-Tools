import argparse
import math
import sys

# Optional dependencies
try:
    import numpy as np
except Exception:
    np = None

try:
    from scipy.signal import welch
except Exception:
    welch = None


def generate_synthetic_ecg(duration_s=60.0, fs=500, hr_bpm=60.0, noise_uV=50.0):
    """Generate a simple synthetic ECG-like waveform for testing.
    - QRS approximated by triangular pulses at R-peak times
    - Baseline wander and low-amplitude P/T waves modeled crudely
    Returns t, ecg (in microvolts)
    """
    if np is None:
        raise RuntimeError(
            "numpy required for synthetic generation; please install numpy"
        )
    t = np.arange(0, duration_s, 1.0 / fs)
    rr = 60.0 / hr_bpm  # seconds per beat
    r_times = np.arange(0.5, duration_s - 0.5, rr)
    ecg = np.zeros_like(t)

    # QRS pulses
    qrs_width = 0.08  # 80 ms
    qrs_amp = 1000.0  # 1 mV ~ 1000 uV
    for rt in r_times:
        idx = int(rt * fs)
        w = int(qrs_width * fs)
        if idx - w // 2 >= 0 and idx + w // 2 < len(ecg):
            # triangular pulse
            for k in range(-w // 2, w // 2):
                ecg[idx + k] += qrs_amp * (1.0 - abs(k) / (w // 2 + 1))

    # P and T waves (low amplitude sinusoids)
    ecg += 100.0 * np.sin(2 * np.pi * 1.2 * t)  # P-like
    ecg += 200.0 * np.sin(2 * np.pi * 0.8 * t + 1.5)  # T-like

    # Baseline wander
    ecg += 50.0 * np.sin(2 * np.pi * 0.2 * t)

    # Add white noise
    ecg += np.random.normal(0, noise_uV, size=ecg.shape)
    return t, ecg


def pan_tompkins_like(ecg_uV, fs, threshold_multiplier=0.3, refractory_ms=200):
    """Simplified R-peak detection pipeline with tunable parameters.
    - Bandpass (5–15 Hz) via naive difference filters
    - Differentiate + square + moving average integration
    - Adaptive thresholding with configurable sensitivity

    Args:
        ecg_uV: ECG signal (microvolts).
        fs: Sampling rate (Hz).
        threshold_multiplier: Fraction of max for peak threshold (0.1–0.5); lower = more sensitive.
        refractory_ms: Minimum time between peaks (milliseconds); default 200 ms.

    Returns:
        peaks: List of peak indices.
    """
    if np is None:
        raise RuntimeError("numpy required for detection; please install numpy")

    # Bandpass via simple high/low-pass IIR approximations (very rough)
    # High-pass (HPF ~5 Hz): y[n] = x[n] - x[n-1] + 0.99*y[n-1]
    hpf = np.zeros_like(ecg_uV)
    for n in range(1, len(ecg_uV)):
        hpf[n] = ecg_uV[n] - ecg_uV[n - 1] + 0.99 * hpf[n - 1]
    # Low-pass (LPF ~15 Hz): y[n] = y[n-1] + (x[n] - y[n-1]) * alpha
    # crude alpha from cutoff fc: alpha ≈ 2πfc/fs (limited)
    alpha = min(1.0, 2 * math.pi * 15.0 / fs)
    bpf = np.zeros_like(hpf)
    for n in range(1, len(hpf)):
        bpf[n] = bpf[n - 1] + (hpf[n] - bpf[n - 1]) * alpha

    # Differentiate
    diff = np.diff(bpf, prepend=bpf[0])
    # Square
    sq = diff**2
    # Moving average window ~150 ms
    win = int(0.15 * fs)
    if win < 1:
        win = 1
    ma = np.convolve(sq, np.ones(win) / win, mode="same")

    # Adaptive threshold: tunable fraction of max
    thr = threshold_multiplier * np.max(ma)
    peaks = []
    refractory = int((refractory_ms / 1000.0) * fs)  # Convert to samples
    if refractory < 1:
        refractory = 1
    last = -refractory
    for i in range(len(ma)):
        if ma[i] > thr and (i - last) > refractory:
            # local maxima search in a small window
            left = max(0, i - int(0.05 * fs))
            right = min(len(ma) - 1, i + int(0.05 * fs))
            loc = left + int(np.argmax(bpf[left : right + 1]))
            peaks.append(loc)
            last = loc
    return peaks


def rr_intervals(peaks, fs):
    """Compute RR intervals (ms) from peak indices."""
    rr_ms = []
    for i in range(1, len(peaks)):
        rr_ms.append(1000.0 * (peaks[i] - peaks[i - 1]) / fs)
    return rr_ms


def time_domain_hrv(rr_ms):
    """Return SDNN, RMSSD, pNN50 from RR intervals (ms)."""
    if len(rr_ms) < 2:
        return None
    arr = np.array(rr_ms)
    sdnn = float(np.std(arr, ddof=1)) if len(arr) > 1 else 0.0
    diff = np.diff(arr)
    rmssd = float(np.sqrt(np.mean(diff**2))) if len(diff) > 0 else 0.0
    pnn50 = (
        float(np.sum(np.abs(diff) > 50.0) * 100.0 / len(diff)) if len(diff) > 0 else 0.0
    )
    return {"SDNN_ms": sdnn, "RMSSD_ms": rmssd, "pNN50_percent": pnn50}


def frequency_domain_hrv(rr_ms):
    """Compute LF/HF via Welch PSD on evenly resampled RR tachogram.
    Requires numpy and scipy; gracefully returns None if unavailable.
    """
    if np is None or welch is None or len(rr_ms) < 4:
        return None
    # Build tachogram (RR in seconds) at uniform sampling (4 Hz)
    rr_s = np.array(rr_ms) / 1000.0
    # Instantaneous heart rate series from RR; resample to 4 Hz
    hr_series = 60.0 / rr_s
    # naive resampling by linear interpolation
    x = np.arange(len(hr_series))
    fs_tacho = 4.0
    new_len = int(len(hr_series) * fs_tacho)
    xi = np.linspace(x[0], x[-1], new_len)
    hr_resampled = np.interp(xi, x, hr_series)
    f, pxx = welch(hr_resampled, fs=fs_tacho, nperseg=min(256, len(hr_resampled)))
    # Integrate LF (0.04–0.15 Hz) and HF (0.15–0.40 Hz)
    lf_band = (f >= 0.04) & (f < 0.15)
    hf_band = (f >= 0.15) & (f < 0.40)
    lf_power = float(np.trapz(pxx[lf_band], f[lf_band]))
    hf_power = float(np.trapz(pxx[hf_band], f[hf_band]))
    lf_hf = float(lf_power / hf_power) if hf_power > 0 else float("inf")
    return {"LF_power": lf_power, "HF_power": hf_power, "LF_HF_ratio": lf_hf}


def run_synthetic(
    duration_s=60.0,
    fs=500,
    hr_bpm=60.0,
    threshold_multiplier=0.3,
    refractory_ms=200,
    output_csv=None,
):
    """Run synthetic ECG test with optional CSV output validation.

    Args:
        duration_s: Duration in seconds.
        fs: Sampling rate (Hz).
        hr_bpm: Target heart rate (bpm).
        threshold_multiplier: Peak detection sensitivity (0.1–0.5).
        refractory_ms: Refractory period (ms).
        output_csv: If provided, write RR intervals and band stats to CSV file.

    Returns:
        Dict with test results.
    """
    t, ecg = generate_synthetic_ecg(duration_s=duration_s, fs=fs, hr_bpm=hr_bpm)
    peaks = pan_tompkins_like(
        ecg, fs, threshold_multiplier=threshold_multiplier, refractory_ms=refractory_ms
    )
    rr = rr_intervals(peaks, fs)
    td = time_domain_hrv(rr)
    fd = frequency_domain_hrv(rr)
    mean_hr = (
        (60.0 / (np.mean(rr) / 1000.0)) if (np is not None and len(rr) > 0) else None
    )

    result = {
        "samples": len(ecg),
        "fs": fs,
        "beats_detected": len(peaks),
        "mean_hr_bpm": mean_hr,
        "time_domain": td,
        "frequency_domain": fd,
    }

    # Write CSV validation output if requested
    if output_csv is not None and np is not None:
        import csv

        try:
            with open(output_csv, "w", newline="") as f:
                writer = csv.writer(f)
                # Header
                writer.writerow(["rr_interval_ms", "beat_number"])
                # RR intervals
                for i, rr_ms in enumerate(rr):
                    writer.writerow([rr_ms, i + 1])
                # Summary stats section
                writer.writerow([])
                writer.writerow(["metric", "value"])
                writer.writerow(["mean_hr_bpm", mean_hr])
                if td:
                    writer.writerow(["SDNN_ms", td.get("SDNN_ms", None)])
                    writer.writerow(["RMSSD_ms", td.get("RMSSD_ms", None)])
                    writer.writerow(["pNN50_percent", td.get("pNN50_percent", None)])
                if fd:
                    writer.writerow(["LF_power", fd.get("LF_power", None)])
                    writer.writerow(["HF_power", fd.get("HF_power", None)])
                    writer.writerow(["LF_HF_ratio", fd.get("LF_HF_ratio", None)])
            result["csv_output"] = output_csv
        except Exception as e:
            result["csv_error"] = str(e)

    return result


def main():
    parser = argparse.ArgumentParser(
        description="HR/RR/HRV test harness: synthetic or CSV input with tunable peak detection"
    )
    parser.add_argument("--mode", choices=["synthetic", "csv"], default="synthetic")
    parser.add_argument(
        "--duration", type=float, default=60.0, help="Duration in seconds (default: 60)"
    )
    parser.add_argument(
        "--fs", type=int, default=500, help="Sampling rate (Hz, default: 500)"
    )
    parser.add_argument(
        "--hr",
        type=float,
        default=60.0,
        help="Target heart rate for synthetic (bpm, default: 60)",
    )
    parser.add_argument(
        "--csv",
        type=str,
        default=None,
        help="Path to CSV with one column: ECG in microvolts; assumes --fs",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.3,
        help="Peak detection threshold multiplier (0.1–0.5; default: 0.3, lower=more sensitive)",
    )
    parser.add_argument(
        "--refractory",
        type=float,
        default=200,
        help="Refractory period (ms, default: 200)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output CSV filename for RR intervals and stats",
    )
    args = parser.parse_args()

    if args.mode == "synthetic":
        try:
            result = run_synthetic(
                duration_s=args.duration,
                fs=args.fs,
                hr_bpm=args.hr,
                threshold_multiplier=args.threshold,
                refractory_ms=args.refractory,
                output_csv=args.output,
            )
        except Exception as e:
            print(f"ERROR: {e}")
            sys.exit(1)
        print("=== Synthetic ECG Test ===")
        for k, v in result.items():
            if isinstance(v, dict):
                print(f"{k}:")
                for k2, v2 in v.items():
                    print(f"  {k2}: {v2}")
            else:
                print(f"{k}: {v}")
    else:
        if np is None:
            print("ERROR: numpy required for CSV mode")
            sys.exit(1)
        if args.csv is None:
            print("ERROR: --csv path required for CSV mode")
            sys.exit(1)
        try:
            ecg = np.loadtxt(args.csv, delimiter=",")
        except Exception as e:
            print(f"ERROR reading CSV: {e}")
            sys.exit(1)
        peaks = pan_tompkins_like(
            ecg,
            args.fs,
            threshold_multiplier=args.threshold,
            refractory_ms=args.refractory,
        )
        rr = rr_intervals(peaks, args.fs)
        td = time_domain_hrv(rr)
        fd = frequency_domain_hrv(rr)
        mean_hr = (60.0 / (np.mean(rr) / 1000.0)) if len(rr) > 0 else None
        print("=== CSV ECG Test ===")
        print(f"samples: {len(ecg)}")
        print(f"fs: {args.fs}")
        print(f"beats_detected: {len(peaks)}")
        print(f"mean_hr_bpm: {mean_hr}")
        if td:
            print(f"time_domain: {td}")
        if fd:
            print(f"frequency_domain: {fd}")

        # Write output CSV if requested
        if args.output:
            import csv

            try:
                with open(args.output, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(["rr_interval_ms", "beat_number"])
                    for i, rr_ms in enumerate(rr):
                        writer.writerow([rr_ms, i + 1])
                    writer.writerow([])
                    writer.writerow(["metric", "value"])
                    writer.writerow(["mean_hr_bpm", mean_hr])
                    if td:
                        writer.writerow(["SDNN_ms", td.get("SDNN_ms", None)])
                        writer.writerow(["RMSSD_ms", td.get("RMSSD_ms", None)])
                        writer.writerow(
                            ["pNN50_percent", td.get("pNN50_percent", None)]
                        )
                    if fd:
                        writer.writerow(["LF_power", fd.get("LF_power", None)])
                        writer.writerow(["HF_power", fd.get("HF_power", None)])
                        writer.writerow(["LF_HF_ratio", fd.get("LF_HF_ratio", None)])
                print(f"Output written to {args.output}")
            except Exception as e:
                print(f"ERROR writing CSV: {e}")
                sys.exit(1)
        print(f"beats_detected: {len(peaks)}")
        print(f"mean_hr_bpm: {mean_hr}")
        print(f"time_domain: {td}")
        print(f"frequency_domain: {fd}")


if __name__ == "__main__":
    main()
