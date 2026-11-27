const assert=require('node:assert/strict');const t=require('../edu/edu-teacher.js');
assert.deepEqual(t.report('U01',['junior:0','junior:0','bad'],['pro:2','start:0']).quiz,['junior:0']);
assert.deepEqual(t.report('U01',[],['pro:2','start:0']).practice,['start:0']);
assert.throws(()=>t.report('<script>',[],[]));assert.throws(()=>t.parse('{}'));assert.throws(()=>t.parse(' '.repeat(20001)));assert.deepEqual(t.parse(JSON.stringify(t.report('U02',[],[]))),t.report('U02',[],[]));console.log('6 testów panelu OK');
