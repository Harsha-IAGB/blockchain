from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import dsa

# Generate private and public keys
private_key = dsa.generate_private_key(
    key_size=1024,  # Key size can be adjusted as needed
    backend=default_backend()
)

# Export private key
private_key_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

# Save private key to a file
with open("private_key_alice.pem", "wb") as f:
    f.write(private_key_pem)


# Generate private and public keys
private_key = dsa.generate_private_key(
    key_size=1024,  # Key size can be adjusted as needed
    backend=default_backend()
)

# Export private key
private_key_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

# Save private key to a file
with open("private_key_bob.pem", "wb") as f:
    f.write(private_key_pem)


# Generate private and public keys
private_key = dsa.generate_private_key(
    key_size=1024,  # Key size can be adjusted as needed
    backend=default_backend()
)

# Export private key
private_key_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

# Save private key to a file
with open("private_key_charlie.pem", "wb") as f:
    f.write(private_key_pem)
