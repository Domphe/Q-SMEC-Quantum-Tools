"""Command-line interface for expert layer.

Usage examples:
  python -m expert.expert_cli rank --limit 5
  python -m expert.expert_cli search "density functional"
  python -m expert.expert_cli context "electron correlation"
  python -m expert.expert_cli snapshot --name pre_semantic
  python -m expert.expert_cli gap
  python -m expert.expert_cli semantic "coupled cluster"
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
from expert.query_api import rank_methods, suggest
from expert.context_builder import build_context
from expert import reasoning
from expert.semantic_search import search_methods
from expert.versioning import create_snapshot
from expert.gap_analysis import analyze as gap_analyze

def cmd_rank(args):
    res = rank_methods(limit=args.limit)
    print(json.dumps(res, indent=2))

def cmd_semantic(args):
    res = search_methods(args.query, top_k=args.top_k)
    print(json.dumps(res, indent=2))

def cmd_context(args):
    ctx = build_context(args.query)
    print(json.dumps(ctx, indent=2))

def cmd_snapshot(args):
    path = create_snapshot(args.name)
    print(json.dumps({'snapshot': str(path)}, indent=2))

def cmd_gap(args):
    report = gap_analyze()
    print(json.dumps(report, indent=2))

def cmd_suggest(args):
    res = suggest(args.goal)
    print(json.dumps(res, indent=2))

def build_parser():
    p = argparse.ArgumentParser(description="Expert Layer CLI")
    sub = p.add_subparsers(dest='command', required=True)

    r = sub.add_parser('rank', help='Rank methods by composite score')
    r.add_argument('--limit', type=int, default=5)
    r.set_defaults(func=cmd_rank)

    s = sub.add_parser('semantic', help='Semantic search over methods')
    s.add_argument('query')
    s.add_argument('--top-k', type=int, default=5)
    s.set_defaults(func=cmd_semantic)

    c = sub.add_parser('context', help='Build context pack for query')
    c.add_argument('query')
    c.set_defaults(func=cmd_context)

    snap = sub.add_parser('snapshot', help='Create snapshot of current graph')
    snap.add_argument('--name', type=str, default=None)
    snap.set_defaults(func=cmd_snapshot)

    gap = sub.add_parser('gap', help='Run gap analysis')
    gap.set_defaults(func=cmd_gap)

    sg = sub.add_parser('suggest', help='Suggest methods for goal text')
    sg.add_argument('goal')
    sg.set_defaults(func=cmd_suggest)

    return p

def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
