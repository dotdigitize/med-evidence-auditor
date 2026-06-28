import json
from backend.mammal_claim_extractor import extract_mammal_claims
from backend.mammal_output_parser import parse_mammal_output as normalize_mammal_output
from backend.models import MammalImportRequest, ModelOutput


def parse_mammal_output(request: MammalImportRequest) -> ModelOutput:
    raw = request.raw_json
    if raw is None and request.raw_text:
        try:
            loaded = json.loads(request.raw_text)
            raw = loaded if isinstance(loaded, dict) else request.raw_text
        except json.JSONDecodeError:
            raw = request.raw_text
    raw = raw or {}
    parsed = normalize_mammal_output(raw)
    claims = extract_mammal_claims(parsed)
    sections: list[str] = []
    if parsed.get("summary_text"):
        sections.append(str(parsed["summary_text"]))
    sections.extend(str(item) for item in parsed.get("findings", []))
    sections.extend(str(item) for item in parsed.get("claims", []))
    for marker in parsed.get("candidate_markers", []):
        if marker.get("name"):
            sections.append(f"{marker['name']} candidate marker score {marker.get('score')}".strip())
    sections.extend(str(item) for item in parsed.get("pathway_notes", []))
    text = "\n".join(section for section in sections if section) or request.raw_text or ""
    output_type = "mammal_json" if isinstance(raw, dict) else "mammal_text"
    return ModelOutput(
        project_id=request.project_id,
        output_title=request.import_title,
        model_name=str(parsed.get("model") or "MAMMAL"),
        output_text=text,
        output_type=output_type,
        metadata_json={
            "mammal_parsed": parsed,
            "mammal_claim_count": len(claims),
        },
    )
