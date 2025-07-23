import React from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

export interface TimeSeriesPoint {
  date: string;
  value: number;
}

export interface TimeSeriesChartProps {
  data: TimeSeriesPoint[];
}

export const TimeSeriesChart: React.FC<TimeSeriesChartProps> = ({ data }) => (
  <div style={{ width: '100%', height: 300 }}>
    <ResponsiveContainer>
      <LineChart data={data} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="value" stroke="#8884d8" />
      </LineChart>
    </ResponsiveContainer>
  </div>
);

export default TimeSeriesChart;
