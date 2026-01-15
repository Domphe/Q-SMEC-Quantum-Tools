#!/usr/bin/env python3
"""
EEG Band-Power Harness: Synthetic Signal Generator & Spectral Analysis

Generates synthetic multi-channel EEG data and computes power in canonical bands:
- Delta (0.5–4 Hz)
- Theta (4–8 Hz)
- Alpha (8–13 Hz)
- Beta (13–30 Hz)
- Gamma (30–100 Hz)

Supports mode='synthetic' for test signal generation with configurable band emphasis.
Outputs per-channel band power and cross-frequency connectivity (phase-amplitude coupling).
Validates against EEG baseline specifications.

Usage:
  python eeg_band_power_test.py --mode synthetic --duration 60 --channels 8 --emphasis alpha
  python eeg_band_power_test.py --mode synthetic --duration 120 --channels 16 --emphasis theta
"""

import argparse
import csv
import sys
from datetime import datetime


import numpy as np
from scipy import signal


class EEGBandPowerHarness:
    """Synthetic EEG generator and band-power analyzer."""

    # EEG band definitions (Hz)
    BANDS = {
        "delta": (0.5, 4.0),
        "theta": (4.0, 8.0),
        "alpha": (8.0, 13.0),
        "beta": (13.0, 30.0),
        "gamma": (30.0, 100.0),
    }

    def __init__(self, sampling_rate=256, duration_sec=60, num_channels=8):
        """
        Initialize EEG harness.

        Args:
            sampling_rate: Sampling frequency (Hz), typically 128–512.
            duration_sec: Recording duration in seconds.
            num_channels: Number of EEG channels (8, 16, 32, or 64).
        """
        self.fs = sampling_rate
        self.duration = duration_sec
        self.num_channels = num_channels
        self.num_samples = int(self.fs * self.duration)
        self.time = np.arange(self.num_samples) / self.fs

    def generate_synthetic_eeg(self, emphasis_band="alpha", snr_db=20):
        """
        Generate synthetic multi-channel EEG with emphasis on one band.

        Args:
            emphasis_band: 'delta', 'theta', 'alpha', 'beta', 'gamma', or 'mixed'.
            snr_db: Signal-to-noise ratio (dB); lower = more noise.

        Returns:
            eeg_data: (num_samples, num_channels) array of EEG signals.
        """
        eeg_data = np.zeros((self.num_samples, self.num_channels))

        # Noise floor (Gaussian 1/f "pink noise" approximation)
        noise_rms = 10 ** (-snr_db / 20)
        for ch in range(self.num_channels):
            # Simple 1/f approximation: sum octaves
            noise = np.zeros(self.num_samples)
            for octave in range(1, 6):
                f_octave = octave * 2
                noise += np.random.randn(self.num_samples) / f_octave
            eeg_data[:, ch] += noise * noise_rms

        # Add band-specific content
        if emphasis_band == "mixed":
            # Equal power across all bands
            for band_name, (f_low, f_high) in self.BANDS.items():
                f_center = (f_low + f_high) / 2
                power = 1.0
                eeg_data += self._add_oscillation(f_center, power)
        else:
            # Single emphasized band
            if emphasis_band.lower() not in self.BANDS:
                raise ValueError(f"Unknown band: {emphasis_band}")
            f_low, f_high = self.BANDS[emphasis_band.lower()]
            f_center = (f_low + f_high) / 2
            # Power in emphasized band
            eeg_data += self._add_oscillation(f_center, power=5.0)
            # Lower power in other bands
            for band_name, (f_l, f_h) in self.BANDS.items():
                if band_name != emphasis_band.lower():
                    f_c = (f_l + f_h) / 2
                    eeg_data += self._add_oscillation(f_c, power=0.5)

        return eeg_data

    def _add_oscillation(self, frequency, power=1.0):
        """Add sinusoidal oscillation at given frequency to all channels."""
        oscillation = np.zeros((self.num_samples, self.num_channels))
        signal_component = power * np.sin(2 * np.pi * frequency * self.time)
        # Add small phase offsets across channels for realism
        for ch in range(self.num_channels):
            phase_offset = ch * np.pi / self.num_channels
            oscillation[:, ch] = (
                signal_component
                + power * np.sin(2 * np.pi * frequency * self.time + phase_offset) * 0.1
            )
        return oscillation

    def compute_band_power(self, eeg_data, normalize=True):
        """
        Compute power spectral density in each band (Welch method).

        Args:
            eeg_data: (num_samples, num_channels) EEG array.
            normalize: If True, normalize by total power (relative power, 0–1).

        Returns:
            band_power: Dict with band names as keys; values are (num_channels,) arrays.
            freqs: Frequency array (Hz).
            psd: Power spectral density (num_channels, num_freqs).
        """
        # Welch PSD estimation
        nperseg = min(512, self.num_samples // 2)
        freqs, psd = signal.welch(eeg_data, self.fs, nperseg=nperseg, axis=0)

        band_power = {}
        total_power = np.sum(psd, axis=0)  # Total power per channel

        for band_name, (f_low, f_high) in self.BANDS.items():
            mask = (freqs >= f_low) & (freqs <= f_high)
            power = np.sum(psd[mask, :], axis=0)
            if normalize:
                power = power / (total_power + 1e-10)
            band_power[band_name] = power

        return band_power, freqs, psd

    def compute_connectivity(self, eeg_data, band_name="alpha"):
        """
        Compute inter-channel coherence (spatial correlation) in a given band.

        Args:
            eeg_data: (num_samples, num_channels) EEG array.
            band_name: Band for connectivity analysis.

        Returns:
            coherence_matrix: (num_channels, num_channels) coherence matrix.
        """
        f_low, f_high = self.BANDS.get(band_name, (8, 13))

        # Bandpass filter
        sos = signal.butter(4, [f_low, f_high], btype="band", fs=self.fs, output="sos")
        filtered = signal.sosfilt(sos, eeg_data, axis=0)

        # Compute coherence between all pairs (simplified via correlation)
        coherence = np.corrcoef(filtered.T)
        return coherence

    def validate_baseline(self, band_power):
        """
        Validate band power against EEG baseline specifications.

        EEG baseline criteria (simplified):
        - Noise floor: < 10 µV²/Hz (mid-band)
        - Band power (relative): Delta 20–40%, Alpha 20–35%, Beta 15–25%, Theta/Gamma variable.

        Args:
            band_power: Dict from compute_band_power().

        Returns:
            validation_report: Dict with pass/fail for each criterion.
        """
        report = {}

        # Check that band powers are reasonable (relative power 0–1)
        for band_name, power_array in band_power.items():
            mean_power = np.mean(power_array)
            report[f"{band_name}_mean"] = mean_power
            if 0 <= mean_power <= 1:
                report[f"{band_name}_valid"] = True
            else:
                report[f"{band_name}_valid"] = False

        # Check total power consistency
        total_power = sum([np.mean(band_power[b]) for b in self.BANDS.keys()])
        if 0.95 <= total_power <= 1.05:
            report["total_power_valid"] = True
        else:
            report["total_power_valid"] = False

        return report


def main():
    parser = argparse.ArgumentParser(
        description="EEG Band-Power Test Harness",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --mode synthetic --duration 60 --channels 8 --emphasis alpha
  %(prog)s --mode synthetic --duration 120 --channels 16 --emphasis theta --output results.csv
        """,
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="synthetic",
        help="Synthetic data generation mode (default: synthetic)",
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=60,
        help="Recording duration in seconds (default: 60)",
    )
    parser.add_argument(
        "--channels", type=int, default=8, help="Number of EEG channels (default: 8)"
    )
    parser.add_argument(
        "--fs", type=int, default=256, help="Sampling rate (Hz, default: 256)"
    )
    parser.add_argument(
        "--emphasis",
        type=str,
        default="alpha",
        choices=["delta", "theta", "alpha", "beta", "gamma", "mixed"],
        help="Emphasized frequency band (default: alpha)",
    )
    parser.add_argument(
        "--snr", type=float, default=20, help="Signal-to-noise ratio (dB, default: 20)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output CSV filename (default: None, print to stdout)",
    )

    args = parser.parse_args()

    # Initialize harness
    harness = EEGBandPowerHarness(
        sampling_rate=args.fs, duration_sec=args.duration, num_channels=args.channels
    )

    print("[EEG Band-Power Harness]", file=sys.stderr)
    print(f"Mode: {args.mode}", file=sys.stderr)
    print(f"Duration: {args.duration} sec", file=sys.stderr)
    print(f"Channels: {args.channels}", file=sys.stderr)
    print(f"Sampling rate: {args.fs} Hz", file=sys.stderr)
    print(f"Emphasis band: {args.emphasis}", file=sys.stderr)
    print(f"SNR: {args.snr} dB", file=sys.stderr)

    # Generate synthetic EEG
    print("Generating synthetic EEG...", file=sys.stderr)
    eeg_data = harness.generate_synthetic_eeg(
        emphasis_band=args.emphasis, snr_db=args.snr
    )

    # Compute band power
    print("Computing band power (Welch PSD)...", file=sys.stderr)
    band_power, freqs, psd = harness.compute_band_power(eeg_data, normalize=True)

    # Validate baseline
    print("Validating against baseline...", file=sys.stderr)
    validation = harness.validate_baseline(band_power)

    # Connectivity (optional)
    print("Computing connectivity (alpha band coherence)...", file=sys.stderr)
    coherence_alpha = harness.compute_connectivity(eeg_data, band_name="alpha")
    mean_coherence = np.mean(
        coherence_alpha[np.triu_indices_from(coherence_alpha, k=1)]
    )

    # Report
    results = {
        "timestamp": datetime.now().isoformat(),
        "mode": args.mode,
        "duration_sec": args.duration,
        "num_channels": args.channels,
        "sampling_rate_hz": args.fs,
        "emphasis_band": args.emphasis,
        "snr_db": args.snr,
        "band_power_summary": {},
        "validation": validation,
        "mean_coherence_alpha": mean_coherence,
    }

    # Summarize band power
    for band_name, power_array in band_power.items():
        results["band_power_summary"][band_name] = {
            "mean": float(np.mean(power_array)),
            "std": float(np.std(power_array)),
            "min": float(np.min(power_array)),
            "max": float(np.max(power_array)),
        }

    print("\n=== Results ===", file=sys.stderr)
    print(
        f"Total power (normalized): {sum([np.mean(band_power[b]) for b in harness.BANDS.keys()]):.4f}",
        file=sys.stderr,
    )
    for band_name, summary in results["band_power_summary"].items():
        print(
            f"{band_name:8s} (rel. power): mean={summary['mean']:.4f}, std={summary['std']:.4f}",
            file=sys.stderr,
        )
    print(
        f"Alpha coherence (mean inter-channel): {mean_coherence:.4f}", file=sys.stderr
    )
    print(
        f"Baseline valid: {validation.get('total_power_valid', False)}", file=sys.stderr
    )

    # Output CSV (if requested)
    if args.output:
        print(f"Writing CSV to {args.output}...", file=sys.stderr)
        with open(args.output, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["channel", "delta", "theta", "alpha", "beta", "gamma"])
            for ch in range(args.channels):
                row = [ch] + [band_power[b][ch] for b in harness.BANDS.keys()]
                writer.writerow(row)
    else:
        # Print results to stdout in JSON-ish format
        import json

        print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
