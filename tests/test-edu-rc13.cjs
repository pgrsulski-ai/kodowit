const assert=require('node:assert/strict');const {ocen}=require('../edu/edu-grade.js');const {uruchom}=require('../edu/edu-core.js');const {zolw}=require('../edu/edu-turtle.js');const p=require('../edu/edu-practice.js');let n=0;
function grade(l,i,code){const g=zolw(),s={};return ocen(l,i,uruchom(code,g,s),g.linie,s).ok;}
for(const [l,ts] of Object.entries(p))ts.forEach((t,i)=>{if(t){assert.equal(grade(l,i,t[1]),true);n++;}});
for(const [l,i,c] of [['junior',1,'wypisz("Hej\\nHej\\nHej\\nHej\\nHej")'],['junior',2,'wypisz("Tak")'],['start',0,'wypisz(12)'],['pro',0,'wypisz(21)'],['pro',1,'wypisz(15)'],['pro',3,'wypisz("0\\n2\\n4\\n6\\n8")']]){assert.equal(grade(l,i,c),false);n++;}console.log(n+' RC13 checks OK');
