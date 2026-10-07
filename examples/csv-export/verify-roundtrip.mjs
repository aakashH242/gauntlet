import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { toCsv } from './csv.mjs';

const targetHash = createHash('sha256').update(readFileSync(new URL('./csv.mjs', import.meta.url))).digest('hex');
assert.equal(targetHash, '99aaf5953069b99aa70215962abed6a3042da1ce6605d716bbc96692e12849b8');

// Independent reader: consume quoted fields, then require a delimiter or CRLF.
function parseCsv(csv) {
  if (csv === '') return [];
  const rows = [];
  let row = [];
  let position = 0;
  while (true) {
    let field = '';
    if (csv[position] === '"') {
      position++;
      let closed = false;
      while (position < csv.length) {
        const character = csv[position++];
        if (character !== '"') {
          field += character;
        } else if (csv[position] === '"') {
          field += '"';
          position++;
        } else {
          closed = true;
          break;
        }
      }
      assert.ok(closed, 'Unterminated quoted field');
    } else {
      while (position < csv.length && csv[position] !== ',' && csv[position] !== '\r') {
        assert.ok(csv[position] !== '"' && csv[position] !== '\n', 'Bare quote or LF');
        field += csv[position++];
      }
    }
    row.push(field);
    if (position === csv.length) {
      rows.push(row);
      return rows;
    }
    if (csv[position] === ',') {
      position++;
    } else {
      assert.equal(csv.slice(position, position + 2), '\r\n', 'Invalid record boundary or characters after quote');
      rows.push(row);
      row = [];
      position += 2;
    }
  }
}

const validParserCases = [
  ['', []],
  [',', [['', '']]],
  ['a,b\r\nc,d', [['a', 'b'], ['c', 'd']]],
  ['"a,b","say ""hi"""', [['a,b', 'say "hi"']]],
  ['"a\rb","c\nd"\r\n"e\r\nf",', [['a\rb', 'c\nd'], ['e\r\nf', '']]],
  ['"""",z', [['"', 'z']]],
  ['\r\n', [[''], ['']]],
];
for (const [csv, expected] of validParserCases) assert.deepEqual(parseCsv(csv), expected);
const invalidParserCases = ['"unclosed', 'a"b,c', 'a\nb,c', 'a\rb,c', '"a"x,b'];
for (const csv of invalidParserCases) assert.throws(() => parseCsv(csv));

let roundTripCases = 0;
function check(rows) {
  const original = rows.map(row => row.slice());
  for (const row of rows) Object.freeze(row);
  Object.freeze(rows);
  const expected = original.map(row => row.map(cell => cell === null || cell === undefined ? '' : String(cell)));
  const actual = parseCsv(toCsv(rows));
  assert.deepEqual(actual, expected);
  assert.deepEqual(rows, original, 'Input mutated');
  roundTripCases++;
}

const alphabet = ['a', ',', '"', '\r', '\n'];
const strings = [''];
let level = [''];
for (let length = 1; length <= 3; length++) {
  level = level.flatMap(prefix => alphabet.map(character => prefix + character));
  strings.push(...level);
}
const cells = [...strings, 0, -0, false, true, null, undefined, 1, -1, 1.25, Number.MAX_VALUE, Number.MIN_VALUE];
for (const first of cells) {
  for (const second of cells) check([[first, second]]);
}

// Fixed seed makes every generated multirow case reproducible.
let seed = 0x1234abcd;
function next(maximum) {
  seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0;
  return seed % maximum;
}
for (let sample = 0; sample < 4000; sample++) {
  const width = 2 + next(6);
  const height = 1 + next(7);
  check(Array.from({ length: height }, () => Array.from({ length: width }, () => cells[next(cells.length)])));
}

check([]);
for (const cell of cells) {
  const normalized = cell === null || cell === undefined ? '' : String(cell);
  if (normalized !== '') check([[cell]]);
  else assert.equal(toCsv(Object.freeze([Object.freeze([cell])])), '');
}
check([[''], ['']]);
check([[''], ['x'], ['']]);

console.log(JSON.stringify({ targetHash, parserOracleChecks: validParserCases.length + invalidParserCases.length, scalarPoolSize: cells.length, roundTripCases, ambiguousOneEmptyCellCases: cells.filter(cell => cell === null || cell === undefined || cell === '').length, result: 'passed' }));
