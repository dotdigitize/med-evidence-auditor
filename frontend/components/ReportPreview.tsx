import { FileJson, FileText } from 'lucide-react';
import type { ClaimRow, RiskFlag } from '../hooks/useMedEvidence';

export default function ReportPreview({ claims, flags }: { claims: ClaimRow[]; flags: RiskFlag[] }) {
  return (
    <section className="rounded-md border border-slate-200 bg-white p-4 shadow-sm">
      <div className="flex items-center justify-between gap-3">
        <h2 className="text-base font-semibold text-ink">MAMMAL Evidence Audit Report</h2>
        <div className="flex gap-2 text-clinical">
          <FileText size={18} />
          <FileJson size={18} />
        </div>
      </div>
      <div className="mt-3 rounded-md bg-slate-50 p-4 text-sm text-slate-700">
        <p className="font-semibold text-ink">Audit Summary</p>
        <p className="mt-2">MAMMAL claims reviewed: {claims.length}</p>
        <p>Risk flags: {flags.length}</p>
        <p className="mt-2">Medical safety notice: this MAMMAL evidence review does not diagnose, treat, prescribe, predict individual medical risk, or replace licensed clinical judgment.</p>
      </div>
    </section>
  );
}
