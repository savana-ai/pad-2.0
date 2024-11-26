from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.handle_request("GET")
    
    def do_POST(self):
        self.handle_request("POST")
    
    def do_PUT(self):
        self.handle_request("PUT")
    
    def do_DELETE(self):
        self.handle_request("DELETE")

    def handle_request(self, method):
        # Parse the URL and query parameters
        url_parts = urlparse(self.path)
        path_parts = url_parts.path.strip('/').split('/')
        
        if len(path_parts) >= 2:
            service = path_parts[1]
            action = path_parts[2] if len(path_parts) > 2 else None
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid path")
            return

        # Parse the request body (if any)
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else None
        
        if body:
            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                data = body
        else:
            data = parse_qs(url_parts.query)
        
        try:
            # Call your handler logic
            result = self.handle_logic(service, action, method, data)
            self.send_response(200)
            self.end_headers()
            response = json.dumps({"success": True, "data": result})
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            response = json.dumps({"success": False, "message": str(e)})
        
        # Send the response
        self.wfile.write(response.encode('utf-8'))

    def handle_logic(self, service, action, method, data):
        # Your route logic here (just an example)
        if service == "user":
            if action == "create" and method == "POST":
                return {"message": "User created", "data": data}
            elif action == "get" and method == "GET":
                return {"message": "User data retrieved", "data": data}
            else:
                raise Exception("Unsupported action or method")
        else:
            raise Exception("Unsupported service")
        

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
