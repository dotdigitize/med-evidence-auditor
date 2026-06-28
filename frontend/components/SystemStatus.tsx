import { Cpu, Database, Workflow } from 'lucide-react';

export default function SystemStatus({ status }: { status: { database: string; localLlmAudit: string; mammalImport: string } }) {
  const rows = [
    { label: 'Database', value: status.database, icon: Database },
    { label: 'Local LLM Audit', value: status.localLlmAudit, icon: Cpu },
    { label: 'MAMMAL Import', value: status.mammalImport, icon: Workflow }
  ];

  return (
    <section className="rounded-md border border-slate-200 bg-white p-4 shadow-sm">
      <h2 className="text-base font-semibold text-ink">System Status</h2>
      <div className="mt-4 space-y-3">
        {rows.map((row) => {
          const Icon = row.icon;
          return (
            <div key={row.label} className="flex items-center justify-between rounded-md bg-slate-50 px-3 py-2">
              <span className="flex items-center gap-2 text-sm text-slate-700">
                <Icon size={17} className="text-clinical" />
                {row.label}
              </span>
              <span className="text-sm font-semibold text-review">{row.value}</span>
            </div>
          );
        })}
      </div>
    </section>
  );
}
