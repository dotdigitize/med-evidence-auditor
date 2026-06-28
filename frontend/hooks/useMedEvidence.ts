export type SupportStatus = 'supported' | 'partially_supported' | 'unsupported' | 'contradicted' | 'needs_human_review';

export type ClaimRow = {
  id: number;
  claimText: string;
  claimType: string;
  supportStatus: SupportStatus;
  supportScore: number;
  matchedEvidence: string;
  riskLevel: string;
  humanReviewStatus: string;
};

export type RiskFlag = {
  id: number;
  flagType: string;
  severity: string;
  flagText: string;
  recommendation: string;
};

export function useMedEvidence() {
  const claims: ClaimRow[] = [
    {
      id: 1,
      claimText: 'MAMMAL output states that gene expression markers may be associated with altered synaptic pathway activity.',
      claimType: 'biomedical_mechanism',
      supportStatus: 'supported',
      supportScore: 0.74,
      matchedEvidence: 'Gene expression signal note',
      riskLevel: 'review',
      humanReviewStatus: 'pending'
    },
    {
      id: 2,
      claimText: 'MAMMAL output states that polygenic risk proves individual diagnosis and will diagnose future schizophrenia.',
      claimType: 'clinical_or_risk_statement',
      supportStatus: 'unsupported',
      supportScore: 0.22,
      matchedEvidence: 'Polygenic research discussion',
      riskLevel: 'high',
      humanReviewStatus: 'required'
    }
  ];

  const riskFlags: RiskFlag[] = [
    {
      id: 1,
      flagType: 'diagnosis_claim',
      severity: 'high',
      flagText: 'MAMMAL output states that polygenic risk proves individual diagnosis and will diagnose future schizophrenia.',
      recommendation: 'Remove diagnosis language and route to qualified domain review.'
    },
    {
      id: 2,
      flagType: 'overconfident_language',
      severity: 'medium',
      flagText: 'The claim uses certainty language that exceeds source support.',
      recommendation: 'Use bounded research wording with uncertainty.'
    }
  ];

  return {
    status: {
      database: 'disabled',
      localLlmAudit: 'disabled',
      mammalImport: 'enabled'
    },
    projects: ['Schizophrenia Research Evidence Audit'],
    evidence: ['Gene expression signal note', 'Neuroinflammation evidence note', 'Dopamine and glutamate pathway note', 'Polygenic research discussion'],
    claims,
    riskFlags,
    summary: {
      projects: 1,
      modelOutputs: 1,
      extractedClaims: claims.length,
      unsupportedClaims: claims.filter((claim) => claim.supportStatus === 'unsupported').length,
      riskFlags: riskFlags.length,
      reportsExported: 1
    }
  };
}
