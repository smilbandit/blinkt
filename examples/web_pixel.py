#!/usr/bin/env python
# 
# You can change the pixel via any web browser or tool like curl or wget.
# If you want to change the pixel from a remote computer 
#  change 127.0.0.1 to your Pi's ip address.
#
# Set a pixel
# http://[IP Address]:[Port]/set/[Pixel]/[Red]/[Green]/[Blue]/[Brightness]
#
# Set all pixels
# http://[IP Address]:[Port]/all/[Red]/[Green]/[Blue]/[Brightness]
#
# Clear all pixels
# http://[IP Address]:[Port]/clear 
#
#
# Example 1: set pixel 4 to red 0.5 brightness via curl
# curl http://127.0.0.1:8000/set/4/255/0/0/0.5
#
# Example 2: set all pixels to green full brightness via wget
# wget http://127.0.0.1:8000/all/0/255/0/1
#

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path
import blinkt

class S(BaseHTTPRequestHandler):
  def _set_success_headers(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()

  def _set_fail_headers(self):
    self.send_response(404)
    self.send_header('Content-type', 'text/html')
    self.end_headers()

  def p_set(self,p):
    blinkt.set_pixel(int(p[1]),int(p[2]),int(p[3]),int(p[4]),float(p[5]))
    blinkt.show()
    return '{"done"}'

  def p_clear(self,p):
    blinkt.clear()
    blinkt.show()
    return '{"done"}'

  def p_all(self,p):
    blinkt.set_all(int(p[1]),int(p[2]),int(p[3]),float(p[4]))
    blinkt.show()
    return '{"done"}'

  def do_GET(self):
    commands = {'set': self.p_set,
          'clear': self.p_clear,
          'all': self.p_all
          }
    request = self.path.lower().rsplit('/')
    del request[0]
    if request[0] in 'set,all,clear':
      self._set_success_headers()
      result = commands[request[0]](request)
    else:
      self._set_fail_headers()
      result = '<html><body><h1>Unknown Command</h1></body></html>'

    self.wfile.write(result.encode("utf-8"))

  def do_POST(self):
    # Doesn't do anything with posted data
    self._set_fail_headers()
    result = "<html><body><h1>No POST</h1></body></html>"
    self.wfile.write(result.encode("utf-8"))

  def do_HEAD(self):
    self._set_success_headers()
    
     
def run(server_class=HTTPServer, handler_class=S, port=8000):
  server_address = ('', port)
  httpd = server_class(server_address, handler_class)
  print('Starting httpd...')
  httpd.serve_forever()

if __name__ == "__main__":
  from sys import argv

  if len(argv) == 2:
    run(port=int(argv[1]))
  else:
    run()