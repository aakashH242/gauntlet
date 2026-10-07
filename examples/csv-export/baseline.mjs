import assert from 'node:assert/strict';
import { toCsv } from './csv.mjs';

assert.equal(toCsv([['Name', 'City'], ['Ada', 'London']]), 'Name,City\r\nAda,London');
assert.equal(toCsv([['a,b', 'say "hi"', 'line\nbreak']]), '"a,b","say ""hi""","line\nbreak"');
assert.equal(toCsv([]), '');
console.log('Baseline: 3 assertions passed.');
