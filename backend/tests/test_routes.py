"""Route-level tests for MedGraph AI API."""


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] in ("healthy", "degraded")
    assert "database" in data
    assert "version" in data


def test_root(client):
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["version"] == "2.0.0"
    assert data["status"] == "running"


# ── Auth ─────────────────────────────────────────────────────────────────────


def test_no_auth_returns_401(client):
    endpoints = [
        ("get",  "/api/graph/stats"),
        ("get",  "/api/symptoms/list"),
        ("get",  "/api/drugs/list"),
    ]
    for method, path in endpoints:
        resp = getattr(client, method)(path)
        assert resp.status_code == 401, f"{method.upper()} {path} should be 401, got {resp.status_code}"


def test_wrong_key_returns_401(client):
    resp = client.get("/api/graph/stats", headers={"X-API-Key": "wrong-key"})
    assert resp.status_code == 401


# ── Symptoms / Diagnose ───────────────────────────────────────────────────────


def test_diagnose_valid(client, headers):
    resp = client.post(
        "/api/symptoms/diagnose",
        json={"symptoms": ["Fever", "Cough"]},
        headers=headers,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "diseases" in data
    assert "total" in data


def test_diagnose_empty_symptoms_rejected(client, headers):
    resp = client.post(
        "/api/symptoms/diagnose",
        json={"symptoms": []},
        headers=headers,
    )
    assert resp.status_code == 422


def test_list_symptoms(client, headers):
    resp = client.get("/api/symptoms/list", headers=headers)
    assert resp.status_code == 200
    assert "symptoms" in resp.json()


# ── Drugs ─────────────────────────────────────────────────────────────────────


def test_drug_interactions_valid(client, headers):
    resp = client.post(
        "/api/drugs/interactions",
        json={"drug_names": ["Aspirin", "Warfarin"]},
        headers=headers,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "drugs" in data
    assert "interactions" in data


def test_drug_interactions_single_drug_rejected(client, headers):
    resp = client.post(
        "/api/drugs/interactions",
        json={"drug_names": ["Aspirin"]},
        headers=headers,
    )
    assert resp.status_code == 422


def test_list_drugs(client, headers):
    resp = client.get("/api/drugs/list", headers=headers)
    assert resp.status_code == 200
    assert "drugs" in resp.json()


# ── Graph ─────────────────────────────────────────────────────────────────────


def test_graph_stats(client, headers):
    resp = client.get("/api/graph/stats", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "disease_count" in data
    assert "drug_count" in data


# ── Patients ─────────────────────────────────────────────────────────────────


def test_patient_lookup(client, headers):
    resp = client.get("/api/patients/P001", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["patient_id"] == "P001"


def test_patient_not_found_returns_404(client, headers, mock_tg):
    mock_tg.get_patient.return_value = None
    resp = client.get("/api/patients/NONEXISTENT", headers=headers)
    assert resp.status_code == 404


def test_create_patient_invalid_age(client, headers):
    resp = client.post(
        "/api/patients",
        json={"patient_id": "P999", "name": "Test", "age": 200,
              "gender": "Male", "blood_type": "O+"},
        headers=headers,
    )
    assert resp.status_code == 422


def test_create_patient_invalid_id_chars(client, headers):
    resp = client.post(
        "/api/patients",
        json={"patient_id": "P 99 9!", "name": "Test", "age": 30,
              "gender": "Male", "blood_type": "O+"},
        headers=headers,
    )
    assert resp.status_code == 422
