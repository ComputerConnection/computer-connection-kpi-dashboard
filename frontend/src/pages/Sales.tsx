import React from 'react';
import { useKpiRevenueToday } from '../store/hooks';
import KpiCard from '../components/KpiCard';

export default function Sales() {
  const revenue = useKpiRevenueToday();

  return (
    <div className="grid gap-4 p-4 sm:grid-cols-2 md:grid-cols-3">
      <KpiCard title="Revenue Today" value={revenue.value} status={revenue} />
    </div>
  );
}
