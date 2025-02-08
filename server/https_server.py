from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="client", **kwargs)

httpd = HTTPServer(('localhost', 8443), Handler)
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('localhost.pem', 'localhost-key.pem')
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
print("Serving at https://localhost:8443")
httpd.serve_forever()
