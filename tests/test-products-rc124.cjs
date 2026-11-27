const a=require('node:assert/strict'),b=require('../builder.js'),e=require('../enterprise/enterprise.js');
a.throws(()=>b.expression('1'.repeat(201),[]),/Nieprawidłowa formuła/);
a.throws(()=>b.expression(null,[]),/Nieprawidłowa formuła/);
a.equal(b.expression('1+2',[]),'(1 + 2)');
a.throws(()=>e.validate({units:[null],tasks:[]}),/Niepoprawna jednostka/);
a.throws(()=>e.validate({units:[],tasks:[null]}),/Niepoprawny proces/);
(async()=>{let request,closed=false;global.indexedDB={open(){return request={}}};require('../business/business-store.js');const pending=BusinessStore.open();request.onblocked();await a.rejects(pending,/zablokowana/);request.result={close(){closed=true}};request.onsuccess();a.ok(closed);console.log('OK RC124')})().catch(e=>{console.error(e);process.exitCode=1});
