import http.server
import socketserver
directory = '.'
port = 8000  # You can change this to any available port
Handler = http.server.SimpleHTTPRequestHandler
# Launch to the server (as localhost)
with socketserver.TCPServer(("", port), Handler) as httpd:
    print(f"Serving at http://localhost:{port}")
    import webbrowser
    webbrowser.open(f'http://localhost:{port}')
    httpd.serve_forever()
