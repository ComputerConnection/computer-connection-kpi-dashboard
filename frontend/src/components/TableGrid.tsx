import React from 'react';

export interface TableGridProps {
  columns: string[];
  rows: (string | number)[][];
}

export const TableGrid: React.FC<TableGridProps> = ({ columns, rows }) => (
  <table style={{ width: '100%', borderCollapse: 'collapse' }}>
    <thead>
      <tr>
        {columns.map((c) => (
          <th key={c} style={{ borderBottom: '1px solid #ccc', textAlign: 'left', padding: '0.25rem 0.5rem' }}>
            {c}
          </th>
        ))}
      </tr>
    </thead>
    <tbody>
      {rows.map((row, i) => (
        <tr key={i}>
          {row.map((cell, j) => (
            <td key={j} style={{ padding: '0.25rem 0.5rem' }}>
              {cell}
            </td>
          ))}
        </tr>
      ))}
    </tbody>
  </table>
);

export default TableGrid;
