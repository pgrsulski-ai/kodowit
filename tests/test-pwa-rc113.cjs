const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const root=path.resolve(__dirname,'..'), read=f=>fs.readFileSync(path.join(root,f),'utf8');
const assets=JSON.parse(read('sw.js').match(/const F=(\[.*?\]);/)[1]);
for(const f of fs.readdirSync(root).filter(f=>f.endsWith('.html')&&!f.startsWith('OTWORZ'))){assert(assets.includes(f),f);assert(read(f).includes('shared/pwa.js'),f);assert(/name=["']viewport/.test(read(f)),f);}
assert(assets.includes('shared/pwa.js'));
for(const [protocol,secure,expected] of [['https:',true,1],['http:',true,1],['http:',false,0],['file:',true,0]]){let calls=0;vm.runInNewContext(read('shared/pwa.js'),{navigator:{serviceWorker:{register(url){assert.equal(url,'./sw.js');calls++;return Promise.resolve();}}},window:{isSecureContext:secure},location:{protocol},console});assert.equal(calls,expected);}
console.log('OK: PWA registration, viewport, cache coverage');
