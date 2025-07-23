interface Props {
  title: string;
  value: string | number;
  delta?: number;
  updatedAt: string;
  status: "fresh" | "stale";
}

export function KpiCard({ title, value, delta, updatedAt, status }: Props) {
  return (
    <div className="bg-white shadow rounded p-4">
      <h2 className="text-lg font-semibold">{title}</h2>
      <p className="text-2xl">{value}</p>
      {delta !== undefined && <p className="text-sm">{delta}%</p>}
      <p className="text-xs text-gray-500">{updatedAt} ({status})</p>
    </div>
  );
}
