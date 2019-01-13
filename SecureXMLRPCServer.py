"""
This project is not written by me. I have searched on the internet and compiled
my version of the SecureXMLRPCServer
I have not provided my certificatesself.
You can create your own certificate and keyfile using openssl
"""

import socketserver
from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCDispatcher

import socket
import ssl

KEYFILE = 'serverkey.pem'  # This is the private key file
CERTFILE = 'servercert.pem'  # This is the certificate file
ca_certFile = 'clientcert.pem'


class SecureXMLRPCServer(SimpleXMLRPCServer, SimpleXMLRPCDispatcher):
    def __init__(self, server_address, HandlerClass, logRequests=True,
                 allow_none=False, encoding=None, bind_and_activate=True):
        """Secure XML-RPC server.

        It it very similar to SimpleXMLRPCServer but it uses HTTPS for
        transporting XML data.
        """
        self.logRequests = logRequests

        SimpleXMLRPCDispatcher.__init__(self, False, None)
        socketserver.BaseServer.__init__(self, server_address, HandlerClass)
        self.socket = ssl.wrap_socket(
                        socket.socket(self.address_family, self.socket_type),
                        server_side=True,
                        certfile=CERTFILE, keyfile=KEYFILE,
                        cert_reqs=ssl.CERT_REQUIRED, ca_certs=ca_certFile,
                        ssl_version=ssl.PROTOCOL_SSLv23)

        if bind_and_activate:
            self.server_bind()
            self.server_activate()
