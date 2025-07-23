import { KpiCard } from "../components/KpiCard";

export function App() {
  return (
    <div className="min-h-screen bg-gray-50 p-6 grid gap-6 md:grid-cols-3">
      <KpiCard title="Revenue Today" value="$12,340" delta={8.2} updatedAt="just now" status="fresh" />
      <KpiCard title="Quotes Pending" value={7} delta={-12.5} updatedAt="2m ago" status="fresh" />
      <KpiCard title="Repairs in Queue" value={19} updatedAt="5m ago" status="stale" />
    </div>
  );
}
