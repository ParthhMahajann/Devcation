import os
import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient

# Set env vars before importing app modules (avoids cached settings issues)
os.environ["MEDGRAPH_API_KEY"] = "test-key-12345"
os.environ["TG_HOST"] = "http://localhost"
os.environ["TG_USERNAME"] = "tigergraph"
os.environ["TG_PASSWORD"] = "tigergraph"
os.environ["USE_MOCK_DATA"] = "true"

# Clear lru_cache so settings pick up the test env vars
from app.config import get_settings
get_settings.cache_clear()

from app.main import app
from app.dependencies import get_tg_service
from app.services.tigergraph_service import TigerGraphService


@pytest.fixture
def mock_tg():
    service = MagicMock(spec=TigerGraphService)
    service.conn = MagicMock()  # simulate connected state

    service.diagnose.return_value = [{"diseases": [
        {"disease_id": "D001", "name": "Common Cold", "icd_code": "J00",
         "severity": "mild", "category": "Respiratory", "description": "Test",
         "@score": 4.5, "@match_count": 2, "@matched_symptoms": {}},
    ]}]
    service.check_interactions.return_value = [{"all_drugs": [], "@@interaction_edges": []}]
    service.get_stats.return_value = {
        "@@disease_count": 100, "@@symptom_count": 200, "@@drug_count": 50,
        "@@side_effect_count": 30, "@@gene_count": 10, "@@patient_count": 5,
        "@@body_system_count": 3, "@@medical_test_count": 10,
        "@@biomarker_count": 5, "@@risk_factor_count": 2, "@@pathway_count": 3,
        "@@drug_class_count": 4, "@@procedure_count": 6, "@@has_symptom_count": 100,
        "@@treats_count": 50, "@@interacts_count": 20,
        "@@associated_count": 10, "@@comorbid_count": 15,
    }
    service.list_symptoms.return_value = [
        {"v_id": "S001", "attributes": {"name": "Fever", "body_system": "General", "severity_weight": 0.8}}
    ]
    service.list_drugs.return_value = [
        {"v_id": "DR001", "attributes": {"name": "Aspirin", "drug_class": "NSAID",
                                          "approval_status": "approved", "generic_name": "ASA"}}
    ]
    service.get_patient.return_value = {"patient_id": "P001", "name": "Test Patient", "age": 30}
    return service


@pytest.fixture
def client(mock_tg):
    app.dependency_overrides[get_tg_service] = lambda: mock_tg
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def headers():
    return {"X-API-Key": "test-key-12345"}
