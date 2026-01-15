from pydantic import BaseModel, Field
from typing import Optional, List

class BenchmarkRecord(BaseModel):
    id: str
    benchmark_set: str
    system_name: str
    molecular_formula: str
    reference_energy_kcal: float
    level_of_theory: str
    basis_set: Optional[str]
    property_type: str
    doi: Optional[str]
    journal: Optional[str]
    published: Optional[str]
    smiles: Optional[str]
    inchi: Optional[str]
    inchikey: Optional[str]
    tags: Optional[List[str]]
