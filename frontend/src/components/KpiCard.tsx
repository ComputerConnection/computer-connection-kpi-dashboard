import React from 'react';

export interface KpiCardProps {
  title: string;
  value: string | number;
  status?: { loading: boolean; error?: string; stale: boolean };
}

const cardStyle: React.CSSProperties = {
  border: '1px solid #ccc',
  padding: '1rem',
  borderRadius: '4px',
};

export const KpiCard: React.FC<KpiCardProps> = ({ title, value, status }) => (
  <div style={cardStyle}>
    <h3 style={{ margin: '0 0 0.5rem 0' }}>{title}</h3>
    {status?.loading ? (
      <div className="h-8 bg-gray-300 animate-pulse rounded" />
    ) : (
      <div style={{ fontSize: '2rem', fontWeight: 'bold' }}>{value}</div>
    )}
    {status?.error && (
      <div style={{ color: 'red', fontSize: '0.75rem' }}>error</div>
    )}
    {status?.stale && !status.error && (
      <div style={{ color: '#999', fontSize: '0.75rem' }}>stale</div>
    )}
  </div>
);

export default KpiCard;
