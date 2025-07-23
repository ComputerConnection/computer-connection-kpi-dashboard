import React from 'react';
import {
  useKpiRevenueToday,
  useKpiQuotesPending,
  useKpiRepairsQueue,
} from '../store/hooks';
import KpiCard from '../components/KpiCard';
import { usePrefStore } from '../store/prefs';

export default function Sales() {
  const revenue = useKpiRevenueToday();
  const quotes = useKpiQuotesPending();
  const repairs = useKpiRepairsQueue();
  const order = usePrefStore((s) => s.order);
  const hidden = usePrefStore((s) => s.hidden);
  const setOrder = usePrefStore((s) => s.setOrder);

  const cards: Record<string, JSX.Element> = {
    revenue: <KpiCard title="Revenue Today" value={revenue.value} status={revenue} />,
    quotes: <KpiCard title="Quotes Pending" value={quotes.value} status={quotes} />,
    repairs: <KpiCard title="Repairs Queue" value={repairs.value} status={repairs} />,
  };

  const onDragStart = (e: React.DragEvent<HTMLDivElement>, idx: number) => {
    e.dataTransfer.setData('text/plain', String(idx));
  };
  const onDrop = (e: React.DragEvent<HTMLDivElement>, idx: number) => {
    const from = Number(e.dataTransfer.getData('text/plain'));
    const newOrder = [...order];
    const [moved] = newOrder.splice(from, 1);
    newOrder.splice(idx, 0, moved);
    setOrder(newOrder);
  };
  const onDragOver = (e: React.DragEvent) => e.preventDefault();

  return (
    <div className="grid gap-4 sm:grid-cols-2 md:grid-cols-3">
      {order.filter((id) => !hidden.includes(id)).map((id, idx) => (
        <div
          key={id}
          draggable
          onDragStart={(e) => onDragStart(e, idx)}
          onDragOver={onDragOver}
          onDrop={(e) => onDrop(e, idx)}
        >
          {cards[id]}
        </div>
      ))}
    </div>
  );
}
