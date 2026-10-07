import assert from 'node:assert/strict';
const { toCsv } = await import(process.argv[2] || './csv.mjs');

const cases = [
  ['zero and false', [[0, false]], '0,false'],
  ['nullish and empty', [[null, undefined, '']], ',,'],
  ['carriage return', [['a\rb']], '"a\rb"'],
  ['CRLF in cell', [['a\r\nb']], '"a\r\nb"'],
  ['LF in cell', [['a\nb']], '"a\nb"'],
  ['comma and quotes', [['a,b', '"']], '"a,b",""""'],
  ['record separators', [['x'], ['y']], 'x\r\ny'],
  ['empty matrix', [], ''],
];
const results = cases.map(([name, rows, expected]) => {
  const actual = toCsv(rows);
  return { name, expected, actual, pass: actual === expected };
});
const frozen = Object.freeze([Object.freeze([0, false, 'a\rb'])]);
const before = JSON.stringify(frozen);
toCsv(frozen);
assert.equal(JSON.stringify(frozen), before);
results.push({ name: 'input immutability', pass: true });
console.log(JSON.stringify({ passed: results.filter(r => r.pass).length, total: results.length, results }, null, 2));
process.exitCode = results.every(r => r.pass) ? 0 : 1;
