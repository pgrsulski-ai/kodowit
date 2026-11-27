'use strict';
if(typeof module!=="undefined")global.School=require("./school.js");
const Director=(()=>{
function certificates(s,alias){const r=s.reports.find(x=>x.alias===alias);if(!s.students.some(x=>x.name===alias)||!r)return [];return ['junior','start','pro'].filter(l=>Array.from({length:l==='pro'?32:34},(_,i)=>l+':'+i).every(id=>r.quiz.includes(id)&&r.practice.includes(id)));}
function stats(s){const rows=School.summary(s);return {classes:s.classes.map(c=>{const a=rows.filter(x=>x.group===c.name);return {name:c.name,students:a.length,done:a.reduce((n,x)=>n+x.done,0),total:a.reduce((n,x)=>n+x.total,0)};}),teachers:s.teachers.map(t=>({name:t.name,tasks:s.tasks.filter(x=>x.teacher===t.name).length})),students:rows.length};}
function issue(s,alias,level,id,date){if(!certificates(s,alias).includes(level)||!/^KD-[a-f0-9-]{36}$/.test(id)||!/^\d{4}-\d{2}-\d{2}$/.test(date))throw Error('Brak podstaw do wydania potwierdzenia');return {alias,level,id,date};}
return {certificates,stats,issue};})();
if(typeof module!=='undefined')module.exports=Director;
