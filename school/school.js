'use strict';
const School=(()=>{
const valid=x=>typeof x==='string'&&/^[\p{L}\p{N} _-]{1,40}$/u.test(x)&&x.trim()===x;
const lesson=x=>typeof x==='string'&&/^(junior|start|pro):\d{1,2}$/.test(x)&&Number(x.split(':')[1])<(x.startsWith('pro:')?32:34);
function add(s,kind,name,group){if(!valid(name))throw Error('Nieprawidłowy identyfikator');if(!['classes','teachers','students'].includes(kind))throw Error('Nieznany typ');if(s[kind].length>=500||s[kind].some(x=>x.name===name))throw Error('Limit lub duplikat');if(kind==='students'&&!s.classes.some(x=>x.name===group))throw Error('Nieznana klasa');s[kind].push({name,group:kind==='students'?group:''});}
function assign(s,group,teacher,id){if(!s.classes.some(x=>x.name===group)||!s.teachers.some(x=>x.name===teacher)||!lesson(id))throw Error('Nieprawidłowe przydzielenie');if(s.tasks.length>=2000||s.tasks.some(x=>x.group===group&&x.id===id))throw Error('Limit lub duplikat zadania');s.tasks.push({group,teacher,id});}
function progress(s,r){if(!s.students.some(x=>x.name===r.alias)||!Array.isArray(r.quiz)||!Array.isArray(r.practice)||r.quiz.length>100||r.practice.length>100||![...r.quiz,...r.practice].every(lesson))throw Error('Nieprawidłowy raport');s.reports=s.reports.filter(x=>x.alias!==r.alias);s.reports.push({alias:r.alias,quiz:[...new Set(r.quiz)],practice:[...new Set(r.practice)]});}
function empty(){return {classes:[],teachers:[],students:[],tasks:[],reports:[]};}
function summary(s){return s.students.map(x=>{const tasks=s.tasks.filter(t=>t.group===x.group),r=s.reports.find(r=>r.alias===x.name);return {name:x.name,group:x.group,total:tasks.length,done:tasks.filter(t=>r?.quiz.includes(t.id)).length};});}
return {empty,add,assign,progress,summary,lesson};})();
if(typeof module!=='undefined')module.exports=School;
