import pubchempy as pcp

def resolve_structure(name_or_formula: str):
    try:
        compound = pcp.get_compounds(name_or_formula, namespace='name')
        if not compound:
            compound = pcp.get_compounds(name_or_formula, namespace='formula')
        if compound:
            c = compound[0]
            return {
                "smiles": c.isomeric_smiles,
                "inchi": c.inchi,
                "inchikey": c.inchikey
            }
    except Exception as e:
        return {}
    return {}
