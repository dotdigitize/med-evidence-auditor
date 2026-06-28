import json
import re
from typing import Any


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _string_list(value: Any) -> list[str]:
    items: list[str] = []
    for item in _as_list(value):
        if isinstance(item, dict):
            text = item.get("name") or item.get("label") or item.get("text") or item.get("summary")
            if text:
                items.append(str(text))
        elif item:
            items.append(str(item))
    return items


def _normalize_marker(marker: Any) -> dict[str, Any] | None:
    if isinstance(marker, dict):
        name = marker.get("name") or marker.get("marker") or marker.get("gene") or marker.get("protein")
        if not name:
            return None
        return {
            "name": str(name),
            "type": marker.get("type"),
            "score": marker.get("score") or marker.get("confidence") or marker.get("relevance_score"),
            "direction": marker.get("direction") or marker.get("trend"),
            "source": marker,
        }
    if marker:
        return {"name": str(marker), "type": None, "score": None, "direction": None, "source": marker}
    return None


def _extract_scores(payload: dict[str, Any]) -> dict[str, Any]:
    scores: dict[str, Any] = {}
    for key, value in payload.items():
        lowered = key.lower()
        if lowered == "score" or lowered.endswith("_score") or lowered in {"scores", "confidence", "confidence_score"}:
            scores[key] = value
    return scores


def _summary_text(payload: dict[str, Any]) -> str:
    for key in ("summary", "summary_text", "result_summary", "model_summary"):
        value = payload.get(key)
        if isinstance(value, str):
            return value
    return ""


def _confidence_notes(payload: dict[str, Any]) -> list[str]:
    return _string_list(payload.get("confidence_notes") or payload.get("confidence_note") or payload.get("limitations"))


def parse_mammal_json(payload: dict[str, Any]) -> dict[str, Any]:
    markers = [
        marker
        for marker in (_normalize_marker(item) for item in _as_list(payload.get("candidate_markers") or payload.get("markers")))
        if marker
    ]
    pathway_items = payload.get("pathway_notes") or payload.get("pathways") or payload.get("pathway_clusters")
    findings = _string_list(payload.get("findings") or payload.get("finding") or payload.get("model_findings"))
    claims = _string_list(payload.get("claims"))
    summary = _summary_text(payload)
    return {
        "run_id": payload.get("run_id") or payload.get("id") or payload.get("run"),
        "model": payload.get("model") or payload.get("model_name") or "MAMMAL",
        "candidate_markers": markers,
        "pathway_notes": _string_list(pathway_items),
        "findings": findings,
        "summary_text": summary,
        "claims": claims,
        "confidence_notes": _confidence_notes(payload),
        "scores": _extract_scores(payload),
        "raw": payload,
    }


def parse_mammal_text(raw_text: str) -> dict[str, Any]:
    text = raw_text.strip()
    try:
        loaded = json.loads(text)
    except json.JSONDecodeError:
        loaded = None
    if isinstance(loaded, dict):
        return parse_mammal_json(loaded)

    run_match = re.search(r"\b(?:run_id|run id|run)\s*[:=]\s*([A-Za-z0-9_.-]+)", text, re.IGNORECASE)
    markers: list[dict[str, Any]] = []
    pathway_notes: list[str] = []
    findings: list[str] = []
    summary_lines: list[str] = []
    confidence_notes: list[str] = []
    scores: dict[str, Any] = {}

    for raw_line in text.splitlines():
        line = raw_line.strip(" -\t")
        if not line:
            continue
        lower = line.lower()
        if re.match(r"^(run_id|run id|run)\s*[:=]", line, re.IGNORECASE):
            continue
        score_match = re.search(r"\bscore\s*[:=]?\s*(0(?:\.\d+)?|1(?:\.0+)?)", line, re.IGNORECASE)
        score = float(score_match.group(1)) if score_match else None
        if "candidate" in lower and "marker" in lower:
            marker_match = re.search(r"(?:marker|gene|protein)\s*[:=]\s*([A-Za-z0-9_.-]+)", line, re.IGNORECASE)
            if not marker_match:
                marker_match = re.search(r"\b([A-Z0-9]{2,})\b", line)
            if marker_match:
                markers.append({"name": marker_match.group(1), "type": None, "score": score, "direction": None, "source": line})
        elif lower.startswith("finding") or "finding:" in lower:
            findings.append(re.sub(r"^finding\s*[:=-]\s*", "", line, flags=re.IGNORECASE))
        elif lower.startswith("pathway") or "pathway note:" in lower:
            pathway_notes.append(re.sub(r"^pathway\s*(?:note)?\s*[:=-]\s*", "", line, flags=re.IGNORECASE))
        elif lower.startswith("summary") or "summary:" in lower:
            summary_lines.append(re.sub(r"^summary\s*[:=-]\s*", "", line, flags=re.IGNORECASE))
        elif lower.startswith("confidence") or lower.startswith("limitation"):
            confidence_notes.append(re.sub(r"^(confidence|limitation)s?\s*[:=-]\s*", "", line, flags=re.IGNORECASE))
        else:
            summary_lines.append(line)
        if score is not None:
            scores[f"text_score_{len(scores) + 1}"] = score

    return {
        "run_id": run_match.group(1) if run_match else None,
        "model": "MAMMAL",
        "candidate_markers": markers,
        "pathway_notes": pathway_notes,
        "findings": findings,
        "summary_text": " ".join(summary_lines).strip(),
        "claims": [],
        "confidence_notes": confidence_notes,
        "scores": scores,
        "raw": raw_text,
    }


def parse_mammal_output(raw: dict[str, Any] | str) -> dict[str, Any]:
    if isinstance(raw, dict):
        return parse_mammal_json(raw)
    return parse_mammal_text(raw)
