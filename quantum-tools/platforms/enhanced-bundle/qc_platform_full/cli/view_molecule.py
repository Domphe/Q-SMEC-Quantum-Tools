from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import rdMolDraw2D

def view_smiles(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol:
        Draw.MolToFile(mol, "molecules/output.png")
        print("2D structure saved to molecules/output.png")
    else:
        print("Invalid SMILES.")

# Example:
# view_smiles("CCO")