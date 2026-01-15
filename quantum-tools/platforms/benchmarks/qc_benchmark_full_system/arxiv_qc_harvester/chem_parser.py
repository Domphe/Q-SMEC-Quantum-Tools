from chemdataextractor import Document
from arxiv_qc_harvester.chem_structures import resolve_molecule_to_structure

def extract_and_resolve_chemistry(abstract: str):
    doc = Document(abstract)
    unique_names = list({cem.text for cem in doc.cems})
    resolved = []
    for name in unique_names:
        result = resolve_molecule_to_structure(name)
        result["name"] = name
        resolved.append(result)
    return {
        "chemical_names": unique_names,
        "resolved_structures": resolved
    }

def extract_reactions(abstract: str):
    doc = Document(abstract)
    return [rec.serialize() for rec in doc.records if rec.__class__.__name__ == "Reaction"]
