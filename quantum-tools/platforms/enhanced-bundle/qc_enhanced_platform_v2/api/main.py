
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class MoleculeInput(BaseModel):
    smiles: str

@app.post("/predict")
def predict(input_data: MoleculeInput):
    # Real prediction logic placeholder
    return {"prediction": "dipole=1.25 D", "molecule": input_data.smiles}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
