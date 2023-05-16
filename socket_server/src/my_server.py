import socketserver
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# from .. import funlib


class Tcp_server(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data.decode())
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())


class Udp_server(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request[0].strip()
        socket = self.request[1]
        print("{} wrote:".format(self.client_address[0]))
        print(self.data.upper().decode())
        socket.sendto(self.data.upper(), self.client_address)


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ("/RPC2",)


class Server:
    def __init__(self, host="localhost") -> None:
        self.host = host

    def start_tcp(self, port):
        with socketserver.TCPServer((self.host, port), Tcp_server) as server:
            server.serve_forever()

    def start_udp(self, port):
        with socketserver.UDPServer((self.host, port), Udp_server) as server:
            server.serve_forever()

    """
     def start_xmlrpc(self):
         with SimpleXMLRPCServer((self.host, self.port),
                        requestHandler=RequestHandler) as server:
           server.register_introspection_functions()
           server.register_function(pow)
           server.register_instance(funlib.xml_funs())
           server.serve_forever()
      """
