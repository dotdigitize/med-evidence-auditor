import httpx
from backend.config import Settings, get_settings
from backend.claim_extractor import extract_claims
from backend.models import ExtractedClaim


async def extract_claims_with_optional_llm(text: str, settings: Settings | None = None) -> list[ExtractedClaim]:
    settings = settings or get_settings()
    if not settings.enable_llm_audit:
        return extract_claims(text)
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            response = await client.post(
                f"{settings.ollama_base_url.rstrip('/')}/api/generate",
                json={
                    "model": settings.claim_model,
                    "prompt": f"Extract concise biomedical claims as one claim per line:\n{text}",
                    "stream": False,
                },
            )
            response.raise_for_status()
            lines = [line.strip("- ") for line in response.json().get("response", "").splitlines() if line.strip()]
            claims = [ExtractedClaim(id=i + 1, claim_text=line) for i, line in enumerate(lines)]
            return claims or extract_claims(text)
    except Exception:
        return extract_claims(text)
