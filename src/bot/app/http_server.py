from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/status':
            # Handle GET request
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = json.dumps({'message': 'Hello From Discord Bot'}).encode()
            self.wfile.write(response)
        else:
            self.send_response(404)
            self.end_headers()
            response = json.dumps({'message': 'Page Not Found'}).encode()
            self.wfile.write(response)

    def do_POST(self):
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


class DiscordHTTPServer:
    def __init__(self, host='localhost', port=8000):
        self.server_address = (host, port)

    def run(self):
        httpd = HTTPServer(self.server_address, SimpleHTTPRequestHandler)
        httpd.serve_forever()
