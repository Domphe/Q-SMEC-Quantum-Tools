import joblib
import json

def infer(methods):
    model = joblib.load("models/rf_model.pkl")
    features = [[len(methods)]]
    return model.predict(features)[0]

if __name__ == "__main__":
    methods = ["HF", "MP2", "CCSD(T)"]
    result = infer(methods)
    print(f"Predicted reference energy: {result:.6f} Hartree")