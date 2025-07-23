import { FC } from 'react';

interface Props {
  title: string;
}

const KpiCard: FC<Props> = ({ title, children }) => {
  return (
    <div className="kpi-card">
      <h3>{title}</h3>
      {children}
    </div>
  );
};

export default KpiCard;
