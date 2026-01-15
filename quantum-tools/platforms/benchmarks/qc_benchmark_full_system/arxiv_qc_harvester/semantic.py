from sentence_transformers import SentenceTransformer, util
import torch

model = SentenceTransformer("all-MiniLM-L6-v2")

def rank_by_semantic_similarity(entries, query, top_k=10):
    texts = [entry["title"] + " " + entry["abstract"] for entry in entries]
    embeddings = model.encode(texts, convert_to_tensor=True)
    query_embedding = model.encode(query, convert_to_tensor=True)
    scores = util.pytorch_cos_sim(query_embedding, embeddings)[0]
    top_results = torch.topk(scores, k=min(top_k, len(scores)))
    top_indices = top_results.indices.cpu().numpy()
    return [entries[i] for i in top_indices]
