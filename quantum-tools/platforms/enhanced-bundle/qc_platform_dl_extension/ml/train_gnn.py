import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.data import Data, DataLoader
from torch_geometric.nn import GCNConv
import json
from pathlib import Path

class SimpleGCN(nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super(SimpleGCN, self).__init__()
        self.conv1 = GCNConv(in_channels, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, out_channels)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        x = F.relu(self.conv1(x, edge_index))
        x = self.conv2(x, edge_index)
        return x

def load_synthetic_dataset(jsonl_path):
    data_list = []
    with open(jsonl_path) as f:
        for line in f:
            mol = json.loads(line)
            x = torch.tensor([[float(len(mol["methods"]))]], dtype=torch.float)  # node features
            edge_index = torch.tensor([[0, 0], [0, 0]], dtype=torch.long)  # dummy self-loop
            y = torch.tensor([[mol["reference_energy_hartree"]]], dtype=torch.float)
            data = Data(x=x, edge_index=edge_index, y=y)
            data_list.append(data)
    return data_list

def main():
    dataset_path = Path("data/benchmark.jsonl")
    dataset = load_synthetic_dataset(dataset_path)
    loader = DataLoader(dataset, batch_size=2)

    model = SimpleGCN(in_channels=1, hidden_channels=4, out_channels=1)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    loss_fn = nn.MSELoss()

    for epoch in range(50):
        for batch in loader:
            out = model(batch)
            loss = loss_fn(out, batch.y)
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
        if epoch % 10 == 0:
            print(f"Epoch {epoch}: Loss = {loss.item():.4f}")
    torch.save(model.state_dict(), "models/gcn_model.pt")
    print("Saved model to models/gcn_model.pt")

if __name__ == "__main__":
    main()