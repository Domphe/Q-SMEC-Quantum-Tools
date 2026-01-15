"""
QCDB Embedding Manager
Handles text embeddings with dual backend support and intelligent caching.
"""

import os
import hashlib
import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import numpy as np
import h5py

try:
    from sentence_transformers import SentenceTransformer
    HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    HAS_SENTENCE_TRANSFORMERS = False

try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False


class EmbeddingCache:
    """Content-addressed cache for embedding vectors."""
    
    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file = self.cache_dir / "embeddings_cache.h5"
        self.index_file = self.cache_dir / "cache_index.json"
        self.index = self._load_index()
    
    def _load_index(self) -> Dict:
        """Load cache index."""
        if self.index_file.exists():
            with open(self.index_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_index(self):
        """Save cache index."""
        with open(self.index_file, 'w') as f:
            json.dump(self.index, f, indent=2)
    
    def _compute_hash(self, text: str, model: str) -> str:
        """Compute content hash for text + model combination."""
        content = f"{model}:{text}"
        return hashlib.sha256(content.encode()).hexdigest()
    
    def get(self, text: str, model: str) -> Optional[np.ndarray]:
        """Retrieve embedding from cache."""
        cache_key = self._compute_hash(text, model)
        
        if cache_key in self.index:
            try:
                with h5py.File(self.cache_file, 'r') as f:
                    if cache_key in f:
                        return np.array(f[cache_key])
            except Exception:
                pass
        
        return None
    
    def put(self, text: str, model: str, embedding: np.ndarray):
        """Store embedding in cache."""
        cache_key = self._compute_hash(text, model)
        
        # Store embedding in HDF5
        with h5py.File(self.cache_file, 'a') as f:
            if cache_key in f:
                del f[cache_key]
            f.create_dataset(cache_key, data=embedding, compression='gzip')
        
        # Update index
        self.index[cache_key] = {
            'model': model,
            'text_preview': text[:100],
            'created_at': datetime.now().isoformat(),
            'dim': len(embedding)
        }
        self._save_index()
    
    def stats(self) -> Dict:
        """Get cache statistics."""
        return {
            'total_cached': len(self.index),
            'cache_size_mb': self.cache_file.stat().st_size / (1024 * 1024) if self.cache_file.exists() else 0,
            'models': list(set(entry['model'] for entry in self.index.values()))
        }


class EmbeddingManager:
    """Manage embeddings with dual backend and cost tracking."""
    
    def __init__(
        self,
        cache_dir: Path,
        openai_api_key: Optional[str] = None,
        monthly_budget_usd: float = 50.0
    ):
        self.cache = EmbeddingCache(cache_dir)
        self.monthly_budget = monthly_budget_usd
        
        # Initialize OpenAI client
        self.openai_client = None
        if HAS_OPENAI and openai_api_key:
            self.openai_client = OpenAI(api_key=openai_api_key)
        
        # Initialize local model (lazy loaded)
        self._local_model = None
        self._local_model_name = "sentence-transformers/all-mpnet-base-v2"
        
        # Cost tracking
        self.cost_db_path = cache_dir.parent / "embedding_costs.db"
        self._init_cost_tracking()
    
    def _init_cost_tracking(self):
        """Initialize cost tracking database."""
        import sqlite3
        conn = sqlite3.connect(self.cost_db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS embedding_costs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                model TEXT NOT NULL,
                tokens INTEGER NOT NULL,
                cost_usd REAL NOT NULL,
                month TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()
    
    def _log_cost(self, model: str, tokens: int, cost: float):
        """Log embedding cost."""
        import sqlite3
        conn = sqlite3.connect(self.cost_db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO embedding_costs (timestamp, model, tokens, cost_usd, month)
            VALUES (?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            model,
            tokens,
            cost,
            datetime.now().strftime('%Y-%m')
        ))
        conn.commit()
        conn.close()
    
    def _get_monthly_cost(self) -> float:
        """Get total cost for current month."""
        import sqlite3
        conn = sqlite3.connect(self.cost_db_path)
        cursor = conn.cursor()
        current_month = datetime.now().strftime('%Y-%m')
        cursor.execute("""
            SELECT SUM(cost_usd) FROM embedding_costs WHERE month = ?
        """, (current_month,))
        result = cursor.fetchone()[0]
        conn.close()
        return result if result else 0.0
    
    def _get_local_model(self) -> SentenceTransformer:
        """Lazy load local embedding model."""
        if self._local_model is None:
            if not HAS_SENTENCE_TRANSFORMERS:
                raise RuntimeError("sentence-transformers not installed")
            self._local_model = SentenceTransformer(self._local_model_name)
        return self._local_model
    
    def _embed_openai(self, texts: List[str], model: str = "text-embedding-3-large") -> List[np.ndarray]:
        """Generate embeddings using OpenAI API."""
        if not self.openai_client:
            raise RuntimeError("OpenAI client not initialized")
        
        # Check budget
        monthly_cost = self._get_monthly_cost()
        if monthly_cost >= self.monthly_budget:
            raise RuntimeError(f"Monthly budget exceeded: ${monthly_cost:.2f} / ${self.monthly_budget:.2f}")
        
        # Generate embeddings
        response = self.openai_client.embeddings.create(
            input=texts,
            model=model
        )
        
        # Calculate cost (approximate)
        total_tokens = sum(len(text.split()) * 1.3 for text in texts)  # Rough estimate
        cost_per_1k = 0.00013 if "large" in model else 0.00002
        cost = (total_tokens / 1000) * cost_per_1k
        
        self._log_cost(model, int(total_tokens), cost)
        
        return [np.array(item.embedding) for item in response.data]
    
    def _embed_local(self, texts: List[str]) -> List[np.ndarray]:
        """Generate embeddings using local model."""
        model = self._get_local_model()
        embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
        return [emb for emb in embeddings]
    
    def embed(
        self,
        texts: List[str],
        model: str = "auto",
        use_cache: bool = True
    ) -> List[np.ndarray]:
        """
        Generate embeddings for texts.
        
        Args:
            texts: List of texts to embed
            model: Model to use ("auto", "openai", "local", or specific model name)
            use_cache: Whether to use caching
        
        Returns:
            List of embedding vectors
        """
        embeddings = []
        texts_to_embed = []
        indices_to_embed = []
        
        # Check cache first
        if use_cache:
            for i, text in enumerate(texts):
                cached = self.cache.get(text, model if model != "auto" else "openai")
                if cached is not None:
                    embeddings.append((i, cached))
                else:
                    texts_to_embed.append(text)
                    indices_to_embed.append(i)
        else:
            texts_to_embed = texts
            indices_to_embed = list(range(len(texts)))
        
        # Generate new embeddings if needed
        if texts_to_embed:
            # Determine which backend to use
            if model == "auto":
                # Try OpenAI first if budget allows, fall back to local
                monthly_cost = self._get_monthly_cost()
                if self.openai_client and monthly_cost < self.monthly_budget:
                    try:
                        new_embeddings = self._embed_openai(texts_to_embed)
                        model_used = "text-embedding-3-large"
                    except Exception:
                        new_embeddings = self._embed_local(texts_to_embed)
                        model_used = self._local_model_name
                else:
                    new_embeddings = self._embed_local(texts_to_embed)
                    model_used = self._local_model_name
            elif model == "openai" or "text-embedding" in model:
                new_embeddings = self._embed_openai(texts_to_embed, model)
                model_used = model
            else:
                new_embeddings = self._embed_local(texts_to_embed)
                model_used = self._local_model_name
            
            # Cache new embeddings
            if use_cache:
                for text, emb in zip(texts_to_embed, new_embeddings):
                    self.cache.put(text, model_used, emb)
            
            # Add to results
            for idx, emb in zip(indices_to_embed, new_embeddings):
                embeddings.append((idx, emb))
        
        # Sort by original index and return
        embeddings.sort(key=lambda x: x[0])
        return [emb for _, emb in embeddings]
    
    def get_stats(self) -> Dict:
        """Get embedding system statistics."""
        cache_stats = self.cache.stats()
        monthly_cost = self._get_monthly_cost()
        
        return {
            'cache': cache_stats,
            'monthly_cost_usd': monthly_cost,
            'budget_remaining_usd': self.monthly_budget - monthly_cost,
            'budget_utilization_pct': (monthly_cost / self.monthly_budget) * 100,
            'openai_available': self.openai_client is not None,
            'local_model': self._local_model_name
        }


def main():
    """Test embedding manager."""
    qcbd_root = Path(os.environ.get('QCBD_ROOT', r'G:\My Drive\Databases\QCBD'))
    cache_dir = qcbd_root / "embeddings_cache"
    
    # Initialize manager
    manager = EmbeddingManager(cache_dir)
    
    # Test embedding
    test_texts = [
        "Hartree-Fock is a mean-field approximation to quantum mechanics.",
        "Density functional theory uses functionals of the electron density.",
        "Coupled cluster methods provide high accuracy for electron correlation."
    ]
    
    print("Testing embedding system...")
    embeddings = manager.embed(test_texts, model="local")
    print(f"✓ Generated {len(embeddings)} embeddings")
    print(f"  Dimensions: {len(embeddings[0])}")
    
    # Print stats
    stats = manager.get_stats()
    print("\nEmbedding System Stats:")
    print(f"  Cached embeddings: {stats['cache']['total_cached']}")
    print(f"  Cache size: {stats['cache']['cache_size_mb']:.2f} MB")
    print(f"  Monthly cost: ${stats['monthly_cost_usd']:.4f}")
    print(f"  Budget remaining: ${stats['budget_remaining_usd']:.2f}")


if __name__ == "__main__":
    main()
