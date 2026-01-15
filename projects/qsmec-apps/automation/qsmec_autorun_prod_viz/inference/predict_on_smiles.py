from rdkit import Chem
from utils.ml_utils import load_model, run_inference

def predict(smiles: str, model_path: str):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError("Invalid SMILES")
    return run_inference(mol, model_path)