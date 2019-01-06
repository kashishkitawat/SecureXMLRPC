import SecureXMLRPCServer

LISTEN_HOST = 'localhost'
LISTEN_PORT = 5443


def test(HandlerClass=SecureXMLRPCServer.SecureXMLRpcRequestHandler,
         ServerClass=SecureXMLRPCServer.SecureXMLRPCServer):
    """Test xml rpc over https server"""
    class xmlrpc_registers:
        def add(self, x, y):
            return x + y

        def mult(self, x, y):
            return x*y

        def div(self, x, y):
            return x//y

    server_address = (LISTEN_HOST, LISTEN_PORT)
    server = ServerClass(server_address, HandlerClass)
    server.register_instance(xmlrpc_registers())
    sa = server.socket.getsockname()
    print("Serving HTTPS on", sa[0], "port", sa[1])
    server.serve_forever()


if __name__ == '__main__':
    test()
