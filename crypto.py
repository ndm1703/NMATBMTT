from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA256
import base64

def get_key(key_str):
    return SHA256.new(key_str.encode()).digest()

def encrypt_message(msg, key):
    cipher = AES.new(get_key(key), AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(msg.encode(), AES.block_size))
    return base64.b64encode(cipher.iv + ct_bytes).decode()

def decrypt_message(enc_msg, key):
    raw = base64.b64decode(enc_msg)
    iv, ct = raw[:16], raw[16:]
    cipher = AES.new(get_key(key), AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ct), AES.block_size).decode()