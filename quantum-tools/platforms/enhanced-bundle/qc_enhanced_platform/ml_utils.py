import json

def load_model(path):
    # Placeholder for loading real trained model
    return {"model": "loaded"}

def run_inference(mol, model_path):
    model = load_model(model_path)
    # Realistic dummy output for test
    return {
        "dipole_moment": 1.25,
        "homo_lumo_gap": 6.1,
        "ir_spectrum_peaks": [1230, 1440, 1700]
    }