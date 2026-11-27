const a=require('node:assert/strict'),p=require('../pro-project');
const original=p.validate({files:{index:'abc',mod:'def'}});
a.throws(()=>p.update(original,'index','x'.repeat(100001)));
a.equal(original.files.index,'abc');
a.throws(()=>p.update(original,'missing','x'));
a.equal(p.update(original,'mod','nowy').files.mod,'nowy');
a.equal(original.files.mod,'def');
console.log('OK RC122');
