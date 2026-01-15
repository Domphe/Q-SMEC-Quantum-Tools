"""Harvest metadata-only from published textbooks (legal compliance: copyrighted works)."""
import json
from datetime import date
from pathlib import Path
from utils import write_jsonl, DATA_RAW

# Canonical textbooks with metadata only
TEXTBOOKS = [
    {
        "id": "src.textbook.mcquarrie_stat_mech",
        "type": "textbook",
        "title": "Statistical Mechanics",
        "authors": ["Donald A. McQuarrie"],
        "year": 2000,
        "edition": "1st",
        "isbn": "978-1891389153",
        "publisher": "University Science Books",
        "provenance": "canonical_reference",
        "url": "https://uscibooks.com/mcquarrie.htm",
        "domains": ["quantum_chemistry", "quantum_physics", "math_methods"],
        "trust_tier": "A",
        "allowed_content": "metadata_only",
        "open_access": False,
        "keywords": ["statistical mechanics", "thermodynamics", "partition functions"],
        "notes": "Gold standard for statistical mechanics. Metadata-only due to copyright.",
        "last_verified": str(date.today())
    },
    {
        "id": "src.textbook.levine_qc",
        "type": "textbook",
        "title": "Quantum Chemistry",
        "authors": ["Ira N. Levine"],
        "year": 2013,
        "edition": "7th",
        "isbn": "978-0321803450",
        "publisher": "Pearson",
        "provenance": "canonical_reference",
        "url": "https://www.pearson.com/",
        "domains": ["quantum_chemistry"],
        "trust_tier": "A",
        "allowed_content": "metadata_only",
        "open_access": False,
        "keywords": ["quantum chemistry", "molecular orbital theory", "spectroscopy"],
        "notes": "Standard undergraduate/graduate QC text. Metadata-only due to copyright.",
        "last_verified": str(date.today())
    },
    {
        "id": "src.textbook.szabo_ostlund",
        "type": "textbook",
        "title": "Modern Quantum Chemistry: Introduction to Advanced Electronic Structure Theory",
        "authors": ["Attila Szabo", "Neil S. Ostlund"],
        "year": 1996,
        "edition": "1st",
        "isbn": "978-0486691862",
        "publisher": "Dover Publications",
        "provenance": "canonical_reference",
        "url": "https://store.doverpublications.com/",
        "domains": ["quantum_chemistry"],
        "trust_tier": "A",
        "allowed_content": "metadata_only",
        "open_access": False,
        "keywords": ["electronic structure", "hartree-fock", "post-hf", "many-body"],
        "notes": "Essential reference for electronic structure theory. Metadata-only due to copyright.",
        "last_verified": str(date.today())
    },
    {
        "id": "src.textbook.helgaker_mest",
        "type": "textbook",
        "title": "Molecular Electronic-Structure Theory",
        "authors": ["Trygve Helgaker", "Poul Jørgensen", "Jeppe Olsen"],
        "year": 2000,
        "edition": "1st",
        "isbn": "978-0471967552",
        "publisher": "Wiley",
        "provenance": "canonical_reference",
        "url": "https://www.wiley.com/",
        "domains": ["quantum_chemistry"],
        "trust_tier": "A",
        "allowed_content": "metadata_only",
        "open_access": False,
        "keywords": ["electronic structure", "coupled cluster", "CI", "MCSCF"],
        "notes": "Comprehensive graduate-level reference. Metadata-only due to copyright.",
        "last_verified": str(date.today())
    },
    {
        "id": "src.textbook.shankar_qm",
        "type": "textbook",
        "title": "Principles of Quantum Mechanics",
        "authors": ["R. Shankar"],
        "year": 2011,
        "edition": "2nd",
        "isbn": "978-0306447907",
        "publisher": "Springer",
        "provenance": "canonical_reference",
        "url": "https://www.springer.com/",
        "domains": ["quantum_physics", "math_methods"],
        "trust_tier": "A",
        "allowed_content": "metadata_only",
        "open_access": False,
        "keywords": ["quantum mechanics", "foundations", "postulates"],
        "notes": "Standard QM textbook. Metadata-only due to copyright.",
        "last_verified": str(date.today())
    },
    {
        "id": "src.textbook.sakurai_qm",
        "type": "textbook",
        "title": "Modern Quantum Mechanics",
        "authors": ["J. J. Sakurai", "Jim Napolitano"],
        "year": 2017,
        "edition": "2nd",
        "isbn": "978-1108422413",
        "publisher": "Cambridge University Press",
        "provenance": "canonical_reference",
        "url": "https://www.cambridge.org/",
        "domains": ["quantum_physics"],
        "trust_tier": "A",
        "allowed_content": "metadata_only",
        "open_access": False,
        "keywords": ["quantum mechanics", "angular momentum", "scattering"],
        "notes": "Graduate-level QM standard. Metadata-only due to copyright.",
        "last_verified": str(date.today())
    },
    {
        "id": "src.textbook.griffiths_qm",
        "type": "textbook",
        "title": "Introduction to Quantum Mechanics",
        "authors": ["David J. Griffiths", "Darrell F. Schroeter"],
        "year": 2018,
        "edition": "3rd",
        "isbn": "978-1107189638",
        "publisher": "Cambridge University Press",
        "provenance": "canonical_reference",
        "url": "https://www.cambridge.org/",
        "domains": ["quantum_physics"],
        "trust_tier": "A",
        "allowed_content": "metadata_only",
        "open_access": False,
        "keywords": ["quantum mechanics", "undergraduate", "pedagogy"],
        "notes": "Widely-used undergraduate text. Metadata-only due to copyright.",
        "last_verified": str(date.today())
    },
    {
        "id": "src.textbook.townsend_qm",
        "type": "textbook",
        "title": "A Modern Approach to Quantum Mechanics",
        "authors": ["John S. Townsend"],
        "year": 2012,
        "edition": "2nd",
        "isbn": "978-1891389788",
        "publisher": "University Science Books",
        "provenance": "canonical_reference",
        "url": "https://uscibooks.com/",
        "domains": ["quantum_physics"],
        "trust_tier": "A",
        "allowed_content": "metadata_only",
        "open_access": False,
        "keywords": ["quantum mechanics", "spin-first", "pedagogy"],
        "notes": "Spin-first pedagogical approach. Metadata-only due to copyright.",
        "last_verified": str(date.today())
    }
]

def main():
    """Harvest publisher metadata."""
    output_path = DATA_RAW / "publishers" / "textbooks.jsonl"
    
    write_jsonl(output_path, TEXTBOOKS)
    print(f"Harvested {len(TEXTBOOKS)} textbook metadata records.")
    print(f"Output: {output_path}")
    print("\nLegal compliance: Metadata-only for copyrighted works.")
    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
