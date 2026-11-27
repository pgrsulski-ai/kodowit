"""Opt-in, loopback-only HTTP development server."""
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlsplit

class API:
 def __init__(self): self.routes={}
 def route(self, method, path, body):
  if method not in ('GET','POST') or not isinstance(path,str) or not path.startswith('/') or '?' in path: raise ValueError('Nieprawidłowa trasa')
  json.dumps(body,allow_nan=False)
  self.routes[method,path]=body
 def server(self,port):
  if type(port) is not int or not 0<=port<=65535: raise ValueError('Nieprawidłowy port')
  routes=self.routes
  class Handler(BaseHTTPRequestHandler):
   def setup(self):
    super().setup(); self.connection.settimeout(5)
   def reply(self,status,data):
    raw=json.dumps(data,ensure_ascii=False,allow_nan=False).encode('utf-8')
    self.send_response(status); self.send_header('Content-Type','application/json; charset=utf-8'); self.send_header('Content-Length',str(len(raw))); self.send_header('X-Content-Type-Options','nosniff'); self.end_headers(); self.wfile.write(raw)
   def handle_route(self):
    key=(self.command,urlsplit(self.path).path)
    if key not in routes: return self.reply(404,['Nie znaleziono'])
    body=routes[key]
    if callable(body):
     try:
      n=int(self.headers.get('Content-Length','0'))
      if not 0<=n<=65536: return self.reply(413,['Za duże żądanie'])
      payload=json.loads(self.rfile.read(n)) if n else None
     except (ValueError,UnicodeError): return self.reply(400,['Nieprawidłowy JSON'])
     try:
      result=body(payload); json.dumps(result,allow_nan=False)
     except Exception: return self.reply(500,['Błąd programu'])
     return self.reply(200,result)
    return self.reply(200,body)
   do_GET=do_POST=handle_route
  return HTTPServer(('127.0.0.1',port),Handler)
 def serve(self,port):
  with self.server(port) as server:
   print('KODOWIT HTTP: http://127.0.0.1:'+str(server.server_port),flush=True)
   server.serve_forever()
