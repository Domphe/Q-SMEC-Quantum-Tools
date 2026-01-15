"""Harvest NIST Atomic Spectra Database (ASD)."""
import sys
from datetime import date
from utils import write_jsonl, DATA_RAW

# Stub: Full implementation would use NIST ASD API

SAMPLE_SPECTRA = [
    {
        "id": "ds.nist_asd.hydrogen",
        "name": "Hydrogen Atomic Spectra",
        "domain": "quantum_physics",
        "category": "atomic_spectra",
        "description": "Hydrogen atomic energy levels and transition data from NIST ASD",
        "source_id": "src.gov.nist_asd",
        "url": "https://physics.nist.gov/PhysRefData/ASD/lines_form.html",
        "metadata": {
            "element": "H",
            "atomic_number": 1,
            "ionization_stages": ["I"],
            "wavelength_range": "visible_uv"
        },
        "last_reviewed": str(date.today())
    },
    {
        "id": "ds.nist_asd.helium",
        "name": "Helium Atomic Spectra",
        "domain": "quantum_physics",
        "category": "atomic_spectra",
        "description": "Helium atomic energy levels and transition data from NIST ASD",
        "source_id": "src.gov.nist_asd",
        "url": "https://physics.nist.gov/PhysRefData/ASD/lines_form.html",
        "metadata": {
            "element": "He",
            "atomic_number": 2,
            "ionization_stages": ["I", "II"],
            "wavelength_range": "visible_uv"
        },
        "last_reviewed": str(date.today())
    }
]

SOURCE_RECORD = {
    "id": "src.gov.nist_asd",
    "type": "database",
    "title": "NIST Atomic Spectra Database (ASD)",
    "authors": ["A. Kramida", "Yu. Ralchenko", "J. Reader"],
    "year": 2024,
    "publisher": "NIST",
    "provenance": "gov_us_nist",
    "url": "https://physics.nist.gov/PhysRefData/ASD/index.html",
    "domains": ["quantum_physics"],
    "trust_tier": "A",
    "allowed_content": "full_open_content",
    "open_access": True,
    "keywords": ["atomic physics", "spectroscopy", "energy levels", "transitions"],
    "notes": "NIST ASD Version 5.11 (2024). Full open content as US government work.",
    "last_verified": str(date.today())
}

def main():
    """Harvest NIST ASD data."""
    sources_path = DATA_RAW / "gov" / "nist_asd_source.jsonl"
    datasets_path = DATA_RAW / "gov" / "nist_asd_spectra.jsonl"
    
    write_jsonl(sources_path, [SOURCE_RECORD])
    write_jsonl(datasets_path, SAMPLE_SPECTRA)
    
    print(f"Harvested NIST ASD:")
    print(f"  Source: {sources_path}")
    print(f"  Datasets: {datasets_path} ({len(SAMPLE_SPECTRA)} elements)")
    print("\nNOTE: Placeholder data; full API integration from https://physics.nist.gov/PhysRefData/ASD/ pending.")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
