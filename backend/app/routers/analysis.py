import logging
from fastapi import APIRouter, Depends, Query, HTTPException, Request
from app.models.schemas import SafetyCheck, SafetyCheckRequest
from app.services.tigergraph_service import TigerGraphService
from app.dependencies import get_tg_service
from app.limiter import limiter

logger = logging.getLogger(__name__)
router = APIRouter()


# ── Pharmacogenomics ──────────────────────────────────────────────────────────

@router.get("/{patient_id}/pgx")
@limiter.limit("20/minute")
def pharmacogenomics_report(
    request: Request,
    patient_id: str,
    tg: TigerGraphService = Depends(get_tg_service),
):
    """
    Personalised pharmacogenomics report.
    Shows which of the patient's medications are affected by their gene variants
    (CYP2D6, CYP3A4, VKORC1 etc.) and flags efficacy/toxicity risks.
    """
    try:
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
    except HTTPException:
        raise
    except Exception as e:
        logger.error("pharmacogenomics_report failed for %s: %s", patient_id, e)
        raise HTTPException(status_code=500, detail="Failed to generate pharmacogenomics report")


# ── Disease Progression Risk ──────────────────────────────────────────────────

@router.get("/{patient_id}/progression")
@limiter.limit("20/minute")
def disease_progression_risk(
    request: Request,
    patient_id: str,
    max_depth: int = Query(3, ge=1, le=5),
    tg: TigerGraphService = Depends(get_tg_service),
):
    """
    BFS traversal on PROGRESSES_TO edges from all the patient's active diseases.
    Returns risk chains with cumulative probability and time estimates.
    """
    try:
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
    except HTTPException:
        raise
    except Exception as e:
        logger.error("disease_progression_risk failed for %s: %s", patient_id, e)
        raise HTTPException(status_code=500, detail="Failed to calculate disease progression risk")


# ── Pre-Prescription Safety Check ────────────────────────────────────────────

@router.post("/{patient_id}/safety-check", response_model=SafetyCheck)
@limiter.limit("20/minute")
def contraindication_safety_check(
    request: Request,
    patient_id: str,
    body: SafetyCheckRequest,
    tg: TigerGraphService = Depends(get_tg_service),
):
    """
    Pre-prescription safety check.
    Given a patient and a list of proposed drug names, returns severity-ordered
    alerts covering: drug-drug interactions, contraindications, known allergies,
    black-box warnings, pregnancy categories, and pharmacogenomics flags.
    """
    try:
        raw = tg.contraindication_safety_check(patient_id, body.proposed_drugs)
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
    except HTTPException:
        raise
    except Exception as e:
        logger.error("contraindication_safety_check failed for %s: %s", patient_id, e)
        raise HTTPException(status_code=500, detail="Failed to run safety check")
