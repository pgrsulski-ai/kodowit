const assert=require('assert'),fs=require('fs'),K=require('../compiler.js');
for(const f of fs.readdirSync('szablony').filter(f=>f.endsWith('.kodowit'))) K.compile(fs.readFileSync('szablony/'+f,'utf8'));
const h=K.html(K.compile('strona "Test" { tekst "OK" }'));assert(!h.includes('connect-src'));assert(K.previewHtml(h).includes("connect-src 'none'"));assert(K.previewHtml(h).indexOf('Content-Security-Policy')<K.previewHtml(h).indexOf('<script>'));assert.throws(()=>K.compile('zmienna x = @'));console.log('RC98 OK');
