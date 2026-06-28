import { AlertTriangle } from 'lucide-react';
import type { RiskFlag } from '../hooks/useMedEvidence';

export default function RiskFlagsPanel({ flags }: { flags: RiskFlag[] }) {
  return (
    <section className="rounded-md border border-slate-200 bg-white p-4 shadow-sm">
      <h2 className="text-base font-semibold text-ink">Risk Flags Panel</h2>
      <div className="mt-3 grid gap-3 md:grid-cols-2">
        {flags.map((flag) => (
          <article key={flag.id} className="rounded-md border border-safety/20 bg-safety/5 p-3">
            <div className="flex items-center gap-2">
              <AlertTriangle size={17} className="text-safety" />
              <p className="text-sm font-semibold text-ink">{flag.flagType}</p>
              <span className="rounded-md bg-white px-2 py-1 text-xs font-semibold text-safety">{flag.severity}</span>
            </div>
            <p className="mt-2 text-sm text-slate-700">{flag.flagText}</p>
            <p className="mt-2 text-sm font-medium text-slate-800">{flag.recommendation}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
