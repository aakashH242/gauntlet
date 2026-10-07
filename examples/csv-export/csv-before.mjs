export function toCsv(rows) {
  return rows.map(row => row.map(value => {
    const text = String(value || '');
    return /[,"\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
  }).join(',')).join('\r\n');
}
