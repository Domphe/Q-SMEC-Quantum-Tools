#!/usr/bin/env python3
"""
Batch convert Personal System markdown files to Microsoft Word (.docx) format.
Uses pandoc for high-quality conversion with table support.
"""

import subprocess
import sys
from pathlib import Path

# Map G: drive to /mnt/g for WSL
BASE_DIR = Path(
    "/mnt/g/My Drive/Databases/Client-Projects/Dan Geraci - Water/War-Fighter Level_Water Filtration/Personal System"
)

MD_FILES = [
    "00_RESEARCH_SUMMARY_Personal.md",
    "01_EXECUTIVE_BRIEFING_Personal_20260112.md",
    "02_VALIDATION_REPORT_Personal_Cape_Test.md",
    "03_TECHNICAL_DOSSIER_Personal_System.md",
    "04_MARKET_INTELLIGENCE_Personal_System.md",
    "05_QSMEC_SPEC_Personal_System.md",
    "06_COMPREHENSIVE_SUMMARY_Personal_System.md",
    "07_Personal_System_Deep_Dive.md",
    "08_P248_Schedule_and_Prime_Partners_Personal.md",
]


def check_pandoc():
    """Check if pandoc is installed."""
    try:
        result = subprocess.run(
            ["pandoc", "--version"],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def install_pandoc():
    """Install pandoc using apt."""
    print("Installing pandoc...")
    subprocess.run(["sudo", "apt-get", "update", "-y"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "pandoc"], check=True)


def convert_md_to_docx(md_path: Path):
    """Convert a single markdown file to .docx using pandoc."""
    docx_path = md_path.with_suffix(".docx")
    print(f"Converting: {md_path.name} -> {docx_path.name}")

    result = subprocess.run(
        [
            "pandoc",
            str(md_path),
            "-o",
            str(docx_path),
            "--from=markdown",
            "--to=docx",
            "--standalone",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode == 0:
        print(f"  ✓ Success: {docx_path.name} ({docx_path.stat().st_size:,} bytes)")
        return True
    else:
        print(f"  ✗ Error: {result.stderr}")
        return False


def main():
    # Check/install pandoc
    if not check_pandoc():
        print("Pandoc not found. Installing...")
        try:
            install_pandoc()
        except Exception as exc:
            print(f"Failed to install pandoc: {exc}")
            print("Please run: sudo apt-get install pandoc")
            sys.exit(1)
    else:
        print("Pandoc is already installed.")

    print(f"\nBase directory: {BASE_DIR}")
    print(f"Converting {len(MD_FILES)} markdown files to Word (.docx)...\n")

    success_count = 0
    fail_count = 0

    for md_file in MD_FILES:
        md_path = BASE_DIR / md_file
        if not md_path.exists():
            print(f"⚠ Skipping (not found): {md_file}")
            fail_count += 1
            continue

        if convert_md_to_docx(md_path):
            success_count += 1
        else:
            fail_count += 1

    print(f"\n{'=' * 60}")
    print(f"Conversion complete: {success_count} succeeded, {fail_count} failed")
    print(f"Output location: {BASE_DIR}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
