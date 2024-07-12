from OpenSSL import crypto
from socket import gethostname

# Create a key pair
key = crypto.PKey()
key.generate_key(crypto.TYPE_RSA, 4096)

# Create a self-signed certificate
cert = crypto.X509()
cert.get_subject().CN = gethostname()
cert.set_serial_number(1000)
cert.gmtime_adj_notBefore(0)
cert.gmtime_adj_notAfter(365 * 24 * 60 * 60)  # Valid for 1 year
cert.set_issuer(cert.get_subject())
cert.set_pubkey(key)
cert.sign(key, 'sha256')

with open("key.pem", "wb") as key_file:
    key_file.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
with open("cert.pem", "wb") as cert_file:
    cert_file.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

print("Certificates generated successfully.")
