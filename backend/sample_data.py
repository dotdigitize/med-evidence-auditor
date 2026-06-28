import json
from pathlib import Path
from backend.models import AuditProject, EvidenceItem, ModelOutput

ROOT = Path(__file__).resolve().parent.parent
SAMPLE_DIR = ROOT / "sample_data"


def _load_json(name: str):
    return json.loads((SAMPLE_DIR / name).read_text())


def load_sample_project() -> AuditProject:
    return AuditProject(**_load_json("audit_project.json"))


def load_sample_evidence() -> list[EvidenceItem]:
    return [EvidenceItem(**item) for item in _load_json("evidence_items.json")]


def load_sample_model_output() -> ModelOutput:
    return ModelOutput(project_id=1, output_title="Synthetic schizophrenia MAMMAL output", model_name="MAMMAL", output_text=(SAMPLE_DIR / "model_output_sample.txt").read_text(), output_type="mammal_text")


def sample_overview() -> dict:
    return {
        "project": load_sample_project().model_dump(),
        "evidence_count": len(load_sample_evidence()),
        "mammal_output_title": load_sample_model_output().output_title,
        "fixture_type": "synthetic research fixture",
    }
