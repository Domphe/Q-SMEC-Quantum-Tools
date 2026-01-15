import torch

print('torch', torch.__version__, 'cuda?', torch.cuda.is_available())

try:
    import torch_geometric
    print('torch_geometric OK')
except Exception as e:
    print('torch_geometric import failed:', e)
