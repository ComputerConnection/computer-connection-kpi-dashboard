export function sortRows(rows: any[][], index: number, asc = true) {
  return [...rows].sort((a, b) => {
    if (a[index] < b[index]) return asc ? -1 : 1;
    if (a[index] > b[index]) return asc ? 1 : -1;
    return 0;
  });
}

export function exportCsv(columns: string[], rows: any[][]) {
  const header = columns.join(',');
  const body = rows.map((r) => r.join(',')).join('\n');
  return header + '\n' + body;
}
