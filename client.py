import xmlrpclib
import ssl

context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS)
context.load_verify_locations(cafile='servercert.pem')
server = xmlrpclib.ServerProxy("https://localhost:5443", context=context)
print(server.add(1, 2))
print(server.div(10, 4))
