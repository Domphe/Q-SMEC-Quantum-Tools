
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"msg": "QSMEC API running"}

@app.get("/predict")
def predict(smiles: str):
    return {"input": smiles, "prediction": "placeholder_prediction"}
