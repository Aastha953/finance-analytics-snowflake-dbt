import os
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

key_dir = Path.home() / ".snowflake"
key_dir.mkdir(exist_ok=True)
priv_path = key_dir / "rsa_key.p8"
pub_path = key_dir / "rsa_key.pub"

passphrase = os.environ["SNOWFLAKE_PRIVATE_KEY_PASSPHRASE"].encode()
key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

priv_path.write_bytes(key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.BestAvailableEncryption(passphrase),
))

pub_pem = key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo,
)
pub_path.write_bytes(pub_pem)
print(f"Keys saved to {key_dir}")