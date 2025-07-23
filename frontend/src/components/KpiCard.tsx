import React from 'react';

export interface KpiCardProps {
  title: string;
  value: string | number;
}

const cardStyle: React.CSSProperties = {
  border: '1px solid #ccc',
  padding: '1rem',
  borderRadius: '4px',
};

export const KpiCard: React.FC<KpiCardProps> = ({ title, value }) => (
  <div style={cardStyle}>
    <h3 style={{ margin: '0 0 0.5rem 0' }}>{title}</h3>
    <div style={{ fontSize: '2rem', fontWeight: 'bold' }}>{value}</div>
  </div>
);

export default KpiCard;
