
from typing import List, Optional
from pydantic import BaseModel

class QuantumChemistryMethod(BaseModel):
    id: str
    domain: str
    name: str
    category: str
    brief: str
    long_description: str
    inputs: List[str]
    outputs: List[str]
    equation_refs: List[str]
    workflow_refs: List[str]
    software_implementations: List[str]
    complexity: str
    strengths: str
    limitations: str
    typical_use_cases: str
    standard_refs: List[str]
    last_reviewed: str
    accuracy_level: Optional[str]
    is_multi_reference_safe: Optional[bool]
    has_analytic_gradients: Optional[bool]
    available_in_qcdb: Optional[bool]
    citation_count: Optional[int]
    known_issues: Optional[str]
    related_methods: Optional[List[str]]
    preceding_method: Optional[str]
    successor_method: Optional[str]
