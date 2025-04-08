import os
import signal
import sys
import http.server

def httpServer():

    print("http server running: localhost:8080 pid=", os.getpid())

    from http.server import HTTPServer, CGIHTTPRequestHandler

    try:
        CGIHTTPRequestHandler.cgi_directories = ['/cgi-bin']

        httpd = HTTPServer(('localhost', 8080),             # localhost:8000
                        CGIHTTPRequestHandler)  # CGI support.

        print(f"Running server. Use [ctrl]-c to terminate.")

        httpd.serve_forever()

    except KeyboardInterrupt:
        print(f"\nReceived keyboard interrupt. Shutting down server.")
        httpd.socket.close()

    print("server terminated for an unknown reason")
    os.system("timeout /t 400")

httpServer()