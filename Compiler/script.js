const lines = require('fs').readFileSync(0, 'utf-8').trim().split('\n');
let inputIndex = 0;
function input() { return lines[inputIndex++]; }
let a = parseInt(input());
let b = parseInt(input());
let c = a+b;
console.log(c);