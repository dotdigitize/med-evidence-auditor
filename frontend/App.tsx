import { Activity, AlertTriangle, ClipboardCheck, Database, FileText, ShieldCheck } from 'lucide-react';
import Dashboard from './components/Dashboard';
import SystemStatus from './components/SystemStatus';
import AuditProjectList from './components/AuditProjectList';
import ClaimInputPanel from './components/ClaimInputPanel';
import EvidenceLibrary from './components/EvidenceLibrary';
import AuditRunner from './components/AuditRunner';
import ClaimReviewTable from './components/ClaimReviewTable';
import RiskFlagsPanel from './components/RiskFlagsPanel';
import ReportPreview from './components/ReportPreview';
import { useMedEvidence } from './hooks/useMedEvidence';

export default function App() {
  const data = useMedEvidence();

  return (
    <main className="min-h-screen">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <div>
            <h1 className="text-2xl font-semibold tracking-normal text-ink">MedEvidence Auditor</h1>
            <p className="mt-1 max-w-3xl text-sm text-slate-600">
              MAMMAL Evidence Audit for claim support scoring, risk language detection, and structured verification reporting.
            </p>
          </div>
          <div className="hidden items-center gap-2 rounded-md border border-clinical/30 bg-clinical/10 px-3 py-2 text-sm font-medium text-clinical md:flex">
            <ShieldCheck size={18} />
            MAMMAL research safety layer
          </div>
        </div>
      </header>

      <div className="mx-auto max-w-7xl px-6 py-6">
        <Dashboard
          cards={[
            { label: 'Audit Projects', value: data.summary.projects, icon: ClipboardCheck },
            { label: 'MAMMAL Outputs Reviewed', value: data.summary.modelOutputs, icon: FileText },
            { label: 'MAMMAL Claims', value: data.summary.extractedClaims, icon: Activity },
            { label: 'Unsupported Claims', value: data.summary.unsupportedClaims, icon: AlertTriangle },
            { label: 'Risk Flags', value: data.summary.riskFlags, icon: ShieldCheck },
            { label: 'MAMMAL Evidence Reports', value: data.summary.reportsExported, icon: Database }
          ]}
        />

        <section className="mt-6 grid gap-6 lg:grid-cols-[340px_1fr]">
          <aside className="space-y-6">
            <SystemStatus status={data.status} />
            <AuditProjectList projects={data.projects} />
            <EvidenceLibrary evidence={data.evidence} />
          </aside>
          <div className="space-y-6">
            <ClaimInputPanel />
            <AuditRunner evidence={data.evidence} />
            <ClaimReviewTable claims={data.claims} />
            <RiskFlagsPanel flags={data.riskFlags} />
            <ReportPreview claims={data.claims} flags={data.riskFlags} />
          </div>
        </section>
      </div>
    </main>
  );
}
