// Lokalne moduły projektu, bez dostępu do sieci.
function compileProject(files,entry='index',shared=''){
 const done=new Set(),active=new Set();let total=0;
 function expand(key,source){
  if(active.has(key))throw Error('Cykliczny import: '+[...active,key].join(' → '));
  if(done.has(key))return '';
  if(typeof source!=='string')throw Error('Brak modułu: '+key+'.kodowit');
  if(active.size>=50)throw Error('Zbyt wiele zagnieżdżonych modułów');
  active.add(key);total+=source.length;if(total>100000)throw Error('Limit kodu projektu: 100 000 znaków');
  // Rozpoznawanie dyrektyw poza napisami i komentarzami.
  const pattern=/"(?:[^"\\\n]|\\.)*"|\/\*[\s\S]*?\*\/|\/\/[^\n]*|^[ \t]*importuj[ \t]+"([a-z0-9_-]+)(?:\.kodowit)?"[ \t]*;?[ \t]*(?=\r?$)/gm;
  const result=source.replace(pattern,(match,name)=>name===undefined?match:expand(name,Object.hasOwn(files,name)?files[name]:undefined)+'\n');
  active.delete(key);done.add(key);return result;
 }
 return compile(expand('@shared',shared)+'\n'+expand(entry,Object.hasOwn(files,entry)?files[entry]:undefined));
}
