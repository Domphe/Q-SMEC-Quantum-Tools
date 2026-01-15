from sentence_transformers import SentenceTransformer
import json, os

model = SentenceTransformer('all-MiniLM-L6-v2')
PREPRINT_PATH = "data/preprints/preprints.jsonl"
EMBED_PATH = "embeddings/preprints_embeddings.jsonl"

def embed():
    if not os.path.exists(PREPRINT_PATH):
        print("Preprint file not found.")
        return
    embeddings = []
    with open(PREPRINT_PATH, 'r') as f:
        for line in f:
            record = json.loads(line)
            text = record.get("title", "") + " " + record.get("abstract", "")
            vec = model.encode(text).tolist()
            record['embedding'] = vec
            embeddings.append(record)
    with open(EMBED_PATH, 'w') as out:
        for rec in embeddings:
            out.write(json.dumps(rec) + "\n")
    print(f"Stored embeddings: {EMBED_PATH}")

if __name__ == "__main__":
    embed()