from expert.semantic_search import build_embeddings, search_methods

def test_semantic_search_runs():
    emb = build_embeddings(persist=False)
    # emb may be empty if methods missing; should not raise
    results = search_methods('density functional', top_k=5)
    assert isinstance(results, list)
    if results:
        assert 'similarity' in results[0]
