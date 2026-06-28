from typing import Any

from backend.claim_extractor import classify_claim_type, split_sentences
from backend.models import ExtractedClaim


def _claim(text: str, source_fields: dict[str, Any]) -> ExtractedClaim | None:
    normalized = " ".join(text.split())
    if len(normalized) < 12:
        return None
    return ExtractedClaim(
        claim_text=normalized.rstrip(".") + ".",
        claim_type=classify_claim_type(normalized),
        source_fields=source_fields,
    )


def extract_mammal_claims(parsed_output: dict[str, Any]) -> list[ExtractedClaim]:
    claims: list[ExtractedClaim] = []
    seen: set[str] = set()

    def add(text: str, source_fields: dict[str, Any]) -> None:
        item = _claim(text, source_fields)
        if not item:
            return
        key = item.claim_text.lower()
        if key in seen:
            return
        seen.add(key)
        item.id = len(claims) + 1
        claims.append(item)

    for marker in parsed_output.get("candidate_markers", []):
        name = marker.get("name")
        if not name:
            continue
        direction = f" {marker['direction']}" if marker.get("direction") else ""
        score = f" with score {marker['score']}" if marker.get("score") is not None else ""
        add(
            f"{name}{direction} appears as a candidate biomedical marker{score}",
            {"mammal_field": "candidate_markers", "value": marker, "run_id": parsed_output.get("run_id")},
        )

    for pathway in parsed_output.get("pathway_notes", []):
        add(
            f"{pathway} appears as a MAMMAL pathway note",
            {"mammal_field": "pathway_notes", "value": pathway, "run_id": parsed_output.get("run_id")},
        )

    for field in ("findings", "claims"):
        for text in parsed_output.get(field, []):
            for sentence in split_sentences(text):
                add(sentence, {"mammal_field": field, "value": text, "run_id": parsed_output.get("run_id")})

    for note in parsed_output.get("confidence_notes", []):
        for sentence in split_sentences(note):
            add(sentence, {"mammal_field": "confidence_notes", "value": note, "run_id": parsed_output.get("run_id")})

    summary = parsed_output.get("summary_text")
    if summary:
        for sentence in split_sentences(summary):
            add(sentence, {"mammal_field": "summary_text", "value": summary, "run_id": parsed_output.get("run_id")})

    return claims
