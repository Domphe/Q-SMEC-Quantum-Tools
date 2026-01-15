
import streamlit as st

models = ["Graphormer", "DimeNet", "GAT"]
targets = ["dipole", "HOMO-LUMO gap", "spectra", "frequencies"]

selected_model = st.selectbox("Select GNN Model", models)
selected_target = st.selectbox("Select Prediction Target", targets)

st.write(f"You selected {selected_model} to predict {selected_target}.")
