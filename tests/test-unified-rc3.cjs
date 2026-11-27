const assert=require('node:assert/strict'),vm=require('node:vm'),cp=require('node:child_process');
const edu=require('../edu/edu-core.js'),web=require('../compiler.js');
const html=web.html('');
const helpers=html.slice(html.indexOf('function strictNumber('),html.indexOf('function len('));
for(const [expr,result] of [['bezwzględna(-7)','7'],['podłoga(3.9)','3'],['sufit(3.1)','4'],['bezwzgledna(-2)+podloga(2.9)+sufit(2.1)','7']]){
 const code='wypisz('+expr+')';let out=[];vm.runInNewContext(helpers+'\n'+web.compile(code),{tick(){},print(x){out.push(String(x))}});assert.equal(out.join('\n'),result);assert.equal(edu.uruchom(code),result);assert.equal(cp.execFileSync('python',['core/kodowit.py','-c',code],{encoding:'utf8'}).trim(),result);
}
console.log('OK: 4 nowe wspólne programy');
