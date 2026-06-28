from backend.mammal_importer import parse_mammal_output
from backend.models import MammalImportRequest


def test_mammal_importer_accepts_json_payload():
    output = parse_mammal_output(
        MammalImportRequest(
            raw_json={
                "model": "MAMMAL synthetic output",
                "run_id": "mammal_import_001",
                "summary": "Gene expression marker summary.",
                "claims": ["Inflammation pathway markers may be associated with cohort observations."],
            }
        )
    )
    assert "Inflammation pathway" in output.output_text
    assert output.output_type == "mammal_json"
    assert output.metadata_json
    assert output.metadata_json["mammal_parsed"]["run_id"] == "mammal_import_001"
    assert output.metadata_json["mammal_claim_count"] >= 1


def test_mammal_importer_accepts_text_payload():
    output = parse_mammal_output(
        MammalImportRequest(
            raw_text="run_id: mammal_text_import\nSummary: Dopamine pathway markers may be candidate research markers."
        )
    )

    assert output.output_type == "mammal_text"
    assert output.model_name == "MAMMAL"
    assert "Dopamine pathway" in output.output_text
