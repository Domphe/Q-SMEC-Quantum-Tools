
from typing import List, Optional, Literal
from pydantic import BaseModel
from datetime import date

class PatentMetadata(BaseModel):
    id: str
    type: Literal["patent"]
    title: str
    inventors: List[str]
    assignee: Optional[str]
    abstract: Optional[str]
    publication_number: str
    application_number: Optional[str]
    filing_date: Optional[str]
    publication_date: Optional[str]
    jurisdiction: str  # e.g., "US", "EP", "WO"
    kind_code: Optional[str]
    classification: List[str]
    related_to: List[str]
    domains: List[str]
    keywords: List[str]
    provenance: str
    trust_tier: Literal["B"]
    open_access: bool
    last_verified: date

class ExperimentalProtocol(BaseModel):
    id: str
    type: Literal["protocol"]
    title: str
    authors: List[str]
    source: str
    url: str
    doi: Optional[str]
    abstract: Optional[str]
    steps: List[str]
    materials: List[str]
    estimated_time: Optional[str]
    license: Optional[str]
    domains: List[str]
    trust_tier: Literal["B"]
    open_access: bool
    related_to: List[str]
    last_verified: date

class DissertationMetadata(BaseModel):
    id: str
    type: Literal["dissertation"]
    title: str
    author: str
    institution: str
    degree: str
    year: int
    advisors: Optional[List[str]]
    abstract: Optional[str]
    url: Optional[str]
    doi: Optional[str]
    keywords: List[str]
    related_to: List[str]
    provenance: str
    domains: List[str]
    trust_tier: Literal["B"]
    open_access: bool
    last_verified: date
