import requests

def resolve_molecule_to_structure(name):
    try:
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{name}/property/IsomericSMILES,InChIKey/JSON"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        props = data["PropertyTable"]["Properties"][0]
        return {
            "SMILES": props.get("IsomericSMILES"),
            "InChIKey": props.get("InChIKey")
        }
    except Exception as e:
        return {"error": str(e)}
