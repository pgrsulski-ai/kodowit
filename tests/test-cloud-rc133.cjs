const assert=require('node:assert/strict');const P=require('../pro-project');
const p={files:{index:'zażółć\n"',mod:'test'},secret:'nie eksportuj'};
assert.deepEqual(JSON.parse(P.backup(p)),{files:p.files});
assert.equal(P.validate(JSON.parse(P.backup(p))).files.index,p.files.index);
assert.throws(()=>P.backup({files:{bad:'x'}}));
assert.throws(()=>P.backup({files:{index:'x'.repeat(100001)}}));
assert.ok(Buffer.byteLength(P.backup({files:{index:'\u0000'.repeat(100000)}}))<700000);
console.log('OK RC133 backup');
