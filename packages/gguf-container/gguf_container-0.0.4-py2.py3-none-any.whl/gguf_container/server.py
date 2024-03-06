import http.server
import socketserver
# import os
# directory = os.path.join(os.path.dirname(__file__), '.')
# Set the directory containing your index.html
directory = '.'  # You can change this to the path of your directory
# Set the port number for localhost
port = 8000  # You can change this to any available port
# Combine a simple server with the specified directory and port
Handler = http.server.SimpleHTTPRequestHandler
# Launch the server
with socketserver.TCPServer(("", port), Handler) as httpd:
    print(f"Serving at http://localhost:{port}")
    # Open the default web browser to the localhost URL
    import webbrowser
    webbrowser.open(f'http://localhost:{port}')
    httpd.serve_forever()
