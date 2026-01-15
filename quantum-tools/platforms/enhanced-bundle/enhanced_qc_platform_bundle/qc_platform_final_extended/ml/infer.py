import json
from pathlib import Path
import joblib

def infer(example):
    model = joblib.load("models/benchmark_rf_model.pkl")
    x = [[len(example.get("methods", []))]]
    pred = model.predict(x)[0]
    return pred

if __name__ == "__main__":
    example = {
        "name": "Formaldehyde",
        "methods": ["HF", "MP2", "B3LYP"]
    }
    prediction = infer(example)
    print(f"Predicted energy (Hartree): {prediction}")