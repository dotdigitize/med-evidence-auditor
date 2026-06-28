from backend.audit_store import InMemoryAuditStore
from backend.models import AuditRunRequest
from backend.reporting import export_audit_report, render_markdown_report
from backend.sample_data import load_sample_model_output


def test_reporting_exports_markdown_and_json(tmp_path):
    result = InMemoryAuditStore().run_audit(AuditRunRequest(model_output=load_sample_model_output()))
    markdown = render_markdown_report(result)
    assert "## Audit Summary" in markdown
    assert "## MAMMAL Output Reviewed" in markdown
    assert "## Medical Safety Notice" in markdown
    paths = export_audit_report(result, tmp_path)
    assert (tmp_path / "latest_audit_report.md").exists()
    assert (tmp_path / "latest_audit_report.json").exists()
    assert paths["markdown"].endswith("latest_audit_report.md")
