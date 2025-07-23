import React, { useState } from 'react';
import { sortRows, exportCsv } from './tableUtils';

export interface TableGridProps {
  columns: string[];
  rows: (string | number)[][];
}

export const TableGrid: React.FC<TableGridProps> = ({ columns, rows }) => {
  const [sortedRows, setSortedRows] = useState(rows);

  const handleSort = (index: number) => {
    setSortedRows(sortRows(sortedRows, index));
  };

  const handleExport = () => {
    const csv = exportCsv(columns, sortedRows);
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'table.csv';
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div>
      <button onClick={handleExport} className="mb-2 text-sm text-blue-600">Export CSV</button>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            {columns.map((c, idx) => (
              <th
                key={c}
                onClick={() => handleSort(idx)}
                style={{ borderBottom: '1px solid #ccc', textAlign: 'left', padding: '0.25rem 0.5rem', cursor: 'pointer' }}
              >
                {c}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {sortedRows.map((row, i) => (
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
    </div>
  );
};

export default TableGrid;
