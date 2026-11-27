// Szczyt RSS procesu Node, obejmuje runtime; nie jest pomiarem pamięci przeglądarki.
const c=require('../compiler.js');
const source='strona "Test" {\n'+'tekst "Próba"\n'.repeat(3000)+'}';
for(let i=0;i<26;i++) c.compile(source);
console.log('Szczyt RSS Node: '+(process.resourceUsage().maxRSS/1024).toFixed(2)+' MiB');
