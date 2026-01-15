import json
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

def load_data(jsonl_path):
    X, y = [], []
    with open(jsonl_path, "r") as f:
        for line in f:
            entry = json.loads(line)
            if "reference_energy_hartree" in entry:
                props = [len(entry.get("methods", []))]
                X.append(props)
                y.append(entry["reference_energy_hartree"])
    return X, y

def main():
    data_path = Path("data/benchmarks/benchmark_dataset.json")
    X, y = load_data(data_path)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)
    model = RandomForestRegressor().fit(X_train, y_train)
    preds = model.predict(X_test)
    print("MAE:", mean_absolute_error(y_test, preds))
    model_path = Path("models/benchmark_rf_model.pkl")
    model_path.parent.mkdir(exist_ok=True)
    import joblib; joblib.dump(model, model_path)
    print(f"Model saved to: {model_path}")
if __name__ == "__main__":
    main()