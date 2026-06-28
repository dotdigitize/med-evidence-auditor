from pathlib import Path


def test_required_sql_files_exist_and_define_tables():
    root = Path(__file__).resolve().parent.parent
    schema = (root / "db" / "schema.sql").read_text()
    for name in [
        "audit_projects", "source_documents", "evidence_items", "model_outputs",
        "extracted_claims", "claim_evidence_links", "risk_flags", "audit_runs",
        "audit_reports", "mammal_imports", "audit_events",
    ]:
        assert f"CREATE TABLE IF NOT EXISTS {name}" in schema
    assert "ENGINE=InnoDB" in schema
    assert "JSON NULL" in schema
    assert "FOREIGN KEY" in schema
