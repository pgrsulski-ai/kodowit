// Zewnętrzny silnik wstrzymany do wdrożenia na odrębnym originie.
self.onmessage=e=>self.postMessage({id:e.data?.id,error:'AI Web wymaga osobnego originu'});
