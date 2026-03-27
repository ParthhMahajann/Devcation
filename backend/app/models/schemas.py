from pydantic import BaseModel
from typing import Optional, List, Dict, Any


# ─── Request Models ────────────────────────────────────────────────────────────

class DiagnoseRequest(BaseModel):
    symptoms: List[str]

class DrugInteractionRequest(BaseModel):
    drug_names: List[str]

class PatientCreate(BaseModel):
    patient_id: str
    name: str
    age: int
    gender: str
    blood_type: str

class GraphExploreRequest(BaseModel):
    center_type: Optional[str] = None
    center_id: Optional[str] = None
    max_hops: int = 2
    limit_per_hop: int = 20


# ─── Response Models ───────────────────────────────────────────────────────────

class DiseaseResult(BaseModel):
    disease_id: str
    name: str
    icd_code: Optional[str] = None
    severity: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    score: float = 0.0
    match_count: int = 0
    matched_symptoms: Dict[str, float] = {}

class DiagnoseResponse(BaseModel):
    diseases: List[DiseaseResult]
    total: int

class DrugInfo(BaseModel):
    drug_id: str
    name: str
    drug_class: Optional[str] = None
    approval_status: Optional[str] = None
    generic_name: Optional[str] = None

class InteractionEdge(BaseModel):
    from_drug: str
    to_drug: str
    interaction_type: Optional[str] = None
    severity: Optional[str] = None

class DrugInteractionResponse(BaseModel):
    drugs: List[DrugInfo]
    interactions: List[InteractionEdge]

class GraphStats(BaseModel):
    disease_count: int = 0
    symptom_count: int = 0
    drug_count: int = 0
    side_effect_count: int = 0
    gene_count: int = 0
    patient_count: int = 0

class GraphNode(BaseModel):
    id: str
    label: str
    type: str
    properties: Dict[str, Any] = {}

class GraphEdge(BaseModel):
    source: str
    target: str
    type: str
    properties: Dict[str, Any] = {}

class GraphData(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]
