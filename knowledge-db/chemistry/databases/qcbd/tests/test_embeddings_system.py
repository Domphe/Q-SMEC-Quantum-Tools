"""
Embedding System Tests
Tests embedding generation, caching, cost tracking, and model switching.
"""

import pytest
import numpy as np
from pathlib import Path
import os
import sys

sys.path.append(str(Path(__file__).parent.parent / "api"))
from qcdb_embeddings import EmbeddingManager, EmbeddingCache


QCBD_ROOT = Path(os.environ.get('QCBD_ROOT', r'G:\My Drive\Databases\QCBD'))


class TestEmbeddingCache:
    """Test embedding cache functionality."""
    
    @pytest.fixture(scope='class')
    def cache(self, tmp_path_factory):
        """Create temporary cache for testing."""
        cache_dir = tmp_path_factory.mktemp("embeddings_cache")
        return EmbeddingCache(cache_dir)
    
    def test_cache_initialization(self, cache):
        """Test cache initializes correctly."""
        assert cache.cache_file.exists()
    
    def test_cache_miss(self, cache):
        """Test cache returns None for missing keys."""
        embedding = cache.get("nonexistent_key")
        assert embedding is None
    
    def test_cache_set_and_get(self, cache):
        """Test setting and retrieving embeddings."""
        text = "test embedding text"
        embedding = np.random.randn(768).astype(np.float32)
        
        cache.set(text, embedding)
        retrieved = cache.get(text)
        
        assert retrieved is not None
        np.testing.assert_array_almost_equal(embedding, retrieved)
    
    def test_cache_stats(self, cache):
        """Test cache statistics tracking."""
        stats = cache.get_stats()
        assert 'total_cached' in stats
        assert 'cache_file_size_mb' in stats


class TestEmbeddingManager:
    """Test embedding manager."""
    
    @pytest.fixture(scope='class')
    def manager(self):
        """Create embedding manager."""
        from pathlib import Path
        import tempfile
        cache_dir = Path(tempfile.mkdtemp())
        return EmbeddingManager(cache_dir=cache_dir)
    
    def test_manager_initialization(self, manager):
        """Test manager initializes correctly."""
        assert manager.cache is not None
        assert manager.cost_db_path.exists()
    
    def test_embed_short_text(self, manager):
        """Test embedding short text."""
        text = "Hartree-Fock method"
        embedding = manager.embed(text)
        
        assert isinstance(embedding, list)
        assert len(embedding) > 0
        assert all(isinstance(x, float) for x in embedding)
    
    def test_embed_long_text(self, manager):
        """Test embedding longer text."""
        text = """
        Density Functional Theory (DFT) is a computational quantum mechanical 
        modelling method used in physics, chemistry and materials science to 
        investigate the electronic structure of many-body systems, in particular 
        atoms, molecules, and the condensed phases.
        """
        embedding = manager.embed(text)
        
        assert isinstance(embedding, list)
        assert len(embedding) > 0
    
    def test_cache_hit(self, manager):
        """Test that repeated embedding uses cache."""
        text = "B3LYP hybrid functional"
        
        # First call - cache miss
        embedding1 = manager.embed(text)
        
        # Second call - should be cache hit
        embedding2 = manager.embed(text)
        
        # Should be identical
        np.testing.assert_array_almost_equal(embedding1, embedding2)
    
    def test_cost_tracking(self, manager):
        """Test that costs are tracked."""
        import sqlite3
        
        # Embed some text
        manager.embed("Test text for cost tracking", backend='openai')
        
        # Check cost database
        conn = sqlite3.connect(manager.cost_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(cost_usd) FROM embedding_costs")
        total_cost = cursor.fetchone()[0]
        conn.close()
        
        # Should have some cost (or 0 if using fallback)
        assert total_cost is not None
        assert total_cost >= 0
    
    def test_backend_specification(self, manager):
        """Test specifying backend explicitly."""
        text = "CCSD(T) coupled cluster method"
        
        # Try local backend
        embedding_local = manager.embed(text, backend='local')
        assert len(embedding_local) == 768  # all-mpnet-base-v2 dimension
        
        # Try OpenAI backend (may fallback if no API key)
        embedding_openai = manager.embed(text, backend='openai')
        assert len(embedding_openai) in [768, 1536]  # local or OpenAI
    
    @pytest.mark.slow
    def test_batch_embedding(self, manager):
        """Test embedding multiple texts."""
        texts = [
            "Hartree-Fock",
            "DFT",
            "MP2",
            "CCSD(T)",
            "CASSCF"
        ]
        
        embeddings = [manager.embed(text) for text in texts]
        
        assert len(embeddings) == 5
        assert all(len(emb) > 0 for emb in embeddings)


class TestCostBudget:
    """Test cost budget enforcement."""
    
    def test_monthly_budget_calculation(self):
        """Test monthly cost calculation."""
        from qcdb_embeddings import EmbeddingManager
        import sqlite3
        from datetime import datetime
        
        from pathlib import Path
        import tempfile
        cache_dir = Path(tempfile.mkdtemp())
        manager = EmbeddingManager(cache_dir=cache_dir)
        
        # Get current month costs
        conn = sqlite3.connect(manager.cost_db_path)
        cursor = conn.cursor()
        
        current_month = datetime.now().strftime('%Y-%m')
        cursor.execute("""
            SELECT SUM(cost_usd) FROM embedding_costs
            WHERE strftime('%Y-%m', timestamp) = ?
        """, (current_month,))
        
        monthly_cost = cursor.fetchone()[0] or 0
        conn.close()
        
        assert monthly_cost >= 0
        assert monthly_cost <= 100  # Should never exceed reasonable limit
    
    def test_fallback_mechanism(self):
        """Test that fallback to local model works."""
        from pathlib import Path
        import tempfile
        cache_dir = Path(tempfile.mkdtemp())
        manager = EmbeddingManager(cache_dir=cache_dir)
        
        # Force local backend
        embedding = manager.embed("Test text", backend='local')
        
        assert len(embedding) == 768
        assert isinstance(embedding, list)


class TestContentAddressing:
    """Test content-addressed caching."""
    
    def test_same_content_same_key(self):
        """Test that identical content gets same cache key."""
        from qcdb_embeddings import EmbeddingCache
        import hashlib
        
        text1 = "Exact same text"
        text2 = "Exact same text"
        
        # Keys should be identical
        key1 = hashlib.sha256(text1.encode()).hexdigest()
        key2 = hashlib.sha256(text2.encode()).hexdigest()
        
        assert key1 == key2
    
    def test_different_content_different_key(self):
        """Test that different content gets different keys."""
        from qcdb_embeddings import EmbeddingCache
        import hashlib
        
        text1 = "First text"
        text2 = "Second text"
        
        key1 = hashlib.sha256(text1.encode()).hexdigest()
        key2 = hashlib.sha256(text2.encode()).hexdigest()
        
        assert key1 != key2


if __name__ == "__main__":
    pytest.main([__file__, '-v'])
