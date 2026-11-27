const assert=require('node:assert/strict'),edu=require('../edu/edu-core.js');
for(const [expr,out] of [['-5%3','1'],['5%-3','-1'],['[1,2][-1]','2'],['[1,[2]]==[1,[2]]','prawda'],['2 oraz 3','prawda'],['[] lub 0','fałsz']])assert.equal(edu.uruchom('wypisz('+expr+')'),out);
assert.throws(()=>edu.uruchom('wypisz(1%0)'));
