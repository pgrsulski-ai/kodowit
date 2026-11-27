'use strict';
const Exams=(()=>{
function student(s,id){const p=s.students.find(x=>x.name===id);if(!p)throw Error('Nieznany profil');const r=s.reports.find(x=>x.alias===id);const tasks=s.tasks.filter(t=>t.group===p.group).map(t=>({...t,done:!!r?.quiz.includes(t.id)}));const points=tasks.filter(t=>t.done).length*10;return {tasks,points,badge:points>=100?'Mistrz nauki':points>=10?'Pierwsze kroki':'Start'};}
function validate(e){if(!e||typeof e.title!=='string'||!e.title.trim()||e.title.length>100||!Array.isArray(e.questions)||!e.questions.length||e.questions.length>30)throw Error('Nieprawidłowy sprawdzian');for(const q of e.questions){if(!q||typeof q.prompt!=='string'||!q.prompt.trim()||q.prompt.length>1000||typeof q.answer!=='string'||!q.answer.trim()||q.answer.length>1000)throw Error('Nieprawidłowe pytanie');}return e;}
function grade(e,a){validate(e);if(!Array.isArray(a)||a.length!==e.questions.length||!a.every(x=>typeof x==='string'&&x.length<=1000))throw Error('Nieprawidłowe odpowiedzi');const results=e.questions.map((q,i)=>q.answer.trim().replace(/\r\n/g,'\n')===a[i].trim().replace(/\r\n/g,'\n'));return {points:results.filter(Boolean).length,total:results.length,results};}
return {student,validate,grade};})();
if(typeof module!=='undefined')module.exports=Exams;
