from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

def generate_key():
    private_key = rsa.generate_private_key(
        public_exponent=65537, 
        key_size=2048, 
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def encrypt_message(public_key, message):
    encrypted = public_key.encrypt(
        message.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()), 
            algorithm=hashes.SHA256(), 
            label=None
        )
    )
    return encrypted

def decrypt_message(private_key, encrypted):
    original_message = private_key.decrypt(
        encrypted,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()), 
            algorithm=hashes.SHA256(), 
            label=None
        )
    )
    return original_message.decode('utf-8')


# Example usage
priv_key, pub_key = generate_key()
secret_message = "This is a top secret message"

encrypted_msg = encrypt_message(pub_key, secret_message)
print(f"Encrypted: {encrypted_msg}")

decrypted_msg = decrypt_message(priv_key, encrypted_msg)
print("Decrypted:", decrypted_msg)
