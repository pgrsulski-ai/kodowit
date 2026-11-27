import unittest, threading, urllib.request, urllib.error, json
from http_api import API
from kodowit import Core, Blad
class HTTPTests(unittest.TestCase):
 def test_disabled(self):
  with self.assertRaises(Blad): Core().run('api_start(8080)')
 def test_http(self):
  api=API(); api.route('GET','/ok',['żółć']); api.route('POST','/echo',None); api.routes['POST','/echo']=lambda x:x
  with api.server(0) as s:
   t=threading.Thread(target=s.serve_forever); t.start()
   try:
    base='http://127.0.0.1:'+str(s.server_port)
    with urllib.request.urlopen(base+'/ok') as r: self.assertEqual(json.load(r),['żółć'])
    with urllib.request.urlopen(urllib.request.Request(base+'/echo',data=b'[42]',method='POST')) as r: self.assertEqual(json.load(r),[42])
    with self.assertRaises(urllib.error.HTTPError) as e: urllib.request.urlopen(base+'/missing')
    self.assertEqual(e.exception.code,404)
   finally: s.shutdown(); t.join()
 def test_kodowit_handler(self):
  from unittest.mock import patch
  with patch.object(API,'serve',lambda self,p: self.routes['POST','/x']([4])):
   out=[]; Core(out.append,network=True).run('funkcja f(d) { zwróć d[0]*2 }; api_trasa("POST","/x",f); wypisz(api_start(8080))'); self.assertEqual(out,[8])
