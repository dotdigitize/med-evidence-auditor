import { Play, ShieldAlert } from 'lucide-react';

export default function AuditRunner({ evidence }: { evidence: string[] }) {
  return (
    <section className="rounded-md border border-slate-200 bg-white p-4 shadow-sm">
      <div className="flex items-center justify-between gap-3">
        <h2 className="text-base font-semibold text-ink">MAMMAL Output Review</h2>
        <button className="inline-flex items-center gap-2 rounded-md bg-clinical px-3 py-2 text-sm font-semibold text-white hover:bg-clinical/90" type="button">
          <Play size={16} />
          Run MAMMAL Evidence Audit
        </button>
      </div>
      <textarea
        className="mt-3 h-28 w-full resize-y rounded-md border border-slate-300 p-3 text-sm outline-none focus:border-clinical focus:ring-2 focus:ring-clinical/20"
        defaultValue={'Paste or review MAMMAL output here before running claim extraction and evidence matching.'}
      />
      <div className="mt-3 grid gap-3 md:grid-cols-3">
        <select className="rounded-md border border-slate-300 px-3 py-2 text-sm">
          {evidence.map((item) => (
            <option key={item}>{item}</option>
          ))}
        </select>
        <div className="rounded-md bg-review/10 px-3 py-2 text-sm font-medium text-review">Support summary: 1 supported, 1 unsupported</div>
        <div className="flex items-center gap-2 rounded-md bg-safety/10 px-3 py-2 text-sm font-medium text-safety">
          <ShieldAlert size={16} />
          Risk flag summary: 2 flags
        </div>
      </div>
    </section>
  );
}
