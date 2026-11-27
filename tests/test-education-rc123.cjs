const a=require('node:assert/strict'),vm=require('node:vm'),fs=require('node:fs');
const {ocen}=require('../edu/edu-grade');
for(const v of [null,[null,null,null,null],[[0,0,1,0],[1,0,1,1],[1,1,0,1],[0,1,0,0]]]) a.equal(ocen('junior',3,'',v).ok,v?.[0]?.[0]===0);
const nodes=new Map();const document={createElement:()=>({append(){}}),getElementById(id){if(!nodes.has(id))nodes.set(id,this.createElement());return nodes.get(id)}};
const paths=require('../academy/academy-paths');const localStorage={getItem:()=>JSON.stringify(['0:0','0:0','99:99',3])};
vm.runInNewContext(fs.readFileSync('academy/academy-paths-ui.js','utf8'),{document,paths,localStorage});a.equal(nodes.get('status').textContent,'Postęp: 1 / 12');
console.log('RC123: walidacja postępu i geometrii');
