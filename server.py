
from http.server import BaseHTTPRequestHandler, HTTPServer
# import SocketServer
import json
import cgi


class Game():
    def handle_request(self, dict):
        if dict["action"] == "move":
            return self.handle_move(dict)

    def handle_move(self, dict):
        if dict["direction"] == "left":
            dict["current_position"]["x"] -= 1
        if dict["direction"] == "right":
            dict["current_position"]["x"] += 1
        if dict["direction"] == "up":
            dict["current_position"]["y"] -= 1
        if dict["direction"] == "down":
            dict["current_position"]["y"] += 1
        return dict

class Server(BaseHTTPRequestHandler):

    game = Game()

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        BaseHTTPRequestHandler.end_headers(self)

    def _set_headers(self):
        self.send_response(200)
        self.send_header('content-type', 'application/json')
        self.end_headers()
        
    def do_HEAD(self):
        self._set_headers()

    def do_OPTIONS(self):           
        self.send_response(200, "ok")       
        # self.send_header('Access-Control-Allow-Origin', '*')                
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", " *")        
        self.end_headers()
        
    # GET sends back a Hello world message
    def do_GET(self):
        self._set_headers()
        self.send_header('Access-Control-Allow-Origin', '*')

        self.wfile.write(json.dumps({'hello': 'world', 'received': 'ok'}))
        
    # POST echoes the message adding a JSON field
    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
        
        # refuse to receive non-json content
        if ctype != 'application/json' and ctype != 'text/plain':
            self.send_response(400)
            self.end_headers()
            return
            
        # read the message and convert it into a python dictionary
        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))

        print(message)
        
        # add a property to the object, just to mess with data
        message['received'] = 'ok'

        new_message = self.game.handle_request(message)
        
        # send the message back
        self._set_headers()
        self.wfile.write(bytes(json.dumps(message), 'utf-8'))






def run(server_class=HTTPServer, handler_class=Server, port=8008):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    
    print('Starting httpd on port %d...' % port)
    httpd.serve_forever()
    
if __name__ == "__main__":
    from sys import argv
    
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
        