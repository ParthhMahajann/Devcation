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
    body_system_count: int = 0
    medical_test_count: int = 0
    biomarker_count: int = 0
    risk_factor_count: int = 0
    pathway_count: int = 0
    drug_class_count: int = 0
    procedure_count: int = 0
    # Edge counts
    has_symptom_count: int = 0
    treats_count: int = 0
    interacts_count: int = 0
    associated_count: int = 0
    comorbid_count: int = 0


class PgxAlert(BaseModel):
    drug_name: str
    gene_symbol: str
    metabolism_type: Optional[str] = None
    impact_on_efficacy: Optional[str] = None
    patient_phenotype: Optional[str] = None


class PgxReport(BaseModel):
    patient_id: str
    high_risk_drugs: List[str] = []
    patient_phenotypes: List[str] = []
    pgx_matrix: Dict[str, str] = {}
    alerts: List[PgxAlert] = []


class ProgressionNode(BaseModel):
    disease_id: str
    name: str
    severity: Optional[str] = None
    cumulative_risk: float = 0.0
    min_years: float = 0.0
    progression_chain: List[str] = []
    prevention_notes: List[str] = []


class ProgressionRisk(BaseModel):
    patient_id: str
    active_diseases: List[DiseaseResult] = []
    progression_stages: List[ProgressionNode] = []
    critical_chains: List[str] = []


class SafetyCheck(BaseModel):
    patient_id: str
    critical_count: int = 0
    major_count: int = 0
    critical_alerts: List[str] = []
    major_alerts: List[str] = []
    moderate_alerts: List[str] = []
    info_alerts: List[str] = []

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
