import { BookOpenCheck } from 'lucide-react';

export default function EvidenceLibrary({ evidence }: { evidence: string[] }) {
  return (
    <section className="rounded-md border border-slate-200 bg-white p-4 shadow-sm">
      <h2 className="text-base font-semibold text-ink">Evidence Library</h2>
      <div className="mt-3 space-y-2">
        {evidence.map((item) => (
          <div key={item} className="flex gap-2 rounded-md bg-slate-50 p-3 text-sm text-slate-700">
            <BookOpenCheck size={17} className="mt-0.5 shrink-0 text-review" />
            <span>{item}</span>
          </div>
        ))}
      </div>
    </section>
  );
}
