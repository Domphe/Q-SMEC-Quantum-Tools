from __future__ import annotations
from typing import Literal, Optional, List, Dict, Any
from pydantic import BaseModel, Field

EntityType = Literal["utility","vendor","technology","asset","network","dataset","model","standard","program","site"]
EvidenceType = Literal["webpage","pdf","press_release","case_study","product_sheet","video","rss_item"]

class Evidence(BaseModel):
    evidence_type: EvidenceType
    url: str
    retrieved_at: str
    sha256: str
    title: Optional[str]=None
    publisher: Optional[str]=None

class Entity(BaseModel):
    entity_id: str
    entity_type: EntityType
    name: str
    aliases: List[str]=Field(default_factory=list)
    attributes: Dict[str, Any]=Field(default_factory=dict)
    evidence: List[Evidence]=Field(default_factory=list)

class Event(BaseModel):
    event_id: str
    event_type: str
    occurred_on: Optional[str]=None
    location: Optional[Dict[str,str]]=None
    participants: List[str]=Field(default_factory=list) # entity_ids
    dataflows: List[Dict[str,Any]]=Field(default_factory=list)
    outcomes: Dict[str,Any]=Field(default_factory=dict)
    constraints: List[str]=Field(default_factory=list)
    evidence: List[Evidence]=Field(default_factory=list)

class ResearchRecord(BaseModel):
    record_id: str
    source_id: str
    url: str
    title: Optional[str]=None
    fetched_at: str
    extracted_text: str
    entities: List[Entity]=Field(default_factory=list)
    events: List[Event]=Field(default_factory=list)
