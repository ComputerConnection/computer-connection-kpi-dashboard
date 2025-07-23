import { useEffect, useState } from 'react';
import { gql } from '../lib/graphql';
import { usePrefStore } from './prefs';

const KPI_FIELDS = `fragment kpiFields on Kpi { value }`;

export interface KpiHook {
  loading: boolean;
  error?: string;
  stale: boolean;
  value: number | '-';
  retry: () => void;
}

function useKpi(query: string): KpiHook {
  const [value, setValue] = useState<number | '-'>('-');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>();
  const [timestamp, setTimestamp] = useState<number>(0);
  const dateRange = usePrefStore((s) => s.dateRange);
  const granularity = usePrefStore((s) => s.granularity);

  const fetchData = () => {
    setLoading(true);
    setError(undefined);
    gql<{ v: number }>(query, {
      start: dateRange.start,
      end: dateRange.end,
      granularity,
    })
      .then((d) => {
        setValue((d as any).revenueToday ?? (d as any).salesDaily ?? (d as any).quotesPending ?? (d as any).repairsQueue ?? '-');
        setTimestamp(Date.now());
      })
      .catch((e) => setError(String(e)))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchData();
    const id = setInterval(fetchData, 60000);
    return () => clearInterval(id);
  }, [dateRange, granularity]);

  const stale = Date.now() - timestamp > 60000;

  return { loading, error, stale, value, retry: fetchData };
}

export const useKpiRevenueToday = () => useKpi('query { revenueToday }');
export const useKpiSalesDaily = () => useKpi('query { salesDaily }');
export const useKpiQuotesPending = () => useKpi('query { quotesPending }');
export const useKpiRepairsQueue = () => useKpi('query { repairsQueue }');
