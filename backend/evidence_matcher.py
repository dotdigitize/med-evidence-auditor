import re
from backend.models import EvidenceItem, ExtractedClaim, SupportStatus

NEGATION_TERMS = {"not", "no", "without", "failed", "fails", "contradicts", "contradicted", "reduced", "absence"}


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\s-]", " ", text.lower())).strip()


def _tokens(text: str) -> set[str]:
    stop = {"the", "and", "or", "of", "to", "in", "a", "an", "for", "with", "may", "is", "are", "be"}
    return {token for token in normalize_text(text).split() if len(token) > 2 and token not in stop}


def token_overlap_score(claim: str, evidence: str) -> float:
    claim_tokens = _tokens(claim)
    evidence_tokens = _tokens(evidence)
    if not claim_tokens or not evidence_tokens:
        return 0.0
    return len(claim_tokens & evidence_tokens) / len(claim_tokens)


def phrase_overlap_score(claim: str, evidence: str) -> float:
    claim_words = normalize_text(claim).split()
    evidence_norm = normalize_text(evidence)
    if len(claim_words) < 3:
        return 0.0
    phrases = [" ".join(claim_words[i:i + 3]) for i in range(len(claim_words) - 2)]
    if not phrases:
        return 0.0
    return sum(1 for phrase in phrases if phrase in evidence_norm) / len(phrases)


def support_score(claim: str, evidence: str) -> float:
    return round((0.7 * token_overlap_score(claim, evidence)) + (0.3 * phrase_overlap_score(claim, evidence)), 5)


def classify_support_status(score: float, claim: str = "", evidence: str = "") -> SupportStatus:
    claim_tokens = _tokens(claim)
    evidence_tokens = _tokens(evidence)
    if score >= 0.28 and (claim_tokens & evidence_tokens) and (NEGATION_TERMS & evidence_tokens):
        return "contradicted"
    if score >= 0.62:
        return "supported"
    if score >= 0.32:
        return "partially_supported"
    if score > 0:
        return "unsupported"
    return "needs_human_review"


def match_claim_to_evidence(claim: ExtractedClaim, evidence_items: list[EvidenceItem]) -> ExtractedClaim:
    best: tuple[float, EvidenceItem | None] = (0.0, None)
    for item in evidence_items:
        score = support_score(claim.claim_text, item.evidence_text)
        if score > best[0]:
            best = (score, item)
    claim.support_score = best[0]
    if best[1]:
        claim.matched_evidence = [best[1]]
        claim.support_status = classify_support_status(best[0], claim.claim_text, best[1].evidence_text)
    else:
        claim.support_status = "needs_human_review"
    return claim


def match_claims(claims: list[ExtractedClaim], evidence_items: list[EvidenceItem]) -> list[ExtractedClaim]:
    return [match_claim_to_evidence(claim, evidence_items) for claim in claims]
