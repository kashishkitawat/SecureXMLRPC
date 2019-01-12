"""
This project is not written by me. I have searched on the internet and compiled
my version of the SecureXMLRPCServer
I have not provided my certificatesself.
You can create your own certificate and keyfile using openssl
"""

import socketserver
from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCDispatcher, SimpleXMLRPCRequestHandler

import socket
import ssl

KEYFILE = 'serverkey.pem'  # This is the private key file
CERTFILE = 'servercert.pem'  # This is the certificate file


class SecureXMLRPCServer(SimpleXMLRPCServer, SimpleXMLRPCDispatcher):
    def __init__(self, server_address, HandlerClass, logRequests=True,
                 allow_none=False, encoding=None, bind_and_activate=True):
        """Secure XML-RPC server.

        It it very similar to SimpleXMLRPCServer but it uses HTTPS for
        transporting XML data.
        """
        self.logRequests = logRequests

        SimpleXMLRPCServer.SimpleXMLRPCDispatcher.__init__(self, False, None)
        socketserver.BaseServer.__init__(self, server_address, HandlerClass)
        self.socket = ssl.wrap_socket(
                        socket.socket(self.address_family, self.socket_type),
                        server_side=True,
                        certfile=CERTFILE, keyfile=KEYFILE,
                        ssl_version=ssl.PROTOCOL_SSLv23)

        if bind_and_activate:
            self.server_bind()
            self.server_activate()


class SecureXMLRPCRequestHandler(SimpleXMLRPCRequestHandler):
    """Secure XML-RPC request handler class.

    It it very similar to SimpleXMLRPCRequestHandler but it uses HTTPS for
    transporting XML data.
    """
    def setup(self):
        self.connection = self.request
        self.rfile = self.connection.makefile("rb", self.rbufsize)
        self.wfile = self.connection.makefile("wb", self.wbufsize)

    def do_POST(self):
        """Handles the HTTPS POST request.

        It was copied out from SimpleXMLRPCServer.py and modified to
        shutdown the socket cleanly.
        """

        try:
            # get arguments
            data = self.rfile.read(int(self.headers["content-length"]))
            response = self.server._marshaled_dispatch(
                    data, getattr(self, '_dispatch', None))
        except Exception:
            self.send_response(500)
            self.end_headers()
        else:
            # got a valid XML RPC response
            self.send_response(200)
            self.send_header("Content-type", "text/xml")
            self.send_header("Content-length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)

            # shut down the connection
            self.wfile.flush()
            self.connection.shutdown(socket.SHUT_RDWR)
            self.connection.close()
