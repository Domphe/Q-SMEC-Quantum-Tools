from __future__ import annotations
import re, datetime, hashlib
from typing import List, Dict, Any
from .schema import Entity, Event, Evidence

# --- Minimal rule-based extractor (v1) ---
# You can replace this with spaCy, LLMs, or your in-house "QuantumAI" models.

COMPANY_PATTERNS = [
  ("vendor.neptune","Neptune Technology Group|Neptune\s+R900"),
  ("vendor.tadiran","Tadiran Batteries|Tadiran"),
  ("vendor.suez","SUEZ|Suez"),
  ("vendor.microsoft","Microsoft"),
  ("vendor.aganova","Aganova|Nautilus"),
  ("vendor.xylem","Xylem"),
  ("vendor.sensus","Sensus|FlexNet"),
  ("vendor.bentley","Bentley Systems|Bentley"),
  ("vendor.krohne","KROHNE")
]

def make_entity_id(prefix: str, name: str) -> str:
    h = hashlib.sha256((prefix+name).encode("utf-8")).hexdigest()[:12]
    return f"{prefix}.{h}"

def extract_entities(text: str, ev: Evidence) -> List[Entity]:
    found=[]
    for prefix, pat in COMPANY_PATTERNS:
        if re.search(pat, text, flags=re.IGNORECASE):
            # normalize canonical names
            canonical = {
              "vendor.neptune":"Neptune Technology Group",
              "vendor.tadiran":"Tadiran Batteries",
              "vendor.suez":"SUEZ",
              "vendor.microsoft":"Microsoft",
              "vendor.aganova":"Aganova",
              "vendor.xylem":"Xylem",
              "vendor.sensus":"Sensus (Xylem brand)",
              "vendor.bentley":"Bentley Systems",
              "vendor.krohne":"KROHNE Inc."
            }[prefix]
            ent = Entity(
                entity_id=make_entity_id(prefix, canonical),
                entity_type="vendor",
                name=canonical,
                aliases=[],
                attributes={},
                evidence=[ev]
            )
            found.append(ent)
    return dedupe_entities(found)

def dedupe_entities(entities: List[Entity]) -> List[Entity]:
    by={}
    for e in entities:
        by.setdefault(e.entity_id, e)
    return list(by.values())

def extract_events(text: str, ev: Evidence) -> List[Event]:
    events=[]
    if "Frisco" in text and ("Neptune" in text or "R900" in text) and ("15-minute" in text or "15 minute" in text):
        events.append(Event(
            event_id="event.frisco_ami_overlay",
            event_type="AMI_overlay_migration",
            occurred_on=None,
            location={"city":"Frisco","state":"Texas","country":"USA"},
            participants=[],
            dataflows=[{
              "sampling_interval":"15m",
              "flow":"endpoint->collector->headend->mdm/analytics",
              "topology":"zonal_collectors",
              "zones":9
            }],
            outcomes={
              "asset_preservation":True,
              "leak_detection_enabled":True,
              "customer_engagement_enabled":True
            },
            constraints=["Cybersecurity details not provided in summary"],
            evidence=[ev]
        ))
    if "Dublin" in text and ("Nautilus" in text or "Aganova" in text) and ("deep-learning" in text or "deep learning" in text):
        events.append(Event(
            event_id="event.dublin_trunk_main_acoustic_ai",
            event_type="in_pipe_acoustic_inspection_ai",
            occurred_on=None,
            location={"city":"Dublin","country":"Ireland"},
            participants=[],
            dataflows=[{
              "flow":"in-pipe sensing->acoustic signal->cloud model->anomaly report",
              "modality":"acoustic",
              "ai":"deep_learning"
            }],
            outcomes={
              "leak_localization":True,
              "structural_anomaly_detection":True,
              "service_disruption":False
            },
            constraints=["Inspection is periodic; not continuous monitoring"],
            evidence=[ev]
        ))
    if "Walla Walla" in text and ("FlexNet" in text or "Sensus" in text or "PRV" in text):
        events.append(Event(
            event_id="event.walla_walla_dma_prv_instrumentation",
            event_type="dma_pressure_management_telemetry",
            occurred_on=None,
            location={"city":"Walla Walla","state":"Washington","country":"USA"},
            participants=[],
            dataflows=[{
              "flow":"prv+sensors->flexnet->monitoring/analytics",
              "telemetry":"near_real_time"
            }],
            outcomes={
              "non_revenue_water_below_10_percent":"claimed_in_summary",
              "major_leak_fixed":"65 gpm (claimed)"
            },
            constraints=["Hydraulic model alignment required for best results"],
            evidence=[ev]
        ))
    return events
