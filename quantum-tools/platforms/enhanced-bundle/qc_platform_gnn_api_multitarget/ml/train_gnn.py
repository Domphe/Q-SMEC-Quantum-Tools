import torch
from torch_geometric.nn import SchNet
from torch_geometric.data import DataLoader, Data
import pickle

# Dummy dataset (should be replaced with real molecules from PubChem/NIST)
def load_dummy_dataset():
    x = torch.tensor([[1], [8]], dtype=torch.long)
    pos = torch.tensor([[0.0, 0.0, 0.0], [0.0, 0.0, 1.0]], dtype=torch.float)
    y = torch.tensor([[0.0, 1.5, 0.2]])  # multi-target: energy, dipole, frequency
    return [Data(z=x.view(-1), pos=pos, y=y)]

dataset = load_dummy_dataset()
loader = DataLoader(dataset, batch_size=1)

model = SchNet(hidden_channels=64, num_filters=64, num_interactions=3)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

model.train()
for epoch in range(50):
    for batch in loader:
        optimizer.zero_grad()
        pred = model(batch.z, batch.pos, batch.batch if hasattr(batch, 'batch') else None)
        loss = torch.nn.functional.mse_loss(pred, batch.y)
        loss.backward()
        optimizer.step()
    print(f"Epoch {epoch+1}: Loss = {loss.item():.4f}")

# Save model
torch.save(model.state_dict(), "ml/gnn_model.pt")
print("Model saved to ml/gnn_model.pt")