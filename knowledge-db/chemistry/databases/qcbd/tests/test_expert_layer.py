import pytest
from expert import load_expert_graph
from expert.query_api import rank_methods, filter_methods, suggest
from expert.context_builder import build_context
from expert import reasoning


def test_graph_load():
    g = load_expert_graph.load_graph()
    assert 'Methods' in g
    # Physics or chemistry extension presence (lenient)
    extension_keys = {'Hamiltonians','BasisSets','ManyBodyMethods','QFTApproaches'}
    assert any(k in g for k in extension_keys)
    assert 'expert_layer' in g['metadata'] and 'added_entity_types' in g['metadata']['expert_layer']


def test_method_ranking():
    methods = rank_methods(limit=5)
    assert isinstance(methods, list)
    if methods:
        assert 'composite_score' in methods[0]


def test_reasoning_top_methods():
    top = reasoning.ranked_methods(limit=3)
    assert isinstance(top, list)
    if top:
        assert 'efficiency_score' in top[0]


def test_context_builder():
    ctx = build_context("electron correlation")
    assert ctx['query'] == "electron correlation"
    assert 'methods' in ctx and 'concepts' in ctx
    assert isinstance(ctx['methods'], list)
    assert 'metadata' in ctx and ctx['metadata'].get('source') == 'expert-layer'


def test_query_filters():
    res = filter_methods(min_accuracy=0)
    assert isinstance(res, list)


def test_suggestion():
    sugg = suggest('electron correlation')
    assert isinstance(sugg, list)
