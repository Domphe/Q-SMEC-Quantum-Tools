import json
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib

def load_dataset(filepath):
    X, y = [], []
    with open(filepath) as f:
        for line in f:
            data = json.loads(line)
            if "reference_energy_hartree" in data:
                features = [len(data.get("methods", []))]
                X.append(features)
                y.append(data["reference_energy_hartree"])
    return X, y

def main():
    path = Path("data/benchmark.jsonl")
    X, y = load_dataset(path)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model = RandomForestRegressor().fit(X_train, y_train)
    pred = model.predict(X_test)
    print("MAE:", mean_absolute_error(y_test, pred))
    joblib.dump(model, "models/rf_model.pkl")
    print("Model saved to models/rf_model.pkl")

if __name__ == "__main__":
    main()