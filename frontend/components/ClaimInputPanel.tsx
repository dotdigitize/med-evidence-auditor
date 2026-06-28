export default function ClaimInputPanel() {
  return (
    <section className="rounded-md border border-slate-200 bg-white p-4 shadow-sm">
      <h2 className="text-base font-semibold text-ink">MAMMAL Claims</h2>
      <textarea
        className="mt-3 h-32 w-full resize-y rounded-md border border-slate-300 p-3 text-sm outline-none focus:border-clinical focus:ring-2 focus:ring-clinical/20"
        defaultValue={'MAMMAL claim: Gene expression markers may be associated with altered synaptic pathway activity in schizophrenia research summaries.'}
      />
    </section>
  );
}
