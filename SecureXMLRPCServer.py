"""
This project is not written by me. I have searched on the internet and compiled
my version of the SecureXMLRPCServer
I have not provided my certificatesself.
You can create your own certificate and keyfile using openssl
"""

import socketserver
from xmlrpc.server import SimpleXMLRPCServer

import socket
import ssl

class SecureXMLRPCServer(SimpleXMLRPCServer):
    def __init__(self, server_address, HandlerClass, keyfile, certfile,
                 ssl_version=ssl.PROTOCOL_SSLv23, *args, **kwargs):
        """Secure XML-RPC server.

        It it very similar to SimpleXMLRPCServer but it uses HTTPS for
        transporting XML data.
        """
        super().__init__(server_address, HandlerClass, *args, **kwargs)
        self.keyfile     = keyfile
        self.certfile    = certfile
        self.ssl_version = ssl_version

    def get_request(self):
        """Get the request and client address from the socket."""
        sock, addr  = super().get_request()
        sock = ssl.wrap_socket(sock, server_side=True,
                        certfile=self.certfile, keyfile=self.keyfile,
                        ssl_version=self.ssl_version)
        return sock, addr
