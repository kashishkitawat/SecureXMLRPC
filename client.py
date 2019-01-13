''' I have not provided my certificate files.
You can create your selfsigned certificates using openssl
'''

from xmlrpc import client
import ssl

ca_certFile = 'servercert.pem'  # Add your own certificate file
certFile = 'clientcert.pem'
keyFile = 'clientkey.pem'
context = ssl.SSLContext()  # Arguments can contain SSL PROTOCOL version
context.verify_mode = ssl.CERT_REQUIRED  # Expects cert from other side
context.check_hostname = False
context.load_verify_locations(ca_certFile)
context.load_cert_chain(certfile=certFile, keyfile=keyFile)

server = client.ServerProxy("https://localhost:5443", context=context)
try:

    addResult = server.add(1, 2)
    divResult = server.div(10, 4)

    print("Addition Result = ", addResult)
    print("Division Result = ", divResult)

except ssl.SSLError:
    print('Verification Failed')
