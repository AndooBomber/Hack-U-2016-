import http.server

server_address = ("", 80)
handler_class = http.server.CGIHTTPRequestHandler
server = http.server.HTTPServer(server_address, handler_class)
server.serve_forever()
