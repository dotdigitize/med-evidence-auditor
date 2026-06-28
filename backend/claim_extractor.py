import re
from backend.models import ExtractedClaim

SIGNAL_WORDS = [
    "associated with", "increased", "decreased", "marker", "risk", "pathway",
    "gene", "protein", "inflammation", "dopamine", "glutamate", "synaptic",
    "predicts", "diagnosis", "treatment", "response",
]


def split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", text.replace("\n", " ").strip())
    return [part.strip(" -\t") for part in parts if part.strip()]


def classify_claim_type(sentence: str) -> str:
    lowered = sentence.lower()
    if any(word in lowered for word in ["diagnosis", "treatment", "predicts", "risk"]):
        return "clinical_or_risk_statement"
    if any(word in lowered for word in ["gene", "protein", "pathway", "marker"]):
        return "biomedical_mechanism"
    return "research_summary_statement"


def extract_claims(text: str) -> list[ExtractedClaim]:
    claims: list[ExtractedClaim] = []
    seen: set[str] = set()
    for sentence in split_sentences(text):
        lowered = sentence.lower()
        if len(sentence) < 24:
            continue
        if not any(signal in lowered for signal in SIGNAL_WORDS):
            continue
        if lowered in seen:
            continue
        seen.add(lowered)
        claims.append(
            ExtractedClaim(
                id=len(claims) + 1,
                claim_text=sentence,
                claim_type=classify_claim_type(sentence),
            )
        )
    return claims
