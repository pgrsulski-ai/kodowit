'use strict';
// Eksport ograniczonego podzbioru; nie wykonuje kodu użytkownika.
const helpers = `function __kw_truth(v){return Array.isArray(v)?v.length>0:Boolean(v);}
function __kw_equal(a,b){return Array.isArray(a)||Array.isArray(b)?Array.isArray(a)&&Array.isArray(b)&&a.length===b.length&&a.every((v,i)=>__kw_equal(v,b[i])):a===b;}
function __kw_index(a,i){if(typeof a==='string')a=Array.from(a);if(!Array.isArray(a)||!Number.isInteger(i)||i>=a.length||i< -a.length)throw Error('Niepoprawny indeks');return a.at(i);}
`;
function eksportKodowit(source,target){
 if(!['python','javascript'].includes(target))throw Error('Nieznany język docelowy');
 const parse=typeof module!=='undefined'&&module.exports?require('./edu/edu-core.js').parsujEdu:parsujEdu;
 const js=target==='javascript', end=js?';':'', name=n=>'k_'+n, fail=k=>{throw Error('Eksport nie obsługuje: '+k);};
 const ast=parse(source), functions=new Map(ast.filter(a=>a[0]==='fn').map(a=>[a[1],a[2].length]));
 function expr(a){const [k,x,y,z]=a;
 if(k==='lit'&&(typeof x==='string'||Number.isSafeInteger(x)&&Math.abs(x)<=1000000))return JSON.stringify(x);
 if(k==='var')return name(x);
 if(k==='list')return '['+x.map(expr).join(', ')+']';
 if(k==='un'&&['nie','!'].includes(x))return js?'(!__kw_truth('+expr(y)+'))':'(not '+expr(y)+')';
 if(k==='un'&&x==='-')return '(-'+expr(y)+')';
 if(k==='bin'&&['oraz','lub'].includes(x))return js?'(__kw_truth('+expr(y)+') '+(x==='oraz'?'&&':'||')+' __kw_truth('+expr(z)+'))':'(bool('+expr(y)+') '+(x==='oraz'?'and':'or')+' bool('+expr(z)+'))';
 if(k==='bin'&&js&&['==','!='].includes(x))return '('+(x==='!='?'!':'')+'__kw_equal('+expr(y)+', '+expr(z)+'))';
 if(k==='bin'&&['+','-','*','<','>','<=','>=','==','!='].includes(x))return '('+expr(y)+' '+(js?({'==':'===','!=':'!=='}[x]||x):x)+' '+expr(z)+')';
 if(k==='call'&&x[0]==='var'&&functions.get(x[1])===y.length)return name(x[1])+'('+y.map(expr).join(', ')+')';
 if(k==='idx')return js?'__kw_index('+expr(x)+', '+expr(y)+')':'('+expr(x)+')['+expr(y)+']';
 return fail(k);
 }
 function block(nodes,d=0,local=null,nested=false){const p='    '.repeat(d),lines=[];
 for(const [k,x,y,z] of nodes){
 if(k==='let'){if(nested||local?.has(x))fail('deklaracja w bloku lub ponowna deklaracja');if(local)local.add(x);lines.push(p+(js?'let ':'')+name(x)+' = '+expr(y)+end);}
 else if(k==='set'){if(local&&!local.has(x))fail('zmiana zmiennej zewnętrznej');lines.push(p+name(x)+' = '+expr(y)+end);}
 else if(k==='expr'&&x[0]==='call'&&x[1][0]==='var'&&x[1][1]==='wypisz'&&x[2].length===1)lines.push(p+(js?'console.log':'print')+'('+expr(x[2][0])+')'+end);
 else if(k==='return'&&local)lines.push(p+'return '+expr(x)+end);
 else if(k==='fn'&&!local&&!nested){lines.push(p+(js?'function ':'def ')+name(x)+'('+y.map(name).join(', ')+(js?') {':'):'),...block(z,d+1,new Set(y)));if(js)lines.push(p+'}');}
 else if(k==='while'||k==='if'){lines.push(p+(js?k+' (__kw_truth('+expr(x)+')) {':k+' '+expr(x)+':'),...block(y,d+1,local,true));if(js)lines.push(p+'}');if(k==='if'&&z.length){lines.push(p+(js?'else {':'else:'),...block(z,d+1,local,true));if(js)lines.push(p+'}');}}
 else fail(k);
 }return lines.length?lines:js?[]:[p+'pass'];}
 return (js?helpers:'')+block(ast).join('\n')+'\n';
}
if(typeof module!=='undefined')module.exports={eksportKodowit};
