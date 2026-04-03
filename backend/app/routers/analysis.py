import logging
from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List
from app.models.schemas import SafetyCheck
from app.services.tigergraph_service import TigerGraphService
from app.dependencies import get_tg_service

logger = logging.getLogger(__name__)
router = APIRouter()


# ── Pharmacogenomics ──────────────────────────────────────────────────────────

@router.get("/{patient_id}/pgx")
def pharmacogenomics_report(
    patient_id: str,
    tg: TigerGraphService = Depends(get_tg_service),
):
    """
    Personalised pharmacogenomics report.
    Shows which of the patient's medications are affected by their gene variants
    (CYP2D6, CYP3A4, VKORC1 etc.) and flags efficacy/toxicity risks.
    """
    raw = tg.pharmacogenomics_report(patient_id)
    if not raw:
        return {"patient_id": patient_id, "pgx_report": {}}

    result = raw[0] if isinstance(raw, list) else raw
    return {
        "patient_id": patient_id,
        "high_risk_drugs":    result.get("@@high_risk_drugs", []),
        "patient_phenotypes": result.get("@@patient_phenotypes", []),
        "pgx_matrix":         result.get("@@pgx_matrix", {}),
        "drugs":              result.get("drugs", []),
        "at_risk_genes":      result.get("at_risk_genes", []),
        "patient_variants":   result.get("patient_variants", []),
    }


# ── Disease Progression Risk ──────────────────────────────────────────────────

@router.get("/{patient_id}/progression")
def disease_progression_risk(
    patient_id: str,
    max_depth: int = Query(3, ge=1, le=5),
    tg: TigerGraphService = Depends(get_tg_service),
):
    """
    BFS traversal on PROGRESSES_TO edges from all the patient's active diseases.
    Returns risk chains with cumulative probability and time estimates.
    """
    raw = tg.disease_progression_risk(patient_id, max_depth)
    if not raw:
        return {"patient_id": patient_id, "progression": {}}

    result = raw[0] if isinstance(raw, list) else raw
    return {
        "patient_id":         patient_id,
        "active_diseases":    result.get("active_diseases", []),
        "progression_stages": result.get("all_stages", []),
        "risk_summary":       result.get("@@risk_summary", {}),
        "critical_chains":    result.get("@@critical_chains", []),
    }


# ── Pre-Prescription Safety Check ────────────────────────────────────────────

@router.post("/{patient_id}/safety-check", response_model=SafetyCheck)
def contraindication_safety_check(
    patient_id: str,
    proposed_drugs: List[str],
    tg: TigerGraphService = Depends(get_tg_service),
):
    """
    Pre-prescription safety check.
    Given a patient and a list of proposed drug names, returns severity-ordered
    alerts covering: drug-drug interactions, contraindications, known allergies,
    black-box warnings, pregnancy categories, and pharmacogenomics flags.
    """
    if not proposed_drugs:
        raise HTTPException(status_code=422, detail="proposed_drugs must not be empty")

    raw = tg.contraindication_safety_check(patient_id, proposed_drugs)
    if not raw:
        return SafetyCheck(patient_id=patient_id)

    result = raw[0] if isinstance(raw, list) else raw
    return SafetyCheck(
        patient_id=patient_id,
        critical_count=result.get("@@critical_count", 0),
        major_count=result.get("@@major_count", 0),
        critical_alerts=list(result.get("@@critical_alerts", [])),
        major_alerts=list(result.get("@@major_alerts", [])),
        moderate_alerts=list(result.get("@@moderate_alerts", [])),
        info_alerts=list(result.get("@@info_alerts", [])),
    )
