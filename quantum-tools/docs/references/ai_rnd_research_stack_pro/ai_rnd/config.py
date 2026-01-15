
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
DB_PATH = os.environ.get("AI_RND_DB", os.path.join(ROOT_DIR, "database.db"))
DEFAULT_MIN_RECENCY_DAYS = int(os.environ.get("AI_RND_MIN_RECENCY_DAYS", "730"))
TIMEOUT = int(os.environ.get("AI_RND_TIMEOUT", "30"))
USER_AGENT = os.environ.get("AI_RND_UA", "ai-rnd-agent/1.0 (+https://example.com)")
LOG_INTERACTIONS = True
