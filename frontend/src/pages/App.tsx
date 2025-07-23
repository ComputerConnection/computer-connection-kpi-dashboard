import React, { useEffect, useState } from 'react';
import KpiCard from '../components/KpiCard';
import { gql } from '../lib/graphql';

export default function App() {
  const [revenueToday, setRevenueToday] = useState<number | null>(null);
  const [quotesPending, setQuotesPending] = useState<number | null>(null);
  const [repairsQueue, setRepairsQueue] = useState<number | null>(null);

  useEffect(() => {
    gql<{ revenueToday: number }>('query { revenueToday }').then((d) => setRevenueToday(d.revenueToday));
    gql<{ quotesPending: number }>('query { quotesPending }').then((d) => setQuotesPending(d.quotesPending));
    gql<{ repairsQueue: number }>('query { repairsQueue }').then((d) => setRepairsQueue(d.repairsQueue));
  }, []);

  const gridStyle: React.CSSProperties = {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
    gap: '1rem',
    padding: '1rem',
  };

  return (
    <div style={gridStyle}>
      <KpiCard title="Revenue Today" value={revenueToday ?? '-'} />
      <KpiCard title="Quotes Pending" value={quotesPending ?? '-'} />
      <KpiCard title="Repairs Queue" value={repairsQueue ?? '-'} />
    </div>
  );
}
