import React, { useRef } from 'react';
import { ChartWrapper, Point } from './charts/ChartWrapper';
import { exportPng } from './charts/chartUtils';

export interface TimeSeriesChartProps {
  data: Point[];
}

export const TimeSeriesChart: React.FC<TimeSeriesChartProps> = ({ data }) => {
  const ref = useRef<HTMLDivElement>(null);

  const handleExport = () => {
    if (ref.current) exportPng(ref.current, 'chart.png');
  };

  return (
    <div>
      <button onClick={handleExport} className="mb-2 text-sm text-blue-600">
        Export PNG
      </button>
      <div ref={ref}>
        <ChartWrapper data={data} />
      </div>
    </div>
  );
};

export default TimeSeriesChart;
