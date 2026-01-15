import streamlit as st
from rdkit import Chem
from rdkit.Chem import Draw

def visualize_smiles(smiles: str):
    mol = Chem.MolFromSmiles(smiles)
    if mol:
        st.image(Draw.MolToImage(mol), caption="Molecule Visualization")
    else:
        st.error("Invalid SMILES string.")