import base64
from cryptography.fernet import Fernet
import os

from fumedev.env import absolute_path

# Generate and save a key or load an existing one
def load_or_generate_key():
    key_path = absolute_path('secret.key')
    if os.path.exists(key_path):
        with open(key_path, 'rb') as key_file:
            key = key_file.read()
    else:
        key = Fernet.generate_key()
        with open(key_path, 'wb') as key_file:
            key_file.write(key)
    return key

def encrypt_message(message, key):
    encrypted = Fernet(key).encrypt(message.encode())
    # Encode the bytes to a Base64 string
    return base64.urlsafe_b64encode(encrypted).decode('utf-8')

def decrypt_message(encrypted_message, key):
    encrypted_bytes = base64.urlsafe_b64decode(encrypted_message.encode('utf-8'))
    return Fernet(key).decrypt(encrypted_bytes).decode('utf-8')

key = load_or_generate_key()
