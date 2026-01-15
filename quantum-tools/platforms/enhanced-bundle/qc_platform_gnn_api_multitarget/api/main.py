from fastapi import FastAPI
from pydantic import BaseModel
import torch
from torch_geometric.nn import SchNet
from torch_geometric.data import Data
import numpy as np

app = FastAPI()

class MoleculeInput(BaseModel):
    atomic_numbers: list
    positions: list

@app.on_event("startup")
def load_model():
    global model
    model = SchNet(hidden_channels=64, num_filters=64, num_interactions=3)
    model.load_state_dict(torch.load("ml/gnn_model.pt"))
    model.eval()

@app.post("/predict/")
def predict(input: MoleculeInput):
    x = torch.tensor(input.atomic_numbers, dtype=torch.long).view(-1)
    pos = torch.tensor(input.positions, dtype=torch.float)
    data = Data(z=x, pos=pos)
    with torch.no_grad():
        pred = model(data.z, data.pos, batch=None).view(-1).tolist()
    return {"predictions": pred, "targets": ["energy", "dipole", "vibrational_frequency"]}