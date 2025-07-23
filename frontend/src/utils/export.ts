export function exportCSV(name: string, rows: string[][]) {
  const csv = rows.map(r => r.join(',')).join('\n');
  const blob = new Blob([csv], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = name + '.csv';
  a.click();
  URL.revokeObjectURL(url);
}

export async function exportPNG(name: string, element: HTMLElement) {
  const dataUrl = element.toDataURL('image/png');
  const a = document.createElement('a');
  a.href = dataUrl;
  a.download = name + '.png';
  a.click();
}
