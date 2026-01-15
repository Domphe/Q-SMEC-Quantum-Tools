from pathlib import Path
from datetime import date

ARXIV_API = "https://export.arxiv.org/api/query"
USER_AGENT = "QCBD/1.0 (mailto:qcbd@example.com)"

CATEGORIES = [
    "quant-ph",
    "cond-mat.mtrl-sci",
    "physics.atom-ph",
    "physics.optics",
    "physics.chem-ph",
]

FILTER_TERMS = ["quantum", "superconduct", "DFT", "THz"]

DATA_RAW = Path("data/raw")
TODAY = str(date.today())
