const assert=require('node:assert/strict');const {create}=require('../cloud-api.js');
const url='https://test.supabase.co';const jwt=role=>'x.'+Buffer.from(JSON.stringify({role})).toString('base64url')+'.x';
for(const key of ['sb_secret_test',jwt('service_role'),'garbage'])assert.throws(()=>create({url,key}));
assert.doesNotThrow(()=>create({url,key:jwt('anon')}));
(async()=>{let signal;const api=create({url,key:'sb_publishable_test'},async(u,o)=>{signal=o.signal;return {ok:true,status:200,json:async()=>[]}});await assert.rejects(api.read('12345678-1234-1234-1234-123456789abc'));assert.ok(signal instanceof AbortSignal);console.log('OK RC127')})().catch(e=>{console.error(e);process.exitCode=1});
