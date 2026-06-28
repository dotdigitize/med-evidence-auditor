import { FolderOpen } from 'lucide-react';

export default function AuditProjectList({ projects }: { projects: string[] }) {
  return (
    <section className="rounded-md border border-slate-200 bg-white p-4 shadow-sm">
      <h2 className="text-base font-semibold text-ink">Audit Project List</h2>
      <div className="mt-3 space-y-2">
        {projects.map((project) => (
          <div key={project} className="flex items-start gap-2 rounded-md border border-slate-200 p-3">
            <FolderOpen size={18} className="mt-0.5 text-clinical" />
            <div>
              <p className="text-sm font-medium text-ink">{project}</p>
              <p className="text-xs text-slate-500">Schizophrenia research operations</p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
