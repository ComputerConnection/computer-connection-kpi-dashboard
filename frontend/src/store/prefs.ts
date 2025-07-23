import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export type Granularity = 'day' | 'week' | 'month';

interface PrefState {
  order: string[];
  hidden: string[];
  dateRange: { start: string; end: string };
  granularity: Granularity;
  setOrder: (order: string[]) => void;
  toggleHidden: (id: string) => void;
  setDateRange: (start: string, end: string) => void;
  setGranularity: (g: Granularity) => void;
}

export const usePrefStore = create<PrefState>()(
  persist(
    (set) => ({
      order: ['revenue', 'quotes', 'repairs'],
      hidden: [],
      dateRange: { start: '', end: '' },
      granularity: 'day',
      setOrder: (order) => set({ order }),
      toggleHidden: (id) =>
        set((s) => ({
          hidden: s.hidden.includes(id)
            ? s.hidden.filter((h) => h !== id)
            : [...s.hidden, id],
        })),
      setDateRange: (start, end) => set({ dateRange: { start, end } }),
      setGranularity: (g) => set({ granularity: g }),
    }),
    { name: 'prefs' }
  )
);
