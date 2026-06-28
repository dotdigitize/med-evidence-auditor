from backend.sample_data import load_sample_evidence, load_sample_model_output, load_sample_project


def load_seed_bundle() -> dict:
    return {
        "project": load_sample_project().model_dump(),
        "evidence_items": [item.model_dump() for item in load_sample_evidence()],
        "model_output": load_sample_model_output().model_dump(),
    }
