import type { ClaimRow } from '../hooks/useMedEvidence';

export default function ClaimReviewTable({ claims }: { claims: ClaimRow[] }) {
  return (
    <section className="rounded-md border border-slate-200 bg-white p-4 shadow-sm">
      <h2 className="text-base font-semibold text-ink">MAMMAL Claims</h2>
      <div className="mt-3 overflow-x-auto">
        <table className="w-full min-w-[860px] border-collapse text-left text-sm">
          <thead>
            <tr className="border-b border-slate-200 text-xs uppercase text-slate-500">
              <th className="py-2 pr-3">MAMMAL claim</th>
              <th className="py-2 pr-3">Claim type</th>
              <th className="py-2 pr-3">Support status</th>
              <th className="py-2 pr-3">Support score</th>
              <th className="py-2 pr-3">Matched evidence</th>
              <th className="py-2 pr-3">Risk level</th>
              <th className="py-2">Human review status</th>
            </tr>
          </thead>
          <tbody>
            {claims.map((claim) => (
              <tr key={claim.id} className="border-b border-slate-100 align-top">
                <td className="max-w-md py-3 pr-3 text-slate-800">{claim.claimText}</td>
                <td className="py-3 pr-3 text-slate-600">{claim.claimType}</td>
                <td className="py-3 pr-3 font-semibold text-clinical">{claim.supportStatus}</td>
                <td className="py-3 pr-3 text-slate-700">{claim.supportScore.toFixed(2)}</td>
                <td className="py-3 pr-3 text-slate-600">{claim.matchedEvidence}</td>
                <td className="py-3 pr-3 text-safety">{claim.riskLevel}</td>
                <td className="py-3 text-slate-700">{claim.humanReviewStatus}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
