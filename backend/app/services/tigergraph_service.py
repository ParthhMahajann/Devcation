import pyTigerGraph as tg
from app.config import get_settings
import logging

logger = logging.getLogger(__name__)


class TigerGraphService:
    def __init__(self):
        settings = get_settings()
        try:
            self.conn = tg.TigerGraphConnection(
                host=settings.tg_host,
                graphname=settings.tg_graph,
                restppPort=settings.tg_restpp_port,
                gsPort=settings.tg_gs_port,
                username=settings.tg_username,
                password=settings.tg_password,
            )
            # Token acquisition: API token > explicit secret > auto-create secret
            if settings.tg_api_token:
                self.conn.apiToken = settings.tg_api_token
            elif settings.tg_secret:
                self.conn.getToken(settings.tg_secret)
            else:
                try:
                    secret = self.conn.createSecret()
                    self.conn.getToken(secret)
                except Exception as token_err:
                    # Local CE may not require a token — proceed without one
                    logger.warning(f"Token acquisition skipped: {token_err}")
            logger.info(f"TigerGraph connected → {settings.tg_host}/{settings.tg_graph}")
        except Exception as e:
            logger.error(f"TigerGraph connection failed: {e}")
            self.conn = None

    # ─── Diagnosis ─────────────────────────────────────────────────────────────

    def diagnose(self, symptoms: list[str]) -> dict:
        if not self.conn:
            return self._mock_diagnose(symptoms)
        try:
            result = self.conn.runInstalledQuery(
                "diagnose_from_symptoms",
                {"input_symptoms": symptoms}
            )
            return result
        except Exception as e:
            logger.error(f"diagnose query failed: {e}")
            return self._mock_diagnose(symptoms)

    # ─── Drug Interactions ──────────────────────────────────────────────────────

    def check_interactions(self, drug_names: list[str]) -> dict:
        if not self.conn:
            return self._mock_interactions(drug_names)
        try:
            result = self.conn.runInstalledQuery(
                "check_drug_interactions",
                {"drug_names": drug_names}
            )
            return result
        except Exception as e:
            logger.error(f"check_drug_interactions query failed: {e}")
            return self._mock_interactions(drug_names)

    # ─── Treatment Path ─────────────────────────────────────────────────────────

    def find_treatment_path(self, disease_id: str) -> dict:
        if not self.conn:
            return {}
        try:
            return self.conn.runInstalledQuery(
                "find_treatment_path",
                {"source_disease": disease_id}
            )
        except Exception as e:
            logger.error(f"find_treatment_path query failed: {e}")
            return {}

    # ─── Patient Risk ───────────────────────────────────────────────────────────

    def get_patient_risk(self, patient_id: str) -> dict:
        if not self.conn:
            return {}
        try:
            return self.conn.runInstalledQuery(
                "patient_risk_profile",
                {"p": patient_id}
            )
        except Exception as e:
            logger.error(f"patient_risk_profile query failed: {e}")
            return {}

    # ─── Graph Stats ────────────────────────────────────────────────────────────

    def get_stats(self) -> dict:
        if not self.conn:
            return self._mock_stats()
        try:
            result = self.conn.runInstalledQuery("get_graph_stats", {})
            return result[0] if result else {}
        except Exception as e:
            logger.error(f"get_graph_stats query failed: {e}")
            return self._mock_stats()

    # ─── Graph Explorer ─────────────────────────────────────────────────────────

    def explore_subgraph(
        self,
        center_type: str = "",
        center_id: str = "",
        max_hops: int = 2,
        limit_per_hop: int = 20,
    ) -> dict:
        if not self.conn:
            return {"nodes": [], "edges": []}
        try:
            return self.conn.runInstalledQuery(
                "explore_subgraph",
                {
                    "center_type": center_type,
                    "center_id": center_id,
                    "max_hops": max_hops,
                    "limit_per_hop": limit_per_hop,
                }
            )
        except Exception as e:
            logger.error(f"explore_subgraph query failed: {e}")
            return {"nodes": [], "edges": []}

    # ─── Pharmacogenomics ────────────────────────────────────────────────────────

    def pharmacogenomics_report(self, patient_id: str) -> dict:
        if not self.conn:
            return {}
        try:
            return self.conn.runInstalledQuery(
                "pharmacogenomics_report",
                {"p": patient_id}
            )
        except Exception as e:
            logger.error(f"pharmacogenomics_report query failed: {e}")
            return {}

    # ─── Disease Progression ─────────────────────────────────────────────────────

    def disease_progression_risk(self, patient_id: str, max_depth: int = 3) -> dict:
        if not self.conn:
            return {}
        try:
            return self.conn.runInstalledQuery(
                "disease_progression_risk",
                {"p": patient_id, "max_depth": max_depth}
            )
        except Exception as e:
            logger.error(f"disease_progression_risk query failed: {e}")
            return {}

    # ─── Comorbidity Cluster ─────────────────────────────────────────────────────

    def comorbidity_cluster(self, disease_id: str, max_hops: int = 2, min_rate: float = 0.1) -> dict:
        if not self.conn:
            return {}
        try:
            return self.conn.runInstalledQuery(
                "comorbidity_cluster",
                {"seed_disease": disease_id, "max_hops": max_hops, "min_rate": min_rate}
            )
        except Exception as e:
            logger.error(f"comorbidity_cluster query failed: {e}")
            return {}

    # ─── Contraindication Safety Check ───────────────────────────────────────────

    def contraindication_safety_check(self, patient_id: str, proposed_drugs: list[str]) -> dict:
        if not self.conn:
            return {}
        try:
            return self.conn.runInstalledQuery(
                "contraindication_safety_check",
                {"p": patient_id, "proposed_drug_names": proposed_drugs}
            )
        except Exception as e:
            logger.error(f"contraindication_safety_check query failed: {e}")
            return {}

    # ─── List helpers ───────────────────────────────────────────────────────────

    def list_symptoms(self) -> list:
        if not self.conn:
            return self._mock_symptoms()
        try:
            result = self.conn.getVertices("Symptom")
            return result
        except Exception as e:
            logger.error(f"list_symptoms failed: {e}")
            return self._mock_symptoms()

    def list_drugs(self) -> list:
        if not self.conn:
            return self._mock_drugs()
        try:
            result = self.conn.getVertices("Drug")
            return result
        except Exception as e:
            logger.error(f"list_drugs failed: {e}")
            return self._mock_drugs()

    # ─── Patient CRUD ────────────────────────────────────────────────────────────

    def get_patient(self, patient_id: str) -> dict:
        if not self.conn:
            return {"patient_id": patient_id, "name": "Demo Patient", "age": 45,
                    "conditions": [], "medications": [], "drug_interactions": []}
        try:
            vertices = self.conn.getVerticesById("Patient", patient_id)
            if not vertices:
                raise ValueError(f"Patient {patient_id} not found")
            return vertices[0]
        except Exception as e:
            logger.error(f"get_patient failed: {e}")
            raise

    def upsert_patient(self, patient: dict) -> dict:
        if not self.conn:
            return patient
        try:
            self.conn.upsertVertex(
                "Patient",
                patient["patient_id"],
                attributes={k: v for k, v in patient.items() if k != "patient_id"}
            )
            return patient
        except Exception as e:
            logger.error(f"upsert_patient failed: {e}")
            return patient

    # ─── Mock data (fallback when TG is offline) ─────────────────────────────────

    def _mock_diagnose(self, symptoms):
        return [{"diseases": [
            {"disease_id": "D001", "name": "Common Cold", "icd_code": "J00", "severity": "mild",
             "category": "Respiratory", "description": "Viral upper respiratory infection",
             "@score": 4.5, "@match_count": 2, "@matched_symptoms": {}},
            {"disease_id": "D002", "name": "Influenza", "icd_code": "J10", "severity": "moderate",
             "category": "Respiratory", "description": "Seasonal flu",
             "@score": 3.2, "@match_count": 2, "@matched_symptoms": {}},
        ]}]

    def _mock_interactions(self, drug_names):
        return [{"all_drugs": [], "@@interaction_edges": []}]

    def _mock_stats(self):
        return {
            "@@disease_count": 5247,
            "@@symptom_count": 10392,
            "@@drug_count": 3018,
            "@@side_effect_count": 1784,
            "@@gene_count": 512,
            "@@patient_count": 100,
            "@@body_system_count": 13,
            "@@medical_test_count": 284,
            "@@biomarker_count": 196,
            "@@risk_factor_count": 87,
            "@@pathway_count": 342,
            "@@drug_class_count": 48,
            "@@procedure_count": 213,
            "@@has_symptom_count": 48291,
            "@@treats_count": 9814,
            "@@interacts_count": 4203,
            "@@associated_count": 2917,
            "@@comorbid_count": 3156,
        }

    def _mock_symptoms(self):
        return [
            {"v_id": "S001", "attributes": {"name": "Fever", "body_system": "General", "severity_weight": 0.8}},
            {"v_id": "S002", "attributes": {"name": "Cough", "body_system": "Respiratory", "severity_weight": 0.6}},
            {"v_id": "S003", "attributes": {"name": "Headache", "body_system": "Neurological", "severity_weight": 0.5}},
            {"v_id": "S004", "attributes": {"name": "Fatigue", "body_system": "General", "severity_weight": 0.4}},
            {"v_id": "S005", "attributes": {"name": "Nausea", "body_system": "Gastrointestinal", "severity_weight": 0.5}},
            {"v_id": "S006", "attributes": {"name": "Chest Pain", "body_system": "Cardiovascular", "severity_weight": 0.9}},
            {"v_id": "S007", "attributes": {"name": "Shortness of Breath", "body_system": "Respiratory", "severity_weight": 0.85}},
            {"v_id": "S008", "attributes": {"name": "Sore Throat", "body_system": "Respiratory", "severity_weight": 0.4}},
        ]

    def _mock_drugs(self):
        return [
            {"v_id": "DR001", "attributes": {"name": "Aspirin", "drug_class": "NSAID", "approval_status": "approved", "generic_name": "Acetylsalicylic acid"}},
            {"v_id": "DR002", "attributes": {"name": "Ibuprofen", "drug_class": "NSAID", "approval_status": "approved", "generic_name": "Ibuprofen"}},
            {"v_id": "DR003", "attributes": {"name": "Warfarin", "drug_class": "Anticoagulant", "approval_status": "approved", "generic_name": "Warfarin sodium"}},
            {"v_id": "DR004", "attributes": {"name": "Metformin", "drug_class": "Biguanide", "approval_status": "approved", "generic_name": "Metformin HCl"}},
            {"v_id": "DR005", "attributes": {"name": "Lisinopril", "drug_class": "ACE inhibitor", "approval_status": "approved", "generic_name": "Lisinopril"}},
        ]
