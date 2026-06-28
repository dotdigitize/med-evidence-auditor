import type { LucideIcon } from 'lucide-react';

type Card = {
  label: string;
  value: number;
  icon: LucideIcon;
};

export default function Dashboard({ cards }: { cards: Card[] }) {
  return (
    <section className="grid gap-3 sm:grid-cols-2 lg:grid-cols-6">
      {cards.map((card) => {
        const Icon = card.icon;
        return (
          <div key={card.label} className="rounded-md border border-slate-200 bg-white p-4 shadow-sm">
            <div className="flex items-center justify-between gap-3">
              <p className="text-xs font-medium uppercase text-slate-500">{card.label}</p>
              <Icon className="h-5 w-5 text-clinical" />
            </div>
            <p className="mt-3 text-3xl font-semibold text-ink">{card.value}</p>
          </div>
        );
      })}
    </section>
  );
}
