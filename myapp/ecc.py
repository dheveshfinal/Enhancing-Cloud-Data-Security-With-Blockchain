from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.fernet import Fernet
import os
import base64
# Generate ECC private key for server
server_private_key = ec.generate_private_key(ec.SECP384R1())

# Generate ECC public key for server
server_public_key = server_private_key.public_key()

# Serialize public key to be shared with client
server_public_key_bytes = server_public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Client side - Load server's public key
server_public_key = serialization.load_pem_public_key(server_public_key_bytes)

# Generate ECC private key for client
client_private_key = ec.generate_private_key(ec.SECP384R1())

# Generate ECC public key for client
client_public_key = client_private_key.public_key()

# Serialize client public key to be shared with server
client_public_key_bytes = client_public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Server side - Load client's public key
client_public_key = serialization.load_pem_public_key(client_public_key_bytes)

# Generate a symmetric key using ECDH (Elliptic Curve Diffie-Hellman) for key exchange
server_shared_key = server_private_key.exchange(ec.ECDH(), client_public_key)
client_shared_key = client_private_key.exchange(ec.ECDH(), server_public_key)

# Derive a symmetric key from the shared key
derived_key_server = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b'handshake data'
).derive(server_shared_key)

derived_key_client = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b'handshake data'
).derive(client_shared_key)

# Ensure both derived keys are identical
assert derived_key_server == derived_key_client

# Convert the derived key into a Fernet key (Fernet keys must be 32 bytes and base64-encoded)
fernet_key = Fernet(base64.urlsafe_b64encode(derived_key_server))


