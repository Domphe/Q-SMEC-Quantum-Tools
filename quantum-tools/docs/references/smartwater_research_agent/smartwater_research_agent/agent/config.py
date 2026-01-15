from __future__ import annotations
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Config:
    db_url: str = os.getenv("DB_URL","sqlite:///data/agent.db")
    user_agent: str = os.getenv("USER_AGENT","SmartWaterResearchAgent/1.0")
    timeout_secs: int = int(os.getenv("REQUEST_TIMEOUT_SECS","30"))
    rate_limit_rps: float = float(os.getenv("RATE_LIMIT_RPS","0.2"))
    data_dir: str = os.getenv("DATA_DIR","data")
    respect_robots: bool = os.getenv("RESPECT_ROBOTS","true").lower() in ("1","true","yes","y")

cfg = Config()
