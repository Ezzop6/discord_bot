from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from .bot import DiscordBot
bot_instance = DiscordBot()


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = json.dumps({'message': 'Hello From Discord Bot'}).encode()
            self.wfile.write(response)
        elif self.path == '/send-message':
            # Handle GET request
            pass
        else:
            self.send_response(404)
            self.end_headers()
            response = json.dumps({'message': 'Page Not Found'}).encode()
            self.wfile.write(response)

    def do_POST(self):
        if self.path == '/status':
            # Handle POST request
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            # Do something with the data

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = json.dumps({'status': 'Hello From Discord Bot'}).encode()
            self.wfile.write(response)
        elif self.path == '/send-message':
            # Handle POST request
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            # Do something with the data
            bot_instance.message_queue.put(data)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = json.dumps({'status': 'Message added to queue'}).encode()
            self.wfile.write(response)

        else:
            self.send_response(404)
            self.end_headers()
            response = json.dumps({'message': 'Page Not Found'}).encode()
            self.wfile.write(response)


class DiscordHTTPServer:
    def __init__(self, host='localhost', port=8000):
        self.server_address = (host, port)

    def run(self):
        httpd = HTTPServer(self.server_address, SimpleHTTPRequestHandler)
        httpd.serve_forever()
