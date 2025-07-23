import html2canvas from 'html2canvas';

export function formatDate(value: string) {
  return new Date(value).toLocaleDateString();
}

export async function exportPng(element: HTMLElement, name: string) {
  const canvas = await html2canvas(element);
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
