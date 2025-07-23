import React from 'react';
import { ChartWrapper, Point } from './charts/ChartWrapper';

export interface TimeSeriesChartProps {
  data: Point[];
}

export const TimeSeriesChart: React.FC<TimeSeriesChartProps> = ({ data }) => (
  <ChartWrapper data={data} />
);

export default TimeSeriesChart;
