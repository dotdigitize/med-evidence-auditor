from fastapi.testclient import TestClient
from backend.server import app


def test_health_and_sample_endpoints_do_not_require_services():
    client = TestClient(app)
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["database_enabled"] is False
    status = client.get("/api/system/status")
    assert status.status_code == 200
    assert status.json()["database"] == "disabled"
    sample = client.get("/api/sample/overview")
    assert sample.status_code == 200
    assert sample.json()["fixture_type"] == "synthetic research fixture"


def test_run_audit_endpoint_uses_sample_evidence():
    client = TestClient(app)
    response = client.post(
        "/api/audits/run",
        json={
            "project_id": 1,
            "model_output": {
                "project_id": 1,
                "output_title": "Test output",
                "output_text": "Dopamine and glutamate pathway markers are candidate markers in research summaries."
            }
        },
    )
    assert response.status_code == 200
    assert response.json()["claims"]
