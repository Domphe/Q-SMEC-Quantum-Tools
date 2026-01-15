"""Analysis of redundant folders and cleanup recommendations."""
import os
from pathlib import Path

# Active folders (referenced in run_all.ps1 or currently integrated)
ACTIVE_FOLDERS = {
    "arxiv_qc_harvester_complete_final",  # Referenced in run_all.ps1 Step 0.6
    "qc_benchmark_full_system",           # Referenced in run_all.ps1 Step 0.6
    "full_scientific_linking_graph_pipeline",  # Referenced in run_all.ps1 Step 0.6
    "qc_benchmark_dashboard_runner",      # Methods extraction source
    "qc_registry_platform_extended",      # Methods extraction source
    "qsmec_registry_full_platform",       # Q-SMEC platform (may be used)
    "qsmec_platform_autorun_docker",      # Concepts extraction source
    "qsmec_autorun_prod_viz_updated",     # Concepts extraction source
    "qc_realworld_inference_package",     # Concepts extraction source
    "enhanced_qc_platform_bundle",        # Concepts extraction source
    "qc_enhanced_platform"                # Concepts extraction source
}

# Redundant arxiv harvester variants (superseded by complete_final)
REDUNDANT_ARXIV = [
    "arxiv_qc_harvester_bundle",
    "arxiv_qc_harvester_full_package",
    "arxiv_qc_harvester_ultimate",
    "arxiv_qc_harvester_full_auto_chem",
    "arxiv_qc_harvester_enhanced",
    "arxiv_qc_harvester_dockerized",
    "arxiv_qc_harvester_dashboard",
    "arxiv_qc_harvester_bundle_with_nlp",
    "arxiv_qc_harvester_all_features"
]

# Redundant data files (now in database)
REDUNDANT_FILES = [
    "enriched_glossary_linked.json",  # Integrated into glossary.jsonl
    "enriched_glossary.json",         # Integrated into glossary.jsonl
    "qsmec_use_cases_extracted.csv",  # Integrated into glossary.jsonl
    "qsmec_use_cases_extracted.json"  # Integrated into glossary.jsonl
]

def main():
    base_path = Path(r"G:\My Drive\Databases")
    
    print("=== FOLDER CLEANUP ANALYSIS ===\n")
    
    print("ACTIVE FOLDERS (keep):")
    for folder in sorted(ACTIVE_FOLDERS):
        path = base_path / folder
        if path.exists():
            print(f"  ✓ {folder}")
        else:
            print(f"  ✗ {folder} (NOT FOUND)")
    
    print("\nREDUNDANT ARXIV HARVESTERS (can delete):")
    for folder in sorted(REDUNDANT_ARXIV):
        path = base_path / folder
        if path.exists():
            print(f"  🗑 {folder}")
        else:
            print(f"  - {folder} (already deleted)")
    
    print("\nREDUNDANT DATA FILES (can delete):")
    for file in sorted(REDUNDANT_FILES):
        path = base_path / file
        if path.exists():
            print(f"  🗑 {file}")
        else:
            print(f"  - {file} (already deleted)")
    
    print("\n=== RECOMMENDATIONS ===")
    print("1. Delete 9 redundant arxiv harvester variants")
    print("2. Delete 4 redundant JSON/CSV files (already in database)")
    print("3. Keep arxiv_qc_harvester_complete_final (actively used)")
    print("4. Archive ZIP files if needed for rollback")

if __name__ == '__main__':
    main()
