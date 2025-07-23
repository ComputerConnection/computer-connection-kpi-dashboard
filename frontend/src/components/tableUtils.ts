import html2canvas from 'html2canvas';

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

export async function exportTablePng(table: HTMLElement, name: string) {
  const canvas = await html2canvas(table);
  canvas.toBlob((blob) => {
    if (!blob) return;
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = name;
    a.click();
    URL.revokeObjectURL(url);
  });
}
