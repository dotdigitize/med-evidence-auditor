import pytest
from backend.config import Settings
from backend.llm_auditor import extract_claims_with_optional_llm


@pytest.mark.asyncio
async def test_llm_auditor_falls_back_when_disabled():
    claims = await extract_claims_with_optional_llm(
        "Gene expression markers may be associated with synaptic pathway activity.",
        Settings(enable_llm_audit=False),
    )
    assert claims
    assert "Gene expression" in claims[0].claim_text
