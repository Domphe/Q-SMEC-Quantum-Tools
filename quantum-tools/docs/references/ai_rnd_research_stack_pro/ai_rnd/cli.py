
import argparse, json, sys
from .prereq_manager import ensure_prerequisites
from .ingest import ingest_url
from .db import get_conn, log_interaction

def cmd_setup(args):
    ensure_prerequisites()
    print("[setup] OK")

def cmd_ingest_url(args):
    result = ingest_url(args.url, project_id=args.project, doc_type=args.type, min_recency_days=args.recency_days)
    print(json.dumps(result, indent=2))

def cmd_log(args):
    conn = get_conn()
    log_interaction(conn, args.project, args.mode, args.participants, args.summary, args.actions)
    print("[log] recorded.")

def cmd_seed(args):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO country(iso_code,name) VALUES('US','United States'),('BG','Bulgaria'),('TR','Turkey'),('EU','European Union')")
    conn.commit()
    print("[seed] countries seeded.")

def build_parser():
    p = argparse.ArgumentParser(prog="ai-rnd", description="AI R&D Research & Execution CLI")
    sub = p.add_subparsers()

    ps = sub.add_parser("setup", help="Auto-install prerequisites")
    ps.set_defaults(func=cmd_setup)

    pi = sub.add_parser("ingest-url", help="Ingest a URL (with trust & freshness checks)")
    pi.add_argument("url", help="URL to fetch")
    pi.add_argument("--project", type=int, default=None, help="Project ID to attach")
    pi.add_argument("--type", default="web", help="Document type")
    pi.add_argument("--recency-days", type=int, default=730, help="Require updated content within N days")
    pi.set_defaults(func=cmd_ingest_url)

    pl = sub.add_parser("log", help="Log an interaction note")
    pl.add_argument("--project", type=int, required=True)
    pl.add_argument("--mode", default="note")
    pl.add_argument("--participants", default="ai_agent")
    pl.add_argument("--summary", required=True)
    pl.add_argument("--actions", default="")
    pl.set_defaults(func=cmd_log)

    pq = sub.add_parser("seed", help="Seed minimal reference data")
    pq.set_defaults(func=cmd_seed)

    return p

def main(argv=None):
    argv = argv or sys.argv[1:]
    parser = build_parser()
    args = parser.parse_args(argv)
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()


from .harvesters import harvest_cordis, harvest_grants_gov
from .pdf_ingest import ingest_pdf
from .export_helper import draft_export_classification
from .mitigator import mitigate_sources

def cmd_harvest_cordis(args):
    res = harvest_cordis(args.query, args.date_from, args.date_to, args.max)
    print(json.dumps(res, indent=2))

def cmd_harvest_grants(args):
    res = harvest_grants_gov(args.keyword, args.date_from, args.date_to, args.max)
    print(json.dumps(res, indent=2))

def cmd_ingest_pdf(args):
    res = ingest_pdf(args.path, args.project, args.source_url, args.last_modified, args.recency_days)
    print(json.dumps(res, indent=2))

def cmd_classify_export(args):
    res = draft_export_classification(args.tech_id, args.regime, args.hint)
    print(json.dumps(res, indent=2))

def cmd_mitigate(args):
    res = mitigate_sources(args.project)
    print(json.dumps(res, indent=2))

_old_bp = build_parser
def build_parser():
    p = _old_bp()
    sub = p._subparsers._actions[-1]

    pc = sub.add_parser("harvest-cordis", help="Harvest open calls from CORDIS (EU)")
    pc.add_argument("--query", required=True)
    pc.add_argument("--date-from", dest="date_from")
    pc.add_argument("--date-to", dest="date_to")
    pc.add_argument("--max", type=int, default=50)
    pc.set_defaults(func=cmd_harvest_cordis)

    pg = sub.add_parser("harvest-grants", help="Harvest open calls from Grants.gov (US)")
    pg.add_argument("--keyword", required=True)
    pg.add_argument("--date-from", dest="date_from")
    pg.add_argument("--date-to", dest="date_to")
    pg.add_argument("--max", type=int, default=50)
    pg.set_defaults(func=cmd_harvest_grants)

    pp = sub.add_parser("ingest-pdf", help="Ingest a local PDF (optional source URL and last-modified ISO date)")
    pp.add_argument("path")
    pp.add_argument("--project", type=int, default=None)
    pp.add_argument("--source-url")
    pp.add_argument("--last-modified", dest="last_modified")
    pp.add_argument("--recency-days", type=int, default=730)
    pp.set_defaults(func=cmd_ingest_pdf)

    pe = sub.add_parser("classify-export", help="Draft ECCN/USML classification and open approval gate")
    pe.add_argument("--tech-id", type=int, required=True)
    pe.add_argument("--regime", choices=["ITAR","EAR","EU Dual-Use"], required=True)
    pe.add_argument("--hint", default="")
    pe.set_defaults(func=cmd_classify_export)

    pm = sub.add_parser("mitigate-sources", help="Open risk items for untrusted/stale sources")
    pm.add_argument("--project", type=int, default=None)
    pm.set_defaults(func=cmd_mitigate)

    return p

from .cli import main as _orig_main
def main(argv=None):
    p = build_parser()
    args = p.parse_args(argv)
    if hasattr(args, "func"):
        args.func(args)
    else:
        p.print_help()
