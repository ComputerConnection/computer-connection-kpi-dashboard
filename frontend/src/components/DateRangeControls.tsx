import React from 'react';
import { usePrefStore, Granularity } from '../store/prefs';

export default function DateRangeControls() {
  const dateRange = usePrefStore((s) => s.dateRange);
  const granularity = usePrefStore((s) => s.granularity);
  const setDateRange = usePrefStore((s) => s.setDateRange);
  const setGranularity = usePrefStore((s) => s.setGranularity);

  return (
    <div className="flex items-center gap-2 mb-4">
      <input
        type="date"
        value={dateRange.start}
        onChange={(e) => setDateRange(e.target.value, dateRange.end)}
      />
      <input
        type="date"
        value={dateRange.end}
        onChange={(e) => setDateRange(dateRange.start, e.target.value)}
      />
      <select
        value={granularity}
        onChange={(e) => setGranularity(e.target.value as Granularity)}
      >
        <option value="day">Daily</option>
        <option value="week">Weekly</option>
        <option value="month">Monthly</option>
      </select>
    </div>
  );
}
