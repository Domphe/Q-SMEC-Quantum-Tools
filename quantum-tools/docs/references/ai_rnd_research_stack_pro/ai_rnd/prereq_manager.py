
import importlib, subprocess, sys

REQUIRED = [
    "requests",
    "httpx",
    "beautifulsoup4",
    "lxml",
    "readability_lxml",
    "pdfminer.six",
    "pandas",
    "python-dateutil",
    "tldextract",
    "pyyaml"
]

def ensure_prerequisites(python=sys.executable):
    missing = []
    for pkg in REQUIRED:
        try:
            importlib.import_module(pkg.replace('-', '_').replace('.six','_six'))
        except Exception:
            missing.append(pkg)
    if missing:
        print(f"[auto-install] Missing packages: {missing}")
        cmd = [python, "-m", "pip", "install", "--upgrade"] + missing
        subprocess.check_call(cmd)
        print("[auto-install] Completed.")
    else:
        print("[auto-install] All prerequisites present.")
