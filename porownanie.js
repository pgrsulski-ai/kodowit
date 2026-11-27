'use strict';
const lessons=[['Zmienne','Python nie wymaga let, JavaScript używa let.','zmienna x = 7\nwypisz(x*2)'],['Warunki','Python używa wcięć, JavaScript nawiasów klamrowych.','jeżeli 2 < 3 { wypisz("tak") } inaczej { wypisz("nie") }'],['Pętle','Dopóki odpowiada instrukcji while.','zmienna x = 0\ndopóki x < 5 { x = x+1 }\nwypisz(x)'],['Funkcje','Funkcja odpowiada def lub function, zwróć to return.','funkcja podwoj(x) { zwróć x*2 }\nwypisz(podwoj(6))'],['Listy','Indeks -1 wskazuje ostatni element.','zmienna a = [2,4,6]\nwypisz(a[-1])'],['Logika','Operator oraz sprawdza oba warunki z krótkim spięciem.','jeżeli 2 oraz 3 { wypisz("tak") }'],['Porównanie list','Porównujemy zawartość list, a nie ich tożsamość.','jeżeli [1,2] == [1,2] { wypisz("równe") }']];
if(typeof module!=='undefined')module.exports=lessons;
if(typeof document!=='undefined'){
const get=id=>document.getElementById(id), select=get('lesson');
lessons.forEach((l,i)=>{const o=document.createElement('option');o.value=i;o.textContent=l[0];select.append(o);});
function convert(){get('py').textContent='';get('js').textContent='';try{const s=get('source').value;const py=eksportKodowit(s,'python'),js=eksportKodowit(s,'javascript');get('py').textContent=py;get('js').textContent=js;get('status').textContent='Wygenerowano kod.';}catch(e){get('status').textContent=e.message;}}
function load(){const l=lessons[Number(select.value)];get('explain').textContent=l[1];get('source').value=l[2];convert();}select.addEventListener('change',load);get('convert').addEventListener('click',convert);load();}
